"""
LLM-based smack talk generator for fantasy football matchups.
Supports both prompt-building (offline mode) and live querying (online mode).
"""

from litellm import completion
from fantasy_team import FantasyTeam
import env as env


def build_prompt(home_team: FantasyTeam, away_team: FantasyTeam) -> str:
    """
    Build the witty smack talk prompt for a fantasy matchup.
    """
    return f"""You are observing a fantasy football league containing mildly passionate and competitive players in a work league.

You will be given a matchup between 2 coworkers and the players on each team. Your task is to create a 4-8 sentence summary of the matchup in a funny, goofy, roasting, casual tone to create excitement about the matchup.

To do this, you MUST get an understanding of performances of the players on each team in recent weeks to inform your roasts. For instance, if you see that some player X only scored a very low number of points last week (e.g. 2.0 fantasy points), you should include
this in your roast.

Additionally:
- Make funny puns out of the team names.
- Provide witty, condescending analysis.

Use your creativity to make this hilarious to read without being cringe. Make sure your analysis is actually correct too.

Glossary:
QB - Quarterback
RB - Running back
WR - Wide receiver
TE - Tight end
FLEX - A flexible roster slot that can be RB, WR, or TE.

Matchup:

[TEAM ONE = {home_team.team_name}]
QB: {home_team.qb.name}, RBs: {home_team.rb1.name}, {home_team.rb2.name}, WRs: {home_team.wr1.name}, {home_team.wr2.name}, TE: {home_team.te1.name}, FLEX: {home_team.flex.name if home_team.flex else "None"}

VERSUS

[TEAM TWO = {away_team.team_name}]
QB: {away_team.qb.name}, RBs: {away_team.rb1.name}, {away_team.rb2.name}, WRs: {away_team.wr1.name}, {away_team.wr2.name}, TE: {away_team.te1.name}, FLEX: {away_team.flex.name if away_team.flex else "None"}
""".strip()


def query_llm(prompt: str) -> str:
    """
    Query the configured LLM with a given prompt.
    """
    response = completion(
        model=env.LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=1.0,
        max_tokens=200,
    )
    return response["choices"][0]["message"]["content"]
