from app.models.schemas import DietProfile
from app.services.plan_builder import bmi_category, build_plan, trimester_from_month


def test_trimester_from_month():
    assert trimester_from_month(1) == 1
    assert trimester_from_month(4) == 2
    assert trimester_from_month(9) == 3


def test_bmi_category():
    assert bmi_category(17) == "underweight"
    assert bmi_category(22) == "typical range"
    assert bmi_category(28) == "above typical range"
    assert bmi_category(33) == "well above typical range"


def test_build_plan_basic():
    profile = DietProfile(
        month=5,
        age=28,
        height_cm=160,
        weight_kg=58,
        diet_type="vegetarian",
        allergies=[],
        conditions=["anemia"],
        region="Gujarati",
        season="winter",
    )
    plan = build_plan(profile)

    assert plan["trimester"] == 2
    assert plan["nutrients"]["iron"] >= 1
    assert any("Tea or coffee" in a for a in plan["avoid"])
    assert len(plan["meals"]["breakfast"]) > 0
    assert "disclaimer" in plan


def test_allergy_filtering_excludes_nut_items():
    profile = DietProfile(
        month=2,
        age=25,
        height_cm=158,
        weight_kg=55,
        diet_type="vegan",
        allergies=["nuts"],
        conditions=[],
        region="South Indian",
        season="summer",
    )
    plan = build_plan(profile)
    all_names = " ".join(i["name"] for slot in plan["meals"].values() for i in slot).lower()
    assert "almonds" not in all_names
