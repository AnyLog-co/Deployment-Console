from django.urls import path
import anylog_deploy.views as views
views_options = views.DeploymentConsole()

urlpatterns = [
    path('', views_options.front_page, name='example')
]
