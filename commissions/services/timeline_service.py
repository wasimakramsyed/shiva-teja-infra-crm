from commissions.models import CommissionTimeline


class CommissionTimelineService:

    @staticmethod
    def create(
        commission,
        activity,
        created_by,
        remarks=""
    ):

        return CommissionTimeline.objects.create(
            commission=commission,
            activity=activity,
            remarks=remarks,
            created_by=created_by,
        )