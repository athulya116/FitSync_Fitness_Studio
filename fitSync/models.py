from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

class Client(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=128)  # Store hashed password
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    
class ClassSlot(models.Model):
    CLASS_CHOICES = [
        ('yoga', 'Yoga'),
        ('hiit', 'HIIT'),
        ('zumba', 'Zumba'),
    ]

    class_type = models.CharField(max_length=20, choices=CLASS_CHOICES)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    available_seats = models.PositiveIntegerField(default=10)  # Change default as needed


    def __str__(self):
        return f"{self.class_type.title()} | {self.date} | {self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')}"
    
# class Booking(models.Model):
#     CLASS_CHOICES = [
#         ('yoga', 'Yoga'),
#         ('hiit', 'HIIT'),
#         ('zumba', 'Zumba'),
#     ]

#     client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='bookings')
#     email = models.EmailField()  # Stored separately for direct access
#     class_type = models.CharField(max_length=20, choices=CLASS_CHOICES)
#     date = models.DateField()
#     start_time = models.TimeField(default=datetime.time(6, 0))  # 6:00 AM
#     end_time = models.TimeField(default=datetime.time(7, 0))    # 7:00 AM
#     booked_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.client.full_name} ({self.email}) - {self.class_type.title()} on {self.date} at {self.slot_display()}"

#     def slot_display(self):
#         return f"{self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')}"


# class Booking(models.Model):
#     client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='bookings')
#     email = models.EmailField()  # Optional but helpful for filtering and redundancy
#     class_slot = models.ForeignKey(ClassSlot, on_delete=models.CASCADE, related_name='bookings')
#     booked_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.client.full_name} ({self.email}) - {self.class_slot}"

#     def slot_display(self):
#         return f"{self.class_slot.start_time.strftime('%I:%M %p')} - {self.class_slot.end_time.strftime('%I:%M %p')}"


class Booking(models.Model):
    # client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='bookings')
    # email = models.EmailField()
    # class_slot = models.ForeignKey(ClassSlot, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    # booked_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"{self.client.full_name} - {self.class_slot}"

    # def slot_display(self):
    #     return f"{self.class_slot.start_time.strftime('%I:%M %p')} - {self.class_slot.end_time.strftime('%I:%M %p')}"
    
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('cancelled', 'Cancelled'),
        ('missed', 'Missed'),
        ('attended', 'Attended'),  # Optional future use
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='bookings')
    email = models.EmailField()
    class_slot = models.ForeignKey(ClassSlot, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.full_name} - {self.class_slot.class_type} on {self.class_slot.date} at {self.class_slot.start_time} - {self.status}"

