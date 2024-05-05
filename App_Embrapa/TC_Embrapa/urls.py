"""
URL configuration for TC_Embrapa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from django.urls import path

schema_view = get_schema_view(
    openapi.Info(
        title = "Vini API",
        default_version = "v0.01",
        description = "API para o site teste de consulta de dados sobre" 
                      "vinícolas do Brasil pela Embrapa",
        terms_of_service = "MIT License",
        contact = openapi.Contact(email = "egrojkayode@gmail.com"),
        license = openapi.License(name = "")
    ),
    public = True,
    permission_classes = (permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui("swagger", cache_timeout = 0), name="schema-swagger-ui"),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout = 0), name = 'schema_redoc'),
    path('django_plotly_dash/', include('django_plotly_dash.urls'))
]
