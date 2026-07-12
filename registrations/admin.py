from django.contrib import admin

from .models import Registration

from .models import RegistrationTimeline


@admin.register(Registration)

class RegistrationAdmin(admin.ModelAdmin):

	list_display = (

		"registration_id",

		"customer",

		"booking",

		"registration_date",

	)


@admin.register(RegistrationTimeline)

class RegistrationTimelineAdmin(admin.ModelAdmin):

	list_display = (

		"registration",

		"activity",

		"created_by",

		"created_at",

	)

	list_filter = (

		"created_at",

	)

	search_fields = (

		"registration__registration_id",

		"activity",

	)