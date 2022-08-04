from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class User(models.Model):
    email = models.EmailField()
    role = models.ForeignKey(Role, on_delete= models.PROTECT)

    def __str__(self):
        return self.name