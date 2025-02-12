from django.contrib import admin

from .models import Refbook, RefbookElement, RefbookVersion


class RefbookVersionInline(admin.TabularInline):
    model = RefbookVersion
    extra = 1


class RefbookElementInline(admin.TabularInline):
    model = RefbookElement
    extra = 1


@admin.register(Refbook)
class RefbookAdmin(admin.ModelAdmin):
    list_display = ["id", "code", "name", "current_version", "current_version_start_date"]
    inlines = [RefbookVersionInline]
    search_fields = ["code", "name"]
    list_filter = ["code"]

    def current_version(self, obj):
        latest_version = obj.versions.order_by("-start_date").first()
        return latest_version.version if latest_version else "Нет версий"

    def current_version_start_date(self, obj):
        latest_version = obj.versions.order_by("-start_date").first()
        return latest_version.start_date if latest_version else "Нет даты начала"

    current_version.short_description = "Текущая версия"
    current_version_start_date.short_description = "Дата начала версии"


@admin.register(RefbookVersion)
class RefbookVersionAdmin(admin.ModelAdmin):
    list_display = ["refbook_code", "refbook_name", "version", "start_date"]
    inlines = [RefbookElementInline]
    search_fields = ["version"]
    list_filter = ["refbook", "start_date"]

    def refbook_code(self, obj):
        return obj.refbook.code

    def refbook_name(self, obj):
        return obj.refbook.name

    refbook_code.short_description = "Код справочника"
    refbook_name.short_description = "Наименование справочника"


@admin.register(RefbookElement)
class RefbookElementAdmin(admin.ModelAdmin):
    list_display = ["version", "code", "value"]
    search_fields = ["code", "value"]
    list_filter = ["version"]
