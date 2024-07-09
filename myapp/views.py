from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import datetime
import google.generativeai as gai
import tensorflow as tf
import numpy as np
from PIL import Image
import io

#Create your views here.

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json
import simplejson 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from myapp.models import EnvironmentalMonitoring, Incident
from myapp.serializers import EnvironmentalMonitoringSerializer, IncidentSerializer

@csrf_exempt
def my_endpoint(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Access the individual values from the JSON data
            humidity = data.get('humidity')
            temp = data.get('temp') 
            light = data.get('light')
            
            # Do something with the data, such as saving it to the database
            
            # Prepare the response JSON
            response_data = {
                'humidity': humidity,
                'temp': temp,
                'light': light
            }
            
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
    
def getData(request):
    return render(request, 'myapp/index.html')

@api_view(['POST'])
def create_environment_monitoring(request):
    if request.method == 'POST':
        data = request.data

        required_fields = ['humidity', 'soilNutrient', 'sunIntensity', 'temperature', 'airHumidity', 'plotPlotId']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return Response({'error': f'The following fields are missing: {", ".join(missing_fields)}'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create a new EnvironmentalMonitoring instance
            environmental_monitoring = EnvironmentalMonitoring(
                humidity=data['humidity'],
                soilNutrient=data['soilNutrient'],
                sunIntensity=data['sunIntensity'],
                temperature=data['temperature'],
                airHumidity=data['airHumidity'],
                plotPlotId_id=data['plotPlotId'],
                createdAt=timezone.now()  # Assuming you want to set the createdAt field to the current time
            )
            environmental_monitoring.save()

            # Serialize the created EnvironmentalMonitoring object
            serializer = EnvironmentalMonitoringSerializer(environmental_monitoring)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else : 
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@api_view(['GET'])
def last_environmental_monitoring(request):
    try:
        last_entry = EnvironmentalMonitoring.objects.latest('createdAt')
        serializer = EnvironmentalMonitoringSerializer(last_entry)
        json_data = simplejson.dumps(serializer.data)
        print (json_data)

        return Response(json_data, status=status.HTTP_200_OK, content_type='application/json')
        
    except EnvironmentalMonitoring.DoesNotExist:
        return HttpResponse("No entries found in the database.")
    
@api_view(['GET'])
def get_environmental_monitoring(request):
    data = request.data

    if 'startTime' not in data or 'endTime' not in data:
        return Response({'error': 'Both startTime and endTime fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        start_time = datetime.fromisoformat(data['startTime'])
        end_time = datetime.fromisoformat(data['endTime'])

        environmental_monitoring_queryset = EnvironmentalMonitoring.objects.filter(
            createdAt__gte=start_time,
            createdAt__lte=end_time
        )
        
        serializer = EnvironmentalMonitoringSerializer(environmental_monitoring_queryset, many=True)
        json_data = simplejson.dumps(serializer.data, separators=(',', ':'))
        print (json_data)

        return Response(json_data, status=status.HTTP_200_OK, content_type='application/json')
    except ValueError:
        return Response({'error': 'Invalid datetime format. Please use ISO 8601 format (e.g., 2023-07-06T12:00:00).'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])    
def get_incident(request):
    try: 
        alerts = Incident.objects.all()
        serializer = IncidentSerializer(alerts, many=True)
        json_data = json.dumps(serializer.data)
        return Response(json_data, status=status.HTTP_200_OK, content_type='application/json')
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])    
def discussion(request):
    gai.configure(api_key='AIzaSyCPj-lEv9ZEXrcnKqk3663SUjED2ORRN1Q')

    # for m  in gai.list_models():
    #     if 'generateContent' in m.supported_generation_methods:
    #         print (m.name)
    data =  request.data
    question = data['question']
    words = question.split()
    for word in words:
        if(word.lower() == 'salut'):
            return "Bonjour sur l'application Wi Grow"
        else: 
            model = gai.GenerativeModel('gemini-1.0-pro-latest')
            response = model.generate_content(question)
            return Response({'answer': response.text})



def preprocess_image(image):
    # Charger le modèle TensorFlow
    model = tf.keras.models.load_model('detectionfr.keras')

    # Dictionnaire de mappage des indices de prédiction aux étiquettes
    label_map = {0: 'brulure des feuilles', 1: 'Feuilles saines', 2: 'rouille des feuilles', 3: 'Tache foliaire'}


    # Redimensionner selon les besoins de votre modèle (ici 224x224)
    img = image.resize((32, 32))
    # Convertir l'image en tableau numpy et normaliser les pixels
    img = np.array(img) / 255.0
    # Ajouter une dimension pour correspondre à la forme attendue par le modèle
    img = np.expand_dims(img, axis=0)
    return img


@csrf_exempt
def predict_image(request):
    # Charger le modèle TensorFlow
    model = tf.keras.models.load_model('detectionfr.keras')

    # Dictionnaire de mappage des indices de prédiction aux étiquettes
    label_map = {0: 'brulure des feuilles', 1: 'Feuilles saines', 2: 'rouille des feuilles', 3: 'Tache foliaire'}


    if request.method == 'POST':
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file part'}, status=400)

        file = request.FILES['file']

        if not file.name:
            return JsonResponse({'error': 'No selected file'}, status=400)

        try:
            img = Image.open(io.BytesIO(file.read()))
            img = preprocess_image(img)

            # Faire la prédiction
            predictions = model.predict(img)
            predicted_index = np.argmax(predictions, axis=1)[0]
            predicted_label = label_map[predicted_index]

            # Retourner la prédiction sous forme de texte
            return JsonResponse({'prediction': predicted_label})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
