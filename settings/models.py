from django.db import models


class QA(models.Model):
    Q = models.CharField(max_length=500)
    A = models.TextField()
    
    def __str__(self) -> str:
        return self.Q