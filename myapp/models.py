from django.utils import timezone
from django.db import models

# Create your models here.
class Crop(models.Model):
    cropId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    createdAt = models.DateTimeField(default=timezone.now)

class Farm(models.Model):
    farmId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    ownerName = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phoneNumber = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    createdAt = models.DateTimeField(default=timezone.now)
    
class Plot(models.Model):
    plotId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()
    locationDescription = models.CharField(max_length=100)
    createdAt = models.DateTimeField(default=timezone.now)
    farmFarmId = models.ForeignKey(Farm, on_delete=models.CASCADE)
    cropCropId = models.ForeignKey(Crop, on_delete=models.CASCADE)

class Incident(models.Model):
    incidentId = models.AutoField(primary_key=True)
    incidentType = models.CharField(max_length=100)
    incidentDescription = models.CharField(max_length=100)
    responseAction = models.CharField(max_length=100)
    createdAt = models.DateTimeField(default=timezone.now)
    plotPlotId = models.ForeignKey(Plot, on_delete=models.CASCADE)

class Action(models.Model):
    actionId = models.AutoField(primary_key=True)
    actionType = models.CharField(max_length=100)
    actionDescription = models.CharField(max_length=100)
    createdAt = models.DateTimeField(default=timezone.now)
    incidentIncidentId = models.ForeignKey(Incident, on_delete=models.CASCADE)
    plotPlotId = models.ForeignKey(Plot, on_delete=models.CASCADE)
    
class PlanningCrop(models.Model):
    planningCropId = models.AutoField(primary_key=True)
    plantingDate = models.DateTimeField()
    harvestDate = models.DateTimeField()
    cropYield = models.DateTimeField()
    createdAt = models.DateTimeField(default=timezone.now)
    cropCropId = models.ForeignKey(Crop, on_delete=models.CASCADE)
    
class EnvironmentalMonitoring(models.Model):
    environmentalId = models.AutoField(primary_key=True)
    humidity = models.FloatField()
    soilNutrient = models.FloatField()
    sunIntensity = models.FloatField()
    temperature = models.FloatField()
    airHumidity = models.FloatField()
    createdAt = models.DateTimeField(default=timezone.now)
    plotPlotId = models.ForeignKey(Plot, on_delete=models.CASCADE)
    
    