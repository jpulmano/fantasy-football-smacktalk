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


def findQB(players: List[BoxPlayer]) -> Optional[BoxPlayer]:
    """Return the QB from the given lineup, if any."""
    return next((p for p in players if p.slot_position == "QB"), None)


def findRBs(players: List[BoxPlayer]) -> List[BoxPlayer]:
    """Return all RBs from the given lineup."""
    return [p for p in players if p.slot_position == "RB"]


def findWRs(players: List[BoxPlayer]) -> List[BoxPlayer]:
    """Return all WRs from the given lineup."""
    return [p for p in players if p.slot_position == "WR"]


def findTE(players: List[BoxPlayer]) -> Optional[BoxPlayer]:
    """Return the TE from the given lineup, if any."""
    return next((p for p in players if p.slot_position == "TE"), None)


def getFantasyTeam(matchup: Matchup, team_type: str) -> FantasyTeam:
    """
    Extracts a FantasyTeam object from a matchup.
    
    Args:
        matchup: The ESPN API matchup object.
        team_type: Either "home" or "away".
    
    Returns:
        A FantasyTeam with QB, 2 RBs, 2 WRs, and 1 TE.
    
    Raises:
        AssertionError: If required positions are missing.
    """
    assert team_type in ("home", "away")

    lineup = matchup.home_lineup if team_type == "home" else matchup.away_lineup
    team_name = (
        matchup.home_team.team_name if team_type == "home" else matchup.away_team.team_name
    )

    qb = findQB(lineup)
    rbs = findRBs(lineup)
    wrs = findWRs(lineup)
    te1 = findTE(lineup)

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
    )
