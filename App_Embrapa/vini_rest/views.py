from django.shortcuts import render
from django.http import JsonResponse
from vini_rest.models import plotData
from .dash_app import app
import json

# Create your views here.

def import_json(request):

    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        description = data.get('description')
        url = data.get('url')
        json_data = data.get('json_data')

        plot_data = plotData.objects.create(
                title = title,
                description = description,
                url = url,
                json_data = json_data,
            )
        
        return JsonResponse({'status': 'success', 'id': plot_data.id})
    
    else:
        return JsonResponse({'status': 'error',
                             'message': 'Only POST requests are allowed'})
    
def dashboard_view(request):
    return render(request, 'dashboard.html', {'dash_app': app})
