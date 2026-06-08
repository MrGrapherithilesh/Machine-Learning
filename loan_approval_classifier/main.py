from pathlib import Path
import json

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits, make_blobs, make_classification
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score, mean_absolute_error, r2_score, silhouette_score
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

PROJECT_NAME = 'Loan Approval Classifier'
PROJECT_SUBTITLE = 'Predicts loan approval decisions from applicant and credit profile features.'
ACCENT = '#FF2D55'
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / 'outputs'
SCREENSHOT_DIR = BASE_DIR / 'screenshots'
MODEL_DIR = BASE_DIR / 'models'


def ensure_dirs():
    for folder in [OUTPUT_DIR, SCREENSHOT_DIR, MODEL_DIR]:
        folder.mkdir(exist_ok=True)


def save_json(name, data):
    path = OUTPUT_DIR / name
    path.write_text(json.dumps(data, indent=2), encoding='utf-8')
    return path


def write_preview(metrics, summary_rows):
    rows = ''.join(f'<tr><td>{k}</td><td>{v}</td></tr>' for k, v in summary_rows)
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{PROJECT_NAME}</title>
<style>
:root {{ --accent: {ACCENT}; --bg: #f5f7fb; --ink: #111827; --muted: #667085; }}
body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", sans-serif; background: var(--bg); color: var(--ink); }}
.wrap {{ max-width: 1040px; margin: 0 auto; padding: 34px 20px; }}
.hero {{ background: #fff; border: 1px solid #e6eaf2; border-radius: 18px; padding: 26px; box-shadow: 0 18px 45px rgba(18, 38, 63, .08); }}
.kicker {{ color: var(--accent); font-size: 13px; font-weight: 800; text-transform: uppercase; }}
h1 {{ margin: 8px 0 8px; font-size: 34px; }}
p {{ color: var(--muted); line-height: 1.6; }}
.grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin-top: 18px; }}
.card {{ background: #fff; border: 1px solid #e6eaf2; border-radius: 16px; padding: 18px; }}
.metric {{ font-size: 32px; font-weight: 850; color: var(--accent); }}
table {{ width: 100%; border-collapse: collapse; }}
td {{ padding: 10px 0; border-bottom: 1px solid #edf0f5; }}
img {{ max-width: 100%; border-radius: 12px; border: 1px solid #e6eaf2; }}
@media (max-width: 760px) {{ .grid {{ grid-template-columns: 1fr; }} h1 {{ font-size: 28px; }} }}
</style>
</head>
<body>
<div class="wrap">
<section class="hero">
<div class="kicker">Mithilesh Portfolio Project</div>
<h1>{PROJECT_NAME}</h1>
<p>{PROJECT_SUBTITLE}</p>
<div class="metric">{metrics.get('main_score', 'Ready')}</div>
<p>{metrics.get('score_label', 'Project output generated successfully')}</p>
</section>
<section class="grid">
<div class="card"><h2>Run Summary</h2><table>{rows}</table></div>
<div class="card"><h2>Output Chart</h2><img src="dashboard.png" alt="project dashboard chart"></div>
</section>
</div>
</body>
</html>"""
    path = SCREENSHOT_DIR / 'ui_preview.html'
    path.write_text(html, encoding='utf-8')
    return path


def plot_bar(labels, values, title):
    plt.figure(figsize=(8, 4.8))
    bars = plt.bar(labels, values, color=ACCENT)
    plt.title(title)
    plt.ylabel('Score')
    upper = max(values) * 1.25 if max(values) else 1
    plt.ylim(0, upper)
    plt.grid(axis='y', alpha=0.25)
    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{value:.2f}', ha='center', va='bottom')
    plt.tight_layout()
    path = SCREENSHOT_DIR / 'dashboard.png'
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def build_health_risk():
    feature_names = ['age', 'bmi', 'glucose', 'bp', 'activity_score', 'family_history']
    x, y = make_classification(n_samples=420, n_features=6, n_informative=5, n_redundant=0, weights=[0.58, 0.42], random_state=12)
    df = pd.DataFrame(x, columns=feature_names)
    df['age'] = (df['age'] * 9 + 42).round(1)
    df['bmi'] = (df['bmi'] * 3 + 25).round(1)
    df['glucose'] = (df['glucose'] * 16 + 105).round(1)
    df['bp'] = (df['bp'] * 8 + 78).round(1)
    df['activity_score'] = np.clip((df['activity_score'] * 12 + 55), 5, 100).round(1)
    df['family_history'] = (df['family_history'] > 0).astype(int)
    return df, y, feature_names


def build_house_prices():
    feature_names = ['area_sqft', 'bedrooms', 'bathrooms', 'age_years', 'location_score', 'distance_km']
    rng = np.random.default_rng(8)
    rows = 360
    df = pd.DataFrame({
        'area_sqft': rng.integers(650, 2800, rows),
        'bedrooms': rng.integers(1, 5, rows),
        'bathrooms': rng.integers(1, 4, rows),
        'age_years': rng.integers(0, 28, rows),
        'location_score': rng.integers(35, 98, rows),
        'distance_km': rng.uniform(1, 24, rows).round(1),
    })
    price = df['area_sqft'] * 4200 + df['bedrooms'] * 180000 + df['bathrooms'] * 90000 + df['location_score'] * 25000 - df['age_years'] * 18000 - df['distance_km'] * 22000 + rng.normal(0, 180000, rows)
    return df, price, feature_names


def build_sentiment():
    positives = ['beautiful movie with strong acting', 'really enjoyed the story and music', 'fresh direction and lovely performances', 'emotional film with a satisfying ending', 'smart screenplay and great visuals', 'excellent acting and memorable scenes', 'fun watch with good pacing', 'heartwarming and well made']
    negatives = ['boring movie with weak acting', 'slow story and confusing scenes', 'poor direction and dull music', 'bad screenplay with lazy ending', 'predictable film and flat performances', 'messy editing and weak visuals', 'not worth watching at all', 'dragging plot and forgettable scenes']
    texts = positives * 8 + negatives * 8
    labels = [1] * (len(positives) * 8) + [0] * (len(negatives) * 8)
    return texts, labels


def build_customer_segments():
    x, _ = make_blobs(n_samples=320, centers=4, cluster_std=1.15, random_state=42)
    df = pd.DataFrame({
        'monthly_spend': (x[:, 0] * 900 + 5200).round(2),
        'visits': np.clip((x[:, 1] * 4 + 18).round(), 1, 60),
        'income_score': np.clip((x[:, 0] * 8 + 60).round(), 1, 100),
        'loyalty_score': np.clip((x[:, 1] * 7 + 55).round(), 1, 100),
    })
    return df


def build_loan_data():
    feature_names = ['income', 'credit_score', 'loan_amount', 'existing_loans', 'employment_years', 'debt_ratio']
    rng = np.random.default_rng(17)
    rows = 420
    df = pd.DataFrame({
        'income': rng.integers(18000, 160000, rows),
        'credit_score': rng.integers(520, 860, rows),
        'loan_amount': rng.integers(50000, 1800000, rows),
        'existing_loans': rng.integers(0, 5, rows),
        'employment_years': rng.integers(0, 16, rows),
        'debt_ratio': rng.uniform(0.05, 0.65, rows).round(2),
    })
    score = df['income'] / 35000 + df['credit_score'] / 120 + df['employment_years'] * 0.18 - df['loan_amount'] / 650000 - df['existing_loans'] * 0.45 - df['debt_ratio'] * 2.2
    y = (score > np.median(score)).astype(int)
    return df, y, feature_names


def build_crop_data():
    rng = np.random.default_rng(24)
    labels = []
    rows = []
    centers = {
        'rice': [80, 45, 40, 28, 82, 230],
        'wheat': [50, 55, 35, 21, 55, 90],
        'cotton': [65, 40, 60, 30, 50, 75],
        'maize': [70, 50, 45, 25, 62, 120],
    }
    for crop, center in centers.items():
        for _ in range(90):
            n, p, k, temp, humidity, rainfall = center
            rows.append([rng.normal(n, 9), rng.normal(p, 7), rng.normal(k, 7), rng.normal(temp, 3), rng.normal(humidity, 8), rng.normal(rainfall, 22)])
            labels.append(crop)
    cols = ['nitrogen', 'phosphorus', 'potassium', 'temperature', 'humidity', 'rainfall']
    return pd.DataFrame(rows, columns=cols).round(2), labels, cols


def build_resume_matcher():
    roles = {
        'Data Analyst': 'python sql excel tableau pandas statistics dashboard reporting',
        'ML Intern': 'python machine learning scikit learn numpy pandas model evaluation regression classification',
        'Backend Intern': 'python flask sql database api authentication deployment testing',
        'Computer Vision Intern': 'python opencv image processing cnn classification numpy augmentation',
    }
    resumes = {
        'Resume A': 'python pandas sql dashboard excel statistics reporting',
        'Resume B': 'flask python api database sql testing deployment',
        'Resume C': 'opencv python image classification numpy model training',
        'Resume D': 'python scikit learn regression classification pandas numpy metrics',
    }
    return roles, resumes


def build_sales_data():
    rng = np.random.default_rng(31)
    months = np.arange(1, 49)
    season = np.sin(months / 12 * 2 * np.pi)
    sales = 42000 + months * 950 + season * 5200 + rng.normal(0, 2400, len(months))
    return pd.DataFrame({'month_index': months, 'season': season.round(3), 'sales': sales.round(2)})


def build_traffic_data():
    rng = np.random.default_rng(44)
    rows = 500
    df = pd.DataFrame({
        'hour': rng.integers(0, 24, rows),
        'weekday': rng.integers(0, 7, rows),
        'temperature': rng.uniform(18, 38, rows).round(1),
        'rain_mm': rng.exponential(1.2, rows).round(2),
        'is_event_day': rng.integers(0, 2, rows),
    })
    rush = ((df['hour'].between(8, 10)) | (df['hour'].between(17, 20))).astype(int)
    volume = 900 + rush * 850 + df['is_event_day'] * 420 - df['rain_mm'] * 45 + df['weekday'].isin([5, 6]).astype(int) * 170 + rng.normal(0, 120, rows)
    return df, volume, list(df.columns)


def run_pipeline():
    ensure_dirs()
    kind = 'loan'
    metrics = {}
    rows = []

    if kind == 'classification':
        df, y, features = build_health_risk()
        x_train, x_test, y_train, y_test = train_test_split(df[features], y, test_size=0.22, random_state=6)
        model = Pipeline([('scale', StandardScaler()), ('clf', RandomForestClassifier(n_estimators=120, random_state=6))])
        model.fit(x_train, y_train)
        preds = model.predict(x_test)
        acc = accuracy_score(y_test, preds)
        metrics = {'accuracy': round(float(acc), 4), 'main_score': f'{acc * 100:.1f}%', 'score_label': 'Test accuracy'}
        pd.DataFrame({'actual': y_test, 'predicted': preds}).to_csv(OUTPUT_DIR / 'predictions.csv', index=False)
        plot_bar(['Accuracy'], [acc], PROJECT_NAME)
        joblib.dump(model, MODEL_DIR / 'health_risk_model.joblib')

    elif kind == 'regression':
        df, y, features = build_house_prices()
        x_train, x_test, y_train, y_test = train_test_split(df[features], y, test_size=0.22, random_state=9)
        model = GradientBoostingRegressor(random_state=9)
        model.fit(x_train, y_train)
        preds = model.predict(x_test)
        r2 = r2_score(y_test, preds)
        mae = mean_absolute_error(y_test, preds)
        metrics = {'r2_score': round(float(r2), 4), 'mae': round(float(mae), 2), 'main_score': f'{r2 * 100:.1f}%', 'score_label': 'R2 score'}
        pd.DataFrame({'actual_price': y_test, 'predicted_price': preds.round(2)}).head(25).to_csv(OUTPUT_DIR / 'predictions.csv', index=False)
        plot_bar(['R2'], [max(r2, 0)], PROJECT_NAME)
        joblib.dump(model, MODEL_DIR / 'house_price_model.joblib')

    elif kind == 'sentiment':
        texts, labels = build_sentiment()
        x_train, x_test, y_train, y_test = train_test_split(texts, labels, test_size=0.25, random_state=10, stratify=labels)
        model = Pipeline([('tfidf', TfidfVectorizer(ngram_range=(1, 2))), ('clf', LogisticRegression(max_iter=400))])
        model.fit(x_train, y_train)
        preds = model.predict(x_test)
        acc = accuracy_score(y_test, preds)
        metrics = {'accuracy': round(float(acc), 4), 'main_score': f'{acc * 100:.1f}%', 'score_label': 'Sentiment accuracy'}
        pd.DataFrame({'review': x_test, 'actual': y_test, 'predicted': preds}).to_csv(OUTPUT_DIR / 'sample_predictions.csv', index=False)
        plot_bar(['Accuracy'], [acc], PROJECT_NAME)
        joblib.dump(model, MODEL_DIR / 'sentiment_model.joblib')

    elif kind == 'clustering':
        df = build_customer_segments()
        scaler = StandardScaler()
        x = scaler.fit_transform(df)
        model = KMeans(n_clusters=4, random_state=11, n_init=10)
        clusters = model.fit_predict(x)
        score = silhouette_score(x, clusters)
        df['segment'] = clusters
        metrics = {'silhouette_score': round(float(score), 4), 'segments': 4, 'main_score': f'{score:.2f}', 'score_label': 'Silhouette score'}
        df.to_csv(OUTPUT_DIR / 'customer_segments.csv', index=False)
        counts = df['segment'].value_counts().sort_index()
        plot_bar([f'Segment {i}' for i in counts.index], counts.values.tolist(), PROJECT_NAME)
        joblib.dump({'model': model, 'scaler': scaler}, MODEL_DIR / 'segmentation_model.joblib')

    elif kind == 'loan':
        df, y, features = build_loan_data()
        x_train, x_test, y_train, y_test = train_test_split(df[features], y, test_size=0.22, random_state=18)
        model = Pipeline([('scale', StandardScaler()), ('clf', LogisticRegression(max_iter=500))])
        model.fit(x_train, y_train)
        preds = model.predict(x_test)
        acc = accuracy_score(y_test, preds)
        metrics = {'accuracy': round(float(acc), 4), 'main_score': f'{acc * 100:.1f}%', 'score_label': 'Approval accuracy'}
        pd.DataFrame({'actual': y_test, 'predicted': preds}).to_csv(OUTPUT_DIR / 'approval_predictions.csv', index=False)
        plot_bar(['Accuracy'], [acc], PROJECT_NAME)
        joblib.dump(model, MODEL_DIR / 'loan_model.joblib')

    elif kind == 'crop':
        df, labels, features = build_crop_data()
        x_train, x_test, y_train, y_test = train_test_split(df[features], labels, test_size=0.2, random_state=19, stratify=labels)
        model = RandomForestClassifier(n_estimators=140, random_state=19)
        model.fit(x_train, y_train)
        preds = model.predict(x_test)
        acc = accuracy_score(y_test, preds)
        metrics = {'accuracy': round(float(acc), 4), 'main_score': f'{acc * 100:.1f}%', 'score_label': 'Crop recommendation accuracy'}
        pd.DataFrame({'actual_crop': y_test, 'recommended_crop': preds}).to_csv(OUTPUT_DIR / 'crop_predictions.csv', index=False)
        counts = pd.Series(preds).value_counts().sort_index()
        plot_bar(counts.index.tolist(), counts.values.tolist(), PROJECT_NAME)
        joblib.dump(model, MODEL_DIR / 'crop_model.joblib')

    elif kind == 'matcher':
        roles, resumes = build_resume_matcher()
        all_text = list(roles.values()) + list(resumes.values())
        vectorizer = TfidfVectorizer()
        matrix = vectorizer.fit_transform(all_text)
        role_matrix = matrix[:len(roles)]
        resume_matrix = matrix[len(roles):]
        sim = cosine_similarity(resume_matrix, role_matrix)
        report = []
        for i, resume in enumerate(resumes):
            best_idx = int(np.argmax(sim[i]))
            role = list(roles.keys())[best_idx]
            report.append({'resume': resume, 'best_role': role, 'match_score': round(float(sim[i][best_idx]), 3)})
        score = max(item['match_score'] for item in report)
        metrics = {'best_match_score': score, 'resumes_checked': len(resumes), 'main_score': f'{score * 100:.1f}%', 'score_label': 'Best resume match'}
        pd.DataFrame(report).to_csv(OUTPUT_DIR / 'match_report.csv', index=False)
        plot_bar([r['resume'] for r in report], [r['match_score'] for r in report], PROJECT_NAME)
        joblib.dump(vectorizer, MODEL_DIR / 'skill_vectorizer.joblib')

    elif kind == 'forecast':
        df = build_sales_data()
        features = ['month_index', 'season']
        train = df.iloc[:-8]
        test = df.iloc[-8:]
        model = LinearRegression()
        model.fit(train[features], train['sales'])
        preds = model.predict(test[features])
        r2 = r2_score(test['sales'], preds)
        mae = mean_absolute_error(test['sales'], preds)
        metrics = {'r2_score': round(float(r2), 4), 'mae': round(float(mae), 2), 'main_score': f'{max(r2, 0) * 100:.1f}%', 'score_label': 'Forecast R2 score'}
        pd.DataFrame({'month_index': test['month_index'], 'actual_sales': test['sales'], 'forecast_sales': preds.round(2)}).to_csv(OUTPUT_DIR / 'sales_forecast.csv', index=False)
        plot_bar(['R2'], [max(r2, 0)], PROJECT_NAME)
        joblib.dump(model, MODEL_DIR / 'sales_forecast_model.joblib')

    elif kind == 'digits':
        data = load_digits()
        x_train, x_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.22, random_state=20, stratify=data.target)
        model = Pipeline([('scale', StandardScaler()), ('clf', SVC(kernel='rbf', gamma='scale'))])
        model.fit(x_train, y_train)
        preds = model.predict(x_test)
        acc = accuracy_score(y_test, preds)
        metrics = {'accuracy': round(float(acc), 4), 'main_score': f'{acc * 100:.1f}%', 'score_label': 'Digit recognition accuracy'}
        pd.DataFrame({'actual_digit': y_test, 'predicted_digit': preds}).to_csv(OUTPUT_DIR / 'digit_predictions.csv', index=False)
        values = pd.Series(preds).value_counts().sort_index()
        plot_bar([str(v) for v in values.index], values.values.tolist(), PROJECT_NAME)
        joblib.dump(model, MODEL_DIR / 'digit_svm_model.joblib')

    elif kind == 'traffic':
        df, y, features = build_traffic_data()
        x_train, x_test, y_train, y_test = train_test_split(df[features], y, test_size=0.22, random_state=25)
        model = RandomForestRegressor(n_estimators=130, random_state=25)
        model.fit(x_train, y_train)
        preds = model.predict(x_test)
        r2 = r2_score(y_test, preds)
        mae = mean_absolute_error(y_test, preds)
        metrics = {'r2_score': round(float(r2), 4), 'mae': round(float(mae), 2), 'main_score': f'{max(r2, 0) * 100:.1f}%', 'score_label': 'Traffic volume R2 score'}
        pd.DataFrame({'actual_volume': y_test, 'predicted_volume': preds.round(2)}).head(30).to_csv(OUTPUT_DIR / 'traffic_predictions.csv', index=False)
        plot_bar(['R2'], [max(r2, 0)], PROJECT_NAME)
        joblib.dump(model, MODEL_DIR / 'traffic_model.joblib')

    for key, value in metrics.items():
        if key not in ['main_score', 'score_label']:
            rows.append((key.replace('_', ' ').title(), value))
    save_json('metrics.json', metrics)
    write_preview(metrics, rows)
    (OUTPUT_DIR / 'run_log.txt').write_text(f'{PROJECT_NAME} pipeline completed. Metrics: {json.dumps(metrics)}\n', encoding='utf-8')
    return metrics


if __name__ == '__main__':
    result = run_pipeline()
    print(json.dumps(result, indent=2))
