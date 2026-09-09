from django.db import models

# Create your models here.
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Vehicle(models.Model):
    FUEL_CHOICES = [
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('Electric', 'Electric'),
        ('Hybrid', 'Hybrid'),
    ]

    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    year = models.IntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    fuel_type = models.CharField(max_length=10, choices=FUEL_CHOICES)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.brand} {self.name} ({self.year})"


class Booking(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='bookings')
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=10)
    start_date = models.DateField()
    end_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    def clean(self):
        if self.start_date < timezone.now().date():
            raise ValidationError("Start date cannot be in the past.")

        if self.end_date <= self.start_date:
            raise ValidationError("End date must be after start date.")

        if not self.customer_phone.isdigit() or len(self.customer_phone) != 10:
            raise ValidationError("Phone number must be exactly 10 digits.")

        overlapping = Booking.objects.filter(
            vehicle=self.vehicle,
            start_date__lte=self.end_date,
            end_date__gte=self.start_date,
        ).exclude(pk=self.pk)

        if overlapping.exists():
            raise ValidationError("This vehicle is already booked for the selected dates.")

    def save(self, *args, **kwargs):
        days = (self.end_date - self.start_date).days
        self.total_amount = days * self.vehicle.price_per_day
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer_name} - {self.vehicle} ({self.start_date} to {self.end_date})"