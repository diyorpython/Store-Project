from django.core.management.base import BaseCommand
from faker import Faker
from random import randint
from random import randint
from core.models import (
    Customuser
)

fake = Faker()


class Command(BaseCommand):
    help = 'Create random user'

    def handle(self, *args, **options):
        users_cnt = 100

        for _ in range(users_cnt):
            user_data = {
                'username': fake.user_name(),
                'full_name': f'{fake.first_name()} {fake.last_name()}',
                'email': fake.email(),
                'addres': fake.address(),
                'password': fake.password(),
                'email_code': randint(100000, 999999)
            }
            try:
                Customuser.objects.create(**user_data)
            except Exception:
                users_cnt -= 1
        if users_cnt > 0:
            plural = 's' if users_cnt > 1 else ''
            self.stdout.write(f'{users_cnt} User{plural} created successfully')
        else:
            self.stdout.write('Everything up-to-date!')