import logging

import requests
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from ..models import OauthProvider, ProviderChoice

User = get_user_model()

GOOGLE_OAUTH_SCOPE = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USER_DATA_URL = "https://www.googleapis.com/oauth2/v1/userinfo"


log = logging.getLogger(__name__)


def get_redirect_uri(request):
    r = reverse("social_redirect")
    return request.build_absolute_uri(r)


def redirect_url(request, client_id: str):
    scope = " ".join(GOOGLE_OAUTH_SCOPE)
    return f"https://accounts.google.com/o/oauth2/auth?client_id={client_id}&response_type=code&scope={scope}&redirect_uri={get_redirect_uri(request)}&state=google"


def get_provider():
    return OauthProvider.objects.filter(provider=ProviderChoice.GOOGLE).first()


def redirect_user_to_google_oauth(request):
    provider = get_provider()
    if provider:
        return redirect(redirect_url(request, provider.client_id))
    log.error(f"{provider} is not defined in the admin")
    return Response(
        {"msg": f"{provider} is not enabled."},
        status=status.HTTP_400_BAD_REQUEST,
    )


def validate_code_and_get_user(
    request,
):
    provider = get_provider()
    params = {
        "grant_type": "authorization_code",
        "code": request.GET.get("code"),
        "redirect_uri": get_redirect_uri(request),
        "client_id": provider.client_id,
        "client_secret": provider.secret,
    }
    response = requests.post(GOOGLE_TOKEN_URL, data=params)
    if not response.status_code == 200:
        log.debug(response.json())
        return {
            "is_err": True,
            "msg": "Something went wrong while validating your code",
            "user": None,
        }

    access_token = response.json().get("access_token")
    response = requests.get(GOOGLE_USER_DATA_URL, params={"access_token": access_token})
    if not response.status_code == 200:
        return {
            "is_err": True,
            "msg": "Access token is not valid",
            "user": None,
        }

    user_data = response.json()
    email = user_data.get("email")
    email_verified = user_data.get("verified_email")
    if not email_verified:
        return {
            "is_err": True,
            "msg": "Email not verified",
            "user": None,
        }

    if email:
        try:
            user = User.objects.get(email=email)
            is_new = False
        except User.DoesNotExist:
            # create user
            user = User.objects.create(
                email=email,
                first_name=user_data.get("given_name"),
                last_name=user_data.get("family_name"),
                is_active=True,
                is_social=True,
                # google_profile_img=user_data.get("picture"),
                # google_id=user_data.get("id"),
            )  # may be you want to do something if user is new
            is_new = True
        return {"is_err": False, "msg": "", "user": user, "is_new": is_new}

    else:
        # immpossible (IN THANOS VOICE )
        return {"is_err": True, "msg": "Email does not exist", "user": None}
