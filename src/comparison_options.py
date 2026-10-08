"""Reference-group selection for the synthetic player comparison page.

The UI must only offer valid pairs. The default is a like-for-like
comparison within the same squad and broad role. An explicitly selected
broader scope permits players in different squads, but never different
broad roles, because the percentile reference groups are role dependent.

Pure pandas helpers keep option generation testable without Streamlit.
"""

from __future__ import annotations

import pandas as pd


ROLE_LABELS = {"DEF": "Defenders", "MID": "Midfielders", "ATT": "Attackers"}
ROLE_ORDER = ("DEF", "MID", "ATT")


def player_roster(observations: pd.DataFrame) -> pd.DataFrame:
    """Return a unique synthetic player roster with consistent role/squad."""
    roster = observations[["player_id", "squad", "role"]].drop_duplicates().copy()
    if roster["player_id"].duplicated().any():
        raise ValueError("A player must have one consistent squad and role in this demo.")
    return roster.sort_values("player_id").reset_index(drop=True)


def comparable_roles(roster: pd.DataFrame) -> list[str]:
    """Only show roles containing at least one valid same-squad pair."""
    valid = (
        roster.groupby(["role", "squad"])["player_id"]
        .nunique()
        .reset_index(name="n")
    )
    eligible = set(valid.loc[valid["n"] >= 2, "role"])
    return [role for role in ROLE_ORDER if role in eligible]


def comparable_squads(roster: pd.DataFrame, role: str) -> list[str]:
    """Squads with at least two players of a selected broad role."""
    eligible = roster.loc[roster["role"] == role]
    counts = eligible.groupby("squad")["player_id"].nunique()
    return sorted(counts[counts >= 2].index.tolist())


def candidate_players(roster: pd.DataFrame, role: str, squad: str | None) -> list[str]:
    """Select an analytically comparable pool, never mixing broad roles."""
    eligible = roster.loc[roster["role"] == role]
    if squad is not None:
        eligible = eligible.loc[eligible["squad"] == squad]
    return sorted(eligible["player_id"].tolist())


def second_player_choices(candidates: list[str], player_a: str) -> list[str]:
    """The second selector never offers the player already selected as A."""
    return [player for player in candidates if player != player_a]