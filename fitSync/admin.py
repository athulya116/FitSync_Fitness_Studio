from django.contrib import admin
from .models import Client,Booking,ClassSlot

# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'created_at')
    search_fields = ('full_name', 'email')
    list_filter = ('created_at',)

@admin.register(ClassSlot)
class ClassSlotAdmin(admin.ModelAdmin):
    list_display = ('class_type', 'date', 'start_time', 'end_time')
    list_filter = ('class_type', 'date')
    ordering = ('date', 'start_time')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('client', 'email', 'class_slot', 'booked_at')
    search_fields = ('client__full_name', 'email')
    list_filter = ('class_slot__class_type', 'class_slot__date')
    ordering = ('-booked_at',)