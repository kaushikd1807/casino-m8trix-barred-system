import os
import uuid
import datetime
from django.db import models
from django.conf import settings
from .functions import generate_magic_url_seed, generate_qr_code

class Order(models.Model):
    # Model for all orders, can be extended later

    # Order metadata
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Listing info
    mls_id = models.IntegerField(null=True, blank=True)
    listing_url = models.URLField(max_length=2000, blank=True)
    agent_notes = models.TextField(blank=True)

    # Address Info
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    zip_code = models.CharField(max_length=12, blank=True)
    country = models.CharField(max_length=50, blank=True, default="USA")
    state = models.CharField(max_length=14, blank=True)

    # Status information
    status = models.CharField(max_length=40, blank=True, default="Open")
    escrow_status = models.CharField(max_length=40, blank=True, default="Unpaid")
    down_payment_status = models.CharField(max_length=40, blank=True, default="Unpaid")
    mutually_executed_contract_date = models.DateField(null=True, blank=True, default=None, verbose_name="MEC Date")

    # Payment information and message information
    down_payment_deadline = models.DateField(null=True, blank=True, default=None)
    down_payment_dest = models.CharField(max_length=200, blank=True)
    down_payment_stripe_confirmation_id = models.CharField(max_length=200, blank=True)
    down_payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    escrow_deadline = models.DateField(null=True, blank=True, default=None)
    escrow_payment_dest = models.CharField(max_length=200, blank=True)
    escrow_stripe_confirmation_id = models.CharField(max_length=200, blank=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Agent, Customer and Photo
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        null=True, blank=True, 
        on_delete=models.SET_NULL,
        related_name="agents"
        )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        null=True, blank=True, 
        on_delete=models.SET_NULL,
        related_name="customers"
        )

    # Magic Link for customer payment
    magic_url_seed = models.CharField(max_length=22, blank=True)

    @property
    def mec_days_till_close(self):
        today = datetime.datetime.now().date()
        if self.mutually_executed_contract_date:
            return (self.mutually_executed_contract_date - today).days
        else:
            return None

    @property
    def est_closing_str(self):
        if self.mutually_executed_contract_date:
            lower = self.mutually_executed_contract_date + datetime.timedelta(days=30)
            upper = self.mutually_executed_contract_date + datetime.timedelta(days=45)
            return '{} to {}'.format(lower, upper)
        else:
            return None

    @property
    def magic_link_path(self):
        if self.magic_url_seed:
            return '/pay/{}'.format(self.magic_url_seed)

    @property
    def qr_code(self):
        return generate_qr_code('http://127.0.0.1:8000' + self.magic_link_path)

    def save(self, *args, **kwargs):
        if not self.magic_url_seed:
            self.magic_url_seed = generate_magic_url_seed()
        return super().save(*args, **kwargs)

    def __str__(self):
        return 'MLS {}: {} {}'.format(self.mls_id, self.address1, self.address2)

class Document(models.Model):
    # Model to store shared or private documents
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shared = models.BooleanField(default=False)
    document_file = models.FileField(upload_to="documents/orders/")
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return os.path.basename(self.document_file.name)
