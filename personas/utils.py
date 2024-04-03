import pandas as pd
import streamlit as st

from estilizador import PageStyler
from leitor import DataReader

import pandas as pd
import warnings

warnings.filterwarnings('ignore')

pd.set_option('display.max_columns', None)

class EstilizarPagina:
    """
    This class is responsible for styling the page.

    Args:
        self (object): Instance of the class.
    """
    def __init__(self):
        self.estilizador = PageStyler()
        self.PAGE_CONFIG = {
            "page_title": "Drivers - Loggi",
            "page_icon": "🚛",
            "layout": "centered",
        }

    def set_page_config(self):
        """
        This method sets the page configuration and applies general and sidebar CSS.

        Args:
            _self (object): Instance of the class.
        """
        st.set_page_config(**self.PAGE_CONFIG)
        self.estilizador.apply_general_css()
        self.estilizador.apply_sidebar_css()
        # st.subheader("Last Mile - Análise de Drivers  🚛")

class GerarTabelas:
    """
    This class is responsible for generating tables by reading SQL files.

    Args:
        _self (object): Instance of the class. Self with undercore is used to cache the data and avoid conflicts with streamlit. More informations about it here: https://discuss.streamlit.io/t/from-st-cache-to-st-cache-data-in-a-class/37667
    """
    def __init__(_self):
        _self.leitor = DataReader()

    @st.cache_data(show_spinner=False, ttl=840000)
    def gerar_dados(_self, filename):
        """
        This method reads the 'dados_lex.sql' file and returns its content.

        Args:
            filename (str): The name of the SQL file.

        Returns:
            DataFrame: A pandas DataFrame containing the data read from the SQL file.
        """
        return _self.leitor.read_sql("SQL", f"{filename}.sql")


def filter_by_multiselect(df1, column, label):
    """
    Function to filter two dataframes based on the selected values from a Streamlit multiselect widget.

    Args:
        df1 (DataFrame): The first dataframe to filter.
        df2 (DataFrame): The second dataframe to filter.
        column (str): The column name to use for the multiselect widget and to filter the dataframes.
        label (str): The label to display above the multiselect widget.

    Returns:
        DataFrame, DataFrame: The filtered dataframes.
    """
    selected_values = st.multiselect(label, df1[column].unique(), key=label)
    if selected_values:
        df1 = df1[df1[column].isin(selected_values)]
    return df1


