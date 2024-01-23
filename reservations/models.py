from django.db import models
from django.contrib.auth.models import User

# Create your models here.


time = {
    '18:00': '18:00',
    '19:00': '19:00',
    '20:00': '20:00',
    '21:00': '21:00',
    '22:00': '22:00',
    '23:00': '23:00',
}


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)  # Adicione o campo para o número de telefone
    table = models.IntegerField()
    date = models.DateField()
    time = models.CharField(max_length=5, choices=time, default='18:00')
    number_of_people = models.IntegerField()
    message = models.TextField()

    def __str__(self):
        return f"Reservation for {self.user.username} on {self.date} at {self.time}"