
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

df = pd.read_excel("Ventas-PROMELSA.xlsx", sheet_name="data1")
df["Facturado_total"] = df["Facturado"]
df["GAP_calc"] = df["Meta"] - df["Facturado_total"]

st.set_page_config(layout="wide", page_title="Dashboard Ventas 2025")
st.title("📊 Dashboard de Ventas | 2025")

# Filtros
col1, col2 = st.columns(2)
meses_disponibles = df["Mes"].unique()
qs_disponibles = df["Trimestre"].unique()

with col1:
    filtro_q = st.multiselect("Filtrar por trimestre (Trimestre)", qs_disponibles, default=qs_disponibles)
with col2:
    filtro_mes = st.multiselect("Filtrar por mes", meses_disponibles, default=meses_disponibles)

df_filtrado = df[df["Trimestre"].isin(filtro_q) & df["Mes"].isin(filtro_mes)]

# Aquí defines tus 9 gráficos (puedes personalizarlos más adelante)
def crear_grafico_barras(x, y, titulo, color):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=x, y=y, marker_color=color))
    fig.update_layout(title=titulo, height=300)
    return fig

fig1 = crear_grafico_barras(df_filtrado["Mes"], df_filtrado["Meta"], "Meta por Mes", "skyblue")
fig2 = crear_grafico_barras(df_filtrado["Mes"], df_filtrado["Facturado"], "Facturado por Mes", "limegreen")
fig3 = crear_grafico_barras(df_filtrado["Mes"], df_filtrado["GAP_calc"], "GAP por Mes", "red")
fig4 = crear_grafico_barras(df_filtrado["Trimestre"], df_filtrado["Meta"], "Meta por Trimestre", "blue")
fig5 = crear_grafico_barras(df_filtrado["Trimestre"], df_filtrado["Facturado"], "Facturado por Trimestre", "green")
fig6 = crear_grafico_barras(df_filtrado["Trimestre"], df_filtrado["GAP_calc"], "GAP por Trimestre", "crimson")
fig7 = crear_grafico_barras(df_filtrado["Mes"], df_filtrado["Facturado"].cumsum(), "Facturado Acumulado", "orange")
fig8 = crear_grafico_barras(df_filtrado["Mes"], (df_filtrado["Facturado"]/df_filtrado["Meta"])*100, "Cumplimiento (%)", "purple")
fig9 = crear_grafico_barras(df_filtrado["Mes"], df_filtrado["Facturado_total"], "Facturado + Backlog (si aplica)", "teal")

# Grilla de 3 columnas x 3 filas
def mostrar_fila(fig_a, fig_b, fig_c):
    col1, col2, col3 = st.columns(3)
    with col1: st.plotly_chart(fig_a, use_container_width=True)
    with col2: st.plotly_chart(fig_b, use_container_width=True)
    with col3: st.plotly_chart(fig_c, use_container_width=True)

st.markdown("## 🔹 Fila 1")
mostrar_fila(fig1, fig2, fig3)

st.markdown("## 🔹 Fila 2")
mostrar_fila(fig4, fig5, fig6)

st.markdown("## 🔹 Fila 3")
mostrar_fila(fig7, fig8, fig9)

# KPIs (opcional)
st.markdown("---")
st.subheader("📌 Resumen")
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Total Meta", f"$ {df_filtrado['Meta'].sum():,.2f}")
kpi2.metric("Total Facturado", f"$ {df_filtrado['Facturado'].sum():,.2f}")
kpi3.metric("GAP Total", f"$ {df_filtrado['GAP_calc'].sum():,.2f}")
