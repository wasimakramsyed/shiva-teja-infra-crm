from bookings.models import BookingActivity

class ActivityService:

    @staticmethod
    def log(
        booking,
        activity,
        description="",
        user=None
    ):

        BookingActivity.objects.create(
            booking=booking,
            activity=activity,
            description=description,
            created_by=user
        )