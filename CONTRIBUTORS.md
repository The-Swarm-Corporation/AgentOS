# Contributing to AgentOS

Welcome to the AgentOS community! We're excited that you're interested in contributing. AgentOS is an open-source project that aims to provide a robust foundation for building autonomous AI agents, and we welcome contributions of all kinds from the community.

## Ways to Contribute

There are many ways to contribute to AgentOS:

1. **Code Contributions**
   - Implement new features
   - Fix bugs
   - Improve performance
   - Add new tools and capabilities
   - Enhance existing tools

2. **Documentation**
   - Improve existing documentation
   - Add examples and tutorials
   - Write API documentation
   - Create user guides

3. **Testing**
   - Write unit tests
   - Add integration tests
   - Perform manual testing
   - Report test coverage

4. **Issues and Bug Reports**
   - Report bugs
   - Suggest new features
   - Help reproduce issues
   - Verify bug fixes

5. **Tool Development**
   - Create new tools for AgentOS
   - Enhance existing tools
   - Add support for new models
   - Integrate new services

## Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/AgentOS.git
   cd AgentOS
   ```

2. **Set Up Python Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install poetry
   poetry install
   ```

3. **Install Development Dependencies**
   ```bash
   poetry install --with lint,test
   ```

4. **Set Up Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys:
   # - OPENAI_API_KEY
   # - ANTHROPIC_API_KEY
   # - GEMINI_API_KEY
   ```

## Code Style and Standards

We use several tools to maintain code quality:

1. **Black** for code formatting
   ```bash
   poetry run black .
   ```

2. **Ruff** for linting
   ```bash
   poetry run ruff check .
   ```

3. **MyPy** for type checking
   ```bash
   poetry run mypy .
   ```

Our code style follows these guidelines:
- Line length: 70 characters (as configured in pyproject.toml)
- Python version: 3.10 or higher
- Type hints are required for all new code
- Docstrings follow Google style

## Adding New Tools

AgentOS is designed to be extensible through tools. To add a new tool:

1. Create a new function in the appropriate module
2. Follow this template:
   ```python
   def your_tool_name(
       param1: type1,
       param2: type2,
       # ... other parameters
   ) -> return_type:
       """
       Detailed description of what the tool does.

       Args:
           param1: Description of param1
           param2: Description of param2

       Returns:
           Description of return value

       Example:
           >>> result = your_tool_name(param1, param2)
           >>> print(result)
       """
       # Implementation
   ```

3. Add your tool to the `tools` list in `AgentOS` class
4. Add tests for your tool in the `tests` directory
5. Update documentation to include your tool

## Performance Improvements

When working on performance:

1. **Profiling**
   - Use cProfile or line_profiler to identify bottlenecks
   - Document performance benchmarks

2. **Optimization Strategies**
   - Implement caching where appropriate
   - Use async/await for I/O-bound operations
   - Optimize model calls and token usage
   - Implement batching for multiple operations

3. **Memory Management**
   - Monitor memory usage
   - Implement cleanup for large objects
   - Use generators for large datasets

## Issue Reporting

When reporting issues:

1. **Bug Reports**
   ```markdown
   ### Description
   Clear description of the issue

   ### Steps to Reproduce
   1. Step one
   2. Step two
   3. ...

   ### Expected Behavior
   What should happen

   ### Actual Behavior
   What actually happens

   ### Environment
   - OS:
   - Python version:
   - AgentOS version:
   - Relevant package versions:
   ```

2. **Feature Requests**
   ```markdown
   ### Feature Description
   Clear description of the proposed feature

   ### Use Case
   Why this feature would be useful

   ### Proposed Implementation
   Optional: How you think this could be implemented
   ```

## Pull Request Process

1. **Before Creating a PR**
   - Create a new branch for your changes
   - Run all tests locally
   - Update documentation as needed
   - Add tests for new features

2. **PR Description Template**
   ```markdown
   ### Description
   What does this PR do?

   ### Changes
   - Change 1
   - Change 2
   ...

   ### Testing
   How was this tested?

   ### Documentation
   Links to updated documentation
   ```

3. **Review Process**
   - All PRs require at least one review
   - Address review comments
   - Ensure CI passes
   - Keep PRs focused and small

## Community and Communication

- Join our [Discord](https://discord.gg/jM3Z6M9uMq) for discussions
- Follow us on [Twitter](https://twitter.com/swarms_corp)
- Subscribe to our [YouTube channel](https://www.youtube.com/channel/UC9yXyitkbU_WSy7bd_41SqQ)
- Read our [Blog](https://medium.com/@kyeg)
- Join our [Events](https://lu.ma/5p2jnc2v)

## Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please read and follow our Code of Conduct. [Learn more](./CONTRIBUTORS.md)

## Questions?

If you have any questions about contributing, please:
1. Check the documentation
2. Search existing issues
3. Ask in our Discord community
4. Book an [Onboarding Session](https://cal.com/swarms/swarms-onboarding-session) with Kye Gomez

Thank you for contributing to AgentOS! 🚀 