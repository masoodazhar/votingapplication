from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Generate 1000 users.'

    def handle(self, *args, **options):
        for i in range(1000):
            username = f'user{i}'
            email = f'user{i}@example.com'
            password = 'password123'
            User.objects.create_user(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS('Successfully generated 1000 users.'))