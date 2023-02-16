from django.urls import path, include
from django.views.decorators.cache import cache_page
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products', views.ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('likes/', views.LikeCreateView.as_view()),
    path('likes/<int:pk>/', views.LikeDeleteView.as_view()),
]
