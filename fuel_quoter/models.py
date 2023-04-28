from django.urls import reverse
from django.db import models
from .static.choices import STATE_CODES


class FuelQuote(models.Model):
    user_id = models.BigIntegerField(blank=False, null=False)
    gallons_requested = models.DecimalField(max_digits=7, decimal_places=2, blank=False, null=False)
    delivery_date = models.DateField(blank=False, null=False)
    address1 = models.CharField(max_length=100, blank=False, null=False)
    address2 = models.CharField(max_length=100, blank=True, null=False)
    city = models.CharField(max_length=50, blank=False, null=False)
    state = models.CharField(max_length=2, blank=False, null=False, choices=STATE_CODES)
    zipcode = models.CharField(max_length=10, blank=False, null=False)
    price_rate = models.DecimalField(max_digits=4, decimal_places=2, blank=False, null=False)
    total_due = models.DecimalField(max_digits=9, decimal_places=2, blank=False, null=False)

    def get_absolute_url(self):
        return reverse('quote', kwargs={'id': self.id})
