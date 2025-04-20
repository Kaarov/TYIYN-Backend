from rest_framework import serializers

from .models import ExpenseModel


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseModel
        fields = "__all__"
        read_only_fields = ("user",)

    def validate(self, attrs):
        card = attrs["card"]
        amount = attrs["amount"]
        if card.balance < amount:
            raise serializers.ValidationError("Insufficient funds on the card.")
        return attrs

    def create(self, validated_data):
        card = validated_data["card"]
        amount = validated_data["amount"]
        card.balance -= amount
        card.save()
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        old_amount = instance.amount
        new_amount = validated_data.get("amount", old_amount)
        card = instance.card
        delta = old_amount - new_amount
        if card.balance + delta < 0:
            raise serializers.ValidationError("Insufficient funds after the upgrade.")
        card.balance += delta
        card.save()
        return super().update(instance, validated_data)

    def delete(self):
        self.instance.card.balance += self.instance.amount
        self.instance.card.save()
        self.instance.delete()
