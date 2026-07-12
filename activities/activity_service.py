from activities.models import Activity


class ActivityService:

	@staticmethod
	def create_activity(

		customer,

		booking=None,

		payment=None,

		commission=None,

		registration=None,

		employee=None,

		activity_type="",

		title="",

		description="",

		created_by=None,

		icon="",

		color="",

		is_system_generated=True,

	):

		activity = Activity.objects.create(

			customer=customer,

			booking=booking,

			payment=payment,

			commission=commission,

			registration=registration,

			employee=employee,

			activity_type=activity_type,

			title=title,

			description=description,

			created_by=created_by,

			icon=icon,

			color=color,

			is_system_generated=is_system_generated,

		)

		return activity
