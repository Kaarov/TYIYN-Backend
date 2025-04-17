from rest_framework import serializers

from .models import BudgetModel


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetModel
        exclude = ("id", "user")


class BudgetListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetModel
        exclude = ("user",)
