from enum import unique
from typing_extensions import Required
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.db.models.base import Model
from django.db.models.fields import proxy
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, email, password, **extra_fields)


class CustomAbstractUser(AbstractUser):
    class Types(models.TextChoices):
        ADMIN = "admin"
        MODERATOR = "moderator"
        DRIVER = "driver"
        CUSTOMER = "customer"
        SELLER = "seller"

    base_type = Types.CUSTOMER
    type = models.CharField(_("User type"), max_length=50, choices=Types, default=base_type)
    email = models.EmailField(
        _('Email address'), unique=True, error_messages={'unique': _('A user with email already exists'),},
    )
    phone_number = PhoneNumberField(
        _('Phone number of a customer'), unique=True, error_messages={'unique':_('A user with phone number already exists.'),},
    null=True, blank=True,
    )
    objects = UserManager()

    REQUIRED_FIELDS = ['email', 'type']
    class Meta:
        abstract = True
        ordering = ['username']
        
    def save(self, *args, **kwargs):
        if not self.id:
            self.type = self.base_type
        return super().save(*args, **kwargs)


class User(CustomAbstractUser):
    class Meta(CustomAbstractUser):
        swappable = 'AUTH_USER_MODEL'


class CustomManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.CUSTOMER)


class SellerManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.SELLER)


class DriverManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.DRIVER)


class ModeratorManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.MODERATOR)


class AdminManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.ADMIN)


class CustomMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    birth_date = models.DateTimeField(verbose_name='Birth date of a customer', null=True, blank=True)
    image = models.ImageField(verbose_name='Image of a customer', upload_to='images/customers/', blank=True)
    def __str__(self):
        return f"{self.user.username}'s extra fields"
    
    class Meta:
        verbose_name_plural = 'Customers Extra Fields'
        verbose_name = 'Customer Extra Field'


class Customer(User):
    base_type = User.Types.CUSTOMER
    objects = CustomManager
    @property

    def more(self):
        return self.customermore

    def __str__(self):
        return self.get_full_name() or self.username

    class Meta:
        proxy = True

    
class SellerMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    company_name = models.CharField(max_length=64, verbose_name="Seller's company name")
    image = models.ImageField(verbose_name='Image of seller', upload_to='image/seller/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s extra fields"

    class Meta:
        verbose_name_plural = 'Sellers\Extra Fields'
        verbose_name = 'Seller\Extra Field'


class Seller(User):
    base_type = User.Types.SELLER
    objects = SellerManager()
    
    @property
    def more(self):
        return self.sellermore

    class Meta:
        proxy = True

    def get_phone_number(self):
        return self.more.company_name

    def __str__(self):
        return self.get_full_name() or self.username


class ModeratorMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    
    def __str__(self):
        return f"{self.user.username}'s extra fields"

    class Meta:
        verbose_name_plural = 'Moderators\Extra Fields'
        verbose_name = 'Moderator\Extra Field'


class Moderator(User):
    base_type = User.Types.MODERATOR
    objects = ModeratorManager()

    @property
    def more(self):
        return self.moderatormore

    class Meta:
        proxy = True
    

class AdminMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'Admin'
        verbose_name = 'Admin'

    def __str__(self):
        return f"{self.user.username}'s extra fields"
    
    class Meta:
        verbose_name_plural = 'Admins\Extra Fields'
        verbose_name = 'Admin\Extra Field'


class Admin(User):
    base_type = User.Types.ADMIN
    objects = AdminManager()

    @property
    def more(self):
        return self.adminmore

    class Meta:
        proxy = True
