# Datasets

## In use

**Indian Food Composition Tables 2017 (IFCT 2017)**
Published by ICMR – National Institute of Nutrition, Hyderabad. 542 foods, measured
across six regions of India.

- Official book (PDF): https://www.nin.res.in/ebooks/IFCT2017.pdf
- Structured source used here: https://github.com/nodef/ifct2017
- `data/raw/ifct2017_raw.csv` — the untouched export (421 columns, values stored in
  raw grams/kJ using NIN's internal codes)
- `data/processed/bloomora_ifct2017_nutrition.csv` — cleaned for this project:
  24 nutrients with readable names, converted to standard units (mg / µg / kcal).
  See the conversion notes at the bottom of this file if you regenerate it.

**Known limitation:** IFCT 2017 does not measure vitamin B12. That column is
present in the processed CSV but always reads `"not measured in IFCT 2017"` —
it's flagged rather than silently zero.

## Referenced for rules, not as training data

**ICMR-NIN Dietary Guidelines for Indians (2024)**
Source for the condition-based rules in `backend/app/rules/condition_rules.py`
(anemia, gestational diabetes, hypertension, etc.)
https://nin.res.in/dietaryguidelines/pdfjs/locale/DGI_2024.pdf

## Optional, for the ML risk-classifier layer only

**Maternal Health Risk Data Set (UCI)**
Age, blood pressure, blood sugar, temperature, heart rate → low/mid/high risk.
1,014 rows. Used only by `backend/app/ml/risk_classifier.py`, which is not wired
into the API by default.
https://archive.ics.uci.edu/dataset/863/maternal+health+risk

## Not yet integrated

**USDA FoodData Central** — for international/non-Indian foods, if the region
options expand beyond India.
https://fdc.nal.usda.gov/download-datasets.html

---

### Unit conversion notes (raw -> processed)

The raw IFCT export stores every nutrient in grams (mass) or kJ (energy) per
100g edible portion, regardless of what unit is conventional for that nutrient.
The processed CSV converts each to its normal reporting unit:

| Nutrient type                          | Conversion            |
|-----------------------------------------|------------------------|
| Energy                                  | raw_kJ / 4.184 -> kcal |
| Macronutrients (protein/fat/carb/fiber) | already grams, as-is   |
| Minerals (iron, calcium, zinc, etc.)    | raw_g × 1000 -> mg     |
| B-vitamins, vitamin C, vitamin E        | raw_g × 1000 -> mg     |
| Vitamin A, D, K, folate                 | raw_g × 1,000,000 -> µg|

Values were spot-checked against known nutrition figures for spinach and
amaranth seed during processing.
