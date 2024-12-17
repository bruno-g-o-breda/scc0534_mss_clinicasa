CREATE TABLE usuario (
	username VARCHAR(50),
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(254) NOT NULL,
    senha VARCHAR(128) NOT NULL,
    telefone VARCHAR(15),
    tipo_usuario VARCHAR(9) NOT NULL
		CHECK(tipo_usuario IN('paciente', 'prestador')),
    data_nascimento DATE NOT NULL,
	genero VARCHAR(9) NOT NULL
		CHECK(genero IN('masculino', 'feminino')),
    
    CONSTRAINT pk_username
    PRIMARY KEY (username)
);

CREATE TABLE paciente(
	username VARCHAR(50) NOT NULL,
    cpf VARCHAR(11) NOT NULL,
    historico_medico TEXT NOT NULL,
    observacoes TEXT,
    CONSTRAINT pk_paciente
		PRIMARY KEY (username, cpf),
	CONSTRAINT fk_paciente
    FOREIGN KEY (username) REFERENCES usuario(username)
);

CREATE TABLE prestador (
    username VARCHAR(50) NOT NULL,
    cnpj VARCHAR(14) NOT NULL,
    qualificacoes TEXT,
    PRIMARY KEY (username, cnpj),
    FOREIGN KEY (username) REFERENCES Usuario(username)
);

CREATE TABLE servico(
	username VARCHAR(50) NOT NULL,
    cnpj VARCHAR(14) NOT NULL,
    nome_servico VARCHAR(100),
    CONSTRAINT pk_serviço
		PRIMARY KEY (username, cnpj, nome_servico),
	CONSTRAINT fk_servico
		FOREIGN KEY (username, cnpj) REFERENCES prestador(username, cnpj)
);

CREATE TABLE agendamento(
	username_paciente VARCHAR(50) not null,
    cpf varchar(11) not null,
    username_prestador varchar(50) not null,
    cnpj varchar(14) not null,
    nome_servico varchar(100) not null,
    data_agendamento date not null,
    constraint pk_agendamento
		primary key (username_paciente, cpf, username_prestador, cnpj, nome_servico, data_agendamento),
	constraint fk_paciente_agendamento
		foreign key (username_paciente, cpf) references paciente(username, cpf),
	constraint fk_servico_agendamento
		foreign key (username_prestador, cnpj, nome_servico) references servico(username, cnpj, nome_servico)
	);
