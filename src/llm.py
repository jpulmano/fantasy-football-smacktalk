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
    
    Args:
        home_team: The home FantasyTeam.
        away_team: The away FantasyTeam.
    
    Returns:
        The raw prompt string.
    """
    return f"""
    You are observing a fantasy football league containing mildly passionate players.
    Your task is to:
    - Make puns out of the team names.
    - Provide witty, condescending analysis.
    - Roast the starting lineups using real NFL players.
    - Use recent player news for context if possible.
    - Keep it funny and 4–8 sentences long.

    Matchup:

    {home_team.team_name} (QB: {home_team.qb.name}, RBs: {home_team.rb1.name}, {home_team.rb2.name},
    WRs: {home_team.wr1.name}, {home_team.wr2.name}, TE: {home_team.te1.name})

    vs.

    {away_team.team_name} (QB: {away_team.qb.name}, RBs: {away_team.rb1.name}, {away_team.rb2.name},
    WRs: {away_team.wr1.name}, {away_team.wr2.name}, TE: {away_team.te1.name})
    """.strip()


def query_llm(prompt: str) -> str:
    """
    Query the configured LLM with a given prompt.
    
    Args:
        prompt: The text prompt to send to the LLM.
    
    Returns:
        The LLM's response string.
    """
    response = completion(
        model=env.LLM_MODEL,   # e.g. "openai/gpt-4o"
        messages=[{"role": "user", "content": prompt}],
        temperature=1.0,
        max_tokens=200,
    )
    return response["choices"][0]["message"]["content"]
