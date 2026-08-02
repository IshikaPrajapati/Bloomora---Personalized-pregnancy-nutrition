"""
This is the Python port of the rule engine that lives in
frontend/index.html's <script> (FOOD_POOLS, CONDITION_ADDONS, SEASON_NOTES).

Keeping it in the backend lets the API be the single source of truth if you
later want the frontend to call it instead of generating plans client-side.
"""

FOOD_POOLS = {
    "breakfast": {
        "vegetarian": [
            {"name": "Vegetable moong dal chilla", "reason": "A protein- and folate-rich start that's gentle on the stomach."},
            {"name": "Ragi porridge with milk", "reason": "Ragi is one of the richest plant sources of calcium."},
            {"name": "Poha with peanuts", "reason": "Flattened rice with peanuts and lemon helps iron absorb better."},
        ],
        "nonvegetarian": [
            {"name": "Boiled egg with whole-wheat toast", "reason": "Eggs bring complete protein and natural vitamin B12."},
            {"name": "Vegetable moong dal chilla", "reason": "A protein- and folate-rich start that's gentle on the stomach."},
        ],
        "vegan": [
            {"name": "Ragi porridge with fortified soy milk", "reason": "Fortified plant milk covers calcium and B12 without dairy."},
            {"name": "Poha with peanuts", "reason": "Flattened rice with peanuts and lemon helps iron absorb better."},
        ],
    },
    "midMorning": [
        {"name": "Seasonal fruit bowl", "reason": "Easy fiber and vitamin C to support iron absorption from earlier meals."},
        {"name": "Handful of soaked almonds & walnuts", "allergy_tag": "nuts", "reason": "A steady source of healthy fats and folate."},
        {"name": "Coconut water", "season_only": "summer", "reason": "Natural electrolytes for warmer days."},
    ],
    "lunch": {
        "vegetarian": [
            {"name": "Dal, roti, and a leafy green sabzi", "reason": "A classic thali balance of plant protein, iron and folate."},
            {"name": "Curd with cucumber raita", "reason": "A cooling, calcium-rich side that supports digestion."},
        ],
        "nonvegetarian": [
            {"name": "Grilled fish or chicken with rice and sabzi", "reason": "Lean protein and, with fish, omega-3 for the baby's brain development."},
            {"name": "Dal, roti, and a leafy green sabzi", "reason": "A classic thali balance of plant protein, iron and folate."},
        ],
        "vegan": [
            {"name": "Rajma or chana curry with rice", "reason": "Legumes deliver plant protein and iron together."},
            {"name": "Leafy green sabzi with sesame seeds", "reason": "Sesame is a strong plant source of calcium for those skipping dairy."},
        ],
    },
    "eveningSnack": [
        {"name": "Roasted chana with jaggery", "reason": "A traditional pairing that helps iron levels."},
        {"name": "Vegetable sprouts salad", "reason": "Fiber to keep digestion comfortable in the evening."},
        {"name": "Warm turmeric milk", "season_only": "winter", "reason": "Warming and calcium-rich for cooler weather."},
    ],
    "dinner": {
        "vegetarian": [
            {"name": "Khichdi with ghee and vegetables", "reason": "Light, warm and easy to digest before bed."},
            {"name": "Vegetable soup with whole-grain bread", "reason": "A gentler dinner covering fiber and micronutrients."},
        ],
        "nonvegetarian": [
            {"name": "Light chicken or fish stew with vegetables", "reason": "Protein without an overly heavy meal close to bedtime."},
            {"name": "Khichdi with ghee and vegetables", "reason": "Light, warm and easy to digest before bed."},
        ],
        "vegan": [
            {"name": "Moong dal khichdi with vegetables", "reason": "Light, warm, plant-based and easy to digest before bed."},
            {"name": "Vegetable soup with whole-grain bread", "reason": "A gentler dinner covering fiber and micronutrients."},
        ],
    },
    "bedtime": {
        "vegetarian": [{"name": "Warm milk with a pinch of turmeric", "reason": "Calcium and a calming end to the day."}],
        "nonvegetarian": [{"name": "Warm milk with a pinch of turmeric", "reason": "Calcium and a calming end to the day."}],
        "vegan": [{"name": "Warm fortified plant milk", "reason": "A dairy-free way to close the day with calcium and B12."}],
    },
}

CONDITION_ADDONS = {
    "anemia": {
        "add": [{"slot": "midMorning", "name": "Pomegranate or a citrus fruit",
                 "reason": "Vitamin C alongside iron-rich meals improves how much iron your body absorbs."}],
        "avoid": ["Tea or coffee within an hour of meals — the tannins block iron absorption."],
        "nutrient": "iron",
    },
    "gestationalDiabetes": {
        "add": [{"slot": "eveningSnack", "name": "Cucumber and carrot sticks with hummus",
                 "reason": "A low glycemic-index snack that won't spike blood sugar."}],
        "avoid": ["Sugary fruit juices and sweetened beverages.",
                  "Refined white rice or maida in large portions — favour whole grains instead."],
        "nutrient": "fiber",
    },
    "hypertension": {
        "add": [{"slot": "lunch", "name": "A side of beetroot",
                 "reason": "Naturally supports healthy blood pressure without added salt."}],
        "avoid": ["Pickles, papad and other high-sodium condiments.", "Packaged and processed snacks."],
        "nutrient": "protein",
    },
    "thyroid": {
        "add": [{"slot": "breakfast", "name": "A small serving of iodized-salt cooked vegetables",
                 "reason": "Iodine supports thyroid function during pregnancy."}],
        "avoid": ["Large amounts of raw soy products close to thyroid medication timing."],
        "nutrient": "iron",
    },
    "pcos": {
        "add": [{"slot": "breakfast", "name": "A spoon of flaxseed powder mixed in",
                 "reason": "Fiber and healthy fats that help keep blood sugar steadier."}],
        "avoid": ["Refined sugar and sweetened drinks."],
        "nutrient": "protein",
    },
    "vitaminD": {
        "add": [{"slot": "midMorning", "name": "10-15 minutes of morning sunlight (with your doctor's clearance)",
                 "reason": "Sunlight remains one of the most effective vitamin D sources."}],
        "avoid": [],
        "nutrient": "vitaminD",
    },
    "b12": {
        "add": [{"slot": "dinner", "name": "Fortified cereal or nutritional yeast sprinkle",
                 "reason": "A reliable top-up for vitamin B12, especially if dairy or meat intake is limited."}],
        "avoid": [],
        "nutrient": "b12",
    },
    "calcium": {
        "add": [{"slot": "eveningSnack", "name": "Til (sesame) and jaggery ladoo", "reason": "A traditional, calcium-dense snack."}],
        "avoid": [],
        "nutrient": "calcium",
    },
    "morningSickness": {
        "add": [{"slot": "midMorning", "name": "Ginger tea or a few soaked raisins",
                 "reason": "Ginger is commonly used to ease nausea; small frequent meals help too."}],
        "avoid": ["Very oily or strongly spiced food, which can worsen nausea."],
        "nutrient": None,
    },
}

SEASON_NOTES = {
    "summer": {"add": [{"slot": "midMorning", "name": "Chilled buttermilk", "reason": "Cooling, hydrating and easy on digestion in the heat."}], "avoid": []},
    "monsoon": {"add": [], "avoid": ["Raw, unwashed salads or cut fruit from outside — infection risk rises in the rains.", "Street food during monsoon."]},
    "winter": {"add": [{"slot": "eveningSnack", "name": "Mixed dry fruit and til ladoo", "reason": "Warming, energy-dense and rich in calcium and iron for colder months."}], "avoid": []},
    "spring": {"add": [], "avoid": []},
}

RED_FLAGS = [
    "Heavy vaginal bleeding",
    "Severe or persistent headache with vision changes",
    "Sudden swelling in the face or hands",
    "Reduced or absent fetal movement",
    "High fever",
    "Severe abdominal pain",
]

DISCLAIMER = (
    "This plan is educational guidance generated from general medical and regional "
    "nutrition references. It is not a diagnosis or prescription — please confirm "
    "any changes with your doctor or dietitian."
)
