# from django.contrib import admin

# Register your models here.
# from LottoWebCore.models import University


# class UniversityAdmin(admin.ModelAdmin):
#     class Meta:
#         verbose_name = "Crawled University"
#         verbose_name_plural = "Crawled Universities"
#
#     ordering = ['name']
#     list_display = ['name', 'page']
#     list_filter = ['phd', 'master']
#
#     University.short_description = 'Raffle Owner'
#     University.admin_search_field = 'name'


# admin.site.register(University, UniversityAdmin)
from django.contrib import admin

from LottoWebCore.actions import RequestToUser
from LottoWebCore.models import Ticket, MiddleMan, Raffle, StudentDirectory, University, RegistrationRequest, City, \
    Prize


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'name', 'directory', 'seller', 'notified', 'activated']
    list_filter = ['name', 'notified', 'activated']
    search_fields = ['name', 'notified', 'activated']
    readonly_fields = ['id']


@admin.register(MiddleMan)
class MiddleManAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'name', 'full_name']
    readonly_fields = ['id']


@admin.register(Raffle)
class RaffleAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['id', 'name', 'directory', 'completed']
    list_filter = ['name', 'completed']
    search_fields = ['name', 'directory', 'completed']
    readonly_fields = ['id']


@admin.register(StudentDirectory)
class StudentDirectoryAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['acronym', 'name', 'phone', 'city', 'email', 'university']
    list_filter = ['name', 'room', 'city', 'email', 'university']
    search_fields = ['name', 'university']


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ['name', 'page']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(RegistrationRequest)
class RegistrationRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'raffle', 'directory', 'analysed']
    actions = [RequestToUser]


@admin.register(Prize)
class PrizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'qtde']
