from rest_framework import serializers
from scores.models import Score
from accounts.models import User


def calculate_score(input_value):
    """Custom formula calculation"""
    return input_value + 1


class ScoreSerializer(serializers.ModelSerializer):
    # Field included only in browsable API form, but not actually a part of the Score model
    input_value = serializers.FloatField(write_only=True)

    # Fields to exclude from API form, but include in returned response, and automatically assign this value via create() override
    id = serializers.IntegerField(read_only=True)
    score = serializers.FloatField(read_only=True)
    date_submitted = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Score
        fields = [
            "input_value",
            "id",
            "user",
            "score",
            "date_submitted",
        ]

    def create(self, validated_data):

        # Get user instance
        user = validated_data.get("user")

        # Use input_value to calculate score
        input_value = validated_data.get("input_value")
        score = calculate_score(input_value)

        # Create Score instance
        score_instance = Score.objects.create(user=user, score=score)

        return score_instance
