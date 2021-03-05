import operator

import django_filters

from functools import reduce

from django.conf import settings
from django.db.models import DecimalField
from django.db.models.expressions import Value

DEFAULT_SEARCH_RESULT_SIZE = 2500


class SearchFilter(django_filters.Filter):
    def strip_tsquery_syntax(self, query_terms):
        """
        Remove tsquery syntax from search query.
        """
        syntax = ['(', ')', '&', '|', ':', '*']
        for x in syntax:
            query_terms = query_terms.replace(x, ' ')

        # The string.replace above adds extra spaces which need to be
        # cleaned out and normalized. I'm not adding a delimiter here,
        # because performing a split with the ' ' delimiter adds an
        # empty string there.
        return ' '.join(query_terms.split())

    def strip_stop_words(self, query_terms):
        """
        Remove stop words from the search query.
        :param query_terms: The list of search words supplied by the user
        :type query_terms: list
        :return: A list of the words that are not stop words
        :rtype: list
        Postgresql handles stop words for us both during indexing and
        searchin'. All that one needs to do is to update the stop words
        file usually located in
        /usr/share/postgresql/<version>/tsearch_data/english.stop
        and refresh the search index using the command below:
        $ ./manage.py search_setup
        """
        return query_terms

    def apply_synonyms(self, query_terms):
        """
        Expand the words in the search query with their synonyms.
        :param query_terms: The list of search words supplied by the user
        :type query_terms: list
        :return: A list of the words supplied by the user plus their synonyms
        :rtype: list
        Postgresql handles stop words for us both during indexing and
        searching.
        The synonyms file is located in
        /usr/share/postgresql/<version>/tsearch_data/synonym_sample.syn
        Just like the stop-words refresh the search index using the command
        $ ./manage.py search_setup after updating the synonyms file.
        """
        return query_terms

    def prefix_match_search_terms(self, query_terms):
        """
        Set look_up order of the words in the query.
        :param query_terms: The list of search words supplied by the user
        :type query_terms: list
        :return: A list of the words supplied by the user plus their synonyms
        :rtype: list
        By default there is no lookup order specified for checking
        whether a word is a valid match. So as long the search_term is
        contained in a search document then it is picked as a valid match.
        By doing prefix matching matching, Postgresql ensures the specified
        prefix is the prefix of a valid match.
        Doing this enables us to achieve progressive search
        """
        query_terms = [value + ":*" for value in query_terms if value]
        return query_terms

    def set_search_mode(self, query_terms, search_mode):
        """
        Specify how the search words should appear in a matching document.
        param query_terms: The list of search words supplied by the user
        :type query_terms: list
        :return: A str with search mode set in the words
        :rtype: str
        One could specify or as | or and as & or even as set a specific
        distance between them.
        """
        query_terms = " {} ".format(search_mode).join(query_terms)
        return query_terms

    def correct(self, qs, search_term):
        """
        Correct the typos in the search words.
        param qs: Model queryset that could already have other filters applied
        :type qs: Django queryset
        :return: Model Queryset
        :rtype: Django Queryset
        This is the fall back option if the user supplied search term did
        not have an exact/close hit from ts_vector.
        The rank is different from the rank supplied by ts_vector but
        for transparency to the serializer, it is returned just as rank.
        """
        query_terms = self.strip_tsquery_syntax(search_term)
        query_terms = self.tokenize_search_terms(query_terms)
        query_terms = self.strip_stop_words(query_terms)
        search_term = " ".join(query_terms)
        document_field = getattr(
            qs.model, "_ts_document_field", "ts_document")
        sql = """
            WITH similar_records AS (
                SELECT id, {document}, similarity({document}, %s) AS rank
                FROM {table}
            )
            SELECT id, rank FROM similar_records
            WHERE similarity({document}, %s) > 0.15
            ORDER BY rank DESC
            LIMIT 10;
        """.format(table=self.table, document=document_field)
        sql_params = [search_term, search_term]
        return self.get_search_results(qs, sql, sql_params)

    def tokenize_search_terms(self, search_term):
        """
        Break down the search term into a list of tokens.
        :param query_terms: The list of search words supplied by the user
        :type query_terms: list
        :return: A list of the words that can feed into into the pipeline
        :rtype: list
        """
        query_terms = search_term.split(' ')
        return query_terms

    def get_search_results(self, qs, sql, sql_params):
        results = qs.model.objects.raw(sql, sql_params)

        obj_ranks = {obj.id: obj.rank for obj in results}
        return_objs = []
        # inject rank
        for obj_id, obj_rank in obj_ranks.items():
            return_objs.append(qs.filter(id=obj_id).annotate(
                rank=Value(obj_rank, DecimalField())))
        if len(return_objs) > 0:
            qs = reduce(operator.or_, return_objs)
        else:
            qs = qs.model.objects.none()
        return qs

    def perform_search(self, qs, search_term, search_mode):
        """
        Perform the search.
        First try to do an actual match if no document is found try and correct
        the search_term
        Note the use of Q to return a normal queryset instead of __in filter.
        Q is 1.5  times faster than doing an __in filter.
        """
        # Start the search preprocessing phase. Order here is very important

        query_terms = self.strip_tsquery_syntax(search_term)
        query_terms = self.tokenize_search_terms(query_terms)
        query_terms = self.strip_stop_words(query_terms)
        query_terms = self.apply_synonyms(query_terms)
        query_terms = self.prefix_match_search_terms(query_terms)
        query = self.set_search_mode(query_terms, search_mode)
        # End the preprocessing phase
        document_vector_field = getattr(
            qs.model, "_ts_document_vector_field", "ts_document_vector")

        sql = """
          WITH tsq AS (SELECT to_tsquery(%s) AS query)
            SELECT id, rank
            FROM (
                SELECT id, ts_rank({document_vector}, query) as rank
                FROM {table}, tsq
                WHERE {document_vector} @@ query = true
            ) matches
            ORDER BY rank DESC
            LIMIT {limit};
        """.format(
            table=self.table, limit=self.search_result_size,
            document_vector=document_vector_field)
        sql_params = [query]
        return self.get_search_results(qs, sql, sql_params)

    def filter(self, qs, search_term):
        if not search_term:
            return qs

        self.search_result_size = getattr(
            qs.model, '_search_result_size', getattr(
                settings, 'MAX_SEARCH_RESULT_SIZE',
                DEFAULT_SEARCH_RESULT_SIZE))

        self.table = "{}_{}".format(
            qs.model._meta.app_label, qs.model.__name__.lower())

        exact_hits = self.perform_search(qs, search_term, '&')
        if exact_hits:  # noqa
            return exact_hits

        close_hits = self.perform_search(qs, search_term, '|')
        if close_hits:  # noqa
            return close_hits

        return self.correct(qs, search_term)
