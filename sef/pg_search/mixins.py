import logging

from django.contrib.postgres.search import SearchVectorField
from django.db import connection, models

LOGGER = logging.getLogger(__name__)

LOOKUP_SEP = '.'


class SearchModelMixin(models.Model):
    _ts_document_field = "ts_document"
    _ts_document_vector_field = "ts_document_vector"

    ts_document = models.TextField(
        null=True, blank=True,
        help_text='The content that will be searched over')
    # this field will be used for exact matches.
    # if the exact fails there will be fallback to trigram search using
    # the document field above
    ts_document_vector = SearchVectorField(
        null=True, blank=True,
        help_text='The ts_vector for the document field')

    def get_field_value(self, field):
        opts = self._meta
        this = self

        parts = field.split(LOOKUP_SEP)

        for part in parts:  # pragma: no branch
            field_obj = opts.get_field(part)
            is_relation = getattr(field_obj, 'get_path_info', lambda: None)()
            field_value = getattr(this, part, '')

            if not field_value:
                return ''

            if not is_relation:
                return str(field_value)

            if parts[-1] == part:
                m2m = is_relation[0].m2m
                relation = field_value
                return (
                    " ".join([
                        each.get_search_content()
                        for each in relation.all()])
                ) if m2m else relation.get_search_content()

            opts = is_relation[-1].to_opts
            this = field_value

    def get_search_content(self):
        """
        Gets the content to populate the document field.
        This content is inferred
        from the concatenation of values of fields in the _search_fields
        attribute in the model.
        The items in _search_fields could be fields in the models, a
        ForeignKey.
        """
        if not hasattr(self, '_search_fields'):
            return None

        values = []
        for field in getattr(self, '_search_fields'):
            value = self.get_field_value(field)
            values.append(value)

        search_content = ' '.join(list(set(filter(None, values))))

        return search_content.replace('None', '').strip()

    @classmethod
    def bulk_populate_document(cls):
        table_name = "{}_{}".format(
            cls._meta.app_label, cls.__name__.lower())
        document_field_name = getattr(
            cls, "_ts_document_field", "ts_document")
        query = (
            "update {table_name} set {document}=%s where id=%s".format(
                table_name=table_name, document=document_field_name))
        params = (
            (each.get_search_content(), each.pk)
            for each in cls.objects.only("id"))
        with connection.cursor() as cursor:
            LOGGER.info(
                "Bulk updating document field for all records in {}.".format(
                    cls.__name__))
            cursor.executemany(query, params)

    def save(self, *args, **kwargs):
        document_field_name = getattr(
            self, "_ts_document_field", "ts_document")
        setattr(self, document_field_name, self.get_search_content())
        super(SearchModelMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True
