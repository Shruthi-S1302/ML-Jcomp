
from django.urls import path
from app.summerizer import summarize
from app.views import index
urlpatterns = [
    path('summarize/', summarize, name='summarize'),
    path('', index, name='index'),
]
