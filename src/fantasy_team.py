"""
Fantasy team utilities for extracting lineups from ESPN fantasy matchups.
"""

from typing import Optional, List, Dict
from attr import attrs
from espn_api.football import BoxPlayer, Matchup


@attrs(auto_attribs=True)
class FantasyTeam:
    """
    Represents a simplified fantasy football team lineup with projections.
    Stores a mapping from slot -> player, and slot -> projected points.
    """
    team_name: str
    lineup: Dict[str, Optional[BoxPlayer]]   # slot -> BoxPlayer
    projections: Dict[str, float]            # slot -> projected points
    total_proj: float                        # total team projected points


# ---- Slot helpers ----

def findQB(players: List[BoxPlayer]) -> Optional[BoxPlayer]:
    return next((p for p in players if p.slot_position == "QB"), None)


def findRBs(players: List[BoxPlayer]) -> List[BoxPlayer]:
    return [p for p in players if p.slot_position == "RB"]


def findWRs(players: List[BoxPlayer]) -> List[BoxPlayer]:
    return [p for p in players if p.slot_position == "WR"]


def findTE(players: List[BoxPlayer]) -> Optional[BoxPlayer]:
    return next((p for p in players if p.slot_position == "TE"), None)


def findFlex(players: List[BoxPlayer]) -> Optional[BoxPlayer]:
    return next((p for p in players if p.slot_position in ("RB/WR/TE", "FLEX")), None)


def findKicker(players: List[BoxPlayer]) -> Optional[BoxPlayer]:
    return next((p for p in players if p.slot_position == "K"), None)


def findDefense(players: List[BoxPlayer]) -> Optional[BoxPlayer]:
    # ESPN often uses "D/ST" or just "DST"
    return next((p for p in players if p.slot_position in ("D/ST", "DST")), None)


# ---- Main builder ----

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
    kicker = findKicker(lineup)
    defense = findDefense(lineup)

    # Sanity checks for required positions
    assert qb, "QB not found in lineup"
    assert len(rbs) >= 2, "Not enough RBs in lineup"
    assert len(wrs) >= 2, "Not enough WRs in lineup"
    assert te1, "TE not found in lineup"
    assert kicker, "Kicker not found in lineup"
    assert defense, "Defense not found in lineup"

    # Build slot map
    slot_map: Dict[str, Optional[BoxPlayer]] = {
        "QB": qb,
        "RB1": rbs[0],
        "RB2": rbs[1],
        "WR1": wrs[0],
        "WR2": wrs[1],
        "TE": te1,
        "FLEX": flex,
        "K": kicker,
        "DEF": defense,
    }

    # Projection mapping
    proj_map: Dict[str, float] = {
        slot: (player.projected_points if player else 0.0)
        for slot, player in slot_map.items()
    }

    total_proj = sum(proj_map.values())

    return FantasyTeam(
        team_name=team_name,
        lineup=slot_map,
        projections=proj_map,
        total_proj=total_proj,
    )
