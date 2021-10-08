from django.forms import ModelForm

from posedetectionapp.models import Pose


class PoseCreationForm(ModelForm):
    class Meta:
        model = Pose
        fields = ['image']