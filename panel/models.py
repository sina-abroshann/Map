import uuid
import os
from django.db import models
from django_jalali.db import models as jmodels
from datetime import datetime

def files_upload_location(instance, filename):
    filebase, extension = filename.split('.')
    filebase = uuid.uuid4().urn
    return 'Storage/Files/{filebase}.{ext}'.format(filebase=filebase, ext=extension)

def shp_upload_location(instance, filename):
    filebase, extension = filename.split('.')
    filebase = uuid.uuid4().urn
    return 'Storage/Shp/{filebase}.{ext}'.format(filebase=filebase, ext=extension)

class Submit_Information_Model(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_employer = models.CharField(max_length=500, null=True, blank=True)
    project_manager = models.CharField(max_length=500, null=True, blank=True)
    date_letter = models.DateField(default=datetime.now, null=True, blank=True)
    letter_number = models.CharField(max_length=500, null=True, blank=True)
    recipiant = models.CharField(max_length=500, null=True, blank=True)
    coordinator = models.CharField(max_length=500, null=True, blank=True)
    description_letter = models.CharField(max_length=500, null=True, blank=True)
    phone = models.CharField(max_length=500, null=True, blank=True)
    state = models.CharField(max_length=500, null=True, blank=True)
    date_deposit = models.DateField(default=datetime.now, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    amount_deposit = models.IntegerField(null=True, blank=True)
    tracking_code = models.CharField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=500, null=True, blank=True)
    shp_file = models.FileField(upload_to=shp_upload_location, null=True, blank=True)
    doc_file = models.FileField(upload_to=files_upload_location, null=True, blank=True)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Submit_Information'

    def __str__(self):
        template = '{0.project_id} {0.project_employer} {0.project_manager}'
        return template.format(self)
