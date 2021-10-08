from django.urls import path

from posedetectionapp.views import PoseCreationView, PoseDetailView

app_name = 'posedetectionapp'
urlpatterns = [
    path('',PoseCreationView.as_view(),name='pose'),
    path('result/<int:pk>', PoseDetailView.as_view(), name='result')

]

