
# urls.py
from django.urls import path
from .views import DownloadVideoView, DeleteVideoView,HomePageView

urlpatterns = [
    path('download/', DownloadVideoView.as_view(), name='download_video'),
    path('delete/', DeleteVideoView.as_view(), name='delete_video'),
        path('', HomePageView.as_view(), name='home'),

]



