from projectlyte import appointment
from django.db import models

# Create your models here.
class Appointment(models.Model):
    appointment_date = models.DateField(blank=True, null=True)
    info = models.CharField(max_length=255)

    class Meta:
        db_table = 'appointment'
    
    def __str__(self):
        return self.appointment_date
