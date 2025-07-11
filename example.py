from agentos_sdk import AgentOS
from dotenv import load_dotenv

load_dotenv()

agent = AgentOS(plan_on=False, max_loops=1)

agent.run(
    "Summarize the top high-frequency trading strategies in commodity markets and save the report as 'high_frequency_commodity_strategies.txt'."
)
