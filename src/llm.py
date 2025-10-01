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
        lines = [f"[TEAM = {team.team_name}]"]
        for slot, player in team.lineup.items():
            proj = team.projections.get(slot, 0.0)
            player_name = player.name if player else "None"
            lines.append(f"{slot}: {player_name} ({proj:.1f} proj)")
        lines.append(f"TOTAL TEAM PROJECTION: {team.total_proj:.1f} points")
        return "\n".join(lines)

    return f"""You are observing a fantasy football league containing mildly passionate and competitive players in a work league.

You will be given a matchup between 2 coworkers and the players on each team. Your task is to create a 4-8 sentence summary of the matchup in a funny, goofy, roasting, casual tone to create excitement about the matchup.

You MUST use both the recent performances of players (use external knowledge) AND the ESPN projected points (provided below) in your roasts.
For example, if a FLEX player is only projected 5.0 points, call that out sarcastically. If a team is projected way lower overall, highlight that too.

Additionally:
- Make funny puns out of the team names.
- Provide witty, condescending analysis.

Glossary:
QB - Quarterback
RB - Running back
WR - Wide receiver
TE - Tight end
FLEX - A flexible roster slot that can be RB, WR, or TE.
K - Kicker
DEF - Defense/Special Teams

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
        max_tokens=300,
    )
    return response["choices"][0]["message"]["content"]
