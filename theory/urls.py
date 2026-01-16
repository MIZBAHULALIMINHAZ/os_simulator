from django.urls import path
from .views import FCFSAPI, SJFAPI, SRTFAPI, AlgorithmTheoryAPIView,  PriorityPreemptiveAPI, RoundRobinAPI

urlpatterns = [
    path('fcfs/simulate/', FCFSAPI.as_view(), name='fcfs-simulate'),
    path('sjf/simulate/', SJFAPI.as_view(), name='sjf-simulate'),
    path('srtf/simulate/', SRTFAPI.as_view(), name='srtf-simulate'),
    path('roundrobin/simulate/', RoundRobinAPI.as_view(), name='roundrobin-simulate'),
    path('priority/simulate/', PriorityPreemptiveAPI.as_view(), name='priority-preemptive-simulate'),

    path('fcfs/theory/', AlgorithmTheoryAPIView.as_view(), name='fcfs-theory-list'),          # GET all / POST new
    path('fcfs/theory/<str:name>/', AlgorithmTheoryAPIView.as_view(), name='fcfs-theory-detail'),  # GET/PUT/DELETE by name
]
