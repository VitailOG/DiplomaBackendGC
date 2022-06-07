from django.contrib import admin

from .models import StudentSource


@admin.register(StudentSource)
class StudentSourceAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    list_display_links = ("id", "__str__")
