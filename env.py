from dotenv import load_dotenv
import os

load_dotenv()

LEAGUE_ID = int(os.getenv("LEAGUE_ID"))
YEAR = int(os.getenv("YEAR"))
SWID = os.getenv("SWID")
ESPN_S2 = os.getenv("ESPN_S2")
