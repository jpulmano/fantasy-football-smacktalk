# https://github.com/cwendt94/espn-api/discussions/150
from typing import Optional
from dotenv import load_dotenv

import env
import llm


from espn_api.football import League, BoxPlayer


def findQB(players) -> Optional[BoxPlayer]:
    for player in players:
        if player.position == "QB":
            return player
    return None


def main():
    nfl2024 = League(
        league_id=env.LEAGUE_ID, year=env.YEAR, swid=env.SWID, espn_s2=env.ESPN_S2
    )

    matchup = nfl2024.box_scores()[1]
    print(matchup)
    homeTeam = matchup.home_team
    homeQB = findQB(matchup.home_lineup)
    awayTeam = matchup.away_team
    awayQB = findQB(matchup.away_lineup)

    print(f"{homeTeam.team_name} vs {awayTeam.team_name}")
    print(f"{homeQB.name} vs {awayQB.name}")
    response = llm.mock_quarterbacks(homeTeam.team_name, homeQB.name, awayTeam.team_name, awayQB.name)
    print(response.choices[0])



if __name__ == "__main__":
    main()
