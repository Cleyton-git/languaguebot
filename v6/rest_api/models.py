from django.db import models

class Id(models.Model):
    id = models.TextField(primary_key=True, default=0)
    
    def __str__(self):
        return f"Id: {self.id}"

class Word(models.Model):
    word = models.CharField(primary_key=True, null=False)
    setences = models.TextField(null=False)
    anki = models.BooleanField(null=False, default=False)
    
    def __str__(self):
        return f"Palavra: {self.word}"

class Usuario(models.Model):
    telegram_id = models.IntegerField(primary_key=True)
    palavras = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.telegram_id}"
    
    
    