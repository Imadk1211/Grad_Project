from django.contrib import admin
from .models import Secretary, Student, staff, Advisor, UploadedFile, Chairman, Vicechairman, secnotification, stdnotification, staffnotification

admin.site.register(Secretary)
admin.site.register(staff)
admin.site.register(Student)
admin.site.register(Advisor)
admin.site.register(UploadedFile)
admin.site.register(Chairman)
admin.site.register(Vicechairman)
admin.site.register(secnotification)
admin.site.register(stdnotification)
admin.site.register(staffnotification)