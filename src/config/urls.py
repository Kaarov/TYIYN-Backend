"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

docs_urls = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]

admin_urls = [
    path("jet/", include("jet.urls", "jet")),
    path("jet/dashboard/", include("jet.dashboard.urls", "jet-dashboard")),
    path("admin/", admin.site.urls),
]

app_urls = [
    path("users/", include("users.urls")),
    path("card/", include("card.urls")),
    path("category/", include("category.urls")),
    path("budget/", include("budget.urls")),
    path("goal/", include("goal.urls")),
    path("transfer/", include("transfer.urls")),
    path("income/", include("income.urls")),
    path("expense/", include("expense.urls")),
    path("analytics/", include("analytics.urls")),
]

urlpatterns = [
    *app_urls,
    path("", include(docs_urls)),
    path("", include(admin_urls)),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
