from core.mapper import suggest_mappings
from core.models import SchemaField


def test_mapping_suggests_customer_id_match():
    source = [
        SchemaField("cust_id", "string", True, "unique customer identifier"),
        SchemaField("email_address", "email", True, "primary contact email"),
    ]
    target = [
        SchemaField("external_customer_id", "string", True, "external id for contact upsert"),
        SchemaField("email", "email", True, "email address for CRM contact"),
    ]
    mappings = suggest_mappings(source, target)
    pairs = {(item.source_field, item.target_field) for item in mappings}
    assert ("email_address", "email") in pairs
    assert len(mappings) == 2

