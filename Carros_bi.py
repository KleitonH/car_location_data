import os
import bisect
from collections import defaultdict
from loading_animation import start_animation, stop_animation

clear = lambda: os.system('clear')

def busca_binaria(lista, chave, indice):
    """
    Função de busca binária genérica para encontrar a primeira ocorrência
    de um estado ou cidade em uma lista de linhas (campos separados por ';').
    
    lista: A lista de linhas.
    chave: O valor a ser buscado (estado ou cidade).
    indice: O índice do campo a ser comparado (0 para estado, 1 para cidade).
    """
    esquerda, direita = 0, len(lista) - 1
    while esquerda <= direita:
        meio = (esquerda + direita) // 2
        campo_meio = lista[meio].split(';')[indice].strip().lower()
        if campo_meio < chave.lower():
            esquerda = meio + 1
        elif campo_meio > chave.lower():
            direita = meio - 1
        else:
            # Encontramos o item, agora vamos retroceder para encontrar a primeira ocorrência
            while meio > 0 and lista[meio - 1].split(';')[indice].strip().lower() == chave.lower():
                meio -= 1
            return meio  # Retorna o índice da primeira ocorrência
    return -1  # Retorna -1 se não encontrar


def filtrar_carros_binario(estados=None, cidades=None, modelo=None, ano=None):
    # Lista para armazenar os resultados filtrados
    resultados = []
    quantidade_total = 0.0  # Variável para armazenar a soma das quantidades
    ranking_marcas = defaultdict(float)
    modelos_por_marca = defaultdict(list)

    # Abra o arquivo em modo de leitura
    with open('./Carros_2024.txt', 'r') as file:
        linhas = file.readlines()

    # Se um estado foi fornecido, fazemos a busca binária
    if estados:
        for estado in estados:
            indice_estado = busca_binaria(linhas, estado, 0)  # 0 é o índice do estado no arquivo
            if indice_estado != -1:
                # Percorremos todas as linhas a partir da primeira ocorrência do estado
                for linha in linhas[indice_estado:]:
                    campos = linha.strip().split(';')
                    estado_carro = campos[0].strip()

                    # Parar quando não for mais o mesmo estado
                    if estado_carro.lower() != estado.lower():
                        break

                    # Aplicar filtros para cidade, modelo e ano
                    cidade_carro = campos[1].strip()
                    modelo_carro = campos[2].strip()
                    ano_carro = campos[3].strip()
                    quantidade = campos[4].strip()

                    if (cidades is None or any(cidade.lower() in cidade_carro.lower() for cidade in cidades)) and \
                       (modelo is None or modelo == "" or modelo.lower() in modelo_carro.lower()) and \
                       (ano is None or ano == "" or ano == ano_carro):

                        resultados.append(linha)
                        
                        # Somar a quantidade
                        try:
                            quantidade_float = float(quantidade)
                            quantidade_total += quantidade_float

                            # Usar o modelo completo (incluindo a "/")
                            marca_completa = modelo_carro.split()[0]

                            # Somar a quantidade para esse modelo no ranking
                            ranking_marcas[marca_completa] += quantidade_float
                            modelos_por_marca[marca_completa].append(modelo_carro + ' ' + ano_carro + ' ' + quantidade)

                        except ValueError:
                            print(f"Erro na conversão da quantidade na linha: {linha}")
                            continue  # Pula a linha se houver um erro na conversão de quantidade
    else:
        # Se não há estados, aplicar o filtro de maneira linear
        for linha in linhas:
            campos = linha.strip().split(';')
            estado_carro = campos[0].strip()
            cidade_carro = campos[1].strip()
            modelo_carro = campos[2].strip()
            ano_carro = campos[3].strip()
            quantidade = campos[4].strip()

            if (cidades is None or any(cidade.lower() in cidade_carro.lower() for cidade in cidades)) and \
               (modelo is None or modelo == "" or modelo.lower() in modelo_carro.lower()) and \
               (ano is None or ano == "" or ano == ano_carro):

                resultados.append(linha)

                # Somar a quantidade
                try:
                    quantidade_float = float(quantidade)
                    quantidade_total += quantidade_float

                    # Usar o modelo completo (incluindo a "/")
                    marca_completa = modelo_carro.split()[0]

                    # Somar a quantidade para esse modelo no ranking
                    ranking_marcas[marca_completa] += quantidade_float
                    modelos_por_marca[marca_completa].append(modelo_carro + ' ' + ano_carro + ' ' + quantidade)

                except ValueError:
                    print(f"Erro na conversão da quantidade na linha: {linha}")
                    continue  # Pula a linha se houver um erro na conversão de quantidade

    return resultados, quantidade_total, ranking_marcas, modelos_por_marca

def imprimir_resultados(resultados):
    if resultados:
        print("Resultados encontrados:")
        for resultado in resultados:
            print(resultado)
    else:
        print("Nenhum resultado encontrado.")


def imprimir_quantidade(quantidade_total):
    print(f"Quantidade total: {quantidade_total}")
    return

def imprimir_ranking_geral(ranking_marcas, limite=500):
    print("\nRanking Geral das Marcas:")
    ranking_ordenado = sorted(ranking_marcas.items(), key=lambda item: item[1], reverse=True)
    for posicao, (marca, quantidade) in enumerate(ranking_ordenado[:limite], start=1):
        print(f"{posicao}º - {marca}: {quantidade} unidades")


def imprimir_ranking_modelo(ranking_marcas, modelos_por_marca, limite=500):
    print("\nRanking por Modelo:")
    ranking_ordenado = sorted(ranking_marcas.items(), key=lambda item: item[1], reverse=True)
    for posicao, (marca, quantidade_total) in enumerate(ranking_ordenado[:limite], start=1):
        print(f"{posicao}º - {marca}: {quantidade_total} unidades")
        subranking_modelos = defaultdict(float)
        for modelo_completo in modelos_por_marca[marca]:
            partes = modelo_completo.split()
            modelo = ' '.join(partes[:-2])
            quantidade = float(partes[-1])
            subranking_modelos[modelo] += quantidade
        subranking_ordenado = sorted(subranking_modelos.items(), key=lambda item: item[1], reverse=True)
        for sub_posicao, (modelo, quantidade) in enumerate(subranking_ordenado, start=1):
            print(f"    {sub_posicao}. {modelo}: {quantidade} unidades")


def executar_filtro(estados_input, cidades_input, modelo_input, ano_input):

    def campo_filtro(campos_input, nome):
        if escolha_menu_principal == '1':
            campos_input = input(f"\nDigite o {nome}, ou {nome}s usando vírgula (ou deixe em branco para ignorar): ")
        if campos_input:
            campos_input = [item.strip() for item in campos_input.split(',')]
        else:
            campos_input = None
        return campos_input
    
    estados_input = campo_filtro(estados_input, "estado")
    cidades_input = campo_filtro(cidades_input, "cidade")
    modelo_input = input("\nDigite o modelo do carro (ou deixe em branco para ignorar): ")
    ano_input = input("\nDigite o ano do carro (ou deixe em branco para ignorar): ")

    estados_input = estados_input if estados_input else None
    cidades_input = cidades_input if cidades_input else None
    modelo_input = modelo_input if modelo_input else None
    ano_input = ano_input if ano_input else None

    resultados_filtrados, quantidade_total, ranking_marcas, modelos_por_marca = filtrar_carros_binario(estados_input, cidades_input, modelo_input, ano_input)

    ranking_armazenado = ("geral", ranking_marcas) if not modelo_input else ("modelo", ranking_marcas, modelos_por_marca)

    escolha = ""
    while escolha != '4':
        escolha = input("Digite '1' para imprimir os resultados, '2' para contar as ocorrências, '3' para imprimir o ranking ou '4' para sair: ")
        if escolha == '1':
            imprimir_resultados(resultados_filtrados)
            escolha2 = input("Gostaria de ver a quantidade de carros? '1' para sim, '2' para não: ")
            if escolha2 == '1':
                imprimir_quantidade(quantidade_total)
        elif escolha == '2':
            imprimir_quantidade(quantidade_total)
        elif escolha == '3':
            if ranking_armazenado[0] == "geral":
                imprimir_ranking_geral(ranking_armazenado[1], limite=500)
            else:
                imprimir_ranking_modelo(ranking_armazenado[1], ranking_armazenado[2], limite=500)
        elif escolha == '4':
            clear()
        else:
            print("Escolha inválida. Tente novamente.")


escolha_menu_principal = input("Boas-vindas!\n1 - Inserir informações\n2 - Pesquisa atalho\nEscolha a opção passando o número correspondente: ")

estados_input = None
cidades_input = None
modelo_input = None
ano_input = None

estados_hotspot = "rio grande do sul, santa catarina"
cidades_hotspot = "arroio do sal, capao da canoa, dom pedro de alcantara, itati, mampituba, morrinhos do sul, praia grande, sao joao do sul, terra de areia, torres, tres cachoeiras, tres forquilhas, xangri-la"

if escolha_menu_principal == '1':
    pass
elif escolha_menu_principal == '2':
    escolha_atalho = input("\nDentre as escolhas abaixo, escolha o nome da zona que deseja:\n1 - Hotspot (As principais cidades de interesse comercial)\nInsira o número da opção: ")
    if escolha_atalho == '1' or escolha_atalho.lower == 'hotspot':
        estados_input = estados_hotspot
        cidades_input = cidades_hotspot

    else:
        print("Opção inválida")
else:
    print("Opção inválida")

executar_filtro(estados_input, cidades_input, modelo_input, ano_input)
