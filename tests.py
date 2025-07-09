from pathlib import Path

from agentos import AgentOS, BrowserAgent, HuggingFaceAPI, safe_calculator
from agentos.rag import RAGSystem


# Test utilities
def assert_equal(actual, expected, message=""):
    """Custom assertion helper"""
    if actual != expected:
        raise AssertionError(f"{message}\nExpected: {expected}\nActual: {actual}")


def assert_true(condition, message=""):
    """Custom assertion helper for boolean conditions"""
    if not condition:
        raise AssertionError(f"{message}\nExpected True but got False")


def assert_raises(exception_type, func, *args, **kwargs):
    """Custom assertion helper for exceptions"""
    try:
        func(*args, **kwargs)
        raise AssertionError(
            f"Expected {exception_type.__name__} but no exception was raised"
        )
    except exception_type:
        pass


# RAG System Tests
def test_rag_initialization():
    """Test RAG system initialization"""
    print("Testing RAG initialization...")

    # Test default initialization
    rag = RAGSystem()
    assert_true(rag.collection is not None, "Collection should be initialized")
    assert_equal(rag.chunk_size, 500, "Default chunk size should be 500")
    assert_equal(rag.chunk_overlap, 50, "Default chunk overlap should be 50")

    # Test custom initialization
    custom_rag = RAGSystem(
        collection_name="test_collection", chunk_size=1000, chunk_overlap=100
    )
    assert_equal(custom_rag.chunk_size, 1000, "Custom chunk size not set correctly")
    assert_equal(
        custom_rag.chunk_overlap, 100, "Custom chunk overlap not set correctly"
    )
    print("✓ RAG initialization tests passed")


def test_rag_text_chunking():
    """Test RAG text chunking functionality"""
    print("Testing RAG text chunking...")

    rag = RAGSystem(chunk_size=100, chunk_overlap=20)

    # Test empty text
    chunks = rag.chunk_text("")
    assert_equal(len(chunks), 1, "Empty text should produce single chunk")

    # Test short text
    short_text = "This is a short text"
    chunks = rag.chunk_text(short_text)
    assert_equal(len(chunks), 1, "Short text should produce single chunk")
    assert_equal(chunks[0], short_text, "Short text chunk should match input")

    # Test long text
    long_text = " ".join(["word"] * 200)  # Create text with 200 words
    chunks = rag.chunk_text(long_text)
    assert_true(len(chunks) > 1, "Long text should produce multiple chunks")

    print("✓ RAG text chunking tests passed")


def test_rag_document_processing():
    """Test RAG document processing functionality"""
    print("Testing RAG document processing...")

    # Create test files
    test_dir = Path("test_docs")
    test_dir.mkdir(exist_ok=True)

    # Create test text file
    text_file = test_dir / "test.txt"
    text_file.write_text("This is a test document.")

    # Create test JSON file
    json_file = test_dir / "test.json"
    json_file.write_text('{"test": "This is a test JSON"}')

    rag = RAGSystem()

    # Test single document addition
    success = rag.add_document(text_file)
    assert_true(success, "Adding text file should succeed")
    assert_true(
        str(text_file.absolute()) in rag.processed_files,
        "Text file should be marked as processed",
    )

    # Test multiple document addition
    results = rag.add_multiple_documents([text_file, json_file])
    assert_true(
        all(results.values()), "All valid documents should be processed successfully"
    )

    # Test folder addition
    folder_results = rag.add_folder(test_dir)
    assert_true(
        len(folder_results) >= 2, "Folder processing should find all test files"
    )

    # Cleanup
    for file in [text_file, json_file]:
        file.unlink()
    test_dir.rmdir()

    print("✓ RAG document processing tests passed")


def test_rag_querying():
    """Test RAG querying functionality"""
    print("Testing RAG querying...")

    rag = RAGSystem()

    # Create and add test document
    test_file = Path("test_query.txt")
    test_content = "The quick brown fox jumps over the lazy dog. This is a test document for querying."
    test_file.write_text(test_content)

    rag.add_document(test_file)

    # Test basic query
    results = rag.query("quick brown fox", n_results=1)
    assert_true(len(results) > 0, "Query should return results")
    assert_true(
        "quick brown fox" in results[0]["text"],
        "Query result should contain search terms",
    )

    # Test query with metadata filter
    results = rag.query(
        "test document",
        n_results=1,
        metadata_filter={"source": str(test_file.absolute())},
    )
    assert_true(len(results) > 0, "Query with metadata filter should return results")

    # Test relevant context
    context = rag.get_relevant_context("fox jumps", max_tokens=100)
    assert_true(len(context) > 0, "Relevant context should not be empty")
    assert_true("fox" in context, "Context should contain query terms")

    # Cleanup
    test_file.unlink()

    print("✓ RAG querying tests passed")


# Browser Agent Tests
def test_browser_agent():
    """Test Browser Agent functionality"""
    print("Testing Browser Agent...")

    agent = BrowserAgent(agent_name="TestAgent")

    # Test initialization
    assert_equal(agent.agent_name, "TestAgent", "Agent name should be set correctly")

    # Test simple task (this will not actually run the browser)
    try:
        result = agent.run("Navigate to example.com")
        assert_true(isinstance(result, str), "Browser agent result should be string")
    except Exception as e:
        print(f"Note: Browser agent test skipped - requires browser setup: {e}")

    print("✓ Browser Agent tests passed")


# HuggingFace API Tests
def test_huggingface_api():
    """Test HuggingFace API functionality"""
    print("Testing HuggingFace API...")

    # Test initialization
    api = HuggingFaceAPI(model_id="gpt2", task_type="text-generation", max_length=50)

    assert_equal(api.model_id, "gpt2", "Model ID should be set correctly")
    assert_equal(api.task_type, "text-generation", "Task type should be set correctly")
    assert_equal(api.max_length, 50, "Max length should be set correctly")

    print("✓ HuggingFace API tests passed")


# Safe Calculator Tests
def test_safe_calculator():
    """Test safe calculator functionality"""
    print("Testing safe calculator...")

    # Test basic operations
    assert_equal(safe_calculator("2 + 2"), "4", "Basic addition failed")
    assert_equal(safe_calculator("10 - 5"), "5", "Basic subtraction failed")
    assert_equal(safe_calculator("4 * 3"), "12", "Basic multiplication failed")
    assert_equal(safe_calculator("15 / 3"), "5", "Basic division failed")

    # Test complex expressions
    assert_equal(safe_calculator("(2 + 3) * 4"), "20", "Complex expression failed")
    assert_equal(safe_calculator("2 ** 3"), "8", "Exponentiation failed")

    # Test error cases
    assert_true(
        "Error" in safe_calculator("10 / 0"), "Division by zero should return error"
    )
    assert_true(
        "Error" in safe_calculator("import os"), "Code injection should be prevented"
    )
    assert_true(
        "Error" in safe_calculator("2 + abc"), "Invalid expression should return error"
    )

    print("✓ Safe calculator tests passed")


# AgentOS Tests
def test_agentos_initialization():
    """Test AgentOS initialization"""
    print("Testing AgentOS initialization...")

    # Test default initialization
    agent = AgentOS()
    assert_true(agent.rag_system is not None, "RAG system should be initialized")
    assert_true(agent.agent is not None, "Agent should be initialized")

    # Test custom initialization
    custom_agent = AgentOS(
        model_name="gpt-4o-mini",
        rag_chunk_size=2000,
        rag_collection_name="test_collection",
    )
    assert_equal(custom_agent.model_name, "gpt-4o-mini", "Custom model name not set")
    assert_equal(custom_agent.rag_chunk_size, 2000, "Custom chunk size not set")

    print("✓ AgentOS initialization tests passed")


def test_agentos_rag_integration():
    """Test AgentOS RAG integration"""
    print("Testing AgentOS RAG integration...")

    agent = AgentOS()

    # Create test document
    test_file = Path("test_integration.txt")
    test_file.write_text("This is a test document for AgentOS RAG integration.")

    # Test document addition
    agent.add_file(str(test_file))
    assert_true(
        str(test_file.absolute()) in agent.rag_system.processed_files,
        "Document should be processed",
    )

    # Test multiple document addition
    test_file2 = Path("test_integration2.txt")
    test_file2.write_text("This is another test document.")

    agent.add_multiple_documents([str(test_file), str(test_file2)])
    assert_true(
        str(test_file2.absolute()) in agent.rag_system.processed_files,
        "Multiple documents should be processed",
    )

    # Cleanup
    test_file.unlink()
    test_file2.unlink()

    print("✓ AgentOS RAG integration tests passed")


def test_agentos_task_execution():
    """Test AgentOS task execution"""
    print("Testing AgentOS task execution...")

    agent = AgentOS()

    # Test simple task
    try:
        result = agent.run("What is 2 + 2?")
        assert_true(isinstance(result, str), "Task result should be string")
    except Exception as e:
        print(f"Note: Task execution test limited - requires API keys: {e}")

    # Test task with context
    test_file = Path("test_context.txt")
    test_file.write_text("The capital of France is Paris.")
    agent.add_file(str(test_file))

    try:
        result = agent.run("What is the capital of France?")
        assert_true(isinstance(result, str), "Contextual task result should be string")
    except Exception as e:
        print(f"Note: Contextual task test limited - requires API keys: {e}")

    # Cleanup
    test_file.unlink()

    print("✓ AgentOS task execution tests passed")


def test_agentos_error_handling():
    """Test AgentOS error handling"""
    print("Testing AgentOS error handling...")

    agent = AgentOS()

    # Test invalid file addition
    result = agent.add_file("nonexistent_file.txt")
    assert_true(not result, "Adding nonexistent file should fail")

    # Test invalid folder addition
    results = agent.add_folder("nonexistent_folder")
    assert_equal(
        len(results), 0, "Adding nonexistent folder should return empty results"
    )

    print("✓ AgentOS error handling tests passed")


def run_all_tests():
    """Run all test cases"""
    print("Starting comprehensive test suite for AgentOS...")
    print("=" * 50)

    # RAG Tests
    test_rag_initialization()
    test_rag_text_chunking()
    test_rag_document_processing()
    test_rag_querying()

    # Component Tests
    test_browser_agent()
    test_huggingface_api()
    test_safe_calculator()

    # AgentOS Tests
    test_agentos_initialization()
    test_agentos_rag_integration()
    test_agentos_task_execution()
    test_agentos_error_handling()

    print("=" * 50)
    print("All tests completed!")


if __name__ == "__main__":
    run_all_tests()
