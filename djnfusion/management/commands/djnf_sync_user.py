from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User


from djnfusion import sync_user



class Command(BaseCommand):

    help = 'Synchronizes a user with infusionsoft. Specify user-id or email address as parameter.'

    def handle(self, *args, **options):

        try:
            email_or_userid = args[0]
        except IndexError:
            raise CommandError("Pass user-id or email address as parameter.")

        try:
            u = User.objects.get(email=email_or_userid)
        except User.DoesNotExist:
            try:
                u = User.objects.get(id=email_or_userid)
            except User.DoesNotExist:
                raise CommandError("Could not find user with email or id '%s'." % email_or_userid)

        if sync_user(user=u):
            print "Successful."



