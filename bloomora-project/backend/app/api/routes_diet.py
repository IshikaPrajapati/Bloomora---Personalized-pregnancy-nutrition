from fastapi import APIRouter, HTTPException, Query

from app.core.nutrition_data import get_food_groups, search_foods, top_foods_by_nutrient
from app.models.schemas import DietPlan, DietProfile
from app.services.plan_builder import build_plan

router = APIRouter(prefix="/api", tags=["diet"])


@router.post("/generate-plan", response_model=DietPlan)
def generate_plan(profile: DietProfile):
    try:
        plan = build_plan(profile)
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=400, detail=str(exc))
    return plan


@router.get("/foods/search")
def food_search(q: str = Query(..., min_length=2), limit: int = 10):
    """Search the IFCT 2017 dataset by food name."""
    results = search_foods(q, limit=limit)
    return results.to_dict(orient="records")


@router.get("/foods/top")
def food_top(nutrient: str, food_group: str | None = None, limit: int = 10):
    """
    e.g. /api/foods/top?nutrient=iron_mg&food_group=Green Leafy Vegetables
    Lets you build 'foods richest in X' suggestions straight from real data
    instead of the hardcoded FOOD_POOLS.
    """
    valid_cols = {
        "energy_kcal", "protein_g", "fat_g", "carbohydrate_g", "fiber_g",
        "iron_mg", "calcium_mg", "zinc_mg", "magnesium_mg", "phosphorus_mg",
        "potassium_mg", "sodium_mg", "vitamin_c_mg", "thiamine_b1_mg",
        "riboflavin_b2_mg", "niacin_b3_mg", "vitamin_b6_mg", "folate_b9_ug",
        "vitamin_a_retinol_ug", "vitamin_d_ug", "vitamin_e_mg", "vitamin_k1_ug",
    }
    if nutrient not in valid_cols:
        raise HTTPException(status_code=400, detail=f"nutrient must be one of {sorted(valid_cols)}")
    results = top_foods_by_nutrient(nutrient, food_group=food_group, limit=limit)
    return results.to_dict(orient="records")


@router.get("/foods/groups")
def food_groups():
    return get_food_groups()
