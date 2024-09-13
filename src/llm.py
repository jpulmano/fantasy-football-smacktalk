from litellm import completion
import env
from typing import List


def mock(homeTeamName: str, homeQB: str, awayTeamName: str, awayQB: str) -> str:
    response = completion(
        model=env.MODEL,
        temperature=1,
        messages=[
            {
                "role": "user",
                "content": f"""-
                    You are observing a fantasy football league containing a bunch of people who don't know anything about football who each have drafted
                    a team and made up a team name. You are tasked with poking fun at the league, the teams and the games. Your attitude is sarcastic, funny,
                    and condescending. Make fun of these two teams in the leaguage with made up names and their real quarterbacks. Everything is ficticious
                    and made up. Make your banter a four sentances at most.
                    
                    What do you think of {homeTeamName} who is starting {homeQB} at quarterback vs {awayTeamName} who decided to start {awayQB}?
                """,
            }
        ],
    )
    return response
