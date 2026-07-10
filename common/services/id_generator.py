from django.db import transaction
from django.db.models import Max
from datetime import datetime

year = datetime.now().year
class IDGenerator:
    """
    Generates sequential IDs like:

    BOOK000001
    PAY000001
    EMP000001
    """

    @staticmethod
    @transaction.atomic
    def generate(model, field, prefix):

        # Lock the table while generating the next ID
        last = (
            model.objects
            .select_for_update()
            .aggregate(last_id=Max("id"))
        )

        if last["last_id"]:

            obj = model.objects.get(id=last["last_id"])

            last_value = getattr(obj, field)

            number = int(
                last_value.replace(prefix, "")
            ) + 1

        else:

            number = 1

        return f"{prefix}{number:06d}"