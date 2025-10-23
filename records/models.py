from django.db import models
from django.contrib.auth.models import User
import qrcode
from io import BytesIO
from django.core.files import File

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    medical_condition = models.TextField()
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)

    def save(self, *args, **kwargs):
        qr = qrcode.make(f"http://127.0.0.1:8000/patient/{self.id}")
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        self.qr_code.save(f"qr_{self.user.username}.png", File(buffer), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class Report(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    report_name = models.CharField(max_length=100)
    report_file = models.FileField(upload_to='reports/')
    uploaded_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.report_name} ({self.patient.user.username})"
