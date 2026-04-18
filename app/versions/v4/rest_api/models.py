from django.db import models

class Word(models.Model):
    word = models.CharField(primary_key=True, null=False)
    setences = models.TextField(null=False)
    anki = models.BooleanField(null=False, default=False)
    
    def __str__(self):
        return f"Palavra: {self.word}"

