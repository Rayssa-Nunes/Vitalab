from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from secrets import token_urlsafe
from django.utils import timezone
from datetime import timedelta

class TiposExames(models.Model):
    tipo_choices = (
        ('I', 'Exame de imagem'),
        ('S', 'Exame de sangue')
    )
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=1, choices=tipo_choices)
    preco = models.FloatField()
    disponivel = models.BooleanField(default=True)
    horario_inicial = models.IntegerField()
    horario_final = models.IntegerField()

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Tipo de Exame'
        verbose_name_plural = 'Tipos de Exames'

class SolicitacaoExame(models.Model):
    choice_status = (
        ('E', 'Em análise'),
        ('F', 'Finalizado')
    )
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    exame = models.ForeignKey(TiposExames, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=2, choices=choice_status)
    resultado = models.FileField(upload_to="resultados", null=True, blank=True)
    requer_senha = models.BooleanField(default=False)
    senha = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return f'{self.usuario} | {self.exame.nome}'
    
    class Meta:
        verbose_name = 'Solicitacao de Exame'
        verbose_name_plural = 'Solicitacoes de Exames'

    def badge_template(self):
        if self.status == 'E':
            classe = 'bg-warning'
            texto = 'Em análise'
        elif self.status == 'F':
            classe = 'bg-success'
            texto = 'Finalizado'
        return mark_safe(f'<span class="badge {classe}">{texto}</span>')

class PedidosExames(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    exames = models.ManyToManyField(SolicitacaoExame)
    agendado = models.BooleanField(default=True)
    data = models.DateField()

    def __str__(self):
        return f'{self.usuario} | {self.data}'
    
    class Meta:
        verbose_name = 'Pedido de Exame'
        verbose_name_plural = 'Pedidos de Exames'

class AcessoMedico(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    identificacao = models.CharField(max_length=50)
    tempo_de_acesso = models.IntegerField() # Em horas
    criado_em = models.DateTimeField()
    data_exames_iniciais = models.DateField()
    data_exames_finais = models.DateField()
    token = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.token
    
    class Meta:
        verbose_name = 'Acesso Medico'
        verbose_name_plural = 'Acessos Medicos'
    
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = token_urlsafe(6)

        super(AcessoMedico, self).save(*args, **kwargs)
    
    @property
    def status(self):
        return 'Expirado' if timezone.now() > (self.criado_em + timedelta(self.tempo_de_acesso)) else 'Ativo'
    
    @property
    def url(self):
        return f'http://127.0.0.1:8000/exames/acesso-medico/{self.token}'
