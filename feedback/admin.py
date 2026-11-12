"""Reference data the administrator edits without a developer:
categories and deadlines, routing rules, roles, the directory, the calendar and system settings.
"""
from django.contrib import admin

from . import models


@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "head", "external_id")
    search_fields = ("name",)
    autocomplete_fields = ("head", "parent")


@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("full_name", "position", "department", "access", "deputy", "absent", "is_active")
    list_filter = ("access", "absent", "is_active", "department")
    list_editable = ("absent",)
    search_fields = ("full_name", "position")
    autocomplete_fields = ("deputy", "department")
    exclude = ("telegram_link_code",)


@admin.register(models.FunctionalRole)
class FunctionalRoleAdmin(admin.ModelAdmin):
    list_display = ("name", "holder", "code")
    autocomplete_fields = ("holder",)
    search_fields = ("name",)


class CategoryInline(admin.TabularInline):
    model = models.Category
    extra = 0
    fields = ("name", "first_response_days", "problem_decision_days", "idea_decision_days", "is_active", "sort")


@admin.register(models.CategoryGroup)
class CategoryGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "default_role", "sort")
    inlines = [CategoryInline]


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "group", "first_response_days", "problem_decision_days", "idea_decision_days", "is_active")
    list_editable = ("first_response_days", "problem_decision_days", "idea_decision_days", "is_active")
    list_filter = ("group", "is_active")
    search_fields = ("name", "keywords")


@admin.register(models.RoutingRule)
class RoutingRuleAdmin(admin.ModelAdmin):
    list_display = ("order", "name", "request_type", "target_kind", "target_role", "is_active")
    list_display_links = ("name",)
    list_editable = ("order", "is_active")
    filter_horizontal = ("categories",)
    fieldsets = (
        (None, {"fields": ("order", "name", "is_active")}),
        ("Условия (пустое — любое)", {"fields": ("sensitive_only", "request_type", "categories", "author_department", "priority")}),
        ("Кому направить", {"fields": ("target_kind", "target_role")}),
    )


@admin.register(models.Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ("date", "name", "is_working")
    date_hierarchy = "date"


@admin.register(models.SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not models.SystemSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.Integration)
class IntegrationAdmin(admin.ModelAdmin):
    list_display = ("name", "kind", "mode", "enabled", "last_ok_at", "last_error")
    readonly_fields = ("code", "last_ok_at", "last_error")
