from litellm import completion
import src.env as env
from typing import List


class Roster:
    def __init__(self, qb: str, rb1: str, rb2: str):
        self.qb = qb
        self.rb1 = rb1
        self.rb2 = rb2


def mock(
    homeTeamName: str, homeRoster: Roster, awayTeamName: str, awayRoster: Roster
) -> str:
    response = completion(
        model=env.MODEL,
        temperature=1,
        messages=[
            {
                "role": "user",
                "content": f"""-
                    You are observing a fantasy football league containing a bunch of people mildly passionate about football who each have drafted
                    a team and made up a team name. You are tasked with making puns out of the teams names and providing analyis on the the games. Your attitude is witty, funny,
                    and condescending. Make fun of these two teams in the leaguage with made up names and their real quarterbacks. Everything is ficticious
                    and made up. Make your banter a 2-4 sentances.
                    
                    What do you think about this matchup?
                    {homeTeamName} who is starting {homeRoster.qb} at quarterback and {homeRoster.rb1} and {homeRoster.rb2} at runnning back vs {awayTeamName} who decided to start {awayRoster.qb} at quarterback and {awayRoster.rb1} and {awayRoster.rb2} at running back?
            """,
            }
        ],
    )
    return response
