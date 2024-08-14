from django.urls import path
from . import views

urlpatterns = [
    path('solicitar-exames/', views.solicitar_exames, name='solicitar_exames'),
    path('fechar-pedido/', views.fechar_pedido, name='fechar_pedido'),
    path('gerenciar-pedidos/', views.gerenciar_pedidos, name='gerenciar_pedidos'),
    path('cancelar-pedido/<int:pedido_id>/', views.cancelar_pedido, name='cancelar_pedido'),
    path('gerenciar-exames/', views.gerenciar_exames, name='gerenciar_exames'),
    path('visualizar-pdf/<int:exame_id>', views.visualizar_pdf, name='visualizar_pdf'),
    path('solicitar-senha-exame/<int:exame_id>', views.solicitar_senha_exame, name='solicitar_senha_exame'),
    path('gerar-acesso-medico/', views.gerar_acesso_medico, name='gerar_acesso_medico'),
    path('acesso-medico/<str:token>/', views.acesso_medico, name='acesso_medico'),
]