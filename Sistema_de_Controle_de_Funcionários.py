import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()


conexao = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)

print('Conectado com sucesso!')

cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS funcionarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(20) UNIQUE NOT NULL,
    data_nascimento DATE,
    cargo VARCHAR(100),
    salario DECIMAL(10,2)
)
""")

conexao.commit()

print('Tabela criada com sucesso!')


def menu():
    print('===== SISTEMA DE FUNCIONÁRIOS =====')
    print('1 - Cadastrar funcionário\n'
    '2 - Listar funcionários\n'
    '3 - Pesquisar funcionário\n'
    '4 - Alterar salário\n'
    '5 - Demitir funcionário\n'
    '6 - Estatísticas\n'
    '7 - Sair\n')
class Funcionario:
    def __init__(self):
        self.nome= ''
        self.cpf = ''
        self.data_nascimento = ''
        self.cargo = ''
        self.salario = 0

    def dados_funcionario(self):
        self.nome = input('qual o seu nome?').strip()
        self.cpf = input('qual a sua CPF?')
        if not self.cpf.isdigit():
            print('o cpf deve conter apenas numeros! ')
            return False
        self.data_nascimento = input('qual a sua data de nascimento?(AAAA/MM/DD)')
        self.cargo=input('cargo: ')
        try:
            self.salario = float(input('salario: '))
        except ValueError:
            print('digite um salario valido! ')
            return False
        return True
    def mostrar_dados(self):
        return (
            f'nome = {self.nome}\n'
            f'cpf = {self.cpf}\n'
            f'data de nascimento = {self.data_nascimento}\n'
            f'salario = {self.salario:.2f}\n'
            f'cargo = {self.cargo}'
        )

class Empresa:

       def __init__(self):
         pass

       def cadastro(self):
           funcionario = Funcionario()
           if not funcionario.dados_funcionario():
               return

           sql ="""     
           INSERT INTO funcionarios
           (nome, cpf, data_nascimento, cargo, salario)
           values (%s,%s,%s,%s,%s)
            """

           valores =(
               funcionario.nome,
               funcionario.cpf,
               funcionario.data_nascimento,
               funcionario.cargo,
               funcionario.salario
           )

           cursor.execute(sql, valores)
           conexao.commit()
           print('funcionario cadastrado com sucesso!')


       def listar(self):
           sql = """
           select nome, cpf, data_nascimento, cargo, salario
           from funcionarios
           """

           cursor.execute(sql)

           funcionarios = cursor.fetchall()

           if not funcionarios:
               print('nenhum funcionario registrado!')
               return

           for funcionario in funcionarios:
               print(f'Nome = {funcionario[0]}')
               print(f'CPF = {funcionario[1]}')
               print(f'Data de nascimento = {funcionario[2]}')
               print(f'Cargo = {funcionario[3]}')
               print(f'Salário = R$ {funcionario[4]:.2f}')
               print('==========================')



       def Pesquisar(self):
           print('===bem vindo a pesquisa de funcionarios===')

           procurar_cpf = input('CPF:')

           sql = """ 
           select nome, cpf, data_nascimento, cargo, salario
           from funcionarios
           where cpf = %s 
           """

           cursor.execute(sql,(procurar_cpf,))

           funcionario = cursor.fetchone()

           if funcionario:
               print(f'nome = {funcionario[0]}')
               print(f'cpf = {funcionario[1]}')
               print(f'data de nascimento = {funcionario[2]}')
               print(f'cargo = {funcionario[3]}')
               print(f'salario = {funcionario[4]:.2f}')
           else:
               print('cpf nao cadastrado! ')
       def Novo_salario(self):
           try:
               cpf_salario = input('cpf: ')

               novo_salario = float(input('novo salario: '))

               sql = """
               update funcionarios
               set salario = %s
               where cpf = %s    
               """

               valores = (novo_salario,cpf_salario)

               cursor.execute(sql, valores)
               conexao.commit()

               if cursor.rowcount > 0:
                   print('salario atualizado com sucesso! ')
               else:
                   print('cpf nao cadastrado! ')
           except:
               print('digite numeros inteiros,sem espaços/traços! ')


       def Demitir_funcionario(self):
            try:
                demitir_cpf = str(input('cpf: ').strip())

                sql = """ 
                delete from funcionarios
                where cpf = %s                
                """

                valores = (demitir_cpf,)

                cursor.execute(sql,valores)
                conexao.commit()

                if cursor.rowcount > 0:
                    print('funcionario demitido com sucesso! ')
                else:
                    print('cpf nao cadastrado!')


            except:
                print('digite apenas numeros inteiros, sem traços')

       def estatisticas(self):

           sql = """
           select
                count(*),
                max(salario),
                min(salario),
                avg(salario)
           from funcionarios
            """
           cursor.execute(sql)

           resultado = cursor.fetchone()

           total = resultado[0]
           maior = resultado[1]
           menor = resultado[2]
           media = resultado[3]

           if total == 0:
               print('nenhum funcionario registrado! ')
               return

           print(f'Temos registrados: {total}')
           print(f'Maior salário = R$ {maior:.2f}')
           print(f'Menor salário = R$ {menor:.2f}')
           print(f'Média salarial = R$ {media:.2f}')


empresa = Empresa()

while True:
    menu()
    try:
        op=int(input('escolha: '))
    except ValueError:
        print('digite apenas numeros inteiros: [1/7] ')
        continue
    if op == 1:
        empresa.cadastro()
    elif op == 2:
        empresa.listar()
    elif op == 3:
       empresa.Pesquisar()
    elif op == 4:
       empresa.Novo_salario()
    elif op == 5:
       empresa.Demitir_funcionario()
    elif op == 6:
       empresa.estatisticas()
    elif op == 7:
        print('programa finalizado com sucesso! ')
        break
    else:
        print('opção invalida! ')