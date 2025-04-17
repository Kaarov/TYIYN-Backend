from rest_framework import serializers

from .models import CategoryModel


class CategorySerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = CategoryModel
        fields = ("title",)

    def get_title(self, category):
        language = self.context["request"].user.language
        return category.get_name(language)


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        exclude = ("id", "user")


class CategoryListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = CategoryModel
        fields = ("id", "title")

    def get_title(self, category):
        language = self.context["request"].user.language
        return category.get_name(language)
