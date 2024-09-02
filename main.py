# https://github.com/cwendt94/espn-api/discussions/150
from typing import Optional
from dotenv import load_dotenv

import env
import llm


from espn_api.football import League, BoxPlayer, Matchup


def findQB(players) -> Optional[BoxPlayer]:
    for player in players:
        if player.position == "QB":
            return player
    return None


def generateSmackTalk(matchup: Matchup) -> str:
    homeTeam = matchup.home_team
    homeQB = findQB(matchup.home_lineup)
    awayTeam = matchup.away_team
    awayQB = findQB(matchup.away_lineup)

    print(f"{homeTeam.team_name} vs {awayTeam.team_name}")
    print(f"{homeQB.name} vs {awayQB.name}")
    response = llm.mock(homeTeam.team_name, homeQB, awayTeam.team_name, awayQB)
    return response.choices[0].message.content


def main():
    nfl2024 = League(
        league_id=env.LEAGUE_ID, year=env.YEAR, swid=env.SWID, espn_s2=env.ESPN_S2
    )

    smacktalk = [
        f"""Thoughts on {matchup.home_team.team_name} vs {matchup.away_team.team_name}:
            {generateSmackTalk(matchup)}
        """
        for matchup in nfl2024.box_scores()[5:]
    ]
    print(smacktalk)

    with open("analysis.txt", "w+") as f:
        f.write("Week 1\n============================\n\n")
        for line in smacktalk:
            f.write(line + "\n\n")


if __name__ == "__main__":
    main()
