import streamlit as st
import pandas as pd 


class PageStyler:
    def __init__(self):
        pass

    def apply_general_css(self):
        """
        Function to apply general CSS styling for the Streamlit app.

        No arguments or return value.
        """
        st.markdown(
            """
        <style>

        /* Fonte dos subtítulos */
        h2 {
        font-family: Monteserrat, sans-serif;
        }

        /* Fonte do texto personalizado do sidebar */
        p {
        font-family: Monteserrat, sans-serif;
        }

        /* Texto padrão */
        .custom-text {
        font-family: Monteserrat, sans-serif;
        text-align: justify; /* Justifica o texto */
        }

        /* Largura máxima da área de escrita */
        .css-1y4p8pa {
        max-width: 975px; 
        }

        /* Largura máxima da área de escrita */
        .st-emotion-cache-1y4p8pa {
        max-width: 62rem; 
        }

        /* Formatação do título */
        h1 {
        text-align: center; 
        font-size: 30px; 
        font-family: Monteserrat, sans-serif; 
        font-weight: 400;
        }

        /* Créditos e documentação */
        .custom-sidebar-footer {
        position: relative;
        bottom: 0px; 
        left: 0;
        width: 100%;
        font-size: 14px;
        text-align: left;
        }

        /* Estilos para links quando o mouse passa sobre eles */
        .custom-sidebar-footer a:hover {
        text-decoration: underline;
        }

        /* Estilos para links visitados */
        .custom-sidebar-footer a:visited {
        }

        /* Formatação do subtítulo padrão */
        .subtitle {
        font-family: Monteserrat, sans-serif;
        font-size: 20px;
        font-weight: bold;
        }

        [data-testid=stSidebar] [data-testid=stImage]{
        text-align: center;
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 100%;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )

    def apply_sidebar_css(self):
        """
        Function to apply custom CSS styling to the Streamlit sidebar.
        The styling includes a background image and positioning adjustments.

        No arguments or return value.
        """
        st.markdown(
            """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Imagem_Logo_Completo_Azul.png/250px-Imagem_Logo_Completo_Azul.png);
                background-repeat: no-repeat;
                padding-top: 40px;
                background-position: 20px 20px;
            }
            [data-testid="stSidebarNav"]::before {
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
            unsafe_allow_html=True,
        )


class Dataframes:
    def generate_html(df):
        """
        Generates an HTML representation of the DataFrame.

        Args:
            df (DataFrame): The DataFrame to convert to HTML.

        Returns:
            str: The HTML representation of the DataFrame.
        """
        rendered_table = df.to_html()
        html = """
        <div style="display: flex; justify-content: center;">
        <div style="max-height: 500px; overflow-y: auto;">
                {}
        """.format(rendered_table)
        return html

