from django.contrib import admin

from .models import (
    CommissionRequest,
    CommissionRecord,
    CommissionAllocation,
    CommissionTimeline,
)

admin.site.register(CommissionRequest)
admin.site.register(CommissionRecord)
admin.site.register(CommissionAllocation)
admin.site.register(CommissionTimeline)