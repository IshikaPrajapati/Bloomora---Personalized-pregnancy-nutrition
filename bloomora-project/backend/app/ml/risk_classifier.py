"""
Optional predictive layer, separate from the rule engine in app/rules/.

The rule engine (app/services/plan_builder.py) is what actually generates
food recommendations, and it stays rule-based on purpose: every suggestion
needs to be explainable. This module is for an *additional*, clearly-labeled
risk flag, trained on the UCI Maternal Health Risk dataset:
https://archive.ics.uci.edu/dataset/863/maternal+health+risk

Not wired into the API by default. To use it:

    pip install ucimlrepo scikit-learn joblib
    python -m app.ml.risk_classifier train      # fetches data, trains, saves model
    python -m app.ml.risk_classifier predict --age 29 --systolic 120 --diastolic 80 \
        --bs 7.2 --temp 98 --heart-rate 76
"""
import argparse
import sys
from pathlib import Path

MODEL_PATH = Path(__file__).with_name("risk_model.joblib")


def train():
    from ucimlrepo import fetch_ucirepo
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder
    import joblib
    import pandas as pd


    dataset = fetch_ucirepo(id=863)
    X = dataset.data.features
    y = dataset.data.targets.values.ravel()

    le = LabelEncoder()
    y_enc = le.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_enc, test_size=0.2, random_state=42, stratify=y_enc
    )

    clf = RandomForestClassifier(n_estimators=300, random_state=42)
    clf.fit(X_train, y_train)
    print("Test accuracy:", clf.score(X_test, y_test))

    joblib.dump({"model": clf, "label_encoder": le, "columns": list(X.columns)}, MODEL_PATH)
    print(f"Saved model to {MODEL_PATH}")


# def predict(age, systolic, diastolic, bs, temp, heart_rate):
#     import joblib

#     if not MODEL_PATH.exists():
#         raise SystemExit("No trained model found. Run `train` first.")
#     bundle = joblib.load(MODEL_PATH)
#     clf, le, columns = bundle["model"], bundle["label_encoder"], bundle["columns"]

#     # row = [[age, systolic, diastolic, bs, temp, heart_rate]]
#     # pred = clf.predict(row)
#     # return le.inverse_transform(pred)[0]

#     row = pd.DataFrame([[age, systolic, diastolic, bs, temp, heart_rate]], columns=columns)
#     pred = clf.predict(row)
#     return le.inverse_transform(pred)[0]

def predict(age, systolic, diastolic, bs, temp, heart_rate):
    import joblib
    import pandas as pd

    if not MODEL_PATH.exists():
        raise SystemExit("No trained model found. Run `train` first.")
    bundle = joblib.load(MODEL_PATH)
    clf, le, columns = bundle["model"], bundle["label_encoder"], bundle["columns"]

    row = pd.DataFrame([[age, systolic, diastolic, bs, temp, heart_rate]], columns=columns)
    pred = clf.predict(row)
    return le.inverse_transform(pred)[0]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("train")

    p_predict = sub.add_parser("predict")
    p_predict.add_argument("--age", type=float, required=True)
    p_predict.add_argument("--systolic", type=float, required=True)
    p_predict.add_argument("--diastolic", type=float, required=True)
    p_predict.add_argument("--bs", type=float, required=True)
    p_predict.add_argument("--temp", type=float, required=True)
    p_predict.add_argument("--heart-rate", type=float, required=True)

    args = parser.parse_args()
    if args.cmd == "train":
        train()
    else:
        result = predict(args.age, args.systolic, args.diastolic, args.bs, args.temp, args.heart_rate)
        print("Predicted risk level:", result)
