from django.core.management.base import BaseCommand
from django.utils import lorem_ipsum

from blog.models import Post

# TODO: refactor using bulk create


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(10):
            Post.object.create(title=f'generated post {lorem_ipsum.WORDS(2)}', body=f'{lorem_ipsum}')
            self.stdout.write(self.style.SUCCESS(f'post {i} is generated'))
