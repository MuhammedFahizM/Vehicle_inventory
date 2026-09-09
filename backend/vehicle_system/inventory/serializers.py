from rest_framework import serializers
from .models import Vehicle, Booking


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('total_amount',)

    def validate(self, data):
        # Build a temporary Booking instance so we can reuse the model's
        # clean() logic (overlap check, past-date check, phone check, etc.)
        instance = Booking(
            vehicle=data.get('vehicle'),
            customer_name=data.get('customer_name'),
            customer_phone=data.get('customer_phone'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
        )
        instance.clean()
        return data