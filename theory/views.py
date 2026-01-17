from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SchedulingSimulationSerializer
from .models import AlgorithmTheory
from .serializers import AlgorithmTheorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SchedulingSimulationSerializer
from .algorithms import (
    fcfs, sjf_non_preemptive, srtf_preemptive, round_robin, priority_preemptive,
    bankers_algorithm, first_fit, best_fit,
    fifo_page_replacement, lru_page_replacement, optimal_page_replacement
)

# ---------------- CPU Scheduling ---------------- #
class FCFSAPI(APIView):
    def post(self, request):
        serializer = SchedulingSimulationSerializer(data=request.data)
        if serializer.is_valid():
            return Response(fcfs(serializer.validated_data["processes"]))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SJFAPI(APIView):
    def post(self, request):
        serializer = SchedulingSimulationSerializer(data=request.data)
        if serializer.is_valid():
            return Response(sjf_non_preemptive(serializer.validated_data["processes"]))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SRTFAPI(APIView):
    def post(self, request):
        serializer = SchedulingSimulationSerializer(data=request.data)
        if serializer.is_valid():
            return Response(srtf_preemptive(serializer.validated_data["processes"]))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoundRobinAPI(APIView):
    def post(self, request):
        serializer = SchedulingSimulationSerializer(data=request.data)
        if serializer.is_valid():
            quantum = serializer.validated_data.get("quantum", 1)
            return Response(round_robin(serializer.validated_data["processes"], quantum))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PriorityAPI(APIView):
    def post(self, request):
        serializer = SchedulingSimulationSerializer(data=request.data)
        if serializer.is_valid():
            return Response(priority_preemptive(serializer.validated_data["processes"]))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ---------------- Banker’s Algorithm ---------------- #
class BankerAPI(APIView):
    def post(self, request):
        serializer = SchedulingSimulationSerializer(data=request.data)
        if serializer.is_valid():
            return Response(bankers_algorithm(
                processes=[f"P{i}" for i in range(len(serializer.validated_data["alloc"]))],
                alloc=serializer.validated_data["alloc"],
                max_req=serializer.validated_data["max_req"],
                avail=serializer.validated_data["avail"]
            ))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ---------------- Memory Allocation ---------------- #
class FirstFitAPI(APIView):
    def post(self, request):
        serializer = SchedulingSimulationSerializer(data=request.data)
        if serializer.is_valid():
            return Response(first_fit(serializer.validated_data["processes"], serializer.validated_data["blocks"]))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BestFitAPI(APIView):
    def post(self, request):
        serializer = SchedulingSimulationSerializer(data=request.data)
        if serializer.is_valid():
            return Response(best_fit(serializer.validated_data["processes"], serializer.validated_data["blocks"]))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ---------------- Page Replacement ---------------- #
class FIFOPageAPI(APIView):
    def post(self, request):
        serializer = SchedulingSimulationSerializer(data=request.data)
        if serializer.is_valid():
            return Response(fifo_page_replacement(serializer.validated_data["pages"], len(serializer.validated_data["blocks"])))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LRUPageAPI(APIView):
    def post(self, request):
        serializer = SchedulingSimulationSerializer(data=request.data)
        if serializer.is_valid():
            return Response(lru_page_replacement(serializer.validated_data["pages"], len(serializer.validated_data["blocks"])))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OPTPageAPI(APIView):
    def post(self, request):
        serializer = SchedulingSimulationSerializer(data=request.data)
        if serializer.is_valid():
            return Response(optimal_page_replacement(serializer.validated_data["pages"], len(serializer.validated_data["blocks"])))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AlgorithmTheoryAPIView(APIView):
    """
    Handles GET (list or single), POST, PUT, DELETE for algorithm theory
    """

    def get(self, request, name=None):
        try:
            if name:
                # Single algorithm by name
                algo = AlgorithmTheory.objects(name__iexact=name).first()
                if not algo:
                    return Response({"error": "Algorithm not found"}, status=status.HTTP_404_NOT_FOUND)
                serializer = AlgorithmTheorySerializer(algo)
                return Response(serializer.data)
            else:
                # List all
                algos = AlgorithmTheory.objects.all()
                serializer = AlgorithmTheorySerializer(algos, many=True)
                return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = AlgorithmTheorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, name):
        try:
            algo = AlgorithmTheory.objects(name__iexact=name).first()
            if not algo:
                return Response({"error": "Algorithm not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = AlgorithmTheorySerializer(algo, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, name):
        try:
            algo = AlgorithmTheory.objects(name__iexact=name).first()
            if not algo:
                return Response({"error": "Algorithm not found"}, status=status.HTTP_404_NOT_FOUND)
            algo.delete()
            return Response({"message": f"{name} deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

