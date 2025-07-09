# AgentOS

A minimal, production-ready implementation of Andrej Karpathy's Agent Operating System architecture, developed by Swarms.ai and partners.

![AgentOS Architecture](https://miro.medium.com/v2/resize:fit:748/1*quuHoEjoCzxvu5lVp_SMEQ@2x.jpeg)

## Overview

AgentOS is a lightweight, single-file implementation that provides a robust foundation for building autonomous AI agents. It implements the core concepts outlined in Karpathy's Agent OS architecture while maintaining simplicity and extensibility.

## Features

- **Unified Model Interface**: Seamless integration with multiple LLM providers through LiteLLM
- **Browser Automation**: Built-in browser agent capabilities for web interaction
- **Multi-Modal Support**: Handles text, video, and audio inputs
- **Resource Management**: Efficient handling of computational resources and model selection
- **HuggingFace Integration**: Direct access to open-source models
- **Extensible Architecture**: Easy to add new capabilities and tools

## Core Components

- **Model Management**: Dynamic selection and utilization of language models
- **Browser Automation**: Autonomous web-based task execution
- **Resource Orchestration**: Efficient management of computational resources
- **Context Management**: Maintains system state and task dependencies

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from agentos import AgentOS

# Initialize AgentOS
agent_os = AgentOS()

# Run a task
result = agent_os.run(
    task="Your task description",
    img="optional_image.jpg",
    video="optional_video.mp4",
    audio="optional_audio.mp3"
)
```

## Supported Models

### Anthropic Claude Models
- claude-opus-4-20250514
- claude-sonnet-4-20250514
- claude-3-sonnet-20240229
- claude-3-haiku-20240307
- And more...

### OpenAI GPT Models
- gpt-4-1106-preview
- gpt-4-vision-preview
- gpt-3.5-turbo
- And more...

## License

[License details]

## About

Developed by [Swarms.ai](https://swarms.ai) and partners, AgentOS represents a production-ready implementation of autonomous AI agents, following the architectural principles outlined by Andrej Karpathy.

## Contributing

We welcome contributions from the community. Please see our contributing guidelines for more information. 