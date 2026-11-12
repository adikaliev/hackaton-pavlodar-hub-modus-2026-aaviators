from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Обратная связь — настройки"
admin.site.site_title = "Настройки системы"
admin.site.index_title = "Справочники, правила, сроки, календарь"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("feedback.urls")),
]
