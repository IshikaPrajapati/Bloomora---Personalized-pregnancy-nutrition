"""
Python port of the buildPlan() function from frontend/index.html.
Same logic as the client-side version, so the API and the static frontend
stay in sync if you decide to move generation server-side later.
"""
from copy import deepcopy

from app.models.schemas import DietProfile
from app.rules.condition_rules import (
    CONDITION_ADDONS,
    DISCLAIMER,
    FOOD_POOLS,
    RED_FLAGS,
    SEASON_NOTES,
)

SLOTS = ["breakfast", "midMorning", "lunch", "eveningSnack", "dinner", "bedtime"]


def trimester_from_month(month: int) -> int:
    if month <= 3:
        return 1
    if month <= 6:
        return 2
    return 3


def bmi_category(bmi: float) -> str:
    if bmi < 18.5:
        return "underweight"
    if bmi < 25:
        return "typical range"
    if bmi < 30:
        return "above typical range"
    return "well above typical range"


def _pick(pool, diet_type: str):
    if isinstance(pool, list):
        return deepcopy(pool)
    return deepcopy(pool.get(diet_type, pool["vegetarian"]))


def _filter_allergies(items, allergies):
    if not allergies:
        return items
    out = []
    for item in items:
        text = (item["name"] + " " + item.get("allergy_tag", "")).lower()
        if not any(a and a in text for a in allergies):
            out.append(item)
    return out


def _filter_season(items, season):
    return [i for i in items if not i.get("season_only") or i["season_only"] == season]


def build_plan(profile: DietProfile) -> dict:
    trimester = trimester_from_month(profile.month)
    height_m = profile.height_cm / 100
    bmi = profile.weight_kg / (height_m ** 2)

    meals = {slot: [] for slot in SLOTS}

    def add(slot, item):
        meals[slot].append({"name": item["name"], "reason": item["reason"]})

    allergies = [a.strip().lower() for a in profile.allergies if a.strip()]

    for item in _filter_allergies(_pick(FOOD_POOLS["breakfast"], profile.diet_type), allergies)[:2]:
        add("breakfast", item)
    for item in _filter_season(_filter_allergies(deepcopy(FOOD_POOLS["midMorning"]), allergies), profile.season)[:2]:
        add("midMorning", item)
    for item in _filter_allergies(_pick(FOOD_POOLS["lunch"], profile.diet_type), allergies)[:2]:
        add("lunch", item)
    for item in _filter_season(_filter_allergies(deepcopy(FOOD_POOLS["eveningSnack"]), allergies), profile.season)[:2]:
        add("eveningSnack", item)
    for item in _filter_allergies(_pick(FOOD_POOLS["dinner"], profile.diet_type), allergies)[:1]:
        add("dinner", item)
    for item in _filter_allergies(_pick(FOOD_POOLS["bedtime"], profile.diet_type), allergies)[:1]:
        add("bedtime", item)

    avoid = []
    nutrients = {"iron": 0, "calcium": 0, "protein": 0, "vitaminD": 0, "b12": 0, "fiber": 0}

    for cond in profile.conditions:
        rule = CONDITION_ADDONS.get(cond)
        if not rule:
            continue
        for item in rule["add"]:
            add(item["slot"], item)
        avoid.extend(rule["avoid"])
        if rule["nutrient"] and rule["nutrient"] in nutrients:
            nutrients[rule["nutrient"]] += 1

    season_rule = SEASON_NOTES.get(profile.season)
    if season_rule:
        for item in season_rule["add"]:
            add(item["slot"], item)
        avoid.extend(season_rule["avoid"])

    nutrients["protein"] += 2
    nutrients["iron"] += 1
    nutrients["calcium"] += 1
    if trimester >= 2:
        nutrients["calcium"] += 1
    if trimester == 3:
        nutrients["fiber"] += 1
    nutrients = {k: min(v, 5) for k, v in nutrients.items()}

    return {
        "trimester": trimester,
        "bmi": round(bmi, 1),
        "bmi_category": bmi_category(bmi),
        "region": profile.region,
        "diet_type": profile.diet_type,
        "season": profile.season,
        "meals": meals,
        "avoid": avoid,
        "nutrients": nutrients,
        "red_flags": RED_FLAGS,
        "disclaimer": DISCLAIMER,
    }
