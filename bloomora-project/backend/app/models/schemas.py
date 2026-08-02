"""
Pydantic schemas for the diet-plan API.
These mirror the shape of the form data collected in frontend/index.html
(the multi-step generator: Basics -> Health -> Context).
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class DietProfile(BaseModel):
    month: int = Field(..., ge=1, le=9, description="Pregnancy month, 1-9")
    age: int = Field(..., ge=14, le=55)
    height_cm: float = Field(..., ge=120, le=210)
    weight_kg: float = Field(..., ge=30, le=180)

    diet_type: str = Field(..., pattern="^(vegetarian|nonvegetarian|vegan)$")
    allergies: List[str] = Field(default_factory=list)
    conditions: List[str] = Field(default_factory=list)

    region: str
    season: str = Field(..., pattern="^(summer|monsoon|winter|spring)$")
    budget: Optional[str] = "modest"
    meal_count: Optional[int] = 5


class FoodItem(BaseModel):
    name: str
    reason: str


class NutrientFocus(BaseModel):
    iron: int = 0
    calcium: int = 0
    protein: int = 0
    vitaminD: int = 0
    b12: int = 0
    fiber: int = 0


class DietPlan(BaseModel):
    trimester: int
    bmi: float
    bmi_category: str
    region: str
    diet_type: str
    season: str
    meals: dict  # slot -> List[FoodItem]
    avoid: List[str]
    nutrients: NutrientFocus
    red_flags: List[str]
    disclaimer: str
