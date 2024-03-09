from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name")


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name")

    def update(self, instance, validated_data):
        fname = validated_data.get("first_name")
        lname = validated_data.get("last_name")
        instance.first_name = fname
        instance.lname = lname
        # if avatar:
        #     extension = Path(avatar.name).suffix
        #     filename = f"{uuid.uuid4()}{extension}"
        #     file = ContentFile(avatar.read(), filename)
        #     instance.avatar = file
        # else:
        #     instance.avatar = ""

        instance.save()
        return instance


class UserWriteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(validators=[validate_password], write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "password",
        )

    def create(self, validated_data):
        password = validated_data.pop("password")
        email = validated_data.get("email")
        user = User.objects.create_user(email=email, password=password)
        return user
