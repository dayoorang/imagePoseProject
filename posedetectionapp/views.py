from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView, DetailView

from posedetectionapp.forms import PoseCreationForm
from posedetectionapp.models import Pose


class PoseCreationView(CreateView):
    model = Pose
    form_class = PoseCreationForm
    template_name = 'posedetectionapp/pose.html'

    def get_success_url(self):
        return reverse('posedetectionapp:result', kwargs={'pk':self.object.pk})

class PoseDetailView(DetailView):
    model = Pose
    context_object_name = 'target_pose'
    template_name = 'posedetectionapp/result.html'
