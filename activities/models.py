from django.conf import settings
from django.db import models

from bookings.models import Booking
from commissions.models import CommissionRecord
from customers.models import Customer
from employees.models import Employee
from payments.models import Payment
from registrations.models import Registration


class Activity(models.Model):

	customer = models.ForeignKey(
		Customer,
		on_delete=models.CASCADE,
		related_name="crm_activities",
	)

	booking = models.ForeignKey(
		Booking,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name="crm_activities",
	)

	payment = models.ForeignKey(
		Payment,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name="crm_activities",
	)

	commission = models.ForeignKey(
		CommissionRecord,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name="crm_activities",
	)

	registration = models.ForeignKey(
		Registration,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name="crm_activities",
	)

	employee = models.ForeignKey(
		Employee,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name="crm_activities",
	)

	activity_type = models.CharField(
		max_length=100,
		db_index=True,
	)

	title = models.CharField(
		max_length=200,
	)

	description = models.TextField(
		blank=True,
		null=True,
	)

	created_by = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name="created_crm_activities",
	)

	created_at = models.DateTimeField(
		auto_now_add=True,
		db_index=True,
	)

	icon = models.CharField(
		max_length=50,
		blank=True,
		null=True,
	)

	color = models.CharField(
		max_length=30,
		blank=True,
		null=True,
	)

	is_system_generated = models.BooleanField(
		default=False,
	)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return f"{self.customer.customer_name} - {self.title}"
