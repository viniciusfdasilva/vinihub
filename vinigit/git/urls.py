"""vinigit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from git import views

urlpatterns = [
    path(''                      , views.LoginView.as_view()   , name='main'  ),
    path('painel'                , views.PainelView.as_view()  , name='painel'),
    path('repo/<str:repository>/', views.get_repo              , name='repo'  ),
    path('logout'                , views.LogoutView.as_view()  , name='logout'),
    path('release/<str:repository>/', views.ReleaseView.as_view(), name='release'),
    path('graph/<str:repository>/', views.GitGraphView.as_view(), name='graph'),
    path('release/<str:repository>/<int:id_release>/', views.ReleaseDetailView.as_view(), name='release_detail'),
    path('pull-request/<str:repository>/<int:id_pullrequest>/', views.PullRequestDetailView.as_view(), name='pullrequest_detail'),
    path('pull-request/<str:repository>/<int:id_pullrequest>/merge/', views.PullRequestMergeView.as_view(), name='pullrequest_detail'),
    path('pull-request/<str:repository>/', views.PullRequestView.as_view(), name='pull_request')
]
