from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


from djnfusion import sync_user



class Command(BaseCommand):

    help = 'Synchronizes all users with infusionsoft.'

    def handle(self, *args, **options):

        for u in User.objects.all():
            print "Synchronizing user %s / %s ..." % (u.id, u.email)
            if sync_user(user=u):
                print "Successful."



