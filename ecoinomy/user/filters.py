import re
from django_filters import rest_framework as filters
from django.db.models import Q
from user.models import User


class UserFilter(filters.FilterSet):
    search_q = filters.CharFilter(method='search_q_filter', label='Search Q')
    country = filters.CharFilter(field_name='profile__country_of_residence', lookup_expr="icontains")

    class Meta:
        model = User
        fields = ['is_staff', 'search_q', 'country', 
                  'is_active', 'is_superuser', 'profile__gender']

    @staticmethod
    def search_q_filter(queryset, name, value):
        clean_value = re.sub(r'\s+', ' ', value)
        clean_value = clean_value.strip()
        if re.match(r"[+]?\d{4,}", clean_value):
            return queryset.filter(
                profile__phone_number__icontains=clean_value
                )
        else:
            return queryset.filter(
                Q(profile__first_name__icontains=clean_value) |
                Q(profile__last_name__icontains=clean_value) |
                Q(email__icontains=clean_value) |
                Q(username__icontains=clean_value)
                )