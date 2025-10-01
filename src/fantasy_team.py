"""
Fantasy team utilities for extracting lineups from ESPN fantasy matchups.
"""

from typing import Optional, List, Dict
from attr import attrs
from espn_api.football import BoxPlayer, Matchup


@attrs(auto_attribs=True)
class FantasyTeam:
    """
    Represents a fantasy football team lineup with projections and statuses.
    - lineup: mapping of slot -> BoxPlayer
    - player_info: mapping of slot -> dict(proj, on_bye, status)
    - total_proj: total team projected points
    """
    team_name: str
    lineup: Dict[str, Optional[BoxPlayer]]
    player_info: Dict[str, dict]
    total_proj: float


# ---- Slot finders ----

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

    # Sanity checks
    assert qb, "QB not found"
    assert len(rbs) >= 2, "Need at least 2 RBs"
    assert len(wrs) >= 2, "Need at least 2 WRs"
    assert te1, "TE not found"
    assert kicker, "K not found"
    assert defense, "DEF not found"

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

    # Projection + status map
    info_map: Dict[str, dict] = {}
    for slot, player in slot_map.items():
        if player:
            status = (
                getattr(player, "injuryStatus", None)
                or "could_not_find"
            )

            bye = getattr(player, "on_bye", None)
            if bye is None:
                bye = getattr(player, "onBye", False)

            info_map[slot] = {
                "proj": getattr(player, "projected_points", 0.0) or 0.0,
                "on_bye": bye,
                "status": status,
            }
        else:
            info_map[slot] = {"proj": 0.0, "on_bye": False, "status": "EMPTY"}


    total_proj = sum(info["proj"] for info in info_map.values())

    return FantasyTeam(
        team_name=team_name,
        lineup=slot_map,
        player_info=info_map,
        total_proj=total_proj,
    )
