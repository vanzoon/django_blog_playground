from django.db import models

# Create your models here.


class Contact(models.Model):
    username = models.CharField(max_length=60, blank=False, null=None)
    email = models.EmailField(db_index=True, max_length=100)

    def __str__(self):
        return f'{self.username} with email:{self.email}'