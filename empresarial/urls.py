from django.urls import path
from . import views

urlpatterns = [
    path('gerenciar-clientes/', views.gerenciar_clientes, name="gerenciar_clientes"),
    path('cliente/<int:cliente_id>', views.cliente, name='cliente'),
    path('exame-cliente/<int:exame_id>', views.exame_cliente, name="exame_cliente"),
    path('proxy-pdf/<int:exame_id>', views.proxy_pdf, name="proxy_pdf"),
    path('gerar-senha/<int:exame_id>', views.gerar_senha, name='gerar_senha'),
    path('alterar-dados-exame/<int:exame_id>', views.alterar_dados_exame, name='alterar_dados_exame'),
]