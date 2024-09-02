from litellm import completion
import env


def mock_quarterbacks(homeTeamName: str, homeTeamQB: str, awayTeamName: str, awayTeamQB: str) -> str:
    response = completion(
        model=env.MODEL,
        temperature=1,
        messages=[
            {
                "role": "user",
                "content": "You are observing a fantasy football league containing a bunch of people who don't know anything about football who each have drafted"
                 + "a team and made up a team name. You are tasked with poking fun at the league, the teams and the games. Your attitude is sarcastic, funny, and condescending."
                 + "Make fun of these two teams in the leaguage with made up names and their real quarterbacks. Everything is ficticious and made up. Make your banter a four sentances at most."
                 + f"What do you think of {homeTeamQB} representing {homeTeamName} in their matchup against {awayTeamQB} playing for {awayTeamName}?",
            }
        ],
    )
    return response