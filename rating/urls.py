from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReviewCreateApiView.as_view()),  # api/v1/reviews/ POST
    path('<int:pk>/', views.ReviewUpdateDeleteApiView.as_view()),
]
