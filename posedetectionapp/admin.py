from django.contrib import admin

# Register your models here.
from posedetectionapp.models import Pose


@admin.register(Pose)
class PoseAdmin(admin.ModelAdmin):
    pass