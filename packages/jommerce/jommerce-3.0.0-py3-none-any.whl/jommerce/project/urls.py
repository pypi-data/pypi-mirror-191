from django.urls import path, include
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
]

if "django.contrib.admin" in settings.INSTALLED_APPS:
    from django.contrib import admin

    urlpatterns += [path("admin/", admin.site.urls)]

if "jommerce.auth" in settings.INSTALLED_APPS:
    urlpatterns += [path("auth/", include("jommerce.auth.urls", namespace="auth"))]

if "jommerce.blog" in settings.INSTALLED_APPS:
    urlpatterns += [path("blog/", include("jommerce.blog.urls", namespace="blog"))]

if "debug_toolbar" in settings.INSTALLED_APPS:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls", namespace="djdt"))]
