from django.db import models

# Create your models here.
class op_course(models.Model):
    name=models.CharField(max_length=100)
    code=models.CharField(max_length=100)
    subject_ids=models.ManyToManyField('op_subject')
    class Meta:
        db_table='op_course'

class op_subject(models.Model):
    name=models.CharField(max_length=100)
    code=models.CharField(max_length=100)
    class Meta:
        db_table='op_subject'