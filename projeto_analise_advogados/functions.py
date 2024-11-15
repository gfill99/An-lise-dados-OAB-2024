import pandas as pandas
import matplotlib.pyplot as plt
import numpy as np

# Função para criar pirâmide etária por estado
def criar_piramide_etaria(df, estado):
    # Filtrar dados do estado específico
    df_estado = df[df['Estado'] == estado]
    if df_estado.empty:
        print(f"Estado '{estado}' não encontrado no DataFrame!")
        return
    
    # Extrair colunas femininas e masculinas
    categorias = ['Até25', '26até40', '41até59', '60mais']
    feminino = [df_estado[f'{cat}f'].values[0] for cat in categorias]
    masculino = [df_estado[f'{cat}m'].values[0] for cat in categorias]
    
    # Criar gráfico de barras horizontais
    plt.figure(figsize=(10, 6))
    
    # Barras femininas (positivas)
    barras_feminino = plt.barh(categorias, feminino, color='pink', label='Feminino')
    
    # Barras masculinas (negativas para inverter lado)
    barras_masculino = plt.barh(categorias, [-x for x in masculino], color='blue', label='Masculino')
    
    # Configurações do gráfico
    plt.title(f'Pirâmide Etária - {estado}')
    plt.xlabel('População')
    plt.ylabel('Faixa Etária')
    plt.axvline(0, color='black', linewidth=0.8)  # Linha central
    plt.legend()
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Exibir o gráfico
    return plt.show()


def distribuir_genero(df):

    # Calcular a soma das populações de "Masculino" e "Feminino"
    df['Total'] = df['Masculino'] + df['Feminino']

    # Filtrar para obter os 10 maiores estados pela população total
    df_top_10 = df.nlargest(10, 'Total')

    # Ordenar o DataFrame pela coluna 'Total' em ordem crescente (do menor para o maior)
    df_top_10_sorted = df_top_10.sort_values(by='Total', ascending=True)

    # Configuração do tamanho do gráfico
    plt.figure(figsize=(14, 8))

    # Definindo as categorias (Masculino e Feminino)
    categorias = ['Masculino', 'Feminino']

    # Aumentar a largura das barras e a distância entre elas
    largura_barras = 0.6  # Aumentando a largura das barras
    distancia_entre_barras = 0.9  # Distância maior entre as barras (pode ser ajustado)

    # Posições para os estados no eixo Y (ajustando a distância entre as barras)
    y = np.arange(len(df_top_10_sorted['Estado'])) * (largura_barras + distancia_entre_barras)

    # Adicionar barras para cada categoria
    for i, cat in enumerate(categorias):  # Loop pelas categorias ('Masculino' e 'Feminino')
        if cat=='Masculino':
            cor = 'blue'
            barras = plt.barh(y + i * largura_barras, df_top_10_sorted[cat], height=largura_barras, label=cat, color=cor)  # Adiciona a barra para cada categoria
        else: 
            cor = 'pink'  # Definindo a cor rosa para feminino
            barras = plt.barh(y + i * largura_barras, df_top_10_sorted[cat], height=largura_barras, label=cat, color=cor)  # Adiciona a barra para feminino
        
        # Adiciona labels nas barras
        for barra in barras:
            largura = barra.get_width()  # Obtém a largura de cada barra
            plt.text(largura + 5, barra.get_y() + barra.get_height() / 2, f'{largura:.0f}', ha='left', va='center', fontsize=12)

    # Configuração dos rótulos do eixo Y
    plt.yticks(y + largura_barras * (len(categorias) / 2 - 0.5), df_top_10_sorted['Estado'], fontsize=12)  # Define os rótulos do eixo Y (Estados ordenados)

    # Rótulo do eixo X
    plt.xlabel('Quantidade de Advogados', fontsize=14)

    # Rótulo do eixo Y
    plt.ylabel('Estado', fontsize=14)

    # Título do gráfico
    plt.title('Disposição por Gênero', fontsize=16)

    # Legenda para identificar as categorias
    plt.legend(title="Categorias", fontsize=10)

    # Adiciona uma grade no eixo X para facilitar a leitura dos valores
    plt.grid(axis='x', linestyle='--', alpha=0.7)

    # Ajusta o layout para evitar sobreposição de elementos
    plt.tight_layout()

    # Mostra o gráfico na tela
    return plt.show()