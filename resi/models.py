from django.db import models

# from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        if not email and not phone_number:
            raise ValueError("You must provide either an email address or phone number")
        if email:
            email = self.normalize_email(email)
            user = self.model(email=email, **extra_fields)
        else:
            user = self.model(phone_number=phone_number, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
        
    def __str__(self):
        return self.email or self.phone_number 


class Department(models.Model):
    name = models.CharField(max_length=255, null=False)
    address = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=60, null=False)

    def __str__(self):
        return f"{self.user.last_name} - {self.user.email}"


class Room(models.Model):
    name = models.CharField(max_length=100, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="rooms"
    )
    image_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )

    def is_available(self):
        now = timezone.now().date()
        reservations_today = self.reservation_set.filter(
            check_in_date__lte=now, check_out_date__gte=now
        )
        return not reservations_today.exists()

    def save(self, *args, **kwargs):
        self.available = self.is_available()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.create_invoice()

    def create_invoice(self):
        duration = (self.check_out_date - self.check_in_date).days
        total_amount = self.room.price * duration

        if duration >= 3:
            total_amount *= 0.8  # Réduction de 20% si la durée est de 3 jours ou plus

        invoice = Invoice.objects.create(
            name=f"Invoice for {self.room.name}",
            total_amount=total_amount,
            amount_due=total_amount,
            customer=self.customer,
        )
        invoice.save()

    def __str__(self):
        return f"{self.customer.user.username} - {self.room.name} - {self.check_in_date} to {self.check_out_date}"


class Invoice(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.amount_due = self.total_amount - self.amount_paid
        self.paid = self.amount_due == 0
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


"""def save(self, *args, **kwargs):
        # Calcul du montant dû en soustrayant le montant payé du montant total
        self.amount_due = self.total_amount - self.amount_paid
        
        # Mettre à jour le statut de paiement en fonction du montant dû
        self.paid = self.amount_due <= 0
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name"""

class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Mettre à jour le montant payé dans la facture associée
        self.invoice.amount_paid += self.amount
        self.invoice.save()

class Review(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.reservation.room.name}"
