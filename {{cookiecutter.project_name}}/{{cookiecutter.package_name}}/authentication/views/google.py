import logging

from {{cookiecutter.package_name}}.common.authentication import get_user_auth_data
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..oauth.google import redirect_user_to_google_oauth, validate_code_and_get_user

log = logging.getLogger(__name__)


class GoogleOauth(APIView):
    def get(self, request, format=None):
        if "code" not in request.GET:
            return redirect_user_to_google_oauth(request)
        else:
            data = validate_code_and_get_user(request)
            if data["is_err"]:
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            user = data["user"]
            return Response(
                get_user_auth_data(user, request),
            )
