from registrations.models import RegistrationTimeline


class RegistrationTimelineService:

    @staticmethod
    def create(

        registration,

        activity,

        created_by=None,

        remarks="",

    ):

        return RegistrationTimeline.objects.create(

            registration=registration,

            activity=activity,

            created_by=created_by,

            remarks=remarks,

        )
