"""
Entry point for generating fantasy football smack talk.
Can run in two modes:
- Default (prompts only): Save prompts to prompts.txt
- LLM mode: Query LLM and save responses to llm_responses.txt
"""

import env
from espn_api.football import League, Matchup
from fantasy_team import getFantasyTeam
import llm


def generateSmackTalkPrompt(matchup: Matchup) -> str:
    """Generate the raw prompt for a single matchup."""
    home_team = getFantasyTeam(matchup, "home")
    away_team = getFantasyTeam(matchup, "away")
    return llm.build_prompt(home_team, away_team)


def main() -> None:
    """
    Main driver:
    - Always save generated prompts to prompts.txt
    - If should_query_llm = True, also query LLM and save to llm_responses.txt
    """
    league = League(
        league_id=env.LEAGUE_ID,
        year=env.YEAR,
        swid=env.SWID,
        espn_s2=env.ESPN_S2,
    )

    # Setting toggled in env.py
    should_query_llm = getattr(env, "SHOULD_QUERY_LLM", False)

    prompts, responses = [], []

    for matchup in league.box_scores():
        prompt = generateSmackTalkPrompt(matchup)

        # Save the prompt
        prompts.append(f"{prompt}")

        # Optionally query LLM
        if should_query_llm:
            try:
                result = llm.query_llm(prompt)
                responses.append(f"{result}")
            except Exception as e:
                responses.append(f"Error querying LLM: {e}")

    # Save prompts
    with open("prompts.txt", "w+", encoding="utf-8") as f:
        for line in prompts:
            f.write(line + "\n\n" + "-" * 80 + "\n")

    print("Prompts saved to prompts.txt")

    # Save LLM responses if enabled
    if should_query_llm:
        with open("llm_responses.txt", "w+", encoding="utf-8") as f:
            for line in responses:
                f.write(line + "\n\n")

        print("LLM responses saved to llm_responses.txt")


if __name__ == "__main__":
    main()
