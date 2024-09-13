# https://github.com/cwendt94/espn-api/discussions/150
from typing import Optional, List
from dotenv import load_dotenv

import env
import llm


from espn_api.football import League, BoxPlayer, Matchup


def findQB(players) -> Optional[BoxPlayer]:
    for player in players:
        if player.slot_position == "QB":
            return player
    return None


def findRB(players) -> Optional[List[BoxPlayer]]:
    rbs = []
    for player in players:
        if player.slot_position == "RB":
            rbs.append(player)
    return rbs


def generateSmackTalk(matchup: Matchup) -> str:
    homeTeam = matchup.home_team
    homeQB = findQB(matchup.home_lineup)
    homeRBs = findRB(matchup.home_lineup)
    awayTeam = matchup.away_team
    awayQB = findQB(matchup.away_lineup)
    awayRBs = findRB(matchup.away_lineup)

    print(f"{homeTeam.team_name} vs {awayTeam.team_name}")
    response = llm.mock(
        homeTeam.team_name,
        llm.Roster(homeQB.name, homeRBs[0].name, homeRBs[1].name),
        awayTeam.team_name,
        llm.Roster(awayQB.name, awayRBs[0].name, awayRBs[1].name),
    )
    return response.choices[0].message.content


def main():
    nfl2024 = League(
        league_id=env.LEAGUE_ID, year=env.YEAR, swid=env.SWID, espn_s2=env.ESPN_S2
    )

    smacktalk = [
        f"""Thoughts on {matchup.home_team.team_name} vs {matchup.away_team.team_name}:
            {generateSmackTalk(matchup)}
        """
        for matchup in nfl2024.box_scores()
    ]
    print(smacktalk)

    with open("analysis.txt", "w+") as f:
        f.write("Week 1\n============================\n\n")
        for line in smacktalk:
            f.write(line + "\n\n")


if __name__ == "__main__":
    main()
