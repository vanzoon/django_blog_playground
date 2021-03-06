from django.db import models


class Contact(models.Model):
    username = models.CharField(max_length=60)
    email = models.EmailField(db_index=True, unique=True, max_length=100, blank=False)

    def __str__(self):
        return f'{self.username} with email:{self.email}'
