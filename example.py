from agentos_sdk import AgentOS
from dotenv import load_dotenv

load_dotenv()

agent = AgentOS(plan_on=False, max_loops=1)

agent.run(
    "Generate a video of a cat surfing on a wave at sunset, cinematic style. Save it as 'cat_surfing.mp4. We should also add cat sounds and meowing sounds."
)
