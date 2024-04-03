import streamlit as st
from utils import EstilizarPagina, GerarTabelas
from estilizador import Dataframes
import time

estilizador = EstilizarPagina()
estilizador.set_page_config()

text = "Dados carregando... Duração entre 1 e 5 minutos ⌛"
loading_message = st.empty()
loading_message.progress(0, text=text)

st.subheader("Last Mile - Análise de Drivers  🚛")
col1, col2 = st.columns([4, 1])
col1.header("Personas")

tabela = GerarTabelas()
drivers_itinerarios = tabela.gerar_dados("drivers_itinerarios")
loading_message.progress(30, text=text)

tabela = GerarTabelas()
tabela_personas = tabela.gerar_dados("personas")

tabela_personas.dropna(subset=['zip'], inplace=True)

tabela_personas['zip'] = tabela_personas['zip'].replace('-', '', regex=True)

tabela_personas.dropna(subset=['vicinity'], inplace=True)

cols = list(tabela_personas.columns)
cols.remove('driver_id')
cols.insert(0, 'driver_id')  
tabela_personas = tabela_personas[cols]

drivers_itinerarios['zip'] = drivers_itinerarios['zip'].astype(str)
drivers_itinerarios['zip'] = drivers_itinerarios['zip'].str.split('.').str[0]
drivers_itinerarios['zip'] = drivers_itinerarios['zip'].str.zfill(8)

def title_except(s, exceptions):
    word_list = s.split()
    final = [word.lower() if word in exceptions else word.title() for word in word_list]
    return ' '.join(final)

exceptions = ["de", "do", "da", "Da", "De", "Do", "dos", "Dos", "das", "Das"]
tabela_personas['vicinity'] = tabela_personas['vicinity'].astype(str).apply(lambda x: title_except(x, exceptions))


with col2.popover("Sobre a página"):           
    st.write("**Diferença entre as regiões:**")
    st.write("**Região de Cadastro:** Local de residência cadastrado por um motorista.")
    st.write("**Região de Entrega:** Último local onde um motorista realizou entregas.")
    st.write("A quantidade total de drivers inclui apenas drivers ativos, com status de habilitado e que fizeram entregas após 06/2023. Além disso, o valor total difere entre as regiões de cadastro e entrega pois no primeiro também é filtrado apenas drivers com endereço completo cadastrado.")
    st.write("**Diferença entre as buscas:**")
    st.write("**CEP:** A busca por CEP é feita considerando qualquer quantidade de dígitos do CEP (desde que seja inferior a 8), ou seja, ao pesquisar *123*, o total de drivers corresponderá a todos que tiverem CEP iniciando em *123*.")
    st.write("**Bairro/Cidade:** A busca por bairro/cidade é feita considerando a seleção de um ou mais estados, cidades e bairros. Ao selecionar, o total de drivers corresponderá a todos que tiverem endereço com essas informações.")
    st.write("**Importante:** A busca por bairro/cidade pode apresentar divergencias pela forma como os endereços foram cadastrados. Para uma consulta mais assertiva, conte com a ajuda da aba *Descobrir Cabeça de CEP* e realize sua busca por CEP.")

tab1, tab2 = st.tabs(["Região de Cadastro", "Região de Entrega"])

with tab1:

    formato_busca = st.radio(
    "Buscar por:",
    ("CEP", "Bairro/Cidade"),
    key="tab1"
    )

    if formato_busca == "CEP":
        col1, col2, col3 = st.columns(3)
        cep = col1.text_input("Digite o CEP", key="tab11")
        cep = cep.replace('-', '')
        if cep:
            if len(cep) > 8:
                st.write('Quantidade de dígitos inválida')
                st.stop()
        tabela_personas['zip'] = tabela_personas['zip'].astype(str).fillna('')
        filtered_personas = tabela_personas[tabela_personas['zip'].str.startswith(cep)]
        unique_driver_count = filtered_personas['driver_id'].nunique()
        st.divider()
        unique_driver_count_str = "{:,}".format(unique_driver_count).replace(",", ".")
        st.metric(label="Quantidade de Drivers", value=unique_driver_count_str)
        botao_tabela = st.button("Tabela de Drivers")
        if botao_tabela:
            filtered_personas = filtered_personas.head(800)
            filtered_personas.reset_index(drop=True, inplace=True)
            centered_table = Dataframes.generate_html(filtered_personas)
            st.write("  ")
            st.write(centered_table, unsafe_allow_html=True)

    if formato_busca == "Bairro/Cidade":

        col1, col2, col3 = st.columns(3)

        tabela_personas["state"] = tabela_personas["state"].str.upper()
        selected_estado  = col1.multiselect("Selecione o estado", tabela_personas['state'].unique())
        if selected_estado:
            tabela_personas = tabela_personas[tabela_personas['state'].isin(selected_estado)]
        selected_cidade = col2.multiselect("Selecione a cidade", tabela_personas['city'].unique())
        if selected_cidade:
            tabela_personas = tabela_personas[tabela_personas['city'].isin(selected_cidade)]
        selected_bairro = col3.multiselect("Selecione o bairro", tabela_personas['vicinity'].unique())
        if selected_bairro:
            tabela_personas = tabela_personas[tabela_personas['vicinity'].isin(selected_bairro)]
        unique_driver_count = tabela_personas['driver_id'].nunique()
        st.divider()
        unique_driver_count_str = "{:,}".format(unique_driver_count).replace(",", ".")
        st.metric(label="Quantidade de Drivers", value=unique_driver_count_str)
        botao_tabela = st.button("Tabela de Drivers", key="tab12")
        if botao_tabela:
            tabela_personas = tabela_personas.head(800)
            centered_table = Dataframes.generate_html(tabela_personas)
            st.write("  ")
            st.write(centered_table, unsafe_allow_html=True)

loading_message.progress(70, text=text)
with tab2:

    formato_busca = st.radio(
    "Buscar por:",
    ("CEP", "Bairro/Cidade"),
    )

    if formato_busca == "CEP":
        col1, col2, col3 = st.columns(3)
        cep = col1.text_input("Digite o CEP")
        cep = cep.replace('-', '')
        if cep:
            if len(cep) > 8:
                st.write('Quantidade de dígitos inválida')
                st.stop()

        drivers_itinerarios['zip'] = drivers_itinerarios['zip'].astype(str).fillna('')
        drivers_itinerarios = drivers_itinerarios[drivers_itinerarios['zip'].str.startswith(cep)]
        unique_driver_count = drivers_itinerarios['driver_id'].nunique()
        st.divider()
        unique_driver_count_str = "{:,}".format(unique_driver_count).replace(",", ".")
        st.metric(label="Quantidade de Drivers", value=unique_driver_count_str)
        botao_tabela = st.button("Tabela de Drivers", key="tab21")
        if botao_tabela:
            drivers_itinerarios = drivers_itinerarios.head(800)
            drivers_itinerarios.reset_index(drop=True, inplace=True)
            centered_table = Dataframes.generate_html(drivers_itinerarios)
            st.write("  ")
            st.write(centered_table, unsafe_allow_html=True)

    if formato_busca == "Bairro/Cidade":

        col1, col2, col3 = st.columns(3)

        drivers_itinerarios["state"] = drivers_itinerarios["state"].str.upper()
        selected_estado = col1.multiselect("Selecione o estado", drivers_itinerarios['state'].unique())
        if selected_estado:
            drivers_itinerarios = drivers_itinerarios[drivers_itinerarios['state'].isin(selected_estado)]
        selected_cidade = col2.multiselect("Selecione a cidade", drivers_itinerarios['itinerary_city'].unique())
        if selected_cidade:
            drivers_itinerarios = drivers_itinerarios[drivers_itinerarios['itinerary_city'].isin(selected_cidade)]
        selected_bairro = col3.multiselect("Selecione o bairro", drivers_itinerarios['destination_neighborhood'].unique())
        if selected_bairro:
            drivers_itinerarios = drivers_itinerarios[drivers_itinerarios['destination_neighborhood'].isin(selected_bairro)]
        unique_driver_count = drivers_itinerarios['driver_id'].nunique()
        st.divider()
        unique_driver_count_str = "{:,}".format(unique_driver_count).replace(",", ".")
        st.metric(label="Quantidade de Drivers", value=unique_driver_count_str)
        botao_tabela = st.button("Tabela de Drivers", key="tab22")
        if botao_tabela:
            tabela_personas = tabela_personas.head(800)
            centered_table = Dataframes.generate_html(tabela_personas)
            st.write("  ")
            st.write(centered_table, unsafe_allow_html=True)        

loading_message.progress(100, text=text)
time.sleep(1)
loading_message.empty()