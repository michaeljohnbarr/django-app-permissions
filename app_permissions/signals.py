from django.db.models.signals import class_prepared
from django.dispatch import receiver


@receiver(class_prepared)
def my_callback(sender, **kwargs):
    print("Request finished!")
