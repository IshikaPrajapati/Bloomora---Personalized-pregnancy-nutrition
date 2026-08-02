# Bloomora

Personalized pregnancy nutrition — rule engine + regional food data, no login required.

## Project structure

```
bloomora-project/
│
├── frontend/
│   └── index.html              # Complete single-file app (HTML+CSS+JS inlined).
│                                # Works standalone by double-clicking it, or served
│                                # by the backend at "/" (see below).
│
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entrypoint. Serves the API + the frontend.
│   │   ├── api/
│   │   │   └── routes_diet.py   # POST /api/generate-plan, GET /api/foods/*
│   │   ├── core/
│   │   │   ├── config.py        # App settings (env-driven)
│   │   │   └── nutrition_data.py# Loads data/processed/*.csv, food search/lookup
│   │   ├── rules/
│   │   │   └── condition_rules.py  # FOOD_POOLS, CONDITION_ADDONS, SEASON_NOTES —
│   │   │                            # the Python port of the same rules used in
│   │   │                            # frontend/index.html's <script> tag.
│   │   ├── services/
│   │   │   └── plan_builder.py  # build_plan() — same logic as buildPlan() in JS.
│   │   ├── models/
│   │   │   └── schemas.py       # Pydantic request/response models
│   │   └── ml/
│   │       └── risk_classifier.py  # Optional: trains on the UCI Maternal Health
│   │                                 # Risk dataset for a separate risk-flag layer.
│   │                                 # NOT wired into the API by default.
│   ├── tests/
│   │   └── test_plan_builder.py # Real, passing unit tests
│   └── requirements.txt
│
├── data/
│   ├── raw/
│   │   └── ifct2017_raw.csv           # Untouched IFCT 2017 export (421 columns,
│   │                                    # values in raw grams/kJ, cryptic codes)
│   └── processed/
│       └── bloomora_ifct2017_nutrition.csv  # Cleaned version actually used by the
│                                              # backend: 542 foods, readable columns,
│                                              # standard units (mg/µg/kcal).
│
├── docs/
│   └── DATASETS.md              # Where every data source came from, with links
│
└── README.md                    # You are here
```

## Why it's split this way

- **The frontend works with zero backend.** `frontend/index.html` has its own copy
  of the rule engine in JavaScript, so you can open it directly and it fully works —
  useful for demos or if you never want to stand up a server.
- **The backend is there for when you outgrow that.** Same rules, ported to Python,
  plus real endpoints to query the dataset directly (`/api/foods/top?nutrient=iron_mg`)
  instead of only using the hardcoded food lists.
- **Rules and data are deliberately separate from any ML model.** Every food
  recommendation needs to stay explainable, so `plan_builder.py` stays rule-based.
  `ml/risk_classifier.py` is kept as an isolated, optional layer for a genuinely
  predictive task (risk flagging) where a trained model actually makes sense.

## Running it

**Frontend only (no backend):**
Just open `frontend/index.html` in a browser.

**Full stack:**
```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Then visit `http://localhost:8000` — the frontend is served at `/`, and the API
is live at `/api/...` (interactive docs at `/docs`).

**Run tests:**
```bash
cd backend
pip install pytest httpx
pytest
```

## Next steps if you keep building this

1. Point `frontend/index.html`'s form submit at `POST /api/generate-plan` instead of
   generating the plan in-browser, so both stay in sync automatically.
2. Expand `data/processed/` with the USDA FoodData Central CSV for non-Indian foods
   (see `docs/DATASETS.md`).
3. Add a `data/raw/` -> `data/processed/` build script if you update the IFCT export.
