from django.core.management.base import BaseCommand
from django.utils import lorem_ipsum

from blog.models import Post


class Command(BaseCommand):
    def handle(self, *args, **options):
        Post.objects.bulk_create(
            Post(
                title=f'generated post {lorem_ipsum.WORDS(2)}',
                body=f'{lorem_ipsum}'
            ) for i in range(10)
        )
