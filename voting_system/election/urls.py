from django.urls import path
from .views import login_view, dashboard, add_candidate

urlpatterns = [
    path('', login_view, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('add_candidate/', add_candidate, name='add_candidate'),
]
