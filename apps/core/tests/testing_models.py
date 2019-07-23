from django.db import models

from core.models.models import AbstractOrderingModel


class Parent(AbstractOrderingModel):
    pass


class Child(AbstractOrderingModel):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
