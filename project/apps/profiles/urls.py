from django.conf.urls import url
from .views import ProfileView, post_profile_photo


urlpatterns = [
    url(r'^$', ProfileView.as_view()),
    url(r'^photo/$', post_profile_photo),
]
