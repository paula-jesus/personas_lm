import streamlit as st
from utils import EstilizarPagina, GerarTabelas

estilizador = EstilizarPagina()
estilizador.set_page_config()

tabela = GerarTabelas()
drivers_itinerarios = tabela.gerar_dados("drivers_itinerarios")

tabela = GerarTabelas()
tabela_personas = tabela.gerar_dados("personas")

tabela_personas.dropna(subset=['zip'], inplace=True)

tabela_personas['zip'] = tabela_personas['zip'].replace('-', '', regex=True)

col1, col2 = st.columns([3.6, 1.4])
with col2.popover("Diferença entre as regiões"):
    st.write("Região de Cadastro: Local de residência cadastrado por um motorista.")
    st.write("Região de Entrega: Último local onde um motorista realizou entregas.")

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
        st.metric(label="Quantidade de Drivers", value=unique_driver_count)

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
        st.metric(label="Quantidade de Drivers", value=unique_driver_count)

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
        st.metric(label="Quantidade de Drivers", value=unique_driver_count)

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
        st.metric(label="Quantidade de Drivers", value=unique_driver_count)
