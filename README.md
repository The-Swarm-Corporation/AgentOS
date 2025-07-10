# AgentOS

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


A minimal, production-ready implementation of Andrej Karpathy's Agent Operating System architecture, developed by Swarms.ai and partners.

![AgentOS Architecture](https://miro.medium.com/v2/resize:fit:748/1*quuHoEjoCzxvu5lVp_SMEQ@2x.jpeg)

## Overview

AgentOS is a lightweight, single-file implementation that provides a robust foundation for building autonomous AI agents. It implements the core concepts outlined in Karpathy's Agent OS architecture while maintaining simplicity and extensibility.

## Features

- **Unified Model Interface**: Seamless integration with multiple LLM providers through LiteLLM
  - Support for Anthropic Claude models (Opus, Sonnet, Haiku)
  - Integration with OpenAI GPT models
  - Access to optimized variants (GPT-4o, GPT-4o-mini)
- **Browser Automation**: Built-in browser agent capabilities for web interaction using browser-use
- **Multi-Modal Support**: 
  - Text processing and generation
  - Video analysis through Google's Gemini models
  - Audio processing and speech synthesis
  - Image handling capabilities
- **Resource Management**: 
  - Efficient handling of computational resources
  - Dynamic model selection based on task requirements
  - Automatic GPU/CPU optimization
- **HuggingFace Integration**: 
  - Direct access to open-source models
  - Support for text generation and multiple NLP tasks
  - Automatic model quantization and optimization
- **Extensible Architecture**: Easy to add new capabilities and tools

## Core Components

- **Model Management**: Dynamic selection and utilization of language models
- **Browser Automation**: Autonomous web-based task execution
- **Resource Orchestration**: Efficient management of computational resources
- **Context Management**: Maintains system state and task dependencies

## Installation

```bash
pip3 install -U agentos-sdk
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

## About

Developed by [Swarms.ai](https://swarms.ai) and partners, AgentOS represents a production-ready implementation of autonomous AI agents, following the architectural principles outlined by Andrej Karpathy.

## Todo

- Implement python code executor, file finder, and more
- Implement file level embeddings
- Implement Audio summary and analysis
- Implement text to image and text to speech
- Implement text to video 



## Available Tools

AgentOS comes with a powerful set of built-in tools that enable various capabilities. Here's a comprehensive list of all available tools:

| Tool Name | Description | Use Case Examples |
|-----------|-------------|------------------|
| Browser Agent | Autonomous web browser automation tool that can navigate websites, extract information, and perform web-based tasks | - Web scraping<br>- Form filling<br>- Data extraction<br>- Website testing |
| Hugging Face Model | Interface for using various Hugging Face models for text generation and other NLP tasks | - Text generation<br>- Language translation<br>- Text classification<br>- Custom model inference |
| LiteLLM Model | Unified interface for multiple LLM providers including OpenAI, Anthropic, and others | - Text generation<br>- Chat completion<br>- Content creation<br>- Advanced reasoning |
| Safe Calculator | Secure mathematical expression evaluator with built-in safety checks | - Mathematical calculations<br>- Formula evaluation<br>- Secure computation<br>- Numeric processing |
| Terminal Developer Agent | Advanced agent for performing terminal operations and development tasks | - File operations<br>- Code execution<br>- System commands<br>- Development tasks |
| Generate Speech | Text-to-speech conversion tool supporting multiple voices and models | - Audio content creation<br>- Voice synthesis<br>- Accessibility features<br>- Audio narration |
| Generate Video | AI-powered video generation tool using Google's Veo 3.0 model | - Video content creation<br>- Visual storytelling<br>- Animation generation<br>- Creative content |


## Community 

Join our community of agent engineers and researchers for technical support, cutting-edge updates, and exclusive access to world-class agent engineering insights!

| Platform | Description | Link |
|----------|-------------|------|
| 📚 Documentation | Official documentation and guides | [docs.swarms.world](https://docs.swarms.world) |
| 📝 Blog | Latest updates and technical articles | [Medium](https://medium.com/@kyeg) |
| 💬 Discord | Live chat and community support | [Join Discord](https://discord.gg/jM3Z6M9uMq) |
| 🐦 Twitter | Latest news and announcements | [@kyegomez](https://twitter.com/kyegomez) |
| 👥 LinkedIn | Professional network and updates | [The Swarm Corporation](https://www.linkedin.com/company/the-swarm-corporation) |
| 📺 YouTube | Tutorials and demos | [Swarms Channel](https://www.youtube.com/channel/UC9yXyitkbU_WSy7bd_41SqQ) |
| 🎫 Events | Join our community events | [Sign up here](https://lu.ma/5p2jnc2v) |
| 🚀 Onboarding Session | Get onboarded with Kye Gomez, creator and lead maintainer of Swarms | [Book Session](https://cal.com/swarms/swarms-onboarding-session) |

## Contributing

We welcome contributions from the community. Please see our contributing guidelines for more information. 

## License

This project is under the MIT License.
