import pandas as pandas
import getpass

#Tabela total de advogados
user = getpass.getuser()
diretorio = './data/Dados_OAB_2024.xlsx'
tabela_total_de_advogados = pandas.read_excel(diretorio, 'Total_Advogados_2024')

tabela_dinamica_total_advogados = pandas.pivot_table(tabela_total_de_advogados, values=['Advogado(a)', 'Estagiário(a)', 'Suplementar'], index=['Estado'], aggfunc="sum", fill_value=0)

tabela_dinamica_total_advogados['% Share Adv'] = round((tabela_dinamica_total_advogados['Advogado(a)'] / (tabela_dinamica_total_advogados['Advogado(a)'] + tabela_dinamica_total_advogados['Estagiário(a)'] + tabela_dinamica_total_advogados['Suplementar'])) * 100,1)

#Tabela de gêneros de advogados

tabela_dinamica_genero_advogado = pandas.read_excel(diretorio, 'Total_Advogados_Genero')

#Cruza tabela gêneros e tabela total de advogados
inner_total_genero_advogados = pandas.merge(tabela_dinamica_total_advogados, tabela_dinamica_genero_advogado, left_on='Estado', right_on='Estado')

#adicionar uma coluna com o percentual de mulheres em relação ao total de advogados
inner_total_genero_advogados['% De mulheres'] = round((inner_total_genero_advogados['Feminino'] / (inner_total_genero_advogados['Advogado(a)'])) * 100,1)

#Tabela das faixas etárias por gênero

tabela_dinamica_faixa_etaria = pandas.read_excel(diretorio, 'Genero_Faixa_Etaria_2024')

faixa_etaria_feminina = pandas.pivot_table(tabela_dinamica_faixa_etaria, values=['Feminino'], index=['ESTADO'],
                    columns="Faixa Etária", aggfunc="sum", fill_value=0)
faixa_etaria_feminina.columns = faixa_etaria_feminina.columns.droplevel(0)

faixa_etaria_masculina = pandas.pivot_table(tabela_dinamica_faixa_etaria, values=['Masculino'], index=['ESTADO'], columns="Faixa Etária", aggfunc="sum", fill_value=0)
faixa_etaria_masculina.columns = faixa_etaria_masculina.columns.droplevel(0)

faixa_etaria_feminina.rename(columns={'Até 25 Anos':'Até25f', 'De 26 à 40 Anos':'26até40f', 'De 41 à 59 Anos':'41até59f', 'De 60 Anos ou Mais':'60maisf'},inplace=True)

faixa_etaria_masculina.rename(columns={'Até 25 Anos':'Até25m', 'De 26 à 40 Anos':'26até40m', 'De 41 à 59 Anos':'41até59m',
       'De 60 Anos ou Mais':'60maism'},inplace=True)
faixa_etaria_masculina

faixa_etaria_feminina = faixa_etaria_feminina.reset_index()
faixa_etaria_masculina = faixa_etaria_masculina.reset_index()

#Cruzamento de todas as tabelas = total advogados, total gênero e faixa etária
tabela_final01 = pandas.merge(inner_total_genero_advogados, faixa_etaria_feminina, left_on='Estado', right_on='ESTADO')

tabela_final02 = pandas.merge(tabela_final01, faixa_etaria_masculina, left_on='Estado', right_on='ESTADO')
tabela_final02.drop(columns=['ESTADO_x', 'ESTADO_y'], inplace=True)

#Export para pasta data
tabela_final02.to_excel('./data/advogados_idade_genero.xlsx', index=False)