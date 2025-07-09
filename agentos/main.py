from swarms import Agent


import asyncio

from browser_use import Agent as BrowserAgentBase
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    pipeline,
)
import torch
from typing import Optional, Dict, Any, List, Union
from litellm import completion

load_dotenv()


# System prompt for AgentOS
AGENT_OS_SYSTEM_PROMPT = """
# AgentOS: Autonomous Operating System Interface

You are AgentOS, an advanced autonomous operating system interface designed to seamlessly manage and coordinate multiple computational resources, models, and browser-based interactions. Your core function is to serve as an intelligent intermediary between the user and various computational resources.

## Core Capabilities

1. Model Management:
   - Dynamically select and utilize appropriate language models based on task requirements
   - Switch between models (HuggingFace, LiteLLM, etc.) for optimal performance
   - Handle multi-modal inputs including text, images, video, and audio

2. Browser Automation:
   - Execute complex web-based tasks autonomously
   - Navigate websites, fill forms, and extract information
   - Maintain session state and handle authentication

3. Resource Orchestration:
   - Manage computational resources efficiently
   - Handle parallel processing when beneficial
   - Monitor and optimize resource utilization

## Operating Principles

1. Task Analysis:
   - Analyze user requests to determine required resources and tools
   - Break down complex tasks into manageable sub-tasks
   - Plan execution strategy considering available tools and models

2. Intelligent Tool Selection:
   - Choose appropriate tools based on task requirements:
     * Browser automation for web-based tasks
     * HuggingFace models for specific ML tasks
     * LiteLLM for advanced language processing
     * Video/audio processing for multimedia tasks

3. Adaptive Response:
   - Monitor task execution and adjust strategy as needed
   - Handle errors and exceptions gracefully
   - Provide clear feedback on task progress and results

4. Context Management:
   - Maintain awareness of current system state
   - Track ongoing tasks and their dependencies
   - Manage resource allocation and deallocation

## Interaction Protocol

1. Input Processing:
   - Parse user requests for intent and requirements
   - Identify required tools and resources
   - Validate feasibility of requested operations

2. Execution:
   - Select and initialize appropriate tools
   - Monitor execution progress
   - Handle errors and retries when necessary

3. Output Generation:
   - Format results appropriately
   - Provide relevant context and explanations
   - Include any necessary follow-up actions

## Security and Safety

1. Resource Protection:
   - Validate all operations before execution
   - Prevent unauthorized access or harmful operations
   - Maintain system stability and integrity

2. Error Handling:
   - Implement robust error detection and recovery
   - Provide clear error messages and suggested solutions
   - Maintain system state consistency

## Performance Optimization

1. Resource Management:
   - Optimize model selection based on task requirements
   - Manage memory and computational resources efficiently
   - Implement caching when beneficial

2. Task Scheduling:
   - Prioritize tasks based on importance and dependencies
   - Manage parallel execution when possible
   - Handle task queuing and scheduling

Remember: You are an integral part of the system, responsible for making intelligent decisions about resource utilization and task execution. Always strive to provide the most efficient and effective solution to user requests while maintaining system stability and security.
"""


class HuggingFaceAPI:
    """A general class to handle various Hugging Face models and tasks."""

    def __init__(
        self,
        model_id: str,
        task_type: str = "text-generation",
        device: Optional[str] = None,
        max_length: int = 100,
        quantize: bool = False,
        quantization_config: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        """
        Initialize the HuggingFace API wrapper.

        Args:
            model_id (str): The model ID from Hugging Face Hub
            task_type (str): Type of task ("text-generation", "question-answering", etc.)
            device (str, optional): Device to run the model on ("cuda", "cpu")
            max_length (int): Maximum length for generated text
            quantize (bool): Whether to use quantization
            quantization_config (dict, optional): Configuration for quantization
            **kwargs: Additional arguments for model initialization
        """
        self.model_id = model_id
        self.task_type = task_type
        self.device = device or (
            "cuda" if torch.cuda.is_available() else "cpu"
        )
        self.max_length = max_length
        self.quantize = quantize
        self.quantization_config = quantization_config or {}

        # Initialize the pipeline based on task type
        try:
            self.pipeline = pipeline(
                task=task_type,
                model=model_id,
                device=self.device,
                **kwargs,
            )
        except Exception as e:
            print(f"Error initializing pipeline: {e}")
            # Fallback to manual model loading
            self.model = AutoModelForCausalLM.from_pretrained(
                model_id,
                device_map=self.device,
                torch_dtype=(
                    torch.float16
                    if self.device == "cuda"
                    else torch.float32
                ),
                **kwargs,
            )
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            self.pipeline = None

    def generate(
        self,
        prompt: str,
        max_length: Optional[int] = None,
        num_return_sequences: int = 1,
        **kwargs,
    ) -> Union[str, List[str]]:
        """
        Generate text using the model.

        Args:
            prompt (str): Input text prompt
            max_length (int, optional): Override default max_length
            num_return_sequences (int): Number of sequences to generate
            **kwargs: Additional generation parameters

        Returns:
            Union[str, List[str]]: Generated text or list of generated texts
        """
        try:
            if self.pipeline:
                outputs = self.pipeline(
                    prompt,
                    max_length=max_length or self.max_length,
                    num_return_sequences=num_return_sequences,
                    **kwargs,
                )

                if isinstance(outputs, list):
                    if self.task_type == "text-generation":
                        return [
                            out["generated_text"] for out in outputs
                        ]
                    return outputs
                return (
                    outputs["generated_text"]
                    if "generated_text" in outputs
                    else outputs
                )

            # Manual generation if pipeline is not available
            inputs = self.tokenizer(prompt, return_tensors="pt").to(
                self.device
            )
            outputs = self.model.generate(
                **inputs,
                max_length=max_length or self.max_length,
                num_return_sequences=num_return_sequences,
                **kwargs,
            )
            return self.tokenizer.batch_decode(
                outputs, skip_special_tokens=True
            )

        except Exception as e:
            print(f"Error in generation: {e}")
            return f"Error generating text: {str(e)}"

    def run(self, task: str, **kwargs) -> str:
        """
        Run the model on a given task.

        Args:
            task (str): The task/prompt to process
            **kwargs: Additional parameters for generation

        Returns:
            str: Generated output
        """
        result = self.generate(task, **kwargs)
        if isinstance(result, list):
            return result[0]
        return result


def call_huggingface_model(
    task: str,
    model_id: str,
    max_length: int = 100,
) -> str:
    """
    Call a Hugging Face model to perform a text generation task.

    This function provides a simplified interface to interact with Hugging Face models.
    It creates a new instance of HuggingFaceAPI for each call, which ensures clean
    state management but may impact performance for repeated calls to the same model.

    Args:
        task (str): The text prompt or task description to be processed by the model.
            This could be a question, a text completion prompt, or any other text input
            that the model should process.

        model_id (str): The identifier of the Hugging Face model to use.
            Examples:
            - "gpt2" for OpenAI's GPT-2 model
            - "facebook/opt-350m" for Meta's OPT model
            - "bigscience/bloom" for the BLOOM model
            For a complete list, visit: https://huggingface.co/models

        max_length (int, optional): The maximum length of the generated text in tokens.
            Defaults to 100. This parameter helps control the length of the model's
            output and manage computational resources.

    Returns:
        str: The generated text output from the model. The exact format depends on
            the model being used, but typically includes:
            - For text generation: The completed text based on the input prompt
            - For question answering: The answer to the provided question
            - For other tasks: Task-specific output in text format

    Examples:
        >>> # Generate text with GPT-2
        >>> result = call_huggingface_model(
        ...     task="Once upon a time",
        ...     model_id="gpt2",
        ...     max_length=50
        ... )
        >>> print(result)

        >>> # Use a larger model for more complex tasks
        >>> answer = call_huggingface_model(
        ...     task="What is quantum computing?",
        ...     model_id="facebook/opt-1.3b",
        ...     max_length=200
        ... )
        >>> print(answer)

    Notes:
        - The function creates a new model instance for each call, which may be
          inefficient for repeated calls to the same model.
        - The model is automatically placed on GPU if available, falling back to CPU.
        - Error handling is managed by the underlying HuggingFaceAPI class.
        - The actual output length may be shorter than max_length depending on the
          model's generation parameters and stopping criteria.

    Raises:
        Exception: Any exceptions from model loading or generation are caught by
            HuggingFaceAPI and returned as error messages in the output string.
    """
    model = HuggingFaceAPI(
        model_id=model_id,
        task_type="text-generation",
        max_length=max_length,
    )
    return model.run(task)


def call_models_on_litellm(
    model_name: str,
    task: str,
    temperature: float = 0.5,
    system_prompt: str = None,
):
    """
    Call various LLM models through litellm's unified interface with automatic token management.

    This function provides a standardized way to interact with multiple LLM providers and models
    through litellm's abstraction layer. It automatically handles token limits and provides a
    consistent interface across different model providers.

    Available Models:

    Anthropic Claude Models:
        - 'claude-opus-4-20250514': Latest Claude Opus model (most capable)
        - 'claude-sonnet-4-20250514': Latest Claude Sonnet model (balanced)
        - 'claude-3-7-sonnet-20250219': Claude 3.7 Sonnet
        - 'claude-3-5-sonnet-20240620': Claude 3.5 Sonnet
        - 'claude-3-haiku-20240307': Claude 3 Haiku (fastest)
        - 'claude-3-opus-20240229': Claude 3 Opus
        - 'claude-3-sonnet-20240229': Claude 3 Sonnet
        - 'claude-2.1': Legacy Claude 2.1
        - 'claude-2': Legacy Claude 2
        - 'claude-instant-1.2': Legacy Claude Instant 1.2
        - 'claude-instant-1': Legacy Claude Instant 1

    OpenAI GPT Models:
        - 'gpt-4-1106-preview': GPT-4 Turbo
        - 'gpt-4-vision-preview': GPT-4 with vision capabilities
        - 'gpt-4': Base GPT-4 model
        - 'gpt-3.5-turbo': GPT-3.5 Turbo
        - 'gpt-3.5-turbo-16k': GPT-3.5 with 16k context

    Other Models:
        - 'gpt-4o-mini': GPT-4 Optimized Mini variant
        - Additional models supported by litellm (see litellm docs)

    Args:
        model_name (str): The identifier for the model to use. Must be one of the supported
            model names listed above.
        task (str): The task or prompt to send to the model.
        temperature (float, optional): Controls randomness in the model's output.
            Ranges from 0.0 (deterministic) to 1.0 (creative). Defaults to 0.5.
        system_prompt (str, optional): A system-level prompt to guide the model's behavior.
            If None, no system prompt is used.

    Returns:
        str: The model's response text.

    Examples:
        >>> # Using Claude 3 Opus for complex reasoning
        >>> response = call_models_on_litellm(
        ...     model_name="claude-3-opus-20240229",
        ...     task="Explain quantum computing to a high school student",
        ...     temperature=0.7,
        ...     system_prompt="You are a helpful physics teacher"
        ... )
        >>> print(response)

        >>> # Using GPT-4 for code generation
        >>> code = call_models_on_litellm(
        ...     model_name="gpt-4",
        ...     task="Write a Python function to calculate Fibonacci numbers",
        ...     temperature=0.2
        ... )
        >>> print(code)

    Notes:
        - Token limits are automatically handled by litellm based on the model's capabilities
        - The function uses litellm's completion endpoint which provides a unified interface
        - System prompts can help guide the model's behavior and role
        - Temperature values closer to 0 are better for tasks requiring accuracy
        - Temperature values closer to 1 are better for creative tasks
    """
    from litellm.utils import get_max_tokens

    max_llm_tokens = get_max_tokens(model_name)

    response = completion(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": task},
        ],
        temperature=temperature,
        max_tokens=max_llm_tokens,
        top_p=1,
    )

    return response.choices[0].message.content


class BrowserAgent:
    def __init__(
        self,
        agent_name: str = "BrowserAgent",
        model_name: str = "claude-3-5-sonnet-20240620",
    ):
        self.agent_name = agent_name

    async def call_browser_agent(self, task: str):
        """
        Asynchronously executes a browser automation agent to perform a specified task.

        This method creates an instance of the BrowserAgentBase, which is configured to use
        a language model (currently hardcoded to OpenAI's GPT-4o) to interpret and execute
        the provided task in a browser environment. The agent is run asynchronously, and upon
        completion, the result is serialized to a JSON-formatted string with indentation for readability.

        Args:
            task (str): A natural language description of the task to be performed by the browser agent.
                This could be anything from "search for the latest news on AI" to "fill out a web form".

        Returns:
            str: A JSON-formatted string representing the result of the browser agent's execution.
                The structure of the JSON includes details about the actions taken, the final state,
                and any outputs or errors encountered during execution.

        Example:
            >>> agent = BrowserAgent()
            >>> asyncio.run(agent.call_browser_agent("Search for weather in New York"))
            '{\n    "model_output": {...},\n    "result": [...],\n    "state": {...}\n}'
        """
        agent = BrowserAgentBase(
            task=task,
            llm=ChatOpenAI(model="gpt-4o"),
        )
        result = await agent.run()
        return result.model_dump_json(indent=4)

    def run(self, task: str):
        """
        Synchronously runs the browser agent for a given task.

        This method wraps the asynchronous `call_browser_agent` method, allowing users to
        invoke the browser agent in a blocking (synchronous) manner. It is suitable for
        scripts or environments where asynchronous execution is not desired or supported.

        Args:
            task (str): The task description for the browser agent to perform. This should be
                a clear, natural language instruction describing what the agent should do in the browser.

        Returns:
            str: The JSON-formatted result of the browser agent's execution, as returned by
                `call_browser_agent`. This includes the full trace of actions, results, and state.

        Example:
            >>> result = BrowserAgent().run("Find the top 3 trending GitHub repositories")
            >>> print(result)
            {
                "model_output": {...},
                "result": [...],
                "state": {...}
            }
        """
        return asyncio.run(self.call_browser_agent(task))


def process_video_with_gemini(
    video_path: str = None,
    task: str = "Create a detailed and comprehensive summary of the video",
    model_name: str = "gemini-2.0-flash",
):
    from google import genai

    client = genai.Client()

    myfile = client.files.upload(file=video_path)

    response = client.models.generate_content(
        model=model_name, contents=[myfile, task]
    )

    print(response.text)


def run_browser_agent(task: str) -> str:
    """
    Run the browser agent on a given task and return the result as a JSON-formatted string.

    This is a convenience function that instantiates a `BrowserAgent` and executes the specified
    task using the agent. It abstracts away the details of agent instantiation and execution,
    providing a simple interface for running browser automation tasks.

    Args:
        task (str): The task description for the browser agent to perform. This should be a
            natural language instruction, such as "navigate to example.com and extract the headline".

    Returns:
        str: The JSON-formatted result of the browser agent's execution. The output includes
            detailed information about the actions performed, the resulting browser state,
            and any outputs or errors encountered.

    Example:
        >>> output = run_browser_agent("Go to Wikipedia and summarize the main page")
        >>> print(output)
        {
            "model_output": {...},
            "result": [...],
            "state": {...}
        }

    Notes:
        - The agent uses a language model (currently GPT-4o) to interpret and execute the task.
        - The returned JSON can be parsed for further programmatic analysis or logging.
        - This function is blocking and should be called from synchronous code.
    """
    model: BrowserAgent = BrowserAgent()
    return model.run(task)


class AgentOS:
    def __init__(
        self,
        model_name: str = "claude-3-5-sonnet-20240620",
        system_prompt: str = AGENT_OS_SYSTEM_PROMPT,
    ):
        self.model_name = model_name
        self.system_prompt = system_prompt

        self.agent = Agent(
            model=model_name,
            system_prompt=system_prompt,
            agent_name="AgentOS",
            description="An agent that can perform OS-level tasks",
            tools=[
                run_browser_agent,
                call_huggingface_model,
                call_models_on_litellm,
            ],  # Add HuggingFace API as a tool
            dynamic_temperature_enabled=True,
        )

    def run(
        self,
        task: str,
        img: str = None,
        video: str = None,
        audio: str = None,
    ):
        task_prompt = ""

        if video:
            out = process_video_with_gemini(
                video_path=video, task=task
            )

            task_prompt += f"Video Analysis Output:\n{out}\n\n"

        final_output = self.agent.run(task=task_prompt, img=img)

        return final_output
