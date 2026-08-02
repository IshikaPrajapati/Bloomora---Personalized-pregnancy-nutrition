"""
Loads the cleaned IFCT 2017 dataset (data/processed/bloomora_ifct2017_nutrition.csv)
once at startup and exposes simple lookup/query helpers used by the rule engine
and by the /foods search endpoint.
"""
from functools import lru_cache
from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[3] / "data" / "processed" / "bloomora_ifct2017_nutrition.csv"


@lru_cache(maxsize=1)
def load_nutrition_table() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    return df


def search_foods(query: str, limit: int = 10) -> pd.DataFrame:
    """Case-insensitive substring search over food_name."""
    df = load_nutrition_table()
    mask = df["food_name"].str.contains(query, case=False, na=False)
    return df[mask].head(limit)


def top_foods_by_nutrient(nutrient_col: str, food_group: str = None, limit: int = 10) -> pd.DataFrame:
    """
    e.g. top_foods_by_nutrient('iron_mg', food_group='Green Leafy Vegetables')
    Used to build 'foods rich in X' suggestions instead of a hardcoded list.
    """
    df = load_nutrition_table()
    if food_group:
        df = df[df["food_group"] == food_group]
    return df.sort_values(nutrient_col, ascending=False).head(limit)


def get_food_groups() -> list:
    df = load_nutrition_table()
    return sorted(df["food_group"].dropna().unique().tolist())
