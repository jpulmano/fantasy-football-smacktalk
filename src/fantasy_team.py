"""
Fantasy team utilities for extracting lineups from ESPN fantasy matchups.
"""

from typing import Optional, List
from attr import attrs
from espn_api.football import BoxPlayer, Matchup


@attrs(auto_attribs=True)
class FantasyTeam:
    """
    Represents a simplified fantasy football team lineup.
    """
    team_name: str
    qb: BoxPlayer
    rb1: BoxPlayer
    rb2: BoxPlayer
    wr1: BoxPlayer
    wr2: BoxPlayer
    te1: BoxPlayer
    flex: Optional[BoxPlayer] = None


def findQB(players: List[BoxPlayer]) -> Optional[BoxPlayer]:
    return next((p for p in players if p.slot_position == "QB"), None)


def findRBs(players: List[BoxPlayer]) -> List[BoxPlayer]:
    # Only count "true" RB slots, not FLEX
    return [p for p in players if p.slot_position == "RB"]


def findWRs(players: List[BoxPlayer]) -> List[BoxPlayer]:
    return [p for p in players if p.slot_position == "WR"]


def findTE(players: List[BoxPlayer]) -> Optional[BoxPlayer]:
    return next((p for p in players if p.slot_position == "TE"), None)


def findFlex(players: List[BoxPlayer]) -> Optional[BoxPlayer]:
    """Return the FLEX player from the given lineup, if any."""
    return next((p for p in players if p.slot_position in ("RB/WR/TE", "FLEX")), None)


def getFantasyTeam(matchup: Matchup, team_type: str) -> FantasyTeam:
    assert team_type in ("home", "away")

    lineup = matchup.home_lineup if team_type == "home" else matchup.away_lineup
    team_name = (
        matchup.home_team.team_name if team_type == "home" else matchup.away_team.team_name
    )

    qb = findQB(lineup)
    rbs = findRBs(lineup)
    wrs = findWRs(lineup)
    te1 = findTE(lineup)
    flex = findFlex(lineup)

    # Sanity checks
    assert qb, "QB not found in lineup"
    assert len(rbs) >= 2, "Not enough RBs in lineup"
    assert len(wrs) >= 2, "Not enough WRs in lineup"
    assert te1, "TE not found in lineup"

    return FantasyTeam(
        team_name=team_name,
        qb=qb,
        rb1=rbs[0],
        rb2=rbs[1],
        wr1=wrs[0],
        wr2=wrs[1],
        te1=te1,
        flex=flex,
    )
