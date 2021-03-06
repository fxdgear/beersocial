from django.contrib import admin

from socialbeer.core.models import Challenge

class ChallengeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    date_hierarchy = 'start_date'
    list_display = ('name', 'start_date', 'end_date', 'creator')



admin.site.register(Challenge, ChallengeAdmin)
