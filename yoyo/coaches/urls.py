from django.urls import path
from .views import SearchView, CoachDetail

urlpatterns = [
    path('search/', SearchView.as_view(), name='search'),
    path('id<int:pk>', CoachDetail.as_view(), name='detail'),
]
