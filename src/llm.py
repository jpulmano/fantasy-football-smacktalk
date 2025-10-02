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

    return f"""You are observing a fantasy football league containing passionate and competitive players.

You will be given a matchup between 2 people and the players on each team. Your task is to create a 4-8 sentence summary of the matchup in a funny, goofy, roasting, casual tone to create excitement about the matchup.

You MUST:
- Keep your roasts silly, witty, and condescending. They should make the reader laugh.
- Keep your analysis more high-level, and do not get TOO hyper-focused on statlines or individual players.
    - HOWEVER, you *should* look up important, recent news about each player to inform your roasts. For example, if a given player scored 2.0 points last week, you should roast this and say something along the lines of "this player sucked last week and will probably suck this week". Etc.
    - Look up the teams that each player is up against. For instance, if a running back is up against a team with a great running defense, then you should add this to your roast. But do not get too hyper-focused on these matchups.
    - In your summary, you should use a maximum of 2-3 players to analyze per team, without trying to include analysis about every single player.
    - You may cite any sources at the END of the summary; do not include your sources in-line.
- Use ESPN projected points (provided below).
- Make funny puns out of the team names.
- Don't focus too much on the defenses.

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
