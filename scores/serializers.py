from rest_framework import serializers
from scores.models import Score
from accounts.models import User


def calculate_score(input_value):
    """Custom formula calculation"""
    return input_value + 1


class ScoreSerializer(serializers.ModelSerializer):
    # Exclude from API form, but include in returned response, and automatically assign this value via create() override
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    # Field included only in browsable API form, but not actually a part of the Score model
    input_value = serializers.FloatField(write_only=True)

    # Field not included in browsable API form, but included when returning the generated Score instance
    score = serializers.FloatField(read_only=True)

    class Meta:
        model = Score
        fields = ["user", "input_value", "score"]

    def create(self, validated_data):
        # If user is not logged in, record user as null
        user = self.context["request"].user
        if not user.is_authenticated:
            user = None

        # Use input_value to calculate score
        input_value = validated_data.get("input_value")
        score = calculate_score(input_value)

        # Create Score instance
        score_instance = Score.objects.create(user=user, score=score)

        return score_instance
