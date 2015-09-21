from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'/new_repo/', views.new_repo, name='new_repo'),
        url(r'.*', views.index, name='index'),
        ]

