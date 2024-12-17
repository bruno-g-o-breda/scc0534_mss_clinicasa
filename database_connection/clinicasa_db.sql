-- Criação do banco de dados no mysql com permissões para caracteres especiais
CREATE DATABASE clinicasa_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Criando usuários e concedendo permissoes
CREATE USER 'clinicasa_user'@'localhost' IDENTIFIED BY 'senha';
GRANT ALL PRIVILEGES ON clinicasa_db.* TO 'clinicasa_user'@'localhost';
FLUSH PRIVILEGES;
