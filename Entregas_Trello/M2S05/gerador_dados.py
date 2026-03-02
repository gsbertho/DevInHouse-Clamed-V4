#imports
import pandas as pd
import os

PATH_DADOS = os.path.join(os.getcwd(),'dados')
PATH_PRODUTOS = os.path.join(PATH_DADOS,'produtos.csv')
PATH_CLIENTES = os.path.join(PATH_DADOS,'clientes.csv')

def gerar_dados_iniciais() -> None:
    #df produtos

    produtos = pd.DataFrame(
        [
            {'id_produto': 1, 'nome': 'Arroz', 'preco': 4.90},
            {'id_produto': 2, 'nome': 'Feijao', 'preco': 9.90},
            {'id_produto': 3, 'nome': 'Macarrao', 'preco': 4.60}
        ]
    )

    clientes = pd.DataFrame(
        [
            {'id_cliente': 1, 'nome': 'Roberto Fernandes', 'endereco': 'Rua das Palmeiras, 120'},
            {'id_cliente': 2, 'nome': 'Marina Silva', 'endereco': 'Rua das Acacias, 25'},
            {'id_cliente': 3, 'nome': 'Raimundo Souza', 'endereco': 'Rua do Sol, 1310'},
        ]
    )

    print('Verificar dfs criados:')
    print(produtos)
    print(clientes)

    #gerar os arquivos csv a partir dos dfs criados
    produtos.to_csv(PATH_PRODUTOS,index=False)
    print('CSV criado: ',PATH_PRODUTOS)

    clientes.to_csv(PATH_CLIENTES,index=False)
    print('CSV criado: ',PATH_CLIENTES)

def gerar_mudancas() -> None:
     '''altera preço de produto, muda endereço e adiciona cliente.'''

     #conferencia existencia arquivos
     if not os.path.exists(PATH_PRODUTOS) or not os.path.exists(PATH_CLIENTES):
          raise FileNotFoundError('Arquivo CSV não encontrado, gerar os dados primeiro')
     
     produtos = pd.read_csv(PATH_PRODUTOS)
     clientes = pd.read_csv(PATH_CLIENTES)

     #alterar preço do produto id 2
     produtos.loc[produtos['id_produto']==2,'preco'] = 8.90

     #alterar endereço do cliente id 3
     clientes.loc[clientes['id_cliente']==3,'endereco'] = 'Avenida das Maritacas, 123'

     #adicionar novo cliente
     #gerar df do novo cliente
     novo_cliente = pd.DataFrame([
          {'id_cliente': 4, 'nome': 'Rubens Andrade', 'endereco': 'Rua Urubici, 1200'}
     ])

     clientes = pd.concat([clientes, novo_cliente], ignore_index=True)
    
     produtos.to_csv(PATH_PRODUTOS, index=False)
     clientes.to_csv(PATH_CLIENTES, index=False)

     print('Mudanças aplicadas com sucesso.')

#gerar primeiros CSVs
gerar_dados_iniciais()

#gerar as mudanças
#gerar_mudancas()