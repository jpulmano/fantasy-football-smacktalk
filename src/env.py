from dotenv import load_dotenv
import os

load_dotenv()

LEAGUE_ID = int(os.getenv("LEAGUE_ID"))
YEAR = int(os.getenv("YEAR"))
SWID = os.getenv("SWID")
ESPN_S2 = os.getenv("ESPN_S2")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# For LLM mode
SHOULD_QUERY_LLM = False   # Toggle this to True if you want LLM responses
# LLM_MODEL = "claude-3-5-sonnet-20240620"
LLM_MODEL="gpt-4o"
# LLM_MODEL="groq/llama3-8b-8192"
