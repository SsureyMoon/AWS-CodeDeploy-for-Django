from django.conf.urls import url

urlpatterns = [
    url(r'auth/login/$', 'rest_framework_jwt.views.obtain_jwt_token', name="obtain_jwt"),
]