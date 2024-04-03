import streamlit as st
from utils import EstilizarPagina
import pandas as pd
from estilizador import  Dataframes
from leitor import DataReader

estilizador = EstilizarPagina()
estilizador.set_page_config()

col1, col2 = st.columns([4, 1])

col1.subheader("Last Mile - Análise de Drivers  🚛")

with col2.popover("Sobre a página"):
    st.write("Para descobrir a cabeça de um CEP de uma região, selecione o estado, cidade e bairro desejados.")
    st.write("Após a seleção, a cabeça do CEP da região será exibida, juntamente com o CEP inicial e final da região e uma tabela com os demais bairros e/ou cidades que também são contemplados pela cabeça de CEP encontrada.")
    st.write("Quanto mais dígitos do CEP forem selecionados, mais específica será a região encontrada.")

st.write("  ")

leitor_obj = DataReader()
bairros = leitor_obj.read_csv('CSV', 'Bairros por CEP.csv')
cidades = leitor_obj.read_csv('CSV', 'Cidades por CEP.csv')

cidades = cidades.rename(columns={'Cep inicial': 'Cep Inicial', 'Cep final': 'Cep Final'})
bairros = pd.concat([bairros, cidades])

bairros['Bairro'] = bairros['Bairro'].fillna('-')

demais_bairros = bairros.copy()

col1, col2, col3 = st.columns(3)
st.write("  ")
selected_estado = col1.selectbox("Selecione o estado", bairros['Estado'].unique(), index=None, key='b1')
bairros = bairros[bairros['Estado'] == selected_estado]
selected_cidade = col2.selectbox("Selecione a cidade", bairros['Cidade'].unique(), index=None, key='b2')
bairros = bairros[bairros['Cidade'] == selected_cidade]   
selected_bairro = col3.selectbox("Selecione o bairro", bairros['Bairro'].unique(), index=None, key='b3')  
if  selected_bairro:
    bairros = bairros[bairros['Bairro'] == selected_bairro]
qtd_digitos = st.slider("Quantidade de dígitos do CEP", 1, 8, 3, key='b4')
st.divider()

if selected_cidade:

    cep_inicial = bairros['Cep Inicial'].astype(str).str.zfill(8).iloc[0]
    cabeca_cep = bairros['Cep Inicial'].astype(str).str.zfill(8).str.slice(0, qtd_digitos).iloc[0]
    cep_final = bairros['Cep Final'].astype(str).str.zfill(8).iloc[-1]

    col1, col2, col3= st.columns([1,1,4])

    col2.metric(label="Cabeça de CEP", value=cabeca_cep)
    col2.metric(label="CEP inicial da região", value=cep_inicial)
    col2.metric(label="CEP final da região", value=cep_final)

    demais_bairros['Cep Inicial'] = demais_bairros['Cep Inicial'].astype(str).str.zfill(8)
    filtered_bairros = demais_bairros[demais_bairros['Cep Inicial'].str.startswith(cabeca_cep)]

    filtered_bairros = filtered_bairros[['Estado', 'Cidade', 'Bairro']].drop_duplicates()

    filtered_bairros.reset_index(drop=True, inplace=True)

    centered_table = Dataframes.generate_html(filtered_bairros)

    col3.write(centered_table, unsafe_allow_html=True)

