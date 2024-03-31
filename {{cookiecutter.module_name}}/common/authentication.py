from {{cookiecutter.module_name}}.authentication.serializers.token import TokenSerializer
from {{cookiecutter.module_name}}.users.serializers.user import UserReadSerializer


def get_user_auth_data(user, request):
    return {
        "authentication": TokenSerializer(user).data,
        "user": UserReadSerializer(user, context={"request": request}).data,
    }
