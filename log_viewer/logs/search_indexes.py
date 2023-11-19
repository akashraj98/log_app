# yourapp/search_indexes.py

from haystack import indexes
from .models import LogData

class LogDataIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    level = indexes.CharField(model_attr='level')
    message = indexes.CharField(model_attr='message')
    resourceId = indexes.CharField(model_attr='resourceId')
    timestamp = indexes.DateTimeField(model_attr='timestamp')
    traceId = indexes.CharField(model_attr='traceId')
    spanId = indexes.CharField(model_attr='spanId')
    commit = indexes.CharField(model_attr='commit')
    parentResourceId = indexes.CharField(model_attr='parentResourceId')

    def get_model(self):
        return LogData
