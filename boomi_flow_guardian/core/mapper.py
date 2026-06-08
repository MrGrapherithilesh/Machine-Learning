from typing import List

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from core.models import MappingSuggestion, SchemaField
from core.schema_reader import describe_field


def transformation_for(source: SchemaField, target: SchemaField) -> str:
    if source.data_type == target.data_type:
        return "direct"
    numeric = {"integer", "number", "float", "decimal"}
    if source.data_type in numeric and target.data_type in numeric:
        return "numeric_cast"
    if target.data_type == "date":
        return "date_parse"
    if target.data_type == "email":
        return "lowercase_trim"
    if target.data_type == "string":
        return "to_string"
    return "review_required"


def suggest_mappings(source_fields: List[SchemaField], target_fields: List[SchemaField]) -> List[MappingSuggestion]:
    source_docs = [describe_field(field) for field in source_fields]
    target_docs = [describe_field(field) for field in target_fields]
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), analyzer="word")
    matrix = vectorizer.fit_transform(source_docs + target_docs)
    source_matrix = matrix[: len(source_fields)]
    target_matrix = matrix[len(source_fields) :]
    scores = cosine_similarity(source_matrix, target_matrix)

    suggestions = []
    used_targets = set()
    for src_index, source in enumerate(source_fields):
        ranked = np.argsort(scores[src_index])[::-1]
        chosen_index = next((idx for idx in ranked if idx not in used_targets), int(ranked[0]))
        used_targets.add(chosen_index)
        target = target_fields[int(chosen_index)]
        confidence = float(scores[src_index][chosen_index])
        confidence = min(0.98, max(0.15, confidence + name_bonus(source.name, target.name)))
        suggestions.append(
            MappingSuggestion(
                source_field=source.name,
                target_field=target.name,
                confidence=round(confidence, 3),
                transformation=transformation_for(source, target),
                notes=notes_for(confidence, source, target),
            )
        )
    return sorted(suggestions, key=lambda item: item.confidence, reverse=True)


def name_bonus(source_name: str, target_name: str) -> float:
    src = set(source_name.lower().replace("_", " ").split())
    tgt = set(target_name.lower().replace("_", " ").split())
    if not src or not tgt:
        return 0.0
    overlap = len(src & tgt) / max(len(src | tgt), 1)
    return overlap * 0.32


def notes_for(confidence: float, source: SchemaField, target: SchemaField) -> str:
    if confidence >= 0.72:
        return "Strong match based on name, type, and description."
    if source.data_type != target.data_type:
        return "Possible match, but data type conversion must be checked."
    return "Medium confidence match; review before building the map."

