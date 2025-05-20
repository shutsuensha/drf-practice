from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import ExchangeProposal,  Ad, Tag, Category


class ProposalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeProposal
        fields = "__all__"
        read_only_fields = ["status", "created_at"]

    def validate(self, data):
        user = self.context["request"].user
        ad_sender = data.get("ad_sender")
        ad_receiver = data.get("ad_receiver")

        if ad_sender.user != user:
            raise ValidationError(
                "Вы можете отправлять обмены только от своих объявлений (ad_sender)."
            )

        if ad_receiver.user == user:
            raise ValidationError(
                "Вы не можете отправлять обмены на свои объявления (ad_receiver)."
            )

        return data


class ProposalStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeProposal
        fields = "__all__"
        read_only_fields = ["created_at", "ad_sender", "ad_receiver", "comment"]

    def validate(self, data):
        status_value = data.get("status")
        allowed_statuses = ["accepted", "rejected"]

        if status_value not in allowed_statuses:
            raise ValidationError(
                "Недопустимый статус. Разрешены только 'accepted' или 'rejected'."
            )

        return data
    


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class AdSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    tags = TagSerializer(many=True, read_only=True)  # только для чтения
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, write_only=True, required=False
    )
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    image = serializers.ImageField(required=False, allow_null=True)
    description_length = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = [
            'id', 'user', 'title', 'description', 'description_length',
            'image', 'category', 'condition', 'tags', 'tag_ids', 'created_at',
        ]
        read_only_fields = ['id', 'user', 'created_at']

    def validate_title(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Заголовок слишком короткий (мин. 10 символов).")
        return value

    def validate(self, attrs):
        title = attrs.get('title', '')
        category = attrs.get('category')
        if category and category.title == 'Электроника' and 'телефон' not in title.lower():
            raise serializers.ValidationError("Для категории 'Электроника' заголовок должен содержать 'телефон'.")
        return attrs

    def get_description_length(self, obj):
        return len(obj.description) if obj.description else 0

    def create(self, validated_data):
        tags_data = validated_data.pop('tag_ids', [])
        ad = Ad.objects.create(**validated_data)
        ad.tags.set(tags_data)
        return ad

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tag_ids', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tags_data is not None:
            instance.tags.set(tags_data)

        return instance
