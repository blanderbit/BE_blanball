from django.db.models import Value, TextField, FloatField
from django.db.models.functions import Concat
from django.contrib.postgres.search import TrigramSimilarity
from rest_framework import filters
from django.db.models.query import QuerySet
import itertools

class SearchFilter(filters.SearchFilter):

    def get_search_terms(self, request):
        params:str = ' '.join(request.query_params.getlist(self.search_param))
        return params.replace(',', ' ').split()

class RankedFuzzySearchFilter(SearchFilter):

    @staticmethod
    def search_queryset(queryset, search_fields:tuple, search_terms, min_rank) -> QuerySet:
        full_text_vector:tuple = sum(itertools.zip_longest(search_fields, (), fillvalue=Value(' ')), ())
        if len(search_fields) > 1:
            full_text_vector = full_text_vector[:-1]

        full_text_expr:Concat = Concat(*full_text_vector, output_field=TextField())

        similarity:TrigramSimilarity = TrigramSimilarity(full_text_expr, search_terms)
        queryset:QuerySet = queryset.annotate(rank=similarity)

        if min_rank is None:
            queryset = queryset.filter(rank__gt=0.0)
        elif min_rank > 0.0:
            queryset = queryset.filter(rank__gte=min_rank)

        return queryset[:5]

    def filter_queryset(self, request, queryset, view) -> QuerySet:
        search_fields:tuple = getattr(view, 'search_fields', None)
        search_terms = ' '.join(self.get_search_terms(request))

        if search_fields and search_terms:
            min_rank = getattr(view, 'min_rank', None)

            queryset:QuerySet = self.search_queryset(queryset, search_fields, search_terms, min_rank)
        else:
            queryset:QuerySet = queryset.annotate(rank=Value(1.0, output_field=FloatField()))

        return queryset[:5]