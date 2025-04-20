from rest_framework import serializers

from card.models import CardModel

from .models import TransferModel


class TransferCreateSerializer(serializers.ModelSerializer):
    from_card = serializers.PrimaryKeyRelatedField(queryset=CardModel.objects.all())
    to_card = serializers.PrimaryKeyRelatedField(queryset=CardModel.objects.all())
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = TransferModel
        fields = ["from_card", "to_card", "amount"]

    def validate(self, attrs):
        from_card = attrs["from_card"]
        to_card = attrs["to_card"]
        amount = attrs["amount"]

        if from_card == to_card:
            raise serializers.ValidationError("You cannot transfer money to the same card.")

        if from_card.balance < amount:
            raise serializers.ValidationError("There are insufficient funds on the sender's card.")

        return attrs

    def create(self, validated_data):
        from_card = validated_data["from_card"]
        to_card = validated_data["to_card"]
        amount = validated_data["amount"]

        from_card.balance -= amount
        from_card.save()

        to_card.balance += amount
        to_card.save()

        return TransferModel.objects.create(**validated_data)


class TransferListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferModel
        exclude = ("user",)
