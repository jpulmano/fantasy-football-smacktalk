from dotenv import load_dotenv
import os

load_dotenv()

LEAGUE_ID = int(os.getenv("LEAGUE_ID"))
YEAR = int(os.getenv("YEAR"))
SWID = os.getenv("SWID")
ESPN_S2 = os.getenv("ESPN_S2")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL="claude-3-5-sonnet-20240620"
# MODEL='gpt-4o-mini'
