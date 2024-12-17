from django.db import models

# As classes do modelo do sistema são definidas neste arquivo models.py
# Cada classe representa uma tabela do banco de dados MySQL.

# ============================================
# Modelo da tabela "usuario"
# ============================================
class Usuario(models.Model):
    # Campo 'username' usado como chave primária da tabela.
    username = models.CharField(primary_key=True, max_length=50)
    
    # Campo para armazenar o nome completo do usuário.
    nome = models.CharField(max_length=100)
    
    # Campo para armazenar o e-mail do usuário. Deve ser único.
    email = models.EmailField(max_length=254, unique=True)
    
    # Campo para armazenar a senha do usuário.
    senha = models.CharField(max_length=128)
    
    # Campo para armazenar o telefone. É opcional (pode ser nulo ou vazio).
    telefone = models.CharField(max_length=15, blank=True, null=True)

    # Opções predefinidas para o campo 'tipo_usuario'.
    # Define se o usuário é um paciente ou um prestador.
    TIPO_USUARIO_CHOICES = [
        ('paciente', 'Paciente'),
        ('prestador', 'Prestador'),
    ]
    tipo_usuario = models.CharField(max_length=9, choices=TIPO_USUARIO_CHOICES)

    # Opções predefinidas para o campo 'genero'.
    GENERO_CHOICES = [
        ('masculino', 'Masculino'),
        ('feminino', 'Feminino'),
    ]
    genero = models.CharField(max_length=9, choices=GENERO_CHOICES)

    # Campo para armazenar a data de nascimento do usuário.
    data_nascimento = models.DateField()

    class Meta:
        managed = False  # Indica que o Django não deve criar ou gerenciar a tabela.
        db_table = 'usuario'  # Nome da tabela no banco de dados.

# ============================================
# Modelo da tabela "paciente"
# ============================================
class Paciente(models.Model):
    # Campo 'username' como chave primária explícita.
    # Relacionado ao campo 'username' da tabela Usuario.
    username = models.CharField(max_length=150, primary_key=True)

    # Campo 'cpf' que, junto com 'username', forma a chave composta.
    cpf = models.CharField(max_length=11)

    # Campo de texto para armazenar o histórico médico do paciente.
    historico_medico = models.TextField(null=True, blank=True)

    # Campo de texto opcional para observações.
    observacoes = models.TextField(null=True, blank=True)

    class Meta:
        managed = False  # O Django não gerencia a tabela no banco.
        db_table = 'paciente'  # Nome da tabela no banco de dados.
        unique_together = (('username', 'cpf'),)  # Define a chave composta.

    # Método __str__ para representar o modelo como string.
    def __str__(self):
        return f"{self.username} - {self.cpf}"

# ============================================
# Modelo da tabela "prestador"
# ============================================
class Prestador(models.Model):
    # Campo 'username' usado como chave primária.
    username = models.CharField(max_length=50, primary_key=True)

    # Campo para armazenar o CNPJ do prestador.
    cnpj = models.CharField(max_length=14)

    # Campo de texto opcional para armazenar as qualificações do prestador.
    qualificacoes = models.TextField(null=True, blank=True)

    class Meta:
        managed = False  # O Django não gerencia a tabela.
        db_table = 'prestador'  # Nome da tabela no banco de dados.
        unique_together = (('username', 'cnpj'),)  # Define a chave composta.

    # Método __str__ para representação textual do modelo.
    def __str__(self):
        return f"{self.username} - {self.cnpj}"

# ============================================
# Modelo da tabela "servico"
# ============================================
class Servico(models.Model):
    # Campo 'username' do prestador associado ao serviço.
    username = models.CharField(max_length=50, primary_key=True)

    # Campo 'cnpj' associado ao prestador.
    cnpj = models.CharField(max_length=14)

    # Campo 'nome_servico' para descrever o serviço oferecido.
    nome_servico = models.CharField(max_length=100)

    class Meta:
        managed = False  # O Django não gerencia a tabela.
        db_table = 'servico'  # Nome da tabela no banco de dados.
        unique_together = (('username', 'cnpj', 'nome_servico'),)  # Define chave composta.

    # Método __str__ para retornar uma representação textual do serviço.
    def __str__(self):
        return f"{self.nome_servico} ({self.username}, {self.cnpj})"

# ============================================
# Modelo da tabela "agendamento"
# ============================================
class Agendamento(models.Model):
    # Campos que identificam o paciente relacionado ao agendamento.
    username_paciente = models.CharField(max_length=50)
    cpf = models.CharField(max_length=11)

    # Campos que identificam o prestador relacionado ao agendamento.
    username_prestador = models.CharField(max_length=50)
    cnpj = models.CharField(max_length=14)

    # Nome do serviço que está sendo agendado.
    nome_servico = models.CharField(max_length=100)

    # Data do agendamento.
    data_agendamento = models.DateField()

    class Meta:
        managed = False  # O Django não gerencia a tabela.
        db_table = 'agendamento'  # Nome da tabela no banco de dados.
        unique_together = (('username_paciente', 'cpf', 'username_prestador', 
                            'cnpj', 'nome_servico', 'data_agendamento'),)  # Define chave composta.

    # Método __str__ para representação textual do agendamento.
    def __str__(self):
        return f"Agendamento: {self.username_paciente} -> {self.username_prestador} ({self.nome_servico} em {self.data_agendamento})"
