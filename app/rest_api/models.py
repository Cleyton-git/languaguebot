from django.db import models

class Id(models.Model):
    id = models.TextField(primary_key=True, default=0)
    
    def __str__(self):
        return f"Id: {self.id}"

class Usuario(models.Model):
    telegram_id = models.IntegerField(primary_key=True)
    palavra_inicial = models.IntegerField(default=0)
    palavra_atual = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)
    tela_atual = models.TextField(default="deslogado")
    proximo_estudo = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.telegram_id}"
    
class FraseUsuario(models.Model):
    usuario = models.ForeignKey("Usuario", on_delete=models.CASCADE)
    palavra = models.CharField()
    frase = models.TextField()
    
    def __str__(self):
        return f"{self.palavra} + {self.frase}"

class UsuarioOndoku(models.Model):
    usuario = models.ForeignKey("Usuario", on_delete=models.CASCADE)
    ondoku_atual = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.usuario} + {self.ondoku_atual}"