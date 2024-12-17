from django.urls import path
from . import views  # Importa as views definidas no arquivo views.py

# Lista de rotas da aplicação
urlpatterns = [
    # Página inicial
    path('', views.index, name='index'),

    # Rota para cadastro de usuário
    path('cadastrar_usuario/', views.cadastrar_usuario, name='cadastrar_usuario'),

    # Rota para cadastro de paciente
    path('cadastrar_paciente/', views.cadastrar_paciente, name='cadastrar_paciente'),

    # Rota para cadastro de prestador
    path('cadastrar_prestador/', views.cadastrar_prestador, name='cadastrar_prestador'),

    # Rota para cadastro de serviço oferecido pelo prestador
    path('cadastrar_servico/', views.cadastrar_servico, name='cadastrar_servico'),

    # Rota para login do paciente
    path('login_paciente/', views.login_paciente, name='login_paciente'),

    # Rota para listar os serviços disponíveis
    path('agendar_servico/', views.agendar_servico, name='agendar_servico'),

    # Rota para confirmar o agendamento de um serviço
    # Recebe parâmetros: username_prestador, cnpj e nome_servico
    path(
        'confirmar_agendamento/<str:username_prestador>/<str:cnpj>/<str:nome_servico>/',
        views.confirmar_agendamento,
        name='confirmar_agendamento'
    ),

    # Rota para salvar o agendamento no banco de dados
    path('salvar_agendamento/', views.salvar_agendamento, name='salvar_agendamento'),
]
