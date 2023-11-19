from django.shortcuts import render
from django.views import View
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .utils.log_producer import ProducerLogCreated


from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage
import logging
from logs.models import LogData
# Create your views here.
logger = logging.getLogger(__name__)
producerLogCreated=ProducerLogCreated()

class LogsView(View):
    def get(self, request):
        logs = LogData.objects.all().order_by('-timestamp')
        return render(request, 'index.html', {'logs': logs})
    
class LogSearchApiView(View):
    def get(self, request):
        # Get query parameters
        search_query = request.GET.get('q', '')
        level_filter = request.GET.get('level', '')
        message_filter = request.GET.get('message', '')
        resourceId_filter = request.GET.get('resourceId', '')
        timestamp_filter = request.GET.get('timestamp', '')
        traceId_filter = request.GET.get('traceId', '')
        spanId_filter = request.GET.get('spanId', '')
        commit_filter = request.GET.get('commit', '')
        parentResourceId_filter = request.GET.get('parentResourceId', '')
        ordering = request.GET.get('ordering', '-timestamp')  # Default ordering by timestamp
        start_timestamp_filter = request.GET.get('start_timestamp', '')
        end_timestamp_filter = request.GET.get('end_timestamp', '')
        # Convert timestamp strings to datetime objects if provided
        start_datetime = datetime.strptime(start_timestamp_filter, '%Y-%m-%d %I:%M%p') if start_timestamp_filter else None
        end_datetime = datetime.strptime(end_timestamp_filter, '%Y-%m-%d %I:%M%p') if end_timestamp_filter else None
        print(start_datetime)
        print(end_datetime)

        # Build filter conditions
        filter_conditions = Q()
        if search_query:
            filter_conditions |= Q(message__icontains=search_query) |\
                                Q(resourceId__icontains=search_query) | Q(traceId__icontains=search_query) | \
                                Q(spanId__icontains=search_query) | Q(commit__icontains=search_query) | \
                                Q(parentResourceId__icontains=search_query) |Q(level__icontains=search_query) 

        if level_filter:
            filter_conditions &= Q(level__iexact=level_filter)
        if message_filter:
            filter_conditions &= Q(message__icontains=message_filter)
        if resourceId_filter:
            filter_conditions &= Q(resourceId__icontains=resourceId_filter)
        if timestamp_filter:
            filter_conditions &= Q(timestamp__icontains=timestamp_filter)
        if traceId_filter:
            filter_conditions &= Q(traceId__icontains=traceId_filter)
        if spanId_filter:
            filter_conditions &= Q(spanId__icontains=spanId_filter)
        if commit_filter:
            filter_conditions &= Q(commit__icontains=commit_filter)
        if parentResourceId_filter:
            filter_conditions &= Q(parentResourceId__icontains=parentResourceId_filter)
        if start_datetime:
            filter_conditions &= Q(timestamp__gte=start_datetime)
        if end_datetime:
            filter_conditions &= Q(timestamp__lte=end_datetime)

        # Fetch logs based on filters
        logs = LogData.objects.filter(filter_conditions).order_by(ordering)

        # Paginate results
        page = request.GET.get('page', 1) or 1
        paginator = Paginator(logs, 15)  # Show 15 logs per page
        try:
            current_page = paginator.page(page)
        except EmptyPage:
            return JsonResponse({'error': 'Invalid page number'}, status=400)

        # Serialize logs
        serialized_logs = [{
            'level': log.level,
            'message': log.message,
            'resourceId': log.resourceId,
            'timestamp': log.timestamp,
            'traceId': log.traceId,
            'spanId': log.spanId,
            'commit': log.commit,
            'parentResourceId': log.parentResourceId,
        } for log in current_page]

        return JsonResponse({'logs': serialized_logs, 'total_pages': paginator.num_pages, 'current_page': current_page.number})
    
@method_decorator(csrf_exempt, name='dispatch')
class LogIngestionView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            level = data.get('level', 'info')
            # Process the log entry (you can replace this with your own processing logic)
            self.process_log(level, data)

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    def process_log(self, level, data):
        # Your processing logic for an individual log entry
        producerLogCreated.publish('log_created', data)
        logger.info(f"Processing log entry - Level: {level}, Message: {data}")