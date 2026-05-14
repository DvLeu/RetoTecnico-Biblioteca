from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import include, path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("", lambda request: redirect("prestamos_lista")),

    path("admin/", admin.site.urls),

    path("", include("library.urls")),

    path(
        "api/schema/",
        login_required(SpectacularAPIView.as_view()),
        name="schema",
    ),
    path(
        "api/docs/",
        login_required(SpectacularSwaggerView.as_view(url_name="schema")),
        name="swagger_ui",
    ),
    path(
        "api/redoc/",
        login_required(SpectacularRedocView.as_view(url_name="schema")),
        name="redoc",
    ),
]