import logging

from django import apps
from django.db import connection, transaction


LOGGER = logging.getLogger(__name__)

DOCUMENT_VECTOR_SQL = """
DROP TRIGGER IF EXISTS {table_name}_{document_vector}_update_trigger ON {table_name};
DROP INDEX IF EXISTS {table_name}_gin_index;
DROP INDEX IF EXISTS {table_name}_trigram_index;
UPDATE {table_name} set {document_vector}=(select to_tsvector({document}));
CREATE INDEX {table_name}_gin_index ON {table_name} USING gin({document_vector});
CREATE TRIGGER {table_name}_{document_vector}_update_trigger
BEFORE INSERT OR UPDATE
ON {table_name} FOR EACH ROW
EXECUTE PROCEDURE tsvector_update_trigger(
    {document_vector}, 'pg_catalog.english', {document});
CREATE INDEX {table_name}_trigram_index ON {table_name} USING GIN ({document} gin_trgm_ops);
"""  # NOQA


@transaction.atomic
def populate_models_document_field():
    """
    Use SQL to generate the content of the document field in models.
    Raw SQL is necessary to reduce the time taken to populate the search field.
    Raw SQL takes roughly 10 minutes whereas Django takes upwards of 2 hours.
    """
    all_models = apps.apps.get_models()
    search_enhanced_models = [
        model for model in all_models if hasattr(model, '_search_fields')]
    conn = connection.cursor()

    for model in search_enhanced_models:
        model.bulk_populate_document()

        table_name = "{}_{}".format(
            model._meta.app_label, model.__name__.lower())
        document_field_name = getattr(
            model, "_ts_document_field", "ts_document")
        document_vector_field_name = getattr(
            model, "_ts_document_vector_field", "ts_document_vector")

        index_query = DOCUMENT_VECTOR_SQL.format(
            table_name=table_name, document=document_field_name,
            document_vector=document_vector_field_name)

        LOGGER.info("Executing ===> {}".format(index_query))
        conn.execute(index_query)
