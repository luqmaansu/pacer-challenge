from scores.serializers import ScoreSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer


class ScoreCreateView(generics.CreateAPIView):
    serializer_class = ScoreSerializer
    renderer_classes = [JSONRenderer]
    # permission_classes = [IsAuthenticated]