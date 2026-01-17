from django.urls import path
from .views import FCFSAPI, SJFAPI, SRTFAPI, AlgorithmTheoryAPIView, BankerAPI, BestFitAPI, FIFOPageAPI, FirstFitAPI, LRUPageAPI, OPTPageAPI, PriorityAPI,RoundRobinAPI

urlpatterns = [
    path('fcfs/simulate/', FCFSAPI.as_view(), name='fcfs-simulate'),
    path('sjf/simulate/', SJFAPI.as_view(), name='sjf-simulate'),
    path('srtf/simulate/', SRTFAPI.as_view(), name='srtf-simulate'),
    path('roundrobin/simulate/', RoundRobinAPI.as_view(), name='roundrobin-simulate'),
    path('priority/simulate/', PriorityAPI.as_view(), name='priority-simulate'),

    # Banker’s Algorithm
    path('banker/simulate/', BankerAPI.as_view(), name='banker-simulate'),

    # Memory Allocation
    path('firstfit/simulate/', FirstFitAPI.as_view(), name='firstfit-simulate'),
    path('bestfit/simulate/', BestFitAPI.as_view(), name='bestfit-simulate'),

    # Page Replacement
    path('fifo/simulate/', FIFOPageAPI.as_view(), name='fifo-simulate'),
    path('lru/simulate/', LRUPageAPI.as_view(), name='lru-simulate'),
    path('optimal/simulate/', OPTPageAPI.as_view(), name='optimal-simulate'),
    # Algorithm Theory
    
    path('fcfs/theory/', AlgorithmTheoryAPIView.as_view(), name='fcfs-theory-list'),          # GET all / POST new
    path('fcfs/theory/<str:name>/', AlgorithmTheoryAPIView.as_view(), name='fcfs-theory-detail'),  # GET/PUT/DELETE by name
]
