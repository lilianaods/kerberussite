from django.db import models

class Membro(models.Model):
    nome = models.TextField()
    curso = models.CharField(max_length=255)
    foto = models.ImageField(upload_to='membros')

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Membro"
        verbose_name_plural = "Membros"

class Entrada(models.Model):
    membro = models.ForeignKey(Membro, on_delete=models.PROTECT)
    data = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return 'Entrada em {} às {}'.format(self.data.date(), self.data.time())

    class Meta:
        verbose_name = "Entrada"
        verbose_name_plural = "Entradas"
