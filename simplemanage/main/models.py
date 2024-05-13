from django.db import models;
from django.contrib.auth.models import User;
from django.core.exceptions import ValidationError;
from django.utils.translation import gettext_lazy as _;
# Create your models here.


def validate_positive(value):
	if value < 0:
		raise ValidationError(
			_("%(value)  ddeve ser positivo"),
			params = {"value":value}
			)

class Cliente(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length = 200)
	description = models.CharField(max_length = 200, null=True)
	value = models.FloatField(validators=[validate_positive]);

	def __str__(self):
		return self.name


class Funcionario(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length = 200)
	description = models.CharField(max_length = 200, null = True)
	value = models.FloatField()
 
	def __str__(self):
		return self.name
