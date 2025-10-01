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

    def format_team(team: FantasyTeam) -> str:
        lines = [f"[{team.team_name}]"]
        for slot, player in team.lineup.items():
            info = team.player_info.get(slot, {})
            proj = info.get("proj", 0.0)
            bye = info.get("on_bye", "not found")
            status = info.get("status", "not found")
            player_name = player.name if player else "None"
            lines.append(
                f"{slot}: {player_name} ({proj:.1f} proj, status={status}, bye={bye})"
            )
        lines.append(f"TOTAL TEAM PROJECTION: {team.total_proj:.1f} points")
        return "\n".join(lines)

    return f"""You are observing a fantasy football league containing mildly passionate and competitive players in a work league.

You will be given a matchup between 2 coworkers and the players on each team. Your task is to create a 4-8 sentence summary of the matchup in a funny, goofy, roasting, casual tone to create excitement about the matchup.

You MUST:
- Look up important, recent news about each player to inform your roasts. For example, if a given player scored 2.0 points last week, you should roast this and say something along the lines of "this player sucked last week and will probably suck this week".
- Look up the teams that each player is up against. For instance, if a running back is up against a team with a great running defense, then you should add this to your roast.
- Use ESPN projected points (provided below).
- Whether players are OUT, QUESTIONABLE, or on a BYE (also provided).
For example, if a player is projected 0 because they are injured or on bye, call this out in a roasting way.

Additionally:
- Make funny puns out of the team names.
- Provide witty, condescending analysis.

Matchup:

{format_team(home_team)}

VERSUS

{format_team(away_team)}
""".strip()


def query_llm(prompt: str) -> str:
    """
    Query the configured LLM with a given prompt.
    """
    response = completion(
        model=env.LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=1.0,
        max_tokens=400,
    )
    return response["choices"][0]["message"]["content"]
