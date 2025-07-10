import os
import traceback
from typing import List, Optional

from loguru import logger
from swarms import Agent
from swarms.utils.formatter import formatter

from agentos_sdk.banner import AGENTOS_BANNER
from agentos_sdk.rag import RAGSystem
from agentos_sdk.prompt import AGENT_OS_SYSTEM_PROMPT
from agentos_sdk.tools import (
    run_browser_agent,
    call_huggingface_model,
    call_models_on_litellm,
    safe_calculator,
    call_terminal_developer_agent,
    generate_speech,
    respond_to_user,
    generate_video_single_clip,
    process_video_with_gemini,
    create_file,
    update_file,
)


class AgentOS:
    """
    AgentOS: A comprehensive autonomous operating system interface for managing and coordinating multiple computational resources.

    This class serves as the main interface for the AgentOS system, providing capabilities for:
    1. Task execution using various language models
    2. Browser automation
    3. Document retrieval and context management (RAG)
    4. Multi-modal processing (text, image, video, audio)

    The system is designed to be highly modular and extensible, allowing for easy integration
    of new capabilities and tools while maintaining a consistent interface for users.

    Attributes:
        model_name (str): The name of the primary language model to use
        system_prompt (str): The system prompt that defines the agent's behavior
        rag_system (RAGSystem): The retrieval-augmented generation system for document context
        rag_chunk_size (int): Size of chunks for document processing in RAG
        rag_collection_name (str): Name of the RAG document collection

    Example:
        >>> agent = AgentOS(model_name="gpt-4o-mini")
        >>> result = agent.run("Summarize the contents of document.pdf")
        >>> print(result)

    Notes:
        - The agent automatically initializes with a RAG system for document processing
        - Multiple tools are available including browser automation and model calling
        - The system can handle multi-modal inputs (text, images, video, audio)
        - Error handling is built-in for robustness
    """

    def __init__(
        self,
        model_name: str = "gpt-4o-mini",
        system_prompt: str = AGENT_OS_SYSTEM_PROMPT,
        rag_system: Optional[RAGSystem] = None,
        rag_chunk_size: int = 1000,
        rag_collection_name: str = "agentos_docs",
        artifacts_folder: str = "artifacts",
        streaming_on: bool = False,
        plan_on: bool = False,
        max_loops: int = 1,
        reasoning_agent_on: bool = False,
    ):
        self.model_name = model_name
        self.system_prompt = system_prompt
        self.rag_system = rag_system
        self.rag_chunk_size = rag_chunk_size
        self.rag_collection_name = rag_collection_name
        self.artifacts_folder = artifacts_folder
        self.streaming_on = streaming_on
        self.plan_on = plan_on
        self.max_loops = max_loops
        self.reasoning_agent_on = reasoning_agent_on

        self.setup_agent_os()

        tools = [
            run_browser_agent,
            call_huggingface_model,
            call_models_on_litellm,
            safe_calculator,
            call_terminal_developer_agent,
            generate_speech,
            respond_to_user,
            generate_video_single_clip,
            create_file,
            update_file,
        ]

        self.agent = Agent(
            model_name=model_name,
            system_prompt=system_prompt,
            agent_name="AgentOS",
            agent_description="An agent that can perform OS-level tasks",
            dynamic_temperature_enabled=True,
            tools=tools,
            streaming_on=self.streaming_on,
            interactive_on=False,
            max_turns=self.max_loops,
        )

        self.rag_system = self.setup_rag()

    def reasoning_agent(self):
        return Agent(
            agent_name="AgentOS Reasoning Module",
            agent_description="A reasoning agent that can reason about the task and perform it. It has access to the tools available to the main agent.",
            model_name="groq/deepseek-r1-distill-llama-70b",
            system_prompt=f"{AGENT_OS_SYSTEM_PROMPT}\n\nTools available: {self.create_names_for_tools()}",
            streaming_on=True,
        )

    def create_names_for_tools(self) -> str:
        # Get the names of the tools
        tool_names = [tool.__name__ for tool in self.agent.tools]
        return "\n".join(tool_names)

    def setup_agent_os(self):
        title = f"""
        Welcome to AgentOS
        
        {AGENTOS_BANNER}
        
        AgentOS is a comprehensive autonomous operating system interface for managing and coordinating multiple computational resources. 
        AgentOS is designed to be highly modular and extensible, allowing for easy integration of new capabilities and tools while maintaining a consistent interface for users.
        
        Tools available:
        - [Tool 1][Browser Agent][Description: The Browser Agent is a tool that can be used to navigate the web and perform tasks on the web.]
        - [Tool 2][Hugging Face Model][Description: The Hugging Face Model is a tool that can be used to generate text using a Hugging Face model.]
        - [Tool 3][Litellm Model][Description: The Litellm Model is a tool that can be used to generate text using a Litellm model.]
        - [Tool 4][Safe Calculator][Description: The Safe Calculator is a tool that can be used to perform calculations.]
        - [Tool 5][Terminal Developer Agent][Description: The Terminal Developer Agent is a tool that can be used to perform terminal tasks.]
        - [Tool 6][Generate Speech][Description: The Generate Speech is a tool that can be used to generate speech.]
        - [Tool 7][Generate Video][Description: The Generate Video is a tool that can be used to generate video.]
        
        Tutorial:
        
        Simply provide the task you want to perform and the agent will perform it. The more specific the task, the better the result.
        """
        formatter.print_panel(
            content=title,
            title="AgentOS",
        )

        self.env_warning()

    def setup_rag(self):
        """
        Set up the Retrieval-Augmented Generation (RAG) system.

        This method initializes the RAG system with the configured collection name and chunk size.
        The RAG system is used to provide relevant context from stored documents when processing tasks.

        Returns:
            RAGSystem: Initialized RAG system ready for document processing and retrieval.
        """
        return RAGSystem(
            collection_name=self.rag_collection_name,
            chunk_size=self.rag_chunk_size,
        )

    def env_warning(self):
        # We need to add warning for the user to set the environment variables
        if os.getenv("OPENAI_API_KEY") is None:
            logger.warning(
                "OPENAI_API_KEY is not set in your .env Please set the key. This is required for the browser agent and the main model."
            )
        elif os.getenv("ANTHROPIC_API_KEY") is None:
            logger.warning(
                "ANTHROPIC_API_KEY is not set in your .env Please set the key. This is required for the terminal developer agent."
            )
        elif os.getenv("GEMINI_API_KEY") is None:
            logger.warning(
                "GEMINI_API_KEY is not set in your .env Please set the key. This is required for video processing. You can get the key from https://console.cloud.google.com/apis/credentials"
            )
        else:
            logger.info("All environment variables are set")

    def add_file(self, file_path: str):
        """
        Add a single file to the RAG system's document collection.

        Args:
            file_path (str): Path to the file to be added to the RAG system.
                Supported formats depend on the RAG system's capabilities.
        """
        self.rag_system.add_document(file_path)

    def add_multiple_documents(self, file_paths: List[str]):
        """
        Add multiple files to the RAG system's document collection.

        Args:
            file_paths (List[str]): List of file paths to be added to the RAG system.
                All files should be in supported formats.
        """
        self.rag_system.add_multiple_documents(file_paths)

    def add_folder(self, folder_path: str):
        """
        Add all supported files from a folder to the RAG system.

        Args:
            folder_path (str): Path to the folder containing documents to be added.
                The system will recursively process all supported files in the folder.
        """
        self.rag_system.add_folder(folder_path)

    def clear_processed_files(self):
        """
        Clear all processed files from the RAG system.

        This method removes all documents from the RAG system's collection,
        effectively resetting its knowledge base.
        """
        self.rag_system.clear_processed_files()

    def run(
        self,
        task: str,
        img: str = None,
        video: str = None,
        audio: str = None,
    ):
        """
        Execute a task using the AgentOS system with optional multi-modal inputs.

        This method processes the given task using the configured language model and tools.
        It can handle various types of inputs including text, images, video, and audio.
        The system automatically retrieves relevant context from the RAG system if available.

        Args:
            task (str): The main task or query to be processed.
            img (str, optional): Path to an image file for image-based tasks. Defaults to None.
            video (str, optional): Path to a video file for video-based tasks. Defaults to None.
            audio (str, optional): Path to an audio file for audio-based tasks. Defaults to None.

        Returns:
            str: The result of the task execution. If an error occurs, returns an error message.

        Example:
            >>> agent = AgentOS()
            >>> result = agent.run(
            ...     task="Analyze this image and summarize its contents",
            ...     img="path/to/image.jpg"
            ... )
            >>> print(result)

        Notes:
            - The method automatically incorporates RAG context if available
            - Video processing is handled by the Gemini model if video input is provided
            - The system handles None responses gracefully
            - Errors are caught and returned as informative messages
        """
        try:

            task_prompt = ""

            # Plan prompt
            if self.plan_on:
                planning_agent = self.reasoning_agent()
                plan_prompt = planning_agent.run(
                    task=f"Make a plan for the task: {task}. What are the steps to complete the task? Use the following tools: {self.create_names_for_tools()}"
                )
                task_prompt += f"Plan:\n{plan_prompt}\n\n"

            # Add RAG context if available
            if self.rag_system:
                context = self.rag_system.get_relevant_context(task)
                if context:
                    task_prompt += (
                        f"Context from knowledge base:\n{context}\n\n"
                    )

            if video:
                out = process_video_with_gemini(
                    video_path=video, task=task
                )
                task_prompt += f"Video Analysis Output:\n{out}\n\n"

            final_output = self.agent.run(
                task=task_prompt + task if task_prompt else task,
                img=img,
            )

            # Handle None response
            if final_output is None:
                return "No response generated. Please try again."

            return final_output

        except Exception as e:
            logger.error(
                f"Error running AgentOS: {str(e)} Traceback: {traceback.format_exc()}"
            )

    def batched_run(
        self,
        tasks: List[str],
        imgs: List[str] = None,
        videos: List[str] = None,
        audios: List[str] = None,
    ):
        """
        Execute a list of tasks in a batched manner.
        """
        outputs = []
        for task, img, video, audio in zip(
            tasks, imgs, videos, audios
        ):
            outputs.append(self.run(task, img, video, audio))
        return outputs


# if __name__ == "__main__":
#     agent = AgentOS()
#     print(agent.run(task="Use the browser agent to find the best performing crypto coins on coinmarketcap"))
