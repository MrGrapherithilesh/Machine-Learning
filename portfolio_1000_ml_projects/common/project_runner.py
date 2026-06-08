from pathlib import Path
import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs, make_classification, make_regression
from sklearn.decomposition import PCA
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor, IsolationForest, RandomForestClassifier, RandomForestRegressor, VotingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge
from sklearn.metrics import accuracy_score, mean_absolute_error, r2_score, silhouette_score
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

IOS_COLORS = ['#007AFF', '#34C759', '#FF9500', '#AF52DE', '#FF2D55', '#5856D6', '#64D2FF', '#FF3B30', '#30D158', '#BF5AF2']


def setup(project_dir):
    output_dir = project_dir / 'outputs'
    screenshot_dir = project_dir / 'screenshots'
    output_dir.mkdir(exist_ok=True)
    screenshot_dir.mkdir(exist_ok=True)
    return output_dir, screenshot_dir


def rng_for(project_id):
    return np.random.default_rng(5000 + project_id)


def chart(title, label, value, screenshot_dir, accent):
    plt.figure(figsize=(7.6, 4.4))
    plt.bar([label], [value], color=accent)
    plt.ylim(0, max(1.0, value * 1.2))
    plt.title(title)
    plt.grid(axis='y', alpha=0.25)
    plt.tight_layout()
    plt.savefig(screenshot_dir / 'dashboard.png', dpi=130)
    plt.close()


def preview(project_title, project_kind, industry, subject, metrics, screenshot_dir, accent):
    rows = ''.join(f'<tr><td>{key}</td><td>{value}</td></tr>' for key, value in metrics.items())
    main_score = metrics.get('main_score', 'Ready')
    html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{project_title}</title>
<style>
:root {{ --accent: {accent}; --bg: #f5f7fb; --ink: #111827; --muted: #667085; }}
body {{ margin: 0; background: var(--bg); color: var(--ink); font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", sans-serif; }}
.wrap {{ max-width: 980px; margin: 0 auto; padding: 32px 20px; }}
.hero {{ background: #fff; border: 1px solid #e6eaf2; border-radius: 18px; padding: 26px; box-shadow: 0 18px 45px rgba(18, 38, 63, .08); }}
.kicker {{ color: var(--accent); font-size: 13px; font-weight: 800; text-transform: uppercase; }}
h1 {{ margin: 8px 0; font-size: 31px; }} p {{ color: var(--muted); line-height: 1.6; }} .score {{ color: var(--accent); font-size: 34px; font-weight: 850; }}
.grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin-top: 18px; }} .card {{ background: #fff; border: 1px solid #e6eaf2; border-radius: 16px; padding: 18px; }}
table {{ width: 100%; border-collapse: collapse; }} td {{ padding: 10px 0; border-bottom: 1px solid #edf0f5; }} img {{ max-width: 100%; border-radius: 12px; border: 1px solid #e6eaf2; }}
@media (max-width: 760px) {{ .grid {{ grid-template-columns: 1fr; }} }}
</style></head><body><div class="wrap"><section class="hero"><div class="kicker">Mithilesh ML Portfolio</div><h1>{project_title}</h1><p>Medium-level Python ML project for {industry} focused on {subject}. It includes model training, metrics, generated outputs, and a screenshot-friendly preview.</p><div class="score">{main_score}</div></section><section class="grid"><div class="card"><h2>Metrics</h2><table>{rows}</table></div><div class="card"><h2>Chart</h2><img src="dashboard.png" alt="dashboard chart"></div></section></div></body></html>'''
    (screenshot_dir / 'ui_preview.html').write_text(html, encoding='utf-8')


def finish(project_title, project_kind, industry, subject, metrics, output_dir, screenshot_dir, accent, label, value):
    (output_dir / 'metrics.json').write_text(json.dumps(metrics, indent=2), encoding='utf-8')
    (output_dir / 'run_log.txt').write_text(f'{project_title} completed with {json.dumps(metrics)}\n', encoding='utf-8')
    chart(project_title, label, value, screenshot_dir, accent)
    preview(project_title, project_kind, industry, subject, metrics, screenshot_dir, accent)


def advanced_classification(project_id, project_title, industry, subject, project_dir):
    out, shots = setup(project_dir); accent = IOS_COLORS[project_id % len(IOS_COLORS)]
    x, y = make_classification(n_samples=420, n_features=9, n_informative=6, n_redundant=1, weights=[0.62, 0.38], class_sep=1.15, random_state=project_id)
    frame = pd.DataFrame(x, columns=[f'signal_{i}' for i in range(1, 10)])
    xtr, xte, ytr, yte = train_test_split(frame, y, test_size=0.24, random_state=project_id, stratify=y)
    model = GradientBoostingClassifier(random_state=project_id)
    model.fit(xtr, ytr); pred = model.predict(xte)
    score = accuracy_score(yte, pred)
    pd.DataFrame({'actual': yte, 'predicted': pred}).to_csv(out / 'classification_report.csv', index=False)
    metrics = {'accuracy': round(float(score), 4), 'samples': len(frame), 'main_score': f'{score * 100:.1f}%'}
    finish(project_title, 'advanced classification', industry, subject, metrics, out, shots, accent, 'Accuracy', score)
    return metrics


def robust_regression(project_id, project_title, industry, subject, project_dir):
    out, shots = setup(project_dir); accent = IOS_COLORS[project_id % len(IOS_COLORS)]
    x, y = make_regression(n_samples=420, n_features=7, n_informative=5, noise=14, random_state=project_id)
    frame = pd.DataFrame(x, columns=[f'factor_{i}' for i in range(1, 8)])
    xtr, xte, ytr, yte = train_test_split(frame, y, test_size=0.24, random_state=project_id)
    model = GradientBoostingRegressor(random_state=project_id)
    model.fit(xtr, ytr); pred = model.predict(xte)
    r2 = max(0, r2_score(yte, pred)); mae = mean_absolute_error(yte, pred)
    pd.DataFrame({'actual': yte, 'predicted': pred.round(3)}).head(36).to_csv(out / 'regression_predictions.csv', index=False)
    metrics = {'r2_score': round(float(r2), 4), 'mae': round(float(mae), 2), 'main_score': f'{r2 * 100:.1f}%'}
    finish(project_title, 'robust regression', industry, subject, metrics, out, shots, accent, 'R2', r2)
    return metrics


def market_clustering(project_id, project_title, industry, subject, project_dir):
    out, shots = setup(project_dir); accent = IOS_COLORS[project_id % len(IOS_COLORS)]
    x, _ = make_blobs(n_samples=360, centers=5, n_features=5, cluster_std=1.2, random_state=project_id)
    frame = pd.DataFrame(x, columns=['value_score', 'usage_score', 'risk_score', 'growth_score', 'support_score'])
    scaled = StandardScaler().fit_transform(frame)
    model = KMeans(n_clusters=5, n_init=10, random_state=project_id)
    frame['segment'] = model.fit_predict(scaled)
    score = silhouette_score(scaled, frame['segment'])
    frame.to_csv(out / 'segments.csv', index=False)
    metrics = {'silhouette_score': round(float(score), 4), 'segments': 5, 'main_score': f'{score:.2f}'}
    finish(project_title, 'segmentation clustering', industry, subject, metrics, out, shots, accent, 'Silhouette', score)
    return metrics


def seasonal_forecasting(project_id, project_title, industry, subject, project_dir):
    out, shots = setup(project_dir); accent = IOS_COLORS[project_id % len(IOS_COLORS)]
    rng = rng_for(project_id)
    t = np.arange(1, 61)
    seasonal = np.sin(t / 12 * 2 * np.pi)
    target = 800 + t * (8 + project_id % 11) + seasonal * 120 + rng.normal(0, 24, len(t))
    frame = pd.DataFrame({'period': t, 'seasonality': seasonal, 'target': target})
    train, test = frame.iloc[:-10], frame.iloc[-10:]
    model = Ridge(alpha=0.8)
    model.fit(train[['period', 'seasonality']], train['target'])
    pred = model.predict(test[['period', 'seasonality']])
    r2 = max(0, r2_score(test['target'], pred)); mae = mean_absolute_error(test['target'], pred)
    pd.DataFrame({'period': test['period'], 'actual': test['target'].round(2), 'forecast': pred.round(2)}).to_csv(out / 'forecast.csv', index=False)
    metrics = {'r2_score': round(float(r2), 4), 'mae': round(float(mae), 2), 'main_score': f'{r2 * 100:.1f}%'}
    finish(project_title, 'seasonal forecasting', industry, subject, metrics, out, shots, accent, 'R2', r2)
    return metrics


def semantic_nlp(project_id, project_title, industry, subject, project_dir):
    out, shots = setup(project_dir); accent = IOS_COLORS[project_id % len(IOS_COLORS)]
    labels = {'analysis': f'{industry} {subject} analytics metrics dashboard python pandas', 'prediction': f'{industry} {subject} machine learning model prediction sklearn', 'operations': f'{industry} {subject} workflow operations monitoring planning'}
    docs = {'doc_a': f'{industry} dashboard metrics analytics {subject}', 'doc_b': f'{subject} sklearn prediction model for {industry}', 'doc_c': f'{industry} workflow monitoring planning {subject}'}
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(list(labels.values()) + list(docs.values()))
    sims = cosine_similarity(matrix[len(labels):], matrix[:len(labels)])
    label_names = list(labels.keys())
    rows = []
    for idx, doc in enumerate(docs):
        best = int(np.argmax(sims[idx]))
        rows.append({'document': doc, 'best_label': label_names[best], 'score': round(float(sims[idx][best]), 3)})
    best_score = max(row['score'] for row in rows)
    pd.DataFrame(rows).to_csv(out / 'semantic_matches.csv', index=False)
    metrics = {'best_similarity': best_score, 'documents': len(docs), 'main_score': f'{best_score * 100:.1f}%'}
    finish(project_title, 'semantic NLP', industry, subject, metrics, out, shots, accent, 'Similarity', best_score)
    return metrics


def anomaly_detection(project_id, project_title, industry, subject, project_dir):
    out, shots = setup(project_dir); accent = IOS_COLORS[project_id % len(IOS_COLORS)]
    rng = rng_for(project_id)
    normal = rng.normal(0, 1, (320, 6)); rare = rng.normal(4.2, 0.9, (28, 6))
    frame = pd.DataFrame(np.vstack([normal, rare]), columns=[f'metric_{i}' for i in range(1, 7)])
    labels = IsolationForest(contamination=0.08, random_state=project_id).fit_predict(frame)
    frame['anomaly_flag'] = (labels == -1).astype(int)
    rate = float(frame['anomaly_flag'].mean())
    frame.to_csv(out / 'anomaly_flags.csv', index=False)
    metrics = {'anomaly_rate': round(rate, 4), 'flagged_rows': int(frame['anomaly_flag'].sum()), 'main_score': f'{rate * 100:.1f}%'}
    finish(project_title, 'anomaly detection', industry, subject, metrics, out, shots, accent, 'Anomaly Rate', rate)
    return metrics


def recommendation_system(project_id, project_title, industry, subject, project_dir):
    out, shots = setup(project_dir); accent = IOS_COLORS[project_id % len(IOS_COLORS)]
    rng = rng_for(project_id)
    users = [f'user_{i}' for i in range(1, 11)]
    items = [f'option_{i}' for i in range(1, 8)]
    ratings = pd.DataFrame(rng.integers(1, 6, (len(users), len(items))), index=users, columns=items)
    sims = cosine_similarity(ratings)
    target = project_id % len(users)
    neighbor = int(np.argsort(sims[target])[-2])
    item = ratings.iloc[neighbor].idxmax()
    score = float(sims[target][neighbor])
    pd.DataFrame([{'target_user': users[target], 'similar_user': users[neighbor], 'recommended_item': item, 'similarity': round(score, 3)}]).to_csv(out / 'recommendation.csv', index=False)
    metrics = {'similarity': round(score, 4), 'users': len(users), 'main_score': f'{score * 100:.1f}%'}
    finish(project_title, 'recommendation system', industry, subject, metrics, out, shots, accent, 'Similarity', score)
    return metrics


def ensemble_scoring(project_id, project_title, industry, subject, project_dir):
    out, shots = setup(project_dir); accent = IOS_COLORS[project_id % len(IOS_COLORS)]
    x, y = make_classification(n_samples=430, n_features=8, n_informative=6, n_redundant=1, class_sep=1.05, random_state=project_id)
    frame = pd.DataFrame(x, columns=[f'feature_{i}' for i in range(1, 9)])
    xtr, xte, ytr, yte = train_test_split(frame, y, test_size=0.25, random_state=project_id, stratify=y)
    model = VotingClassifier(estimators=[('rf', RandomForestClassifier(n_estimators=70, random_state=project_id)), ('gb', GradientBoostingClassifier(random_state=project_id)), ('lr', LogisticRegression(max_iter=500))], voting='soft')
    model.fit(xtr, ytr); pred = model.predict(xte)
    score = accuracy_score(yte, pred)
    pd.DataFrame({'actual': yte, 'ensemble_prediction': pred}).to_csv(out / 'ensemble_predictions.csv', index=False)
    metrics = {'ensemble_accuracy': round(float(score), 4), 'models': 3, 'main_score': f'{score * 100:.1f}%'}
    finish(project_title, 'ensemble scoring', industry, subject, metrics, out, shots, accent, 'Accuracy', score)
    return metrics


def dimension_reduction(project_id, project_title, industry, subject, project_dir):
    out, shots = setup(project_dir); accent = IOS_COLORS[project_id % len(IOS_COLORS)]
    x, _ = make_blobs(n_samples=360, centers=4, n_features=10, cluster_std=1.4, random_state=project_id)
    frame = pd.DataFrame(x, columns=[f'feature_{i}' for i in range(1, 11)])
    scaled = StandardScaler().fit_transform(frame)
    pca = PCA(n_components=3, random_state=project_id)
    compressed = pca.fit_transform(scaled)
    explained = float(pca.explained_variance_ratio_.sum())
    pd.DataFrame(compressed, columns=['pc1', 'pc2', 'pc3']).to_csv(out / 'compressed_features.csv', index=False)
    metrics = {'explained_variance': round(explained, 4), 'components': 3, 'main_score': f'{explained * 100:.1f}%'}
    finish(project_title, 'dimension reduction', industry, subject, metrics, out, shots, accent, 'Explained', explained)
    return metrics


def model_monitoring(project_id, project_title, industry, subject, project_dir):
    out, shots = setup(project_dir); accent = IOS_COLORS[project_id % len(IOS_COLORS)]
    rng = rng_for(project_id)
    baseline = rng.normal(0, 1, 300)
    current = rng.normal(0.18 + (project_id % 5) * 0.03, 1.08, 300)
    drift = abs(float(current.mean() - baseline.mean()))
    threshold = 0.12
    status = 'attention_needed' if drift > threshold else 'stable'
    pd.DataFrame({'baseline': baseline, 'current': current}).to_csv(out / 'monitoring_sample.csv', index=False)
    metrics = {'drift_score': round(drift, 4), 'threshold': threshold, 'status': status, 'main_score': f'{drift:.2f}'}
    finish(project_title, 'model monitoring', industry, subject, metrics, out, shots, accent, 'Drift', min(drift, 1.0))
    return metrics

RUNNERS = {
    'advanced_classification': advanced_classification,
    'robust_regression': robust_regression,
    'market_clustering': market_clustering,
    'seasonal_forecasting': seasonal_forecasting,
    'semantic_nlp': semantic_nlp,
    'anomaly_detection': anomaly_detection,
    'recommendation_system': recommendation_system,
    'ensemble_scoring': ensemble_scoring,
    'dimension_reduction': dimension_reduction,
    'model_monitoring': model_monitoring,
}


def run_project(project_id, project_title, industry, subject, project_kind, project_dir):
    return RUNNERS[project_kind](project_id, project_title, industry, subject, project_dir)
