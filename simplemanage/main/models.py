from django.db import models;
from django.contrib.auth.models import User;
# Create your models here.

class Cliente(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length = 200)
	description = models.CharField(max_length = 200)
	value = models.FloatField();

	def __str__(self):
		return self.name