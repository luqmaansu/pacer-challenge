from django.urls import path
from scores import views

urlpatterns = [
    path('api/get_score/', views.ScoreCreateView.as_view(), name='get_score'),

]