from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User


from djnfusion import daily_statistics



class Command(BaseCommand):

    help = 'Sends daily statistics for all users to infusionsoft.'

    def handle(self, *args, **options):

        try:
            userid = args[0]
            if userid == 'all':
                query = User.objects.all()
            else:
                query = User.objects.filter(id=userid)
        except IndexError:
            raise CommandError("Pass user-id or 'all' as parameter.")

        for u in query.iterator():
            print "Sending statistics for user %s / %s ..." % (u.id, u.email)
            try:
                if daily_statistics(user=u):
                    print "... successful."
                else:
                    print "... not sent."
            except Exception, e:
                print "... Error: %s" % unicode(e)




