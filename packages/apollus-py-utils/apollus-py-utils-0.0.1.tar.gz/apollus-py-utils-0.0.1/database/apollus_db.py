import boto3
import psycopg2

class ApollusBD:
    """"Classe de conexão com o banco de dados Apollus.
    Ao informar um ambiente e cliente é retornada a propriedade credenciais, que contém:
    - url: URL de conexão com a base de dados do cliente;
    - basedados: Nome da Base de Dados do cliente;
    - usuario: Usuário utilizado para conectar na Base de Dados do cliente;
    - senha: Senha utilizada para conectar na Base de Dados do cliente;
    """
    _credenciais = None
    _conexao = None

    def __init__(self, ambiente: str, cliente: str):
        if ambiente.lower() == "local":
            saas_url = "localhost"
            saas_base_dados = "apollus-saas"
            saas_usuario = "postgres"
            saas_senha = "root"

        # Obtém os dados conexão através do SAAS.
        conexao = psycopg2.connect(host=saas_url,
                                   database=saas_base_dados,
                                   user=saas_usuario,
                                   password=saas_senha)
        cursor = conexao.cursor()
        sql = "select url, username, password from data_source_config where name = '{0}'".format(cliente)
        cursor.execute(sql)
        (cliente_url, cliente_usuario, cliente_senha) = cursor.fetchone()
        cliente_url_f = cliente_url.replace("jdbc:postgresql://", "").split(":")[0]
        cliente_base_dados = cliente_url.split("/")[-1]
        cursor.close()
        conexao.close()

        self._credenciais = {
            "url": cliente_url_f,
            "baseDados": cliente_base_dados,
            "usuario": cliente_usuario,
            "senha": cliente_senha
        }

    def obtem_cursor(self):
        """Função que retorna o cursor a ser utilizado para realizar consulta nos dados da base de dados do cliente."""
        retorno = None
        try:
            self._conexao = psycopg2.connect(host=self._credenciais["url"],
                                             database=self._credenciais["baseDados"],
                                             user=self._credenciais["usuario"],
                                             password=self._credenciais["senha"])
            retorno = self._conexao.cursor()
        finally:
            return retorno

    def encerra_conexao(self):
        """Função que encerra a conexão com a base de dados do cliente."""
        # Primeiro salva.
        self._conexao.commit()
        # Após isto, encerra.
        self._conexao.close()
