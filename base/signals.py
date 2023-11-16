from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Customer


@receiver(post_save, sender=User)
def customer_profile(sender,instance,created, **kwargs):
    if created:
        Customer.objects.create(
            user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name,
            username=instance.username,
            email=instance.email
        )
        print('Profile Created')
post_save.connect(customer_profile,sender=User)


def update_profile(sender,instance, created, **kwargs):
    if created == False:
        try:
            instance.customer.save()
            print('Profile updated!!!')
        except:
            Customer.objects.create(user=instance)
            print('Profile created for existing')

post_save.connect(update_profile, sender=User)
