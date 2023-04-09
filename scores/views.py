from scores.serializers import ScoreSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class ScoreCreateView(generics.CreateAPIView):
    serializer_class = ScoreSerializer
    # permission_classes = [IsAuthenticated]