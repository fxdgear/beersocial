from django.contrib import admin

from socialbeer.core.models import Challenge

class ChallengeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Challenge, ChallengeAdmin)