from agentos_sdk import AgentOS
from dotenv import load_dotenv

load_dotenv()

agent = AgentOS(plan_on=False, max_loops=2)

agent.run(
    "Generate an extensive anime-like video about a zen garden in the mountains of Japan, with large sunny areas, a small river, and water flowing through it. Use the generate video tool to generate the video."
)
