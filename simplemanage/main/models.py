from django.db import models;
from django.contrib.auth.models import User;
from django.core.exceptions import ValidationError;
from django.utils.translation import gettext_lazy as _;
from django.utils import timezone
# Create your models here.


def validate_positive(value):
			if value < 0:
				raise ValidationError(
				_("O campo conta deve ser positivo"),
				params = {"value":value}
				)


class Cliente(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length = 200)
	description = models.CharField(max_length = 200, blank=True)
	value = models.FloatField(validators=[validate_positive]);

	def __str__(self):
		return self.name


class Funcionario(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length = 200)
	description = models.CharField(max_length = 200, blank=True)
	value = models.FloatField()

	def __str__(self):
		return self.name


class RegistroFinanceiro(models.Model):
	category_list = [
		("cliente", "cliente"),
		("custo", "custo"),
		("funcionario", "funcionario"),
	]
	user    = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length = 200)
	description = models.CharField(max_length = 200, blank=True)
	value = models.FloatField(validators= [validate_positive])
	category = models.CharField(max_length = 200, choices = category_list)
	state = models.BooleanField(default=True)
	created_at = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.name


class Cardapio(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length = 200)
	description = models.CharField(max_length = 200, blank=True)
	state = models.BooleanField(default=False)

	def __str__(self):
		return self.name
