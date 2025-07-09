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

## About

Developed by [Swarms.ai](https://swarms.ai) and partners, AgentOS represents a production-ready implementation of autonomous AI agents, following the architectural principles outlined by Andrej Karpathy.

## Todo

- Implement python code executor, file finder, and more
- Implement file level embeddings
- Implement Audio summary and analysis
- Implement text to image and text to speech
- Implement text to video 



## Partners

Thank you to our partners for supporting the development of the agentic operating system. Below are some of the partner projects that we use in AgentOS.

| Partner Name              | Category     | RAG | LLM | Description                                      | Website                                 |
|---------------------------|-------------|-----|-----|--------------------------------------------------|-----------------------------------------|
| ChromaDB                  | Core Infra  | ✅  |     | Vector database for RAG and semantic search       | https://www.trychroma.com/              |
| Anthropic Claude          | LLM         |     | ✅  | Advanced language model (Claude 3 family)         | https://www.anthropic.com/              |
| LiteLLM                   | LLM         |     | ✅  | Unified API for multiple LLM providers            | https://github.com/BerriAI/litellm      |
| HuggingFace Transformers  | LLM         |     | ✅  | Open-source models and local LLM execution        | https://huggingface.co/transformers     |
| Claude Code SDK           | Dev Tool    |     |     | Code generation, manipulation, and execution      | https://github.com/kyegomez/claude-code-sdk |
| Browser-Use               | Automation  |     |     | Web automation and browser control                | https://github.com/kyegomez/browser-use |
| PyPDF2                    | Doc Proc    | ✅  |     | PDF document processing for RAG                   | https://pypi.org/project/PyPDF2/        |
| python-docx               | Doc Proc    | ✅  |     | Word document processing for RAG                  | https://pypi.org/project/python-docx/   |
| python-pptx               | Doc Proc    | ✅  |     | PowerPoint file processing for RAG                | https://pypi.org/project/python-pptx/   |
| BeautifulSoup4            | Doc Proc    | ✅  |     | HTML parsing and processing for RAG               | https://www.crummy.com/software/BeautifulSoup/ |
| Pandas                    | Doc Proc    | ✅  |     | Structured data (CSV, etc.) processing for RAG    | https://pandas.pydata.org/              |


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
