from agentos import AgentOS
import litellm
from dotenv import load_dotenv

load_dotenv()

# litellm._turn_on_debug()

agent = AgentOS()

agent.add_file("readme.md")

agent.run("what is the readme.md file about? Create a summary of the readme.md file and just respond to me don't use any tools")
