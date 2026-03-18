from django.db import models

class User(models.Model):
    name       = models.CharField(max_length=100)
    email      = models.EmailField(unique=True)
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table  = 'users'
        ordering  = ['-created_at']

    def __str__(self):
        return self.email

    def deactivate(self):
        self.is_active = False
        self.save()