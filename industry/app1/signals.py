from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import ShedDetails, ShedUser

@receiver(post_save, sender=ShedDetails)
def create_user_and_sheduser(sender, instance, created, **kwargs):
    if created:
        user = User.objects.create_user(username=instance.name, password=instance.password)
        ShedUser.objects.create(user=user, shed=instance)

@receiver(post_save, sender=ShedDetails)
def create_or_update_user_and_sheduser(sender, instance, created, **kwargs):
    if created:
        user = User.objects.create_user(username=instance.name, password=instance.password)
        ShedUser.objects.create(user=user, shed=instance)
    else:
        user = User.objects.get(username=instance.name)
        if user.check_password(instance.password):
            user.set_password(instance.password)
            user.save()
        shed_user = ShedUser.objects.get(user=user)
        shed_user.shed = instance
        shed_user.save()

@receiver(post_delete, sender=ShedDetails)
def delete_user_and_sheduser(sender, instance, **kwargs):
    try:
        shed_user = ShedUser.objects.get(shed=instance)
        user = shed_user.user
        shed_user.delete()
        user.delete()  
    except ShedUser.DoesNotExist:
        pass  
