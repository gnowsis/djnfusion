from django.core.management.base import BaseCommand

from djnfusion import server

class Command(BaseCommand):

    help = 'Tests connectivity to infusionsoft.'

    def handle(self, *args, **options):

        print server.DataService.echo("Yep, there's a connection!");

