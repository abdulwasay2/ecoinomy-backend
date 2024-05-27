from django.db.models import Count
from django.db.models.functions import TruncDay


def get_total_entity_count(model):
    return model.objects.count()


def get_total_entity_count_between_dates(model, date_range):
    return model.objects.filter(created_at__date__range=date_range).count()


def get_per_day_entity_count_between_dates(model, date_range):
    return model.objects.annotate(day=TruncDay('created_at'), total_count=Count('id')).filter(
        created_at__date__range=date_range).order_by('day').values('day', 'total_count')