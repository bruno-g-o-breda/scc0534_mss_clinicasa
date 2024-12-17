from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Usuario, Paciente, Prestador, Servico, Agendamento
from django.core.exceptions import ValidationError
from datetime import date
from datetime import datetime

# Exibe a página inicial do sistema
def index(request):
    return render(request, "index.html")

# Processa e salva o cadastro de um novo usuário
def cadastrar_usuario(request):
    if request.method == 'POST':
        # Captura os dados enviados pelo formulário
        username = request.POST.get('username')
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        telefone = request.POST.get('telefone')
        tipo_usuario = request.POST.get('tipo_usuario')
        genero = request.POST.get('genero')
        data_nascimento = request.POST.get('data_nascimento')

        # Cria uma instância do modelo Usuario
        usuario = Usuario(
            username=username,
            nome=nome,
            email=email,
            senha=senha,
            telefone=telefone,
            tipo_usuario=tipo_usuario,
            genero=genero,
            data_nascimento=data_nascimento
        )
        
        try:
            # Valida e salva o usuário
            usuario.full_clean() # Valida os campos do objeto
            usuario.save() # Salva o usuário no banco
            messages.success(request, "Usuário cadastrado com sucesso!")
            return redirect('cadastrar_usuario')  # Redireciona para o mesmo formulário após o cadastro
        except ValidationError as e:
            # Trata erros de validação
            messages.error(request, f"Erro ao cadastrar usuário: {e.message_dict}")
    
    return render(request, 'cadastrar_usuario.html')  # Renderiza o formulário

# Permite cadastrar um paciente associado a um usuário existente.
def cadastrar_paciente(request):
    if request.method == 'POST':
        # Captura os dados enviados pelo formulário
        username = request.POST.get('username')
        cpf = request.POST.get('cpf')
        historico_medico = request.POST.get('historico_medico')
        observacoes = request.POST.get('observacoes')

        try:
            # Verifica se o usuário existe no banco de dados
            usuario = Usuario.objects.get(username=username)
            
            # Verifica se o tipo do usuário é 'paciente'
            if usuario.tipo_usuario != 'paciente':
                messages.error(request, "O usuário fornecido não é do tipo 'paciente'.")
                return redirect('cadastrar_paciente')
            
            # Cria uma instância do modelo Paciente
            paciente = Paciente(
                username=username,
                cpf=cpf,
                historico_medico=historico_medico,
                observacoes=observacoes
            )

            # Valida e salva o paciente
            paciente.full_clean()
            paciente.save()
            messages.success(request, "Paciente cadastrado com sucesso!")
            return redirect('cadastrar_paciente')  # Redireciona para o mesmo formulário
        except Usuario.DoesNotExist:
            messages.error(request, "O usuário fornecido não existe. Cadastre o usuário primeiro.")
        except ValidationError as e:
            messages.error(request, f"Erro ao cadastrar paciente: {e.message_dict}")

    return render(request, 'cadastrar_paciente.html')  # Renderiza o formulário

# Permite cadastrar um prestador associado a um usuário existente.
def cadastrar_prestador(request):
    if request.method == 'POST':
        # Captura os dados enviados pelo formulário
        username = request.POST.get('username')
        cnpj = request.POST.get('cnpj')
        qualificacoes = request.POST.get('qualificacoes')

        try:
            # Verifica se o usuário existe no banco de dados
            usuario = Usuario.objects.get(username=username)

            # Verifica se o tipo do usuário é 'prestador'
            if usuario.tipo_usuario != 'prestador':
                messages.error(request, "O usuário fornecido não é do tipo 'prestador'.")
                return redirect('cadastrar_prestador')

            # Cria uma instância do modelo Prestador
            prestador = Prestador(
                username=username,
                cnpj=cnpj,
                qualificacoes=qualificacoes
            )

            # Valida e salva o prestador
            prestador.full_clean()
            prestador.save()
            messages.success(request, "Prestador cadastrado com sucesso!")
            return redirect('cadastrar_prestador')  # Redireciona para o mesmo formulário
        except Usuario.DoesNotExist:
            messages.error(request, "O usuário fornecido não existe. Cadastre o usuário primeiro.")
        except ValidationError as e:
            messages.error(request, f"Erro ao cadastrar prestador: {e.message_dict}")

    return render(request, 'cadastrar_prestador.html')  # Renderiza o formulário

# Permite cadastrar um serviço oferecido por um prestador.
def cadastrar_servico(request):
    if request.method == 'POST':
        # Captura os dados enviados pelo formulário
        username = request.POST.get('username')
        cnpj = request.POST.get('cnpj')
        nome_servico = request.POST.get('nome_servico')

        try:
            # Verifica se o prestador existe no banco de dados
            prestador = Prestador.objects.get(username=username, cnpj=cnpj)

            # Cria uma instância do modelo Servico
            servico = Servico(
                username=username,
                cnpj=cnpj,
                nome_servico=nome_servico
            )

            # Valida e salva o serviço
            servico.full_clean()
            servico.save()
            messages.success(request, "Serviço cadastrado com sucesso!")
            return redirect('cadastrar_servico')  # Redireciona para o mesmo formulário
        except Prestador.DoesNotExist:
            messages.error(request, "O prestador fornecido não existe ou os dados estão incorretos.")
        except ValidationError as e:
            messages.error(request, f"Erro ao cadastrar serviço: {e.message_dict}")

    return render(request, 'cadastrar_servico.html')  # Renderiza o formulário


# Permite que um paciente faça login no sistema.
def login_paciente(request):
    if request.method == 'POST':
        # Captura os dados do formulário
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        try:
            # Verifica se o usuário existe e é do tipo 'paciente'
            usuario = Usuario.objects.get(username=username, senha=senha)

            if usuario.tipo_usuario != 'paciente':
                messages.error(request, "O usuário fornecido não é do tipo 'paciente'.")
                return redirect('login_paciente')

            # Armazena o username do paciente na sessão
            request.session['paciente_username'] = usuario.username

            # Login bem-sucedido, redireciona para a página de agendamento
            messages.success(request, "Login realizado com sucesso!")
            return redirect('agendar_servico')

        except Usuario.DoesNotExist:
            messages.error(request, "Credenciais inválidas. Verifique o username e a senha.")
    
    return render(request, 'login_paciente.html')  # Renderiza o formulário de login

# Agendar serviço
def agendar_servico(request):
    servicos = Servico.objects.all()
    return render(request, 'agendar_servico.html', {'servicos': servicos})

def confirmar_agendamento(request, username_prestador, cnpj, nome_servico):
    if not request.session.get('paciente_username'):
        messages.error(request, "Você precisa estar logado como paciente para agendar um serviço.")
        return redirect('login_paciente')

    # Recupera o serviço selecionado
    try:
        servico = Servico.objects.get(username=username_prestador, cnpj=cnpj, nome_servico=nome_servico)
    except Servico.DoesNotExist:
        messages.error(request, "O serviço selecionado não existe.")
        return redirect('agendar_servico')

    # Recupera o paciente logado
    paciente_username = request.session['paciente_username']
    try:
        paciente = Paciente.objects.get(username=paciente_username)
    except Paciente.DoesNotExist:
        messages.error(request, "Erro ao recuperar os dados do paciente.")
        return redirect('agendar_servico')

    # Dados para exibir no template de confirmação
    context = {
        'servico': servico,
        'paciente': paciente,
        'data_agendamento': date.today()
    }
    return render(request, 'confirmar_agendamento.html', context)

# Salvar agendamento
def salvar_agendamento(request):
    if request.method == 'POST':
        # Captura os dados enviados pelo formulário
        username_paciente = request.POST.get('username_paciente')
        cpf = request.POST.get('cpf')
        username_prestador = request.POST.get('username_prestador')
        cnpj = request.POST.get('cnpj')
        nome_servico = request.POST.get('nome_servico')
        data_agendamento = request.POST.get('data_agendamento')

        try:
            # Converte a data de agendamento para o formato correto
            data_agendamento = datetime.strptime(data_agendamento, "%Y-%m-%d").date()

            # Verifica se o paciente e o serviço existem
            paciente = Paciente.objects.get(username=username_paciente, cpf=cpf)
            servico = Servico.objects.get(username=username_prestador, cnpj=cnpj, nome_servico=nome_servico)

            # Cria uma instância do agendamento
            agendamento = Agendamento(
                username_paciente=username_paciente,
                cpf=cpf,
                username_prestador=username_prestador,
                cnpj=cnpj,
                nome_servico=nome_servico,
                data_agendamento=data_agendamento
            )

            # Valida e salva o agendamento
            agendamento.full_clean()
            agendamento.save()

            messages.success(request, "Agendamento realizado com sucesso!")
            return redirect('agendar_servico')

        except ValueError as e:
            messages.error(request, f"Formato de data inválido: {str(e)}")
        except Paciente.DoesNotExist:
            messages.error(request, "O paciente informado não existe.")
        except Servico.DoesNotExist:
            messages.error(request, "O serviço selecionado não existe.")
        except Exception as e:
            messages.error(request, f"Erro ao salvar agendamento: {str(e)}")

    return redirect('agendar_servico')