"""
LLM-based smack talk generator for fantasy football matchups.
Supports both prompt-building (offline mode) and live querying (online mode).
"""

from litellm import completion
from prompt import PROMPT
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
                f"{slot}: {player_name} ({proj:.1f} projected points, status={status})"
            )
        lines.append(f"TOTAL TEAM PROJECTION: {team.total_proj:.1f} points")
        return "\n".join(lines)

    return PROMPT.format(
        team_one=format_team(home_team),
        team_two=format_team(away_team),
    )


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
