from pathlib import Path
import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs, make_classification, make_regression
from sklearn.ensemble import IsolationForest, RandomForestClassifier, RandomForestRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score, mean_absolute_error, r2_score, silhouette_score
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

IOS_COLORS = ['#007AFF', '#34C759', '#FF9500', '#AF52DE', '#FF2D55', '#5856D6', '#64D2FF', '#FF3B30', '#30D158', '#BF5AF2']


def folders(project_dir):
    output_dir = project_dir / 'outputs'
    screenshot_dir = project_dir / 'screenshots'
    output_dir.mkdir(exist_ok=True)
    screenshot_dir.mkdir(exist_ok=True)
    return output_dir, screenshot_dir


def rng_for(project_id):
    return np.random.default_rng(1000 + project_id)


def plot_metric(project_title, metric_name, metric_value, screenshot_dir, accent):
    plt.figure(figsize=(7.6, 4.4))
    plt.bar([metric_name], [metric_value], color=accent)
    plt.ylim(0, max(1.0, metric_value * 1.2))
    plt.title(project_title)
    plt.grid(axis='y', alpha=0.25)
    plt.tight_layout()
    plt.savefig(screenshot_dir / 'dashboard.png', dpi=150)
    plt.close()


def preview_page(project_title, project_kind, domain, metrics, screenshot_dir, accent):
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
h1 {{ margin: 8px 0; font-size: 32px; }} p {{ color: var(--muted); line-height: 1.6; }} .score {{ color: var(--accent); font-size: 34px; font-weight: 850; }}
.grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin-top: 18px; }} .card {{ background: #fff; border: 1px solid #e6eaf2; border-radius: 16px; padding: 18px; }}
table {{ width: 100%; border-collapse: collapse; }} td {{ padding: 10px 0; border-bottom: 1px solid #edf0f5; }} img {{ max-width: 100%; border-radius: 12px; border: 1px solid #e6eaf2; }}
@media (max-width: 760px) {{ .grid {{ grid-template-columns: 1fr; }} }}
</style></head><body><div class="wrap"><section class="hero"><div class="kicker">Mithilesh ML Portfolio</div><h1>{project_title}</h1><p>A compact {project_kind} project around {domain}, built to show data preparation, model training, evaluation, and output reporting.</p><div class="score">{main_score}</div></section><section class="grid"><div class="card"><h2>Metrics</h2><table>{rows}</table></div><div class="card"><h2>Chart</h2><img src="dashboard.png" alt="dashboard chart"></div></section></div></body></html>'''
    (screenshot_dir / 'ui_preview.html').write_text(html, encoding='utf-8')


def finish(project_title, project_kind, domain, metrics, output_dir, screenshot_dir, accent, chart_label, chart_value):
    (output_dir / 'metrics.json').write_text(json.dumps(metrics, indent=2), encoding='utf-8')
    (output_dir / 'run_log.txt').write_text(f'{project_title} completed with {json.dumps(metrics)}\n', encoding='utf-8')
    plot_metric(project_title, chart_label, chart_value, screenshot_dir, accent)
    preview_page(project_title, project_kind, domain, metrics, screenshot_dir, accent)


def run_classification(project_id, project_title, domain, project_dir):
    output_dir, screenshot_dir = folders(project_dir)
    accent = IOS_COLORS[project_id % len(IOS_COLORS)]
    x, y = make_classification(n_samples=360, n_features=6, n_informative=5, n_redundant=0, random_state=project_id)
    frame = pd.DataFrame(x, columns=[f'feature_{i}' for i in range(1, 7)])
    x_train, x_test, y_train, y_test = train_test_split(frame, y, test_size=0.24, random_state=project_id)
    model = Pipeline([('scale', StandardScaler()), ('model', RandomForestClassifier(n_estimators=90, random_state=project_id))])
    model.fit(x_train, y_train)
    preds = model.predict(x_test)
    score = accuracy_score(y_test, preds)
    pd.DataFrame({'actual': y_test, 'predicted': preds}).to_csv(output_dir / 'predictions.csv', index=False)
    metrics = {'accuracy': round(float(score), 4), 'main_score': f'{score * 100:.1f}%'}
    finish(project_title, 'classification', domain, metrics, output_dir, screenshot_dir, accent, 'Accuracy', score)
    return metrics


def run_regression(project_id, project_title, domain, project_dir):
    output_dir, screenshot_dir = folders(project_dir)
    accent = IOS_COLORS[project_id % len(IOS_COLORS)]
    x, y = make_regression(n_samples=360, n_features=5, noise=18, random_state=project_id)
    frame = pd.DataFrame(x, columns=[f'feature_{i}' for i in range(1, 6)])
    x_train, x_test, y_train, y_test = train_test_split(frame, y, test_size=0.24, random_state=project_id)
    model = RandomForestRegressor(n_estimators=90, random_state=project_id)
    model.fit(x_train, y_train)
    preds = model.predict(x_test)
    r2 = max(0, r2_score(y_test, preds))
    mae = mean_absolute_error(y_test, preds)
    pd.DataFrame({'actual': y_test, 'predicted': preds.round(3)}).head(30).to_csv(output_dir / 'predictions.csv', index=False)
    metrics = {'r2_score': round(float(r2), 4), 'mae': round(float(mae), 2), 'main_score': f'{r2 * 100:.1f}%'}
    finish(project_title, 'regression', domain, metrics, output_dir, screenshot_dir, accent, 'R2', r2)
    return metrics


def run_clustering(project_id, project_title, domain, project_dir):
    output_dir, screenshot_dir = folders(project_dir)
    accent = IOS_COLORS[project_id % len(IOS_COLORS)]
    x, _ = make_blobs(n_samples=300, centers=4, n_features=4, cluster_std=1.25, random_state=project_id)
    frame = pd.DataFrame(x, columns=['spend_score', 'activity_score', 'value_score', 'risk_score'])
    scaled = StandardScaler().fit_transform(frame)
    model = KMeans(n_clusters=4, random_state=project_id, n_init=10)
    frame['cluster'] = model.fit_predict(scaled)
    score = silhouette_score(scaled, frame['cluster'])
    frame.to_csv(output_dir / 'clusters.csv', index=False)
    metrics = {'silhouette_score': round(float(score), 4), 'clusters': 4, 'main_score': f'{score:.2f}'}
    finish(project_title, 'clustering', domain, metrics, output_dir, screenshot_dir, accent, 'Silhouette', score)
    return metrics


def run_forecasting(project_id, project_title, domain, project_dir):
    output_dir, screenshot_dir = folders(project_dir)
    accent = IOS_COLORS[project_id % len(IOS_COLORS)]
    rng = rng_for(project_id)
    months = np.arange(1, 49)
    season = np.sin(months / 12 * 2 * np.pi)
    target = 1200 + months * (18 + project_id % 9) + season * 140 + rng.normal(0, 28, len(months))
    frame = pd.DataFrame({'month_index': months, 'season': season, 'target': target})
    train = frame.iloc[:-8]
    test = frame.iloc[-8:]
    model = LinearRegression()
    model.fit(train[['month_index', 'season']], train['target'])
    preds = model.predict(test[['month_index', 'season']])
    r2 = max(0, r2_score(test['target'], preds))
    mae = mean_absolute_error(test['target'], preds)
    pd.DataFrame({'month': test['month_index'], 'actual': test['target'].round(2), 'forecast': preds.round(2)}).to_csv(output_dir / 'forecast.csv', index=False)
    metrics = {'r2_score': round(float(r2), 4), 'mae': round(float(mae), 2), 'main_score': f'{r2 * 100:.1f}%'}
    finish(project_title, 'forecasting', domain, metrics, output_dir, screenshot_dir, accent, 'R2', r2)
    return metrics


def run_nlp(project_id, project_title, domain, project_dir):
    output_dir, screenshot_dir = folders(project_dir)
    accent = IOS_COLORS[project_id % len(IOS_COLORS)]
    roles = {'analytics': f'{domain} python pandas sql dashboard reporting metrics', 'modeling': f'{domain} machine learning sklearn regression classification training', 'operations': f'{domain} process tracking workflow planning quality checks'}
    samples = {'sample_a': f'{domain} python pandas dashboard metrics', 'sample_b': f'{domain} sklearn model training prediction', 'sample_c': f'{domain} workflow planning quality process'}
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(list(roles.values()) + list(samples.values()))
    similarities = cosine_similarity(matrix[len(roles):], matrix[:len(roles)])
    role_names = list(roles.keys())
    report = []
    for index, sample in enumerate(samples):
        best = int(np.argmax(similarities[index]))
        report.append({'sample': sample, 'best_match': role_names[best], 'score': round(float(similarities[index][best]), 3)})
    best_score = max(item['score'] for item in report)
    pd.DataFrame(report).to_csv(output_dir / 'match_report.csv', index=False)
    metrics = {'best_match_score': best_score, 'samples': len(samples), 'main_score': f'{best_score * 100:.1f}%'}
    finish(project_title, 'NLP matching', domain, metrics, output_dir, screenshot_dir, accent, 'Match', best_score)
    return metrics


def run_anomaly(project_id, project_title, domain, project_dir):
    output_dir, screenshot_dir = folders(project_dir)
    accent = IOS_COLORS[project_id % len(IOS_COLORS)]
    rng = rng_for(project_id)
    x = np.vstack([rng.normal(0, 1, (260, 4)), rng.normal(4, 0.8, (25, 4))])
    frame = pd.DataFrame(x, columns=['signal_1', 'signal_2', 'signal_3', 'signal_4'])
    labels = IsolationForest(contamination=0.09, random_state=project_id).fit_predict(frame)
    frame['is_anomaly'] = (labels == -1).astype(int)
    rate = frame['is_anomaly'].mean()
    frame.to_csv(output_dir / 'anomaly_report.csv', index=False)
    metrics = {'anomaly_rate': round(float(rate), 4), 'flagged_rows': int(frame['is_anomaly'].sum()), 'main_score': f'{rate * 100:.1f}%'}
    finish(project_title, 'anomaly detection', domain, metrics, output_dir, screenshot_dir, accent, 'Anomaly Rate', rate)
    return metrics


def run_recommendation(project_id, project_title, domain, project_dir):
    output_dir, screenshot_dir = folders(project_dir)
    accent = IOS_COLORS[project_id % len(IOS_COLORS)]
    rng = rng_for(project_id)
    users = [f'user_{i}' for i in range(1, 9)]
    items = [f'item_{i}' for i in range(1, 7)]
    ratings = pd.DataFrame(rng.integers(1, 6, (len(users), len(items))), index=users, columns=items)
    similarity = cosine_similarity(ratings)
    target_index = project_id % len(users)
    nearest = int(np.argsort(similarity[target_index])[-2])
    recommendation = ratings.iloc[nearest].idxmax()
    score = float(similarity[target_index][nearest])
    pd.DataFrame([{'target_user': users[target_index], 'similar_user': users[nearest], 'recommended_item': recommendation, 'similarity': round(score, 3)}]).to_csv(output_dir / 'recommendation.csv', index=False)
    metrics = {'similarity': round(score, 4), 'users': len(users), 'main_score': f'{score * 100:.1f}%'}
    finish(project_title, 'recommendation', domain, metrics, output_dir, screenshot_dir, accent, 'Similarity', score)
    return metrics
