import streamlit as st  # pip install streamlit
from deta import Deta  # pip install deta


# Load the environment variables
DETA_KEY = 'e00c52vq_D2SFEkvTriVN7gsofy3XAuEiAK8pTQUg'#st.secrets["DETA_KEY"]

# Initialize with a project key
deta = Deta(DETA_KEY)

# This is how to create/connect a database
db = deta.Base("propiedades")


def insert_parametros(Tipo_Crudo, P_E_ASTM_D86, API_P_E_ASTM_D86, Cont_Asfaltenos, Punto_Nube, Octano_RON,V8,V9):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db.put({"key": Tipo_Crudo, "P_E_ASTM_D86": P_E_ASTM_D86, "API_P_E_ASTM_D86": API_P_E_ASTM_D86, "Cont_Asfaltenos": Cont_Asfaltenos,'Punto_Nube':Punto_Nube, 'Octano_RON': Octano_RON,'V8':V8,'V9':V9 })


def fetch_all_parametros():
    """Returns a dict of all periods"""
    res = db.fetch()
    return res.items


def get_period(period):
    """If not found, the function will return None"""
    return db.get(period)
