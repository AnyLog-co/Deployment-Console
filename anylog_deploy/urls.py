from django.urls import path
import anylog_deploy.views as views
views_options = views.Example()

urlpatterns = [
    path('', views_options.front_page, name='example')
]
