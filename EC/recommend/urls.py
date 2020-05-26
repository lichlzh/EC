from django.conf.urls import url
from . import views
urlpatterns = [
    url('recommend',views.recommend),
    url('submit',views.submit),
]
