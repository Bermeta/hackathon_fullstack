from django.urls import path, include
from django.views.decorators.cache import cache_page
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('likes/', views.LikeCreateView.as_view()),
    path('likes/<int:pk>/', views.LikeDeleteView.as_view()),
    path('list/products/', cache_page(60)(views.ProductListAPIView.as_view()))
]
