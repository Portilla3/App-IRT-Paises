import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# ─── Configuración ───
st.set_page_config(
    page_title="QALAT · IRT · Monitoreo de Resultados",
    page_icon="📊",
    layout="wide"
)

# ─── Constantes ───
PAISES = {
    "Colombia":            st.secrets.get("PASSWORD_COLOMBIA", ""),
    "Panamá":              st.secrets.get("PASSWORD_PANAMA", ""),
    "Honduras":            st.secrets.get("PASSWORD_HONDURAS", ""),
    "Costa Rica":          st.secrets.get("PASSWORD_COSTARICA", ""),
    "República Dominicana": st.secrets.get("PASSWORD_RD", ""),
}
PASSWORD_UNODC = st.secrets.get("PASSWORD_UNODC", "")
TABLA = "irt_registros"

# ─── Helpers Supabase ───
def _sb_headers():
    return {
        "apikey": st.secrets["SUPABASE_KEY"],
        "Authorization": f"Bearer {st.secrets['SUPABASE_KEY']}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

def _sb_url(tabla=TABLA):
    return f"{st.secrets['SUPABASE_URL']}/rest/v1/{tabla}"

def _cargar_supabase(pais=None):
    params = {"select": "*", "order": "created_at.desc"}
    if pais:
        params["pais"] = f"eq.{pais}"
    r = requests.get(_sb_url(), headers=_sb_headers(), params=params)
    if r.status_code == 200:
        return pd.DataFrame(r.json())
    return pd.DataFrame()

def _actualizar_registro(id_reg, campos):
    r = requests.patch(
        f"{_sb_url()}?id=eq.{id_reg}",
        headers=_sb_headers(),
        json=campos
    )
    return r

def _eliminar_registro(id_reg):
    r = requests.delete(
        f"{_sb_url()}?id=eq.{id_reg}",
        headers=_sb_headers()
    )
    return r

# ─── Login ───
if "pais" not in st.session_state:
    st.session_state.pais = None
if "rol" not in st.session_state:
    st.session_state.rol = None

def login():
    st.markdown("## 📊 QALAT · IRT · Monitoreo de Resultados de Tratamiento")
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### Ingrese su clave de acceso")
        clave = st.text_input("Clave", type="password", key="login_input")
        if st.button("Ingresar", use_container_width=True):
            if clave == PASSWORD_UNODC:
                st.session_state.rol = "UNODC"
                st.session_state.pais = "UNODC"
                st.rerun()
            else:
                for p, pw in PAISES.items():
                    if clave == pw:
                        st.session_state.rol = "pais"
                        st.session_state.pais = p
                        st.rerun()
                st.error("Clave incorrecta")

if st.session_state.pais is None:
    login()
    st.stop()

# ─── App principal ───
pais = st.session_state.pais
rol = st.session_state.rol

st.sidebar.markdown(f"### 📊 QALAT IRT")
st.sidebar.markdown(f"**{pais}**")
if st.sidebar.button("🚪 Cerrar sesión"):
    st.session_state.pais = None
    st.session_state.rol = None
    st.rerun()

# ─── Tabs según rol ───
if rol == "UNODC":
    tabs = st.tabs(["📊 Panel de gestión", "📄 Reportes", "✏️ Corrección", "💾 Respaldos"])
else:
    tabs = st.tabs(["📊 Panel de gestión", "📄 Reportes", "✏️ Corrección"])

# Cargar datos
if rol == "UNODC":
    df = _cargar_supabase()
else:
    df = _cargar_supabase(pais)

with tabs[0]:
    st.header("Panel de gestión")
    if df.empty:
        st.info("No hay registros IRT para este país.")
    else:
        st.metric("Total registros IRT", len(df))
        st.dataframe(df.head(20), use_container_width=True)

with tabs[1]:
    st.header("Reportes")
    st.info("🚧 Módulo de reportes en desarrollo (Sesión 6)")

with tabs[2]:
    st.header("Corrección de registros")
    st.info("🚧 Módulo de corrección en desarrollo (Sesión 4)")

if rol == "UNODC" and len(tabs) > 3:
    with tabs[3]:
        st.header("Respaldos")
        st.info("🚧 Módulo de respaldos en desarrollo (Sesión 8)")
