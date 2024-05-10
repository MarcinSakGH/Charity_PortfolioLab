from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)


class Institution(models.Model):
    TYPE_CHOICES = (
        (1, 'Fundacja'),
        (2, 'Organizacja pozarządowa'),
        (3, 'Zbiórka lokalna')
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, default=1)
    categories = models.ManyToManyField(Category)

    @classmethod
    def count_institutions(cls):
        return cls.objects.count()


class Donation(models.Model):
    quantity = models.PositiveSmallIntegerField(help_text="Liczba worków")
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=256, help_text="Ulica plus numer domu")
    phone_number = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)

    @classmethod
    def total_quantity_of_bags(cls):
        return cls.objects.aggregate(total_quantity=Sum('quantity'))['total_quantity']