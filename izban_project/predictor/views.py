from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import get_density_prediction

@csrf_exempt
def predict_density_api(request):
    if request.method != 'POST':
        return JsonResponse({
            'status': 'error',
            'message': 'Only POST requests are supported.'
        }, status=405)
    
    try:
        data = json.loads(request.body)

        required_fields = ['time_of_day', 'day_of_week', 'weekend', 'heat', 'rains_mm', 'station']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return JsonResponse({
            'status': 'error',
            'message': 'Missing parameter sent: {", ".join(missing_fields)}'
        }, status=400)

        prediction = get_density_prediction(
            time_of_day=data["time_of_day"],
            day_of_week=data["day_of_week"],
            weekend=data["weekend"],
            heat=data["heat"],
            rains_mm=data["rains_mm"],
            station=data["station"]
        )

        return JsonResponse({
            'status': 'success',
            'inputs': data,
            'prediction': prediction
        }, status=200)

    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'The data sent is not in a valid JSON format.'
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'A server error occurred: {str(e)}'
        }, status=500)
    
def index_view(request):
    return render(request, 'predictor/index.html')