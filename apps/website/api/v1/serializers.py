from rest_framework import serializers
from website.models import Newsletter
from website.models.tickets import Ticket, TicketMessage

# from website.models.wishlists import Wishlist
from accounts.models import UserType
from order.models import Order
from rest_framework import status


class BaseSerializer(serializers.ModelSerializer):

    absolute_url = serializers.SerializerMethodField()

    def get_absolute_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.get_absolute_url())

    def to_representation(self, instance):
        data = super().to_representation(instance)

        request = self.context.get("request")

        if request:
            kwargs = request.parser_context.get("kwargs", {})

            if kwargs.get("pk"):
                data.pop("absolute_url", None)

        return data


class Newsletterserializer(BaseSerializer):

    class Meta:
        model = Newsletter
        fields = ["id", "email", "absolute_url", "created_at"]


class TicketSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    order = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(), required=False
    )

    class Meta:
        model = Ticket
        fields = [
            "id",
            "user",
            "order",
            "subject",
            "status",
            "category",
            "priority",
            "created_at",
            "updated_at",
            "closed_at",
        ]
        read_only_fields = [
            "status",
            "created_at",
            "updated_at",
            "closed_at",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get("request")

        if request and request.user.is_authenticated:
            self.fields["order"].queryset = Order.objects.filter(user=request.user)

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class TicketMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = TicketMessage
        fields = ["id", "ticket", "sender", "message", "is_staff_reply", "created_at"]
        read_only_fields = ["sender", "is_staff_reply", "created_at"]

    def validate_ticket(self, value):
        request = self.context["request"]
        is_staff = request.user.user_type in [UserType.ADMIN, UserType.SUPERUSER]
        if not is_staff and value.user_id != request.user.id:
            raise serializers.ValidationError(
                "This ticket does not exist.",
                status=status.HTTP_204_NO_CONTENT,
            )
        return value

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["sender"] = request.user
        validated_data["is_staff_reply"] = request.user.user_type in [
            UserType.ADMIN,
            UserType.SUPERUSER,
        ]
        return super().create(validated_data)
