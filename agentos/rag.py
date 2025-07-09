from pathlib import Path
from typing import List, Optional, Union, Dict, Any
import chromadb
from chromadb.utils import embedding_functions
import pandas as pd
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup
import json
import re


class RAGSystem:
    """
    A Retrieval Augmented Generation system that can process various file types,
    embed them using ChromaDB, and enable semantic search capabilities.

    Features:
    - Supports multiple file types (txt, pdf, csv, docx, pptx, json, html)
    - Automatic text chunking based on token count
    - Document embedding using ChromaDB
    - Semantic search capabilities
    - Integration with AgentOS

    Example:
        >>> rag = RAGSystem()
        >>> # Add a single document
        >>> rag.add_document("path/to/document.pdf")
        >>> # Add multiple documents
        >>> rag.add_multiple_documents(["doc1.pdf", "doc2.txt"])
        >>> # Add an entire folder
        >>> rag.add_folder("path/to/docs/")
        >>> # Query the documents
        >>> results = rag.query("What is the main topic?")
    """

    def __init__(
        self,
        collection_name: str = "agentos_docs",
        embedding_model: str = "all-MiniLM-L6-v2",
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ):
        """Initialize the RAG system."""
        # Initialize ChromaDB client
        self.client = chromadb.Client()

        # Set up the embedding function
        self.embedding_fn = (
            embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=embedding_model
            )
        )

        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name, embedding_function=self.embedding_fn
        )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Track processed files to avoid duplicates
        self.processed_files = set()

    def add_document(self, file_path: Union[str, Path]) -> bool:
        """
        Add a single document to the RAG system.

        Args:
            file_path: Path to the document to add

        Returns:
            bool: True if document was successfully processed, False otherwise

        Example:
            >>> rag.add_document("path/to/document.pdf")
            True
        """
        file_path = Path(file_path)
        if not file_path.is_file():
            print(f"Error: {file_path} is not a file")
            return False

        if str(file_path.absolute()) in self.processed_files:
            print(f"Warning: {file_path} has already been processed")
            return False

        success = self._process_file(file_path)
        if success:
            self.processed_files.add(str(file_path.absolute()))
        return success

    def add_multiple_documents(
        self, file_paths: List[Union[str, Path]]
    ) -> Dict[str, bool]:
        """
        Add multiple documents to the RAG system.

        Args:
            file_paths: List of paths to documents

        Returns:
            Dict[str, bool]: Dictionary mapping file paths to their processing status

        Example:
            >>> results = rag.add_multiple_documents(["doc1.pdf", "doc2.txt"])
            >>> for path, success in results.items():
            ...     print(f"{path}: {'Success' if success else 'Failed'}")
        """
        results = {}
        for file_path in file_paths:
            results[str(file_path)] = self.add_document(file_path)
        return results

    def add_folder(
        self,
        folder_path: Union[str, Path],
        recursive: bool = True,
        file_types: Optional[List[str]] = None,
    ) -> Dict[str, bool]:
        """
        Add all documents from a folder to the RAG system.

        Args:
            folder_path: Path to the folder
            recursive: Whether to process subfolders (default: True)
            file_types: List of file extensions to process (e.g., ['.pdf', '.txt'])
                       If None, processes all supported file types

        Returns:
            Dict[str, bool]: Dictionary mapping file paths to their processing status

        Example:
            >>> # Process all files in folder
            >>> rag.add_folder("path/to/docs/")
            >>> # Process only PDFs and TXTs
            >>> rag.add_folder("path/to/docs/", file_types=['.pdf', '.txt'])
            >>> # Process without recursion
            >>> rag.add_folder("path/to/docs/", recursive=False)
        """
        folder_path = Path(folder_path)
        if not folder_path.is_dir():
            print(f"Error: {folder_path} is not a directory")
            return {}

        supported_types = {
            ".txt",
            ".md",
            ".pdf",
            ".csv",
            ".docx",
            ".pptx",
            ".json",
            ".html",
        }

        if file_types:
            file_types = {
                (
                    ext.lower()
                    if ext.startswith(".")
                    else f".{ext.lower()}"
                )
                for ext in file_types
            }
            # Validate file types
            if not all(ext in supported_types for ext in file_types):
                unsupported = [
                    ext
                    for ext in file_types
                    if ext not in supported_types
                ]
                print(
                    f"Warning: Unsupported file types: {unsupported}"
                )
                print(f"Supported types are: {supported_types}")
                file_types = file_types & supported_types
        else:
            file_types = supported_types

        results = {}
        pattern = "**/*" if recursive else "*"

        for file_path in folder_path.glob(pattern):
            if (
                file_path.is_file()
                and file_path.suffix.lower() in file_types
            ):
                results[str(file_path)] = self.add_document(file_path)

        return results

    def get_processed_files(self) -> List[str]:
        """
        Get a list of all processed file paths.

        Returns:
            List[str]: List of absolute paths of processed files

        Example:
            >>> files = rag.get_processed_files()
            >>> for file in files:
            ...     print(file)
        """
        return sorted(list(self.processed_files))

    def clear_processed_files(self) -> None:
        """
        Clear the list of processed files, allowing them to be processed again.

        Example:
            >>> rag.clear_processed_files()
            >>> rag.add_document("previously_processed.pdf")  # Will process again
        """
        self.processed_files.clear()

    def remove_document(self, file_path: Union[str, Path]) -> bool:
        """
        Remove a document and its chunks from the RAG system.

        Args:
            file_path: Path to the document to remove

        Returns:
            bool: True if document was successfully removed, False otherwise

        Example:
            >>> rag.remove_document("path/to/document.pdf")
            True
        """
        file_path = str(Path(file_path).absolute())
        try:
            # Remove all chunks associated with this file
            self.collection.delete(where={"source": file_path})
            self.processed_files.discard(file_path)
            print(f"Successfully removed {file_path}")
            return True
        except Exception as e:
            print(f"Error removing {file_path}: {str(e)}")
            return False

    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks based on token count.

        Args:
            text (str): The text to split into chunks

        Returns:
            List[str]: List of text chunks
        """
        if not text:
            return []

        # Split text into sentences (rough approximation)
        sentences = text.split(".")
        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # Rough estimate of tokens (words + punctuation)
            sentence_length = len(sentence.split())

            # If adding this sentence would exceed chunk size, save current chunk
            if (
                current_length + sentence_length > self.chunk_size
                and current_chunk
            ):
                chunks.append(". ".join(current_chunk) + ".")
                current_chunk = []
                current_length = 0

            current_chunk.append(sentence)
            current_length += sentence_length

        # Add any remaining text as the last chunk
        if current_chunk:
            chunks.append(". ".join(current_chunk) + ".")

        # Handle case where a single sentence is longer than chunk_size
        if not chunks:
            chunks = [text]

        return chunks

    def process_text(self, text: str) -> List[str]:
        """Process and chunk text content."""
        return self.chunk_text(text)

    def process_pdf(self, file_path: str) -> List[str]:
        """Extract and process text from PDF files."""
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return self.chunk_text(text)

    def process_markdown(self, text: str) -> List[str]:
        """Process Markdown files.

        Args:
            text (str): The markdown text content to process

        Returns:
            List[str]: List of text chunks
        """
        # Remove markdown image syntax to avoid issues with long URLs
        # Remove image markdown syntax
        text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
        # Remove URL markdown syntax
        text = re.sub(r"\[([^\]]+)\]\(([^\)]+)\)", r"\1", text)
        return self.chunk_text(text)

    def process_csv(self, file_path: str) -> List[str]:
        """Process CSV files into text chunks."""
        df = pd.read_csv(file_path)
        text = df.to_string()
        return self.chunk_text(text)

    def process_json(self, file_path: str) -> List[str]:
        """Process JSON files."""
        with open(file_path, "r") as f:
            data = json.load(f)
        text = json.dumps(data, indent=2)
        return self.chunk_text(text)

    def process_html(self, file_path: str) -> List[str]:
        """Process HTML files."""
        with open(file_path, "r") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
        text = soup.get_text()
        return self.chunk_text(text)

    def _process_file(self, file_path: Path) -> None:
        """Process a single file based on its extension."""
        processors = {
            ".txt": self.process_text,
            ".md": self.process_markdown,
            ".pdf": self.process_pdf,
            ".csv": self.process_csv,
            ".json": self.process_json,
            ".html": self.process_html,
        }

        try:
            processor = processors.get(file_path.suffix.lower())
            if processor:
                # For text-based files, read content and process
                if file_path.suffix.lower() in [
                    ".txt",
                    ".md",
                    ".json",
                    ".html",
                ]:
                    with open(file_path, "r", encoding="utf-8") as f:
                        chunks = processor(f.read())
                # For binary or special format files, pass the file path
                else:
                    chunks = processor(str(file_path))

                # Add chunks to ChromaDB
                if chunks:
                    self.collection.add(
                        documents=chunks,
                        metadatas=[
                            {"source": str(file_path)} for _ in chunks
                        ],
                        ids=[
                            f"{file_path.stem}_{i}"
                            for i in range(len(chunks))
                        ],
                    )
                    print(f"Successfully processed {file_path}")
                    return True
            else:
                print(f"Unsupported file type: {file_path}")
            return False
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            return False

    def query(
        self,
        query: str,
        n_results: int = 5,
        metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Query the document collection.

        Args:
            query: The search query
            n_results: Number of results to return
            metadata_filter: Optional filter for metadata fields

        Returns:
            List of dictionaries containing matched documents and their metadata
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=metadata_filter,
        )

        return [
            {"text": doc, "metadata": meta, "distance": dist}
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            )
        ]

    def get_relevant_context(
        self, query: str, max_tokens: int = 3000
    ) -> str:
        """
        Get relevant context for a query, ensuring the total tokens stay within limit.

        Args:
            query: The search query
            max_tokens: Maximum number of tokens to return

        Returns:
            A string containing the relevant context
        """
        results = self.query(query, n_results=10)
        context = ""
        current_tokens = 0

        for result in results:
            text = result["text"]
            # Rough estimate of tokens using word count
            word_count = len(text.split())

            if current_tokens + word_count > max_tokens:
                break

            context += text + "\n\n"
            current_tokens += word_count

        return context.strip()
