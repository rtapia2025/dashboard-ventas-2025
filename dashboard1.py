import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

# Configuración de página
st.set_page_config(layout="wide", page_title="Dashboard Ventas 2025")
st.markdown("<h2 style='margin-top:0;'>📊 Dashboard de Ventas | 2025</h2>", unsafe_allow_html=True)

# Funciones para cargar datos
@st.cache_data
def cargar_datos():
    df = pd.read_excel("Ventas-PROMELSA.xlsx", sheet_name="meta_fac")
    df["Facturado_total"] = df["Facturado"]
    df["GAP_calc"] = df["Meta"] - df["Facturado_total"]
    df["Año"] = df["Año"].astype(str)  # aseguramos que Año es string
    return df

@st.cache_data
def cargar_fac_cli():
    df_cli = pd.read_excel("Ventas-PROMELSA.xlsx", sheet_name="fac_cli")
    df_cli["Año"] = df_cli["Año"].astype(str)
    return df_cli

df = cargar_datos()
df_cli = cargar_fac_cli()

# --- Variables auxiliares
anio_actual = datetime.now().year
mes_actual_num = datetime.now().month
orden_meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
               'Julio', 'Agosto', 'Setiembre', 'Octubre', 'Noviembre', 'Diciembre']
meses_a_la_fecha = orden_meses[:mes_actual_num]

# --- Filtros globales en la barra lateral
st.sidebar.header("🎯 Filtros generales")
anios_disponibles = sorted(df["Año"].unique())
anio_sel = st.sidebar.selectbox("Seleccionar año", options=anios_disponibles, index=anios_disponibles.index(str(anio_actual)))
meses_sel = st.sidebar.multiselect("Seleccionar meses", options=orden_meses, default=meses_a_la_fecha)

# --- Filtrar data de gráfico 1
df_filtrado = df[(df["Año"] == anio_sel) & (df["Mes"].isin(meses_sel))]

# Calcular KPIs
total_meta = df_filtrado['Meta'].sum()
total_fact = df_filtrado['Facturado'].sum()
total_gap = df_filtrado['GAP_calc'].sum()
avance_pct = (total_fact / total_meta * 100) if total_meta != 0 else 0

# --- Gráfico 1
fig1 = go.Figure()
fig1.add_trace(go.Bar(x=df_filtrado["Mes"], y=df_filtrado["Meta"], name='Meta', marker_color='skyblue'))
fig1.add_trace(go.Bar(x=df_filtrado["Mes"], y=df_filtrado["Facturado_total"], name='Facturado', marker_color='limegreen'))

for _, row in df_filtrado.iterrows():
    if row["GAP_calc"] > 0:
        fig1.add_trace(go.Scatter(
            x=[row["Mes"]],
            y=[row["Meta"]],
            mode='markers+text',
            text=[f"-{int(row['GAP_calc']):,}"],
            textposition="top center",
            marker=dict(color="red", size=10),
            showlegend=False
        ))

kpi_text = (
    f"<b>Total Meta</b><br>$ {total_meta:,.2f}" +
    f"<br><b>Total Facturado</b><br>$ {total_fact:,.2f}" +
    f"<br><b>GAP Total</b><br><span style='color:{'red' if total_gap > 0 else 'blue'};'>$ {total_gap:,.2f}</span>" +
    f"<br><b>Avance</b><br>{avance_pct:.1f}%"
)

fig1.add_annotation(
    text=kpi_text,
    xref="paper", yref="paper",
    x=1.28, y=0.7,
    showarrow=False,
    align="left",
    font=dict(size=12),
    bgcolor="white",
    bordercolor="white",
    borderwidth=1
)

fig1.update_layout(
    barmode='group',
    title="Meta vs Facturado por Mes",
    yaxis_title="Monto ($.)",
    xaxis_title="Mes",
    height=500,
    margin=dict(r=250)
)

# Mostrar gráfico
st.plotly_chart(fig1, use_container_width=True)
