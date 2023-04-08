from rest_framework import serializers
from scores.models import Score
from accounts.models import User


def calculate_score(input_value):
    """Custom formula calculation"""
    return input_value + 1


class ScoreSerializer(serializers.ModelSerializer):
    # To use user_id number directly instead of User dropdown
    user_id = serializers.IntegerField()

    # Field included only in browsable API form, but not actually a part of the Score model
    input_value = serializers.FloatField(write_only=True)

    # Field not included in browsable API form, but included when returning the generated Score instance
    score = serializers.FloatField(read_only=True)

    class Meta:
        model = Score
        fields = ["user_id", "input_value", "score"]

    def validate_user_id(self, value):
        # If user_id is supplied, make sure the user instance exists
        if value and not User.objects.filter(pk=value).exists():
            raise serializers.ValidationError(f"User with id '{value}' does not exist.")

        # Explicit checking to allow empty user_id -> None
        elif not value:
            value = None

        return value

    def create(self, validated_data):
        # Use user_id to get the User instance
        user_id = validated_data.get("user_id")
        user = User.objects.filter(pk=user_id).first() or None

        # Use input_value to calculate score
        input_value = validated_data.get("input_value")
        score = calculate_score(input_value)

        # Create Score instance
        score_instance = Score.objects.create(user=user, score=score)

        return score_instance
