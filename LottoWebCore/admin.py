from django.contrib import admin

# Register your models here.
from LottoWebCore.models import University


class UniversityAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "Crawled University"
        verbose_name_plural = "Crawled Universities"

    ordering = ['name']
    list_display = ['name', 'page']
    list_filter = ['phd', 'master']

    University.short_description = 'Raffle Owner'
    University.admin_search_field = 'name'


admin.site.register(University, UniversityAdmin)
