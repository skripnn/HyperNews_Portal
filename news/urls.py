from django.urls import path
from .views import *

urlpatterns = [
    path('<int:link>/', OneNews.as_view()),
    path('', AllNews.as_view())
]