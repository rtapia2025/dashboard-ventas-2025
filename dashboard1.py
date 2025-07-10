
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

df = pd.read_excel("ventas-PROMELSA.xlsx", sheet_name="data1")
df["Fac_backlog"] = df["Fac_backlog"].fillna(0)
df["Facturado_total"] = df["Facturado"]
df["GAP_calc"] = df["Meta"] - df["Facturado_total"]

st.set_page_config(layout="wide", page_title="Dashboard Ventas 2025")
st.title("📊 Dashboard de Ventas 2025 | PROMELSA")

# Filtros
col1, col2 = st.columns(2)
meses_disponibles = df["Mes"].unique()
qs_disponibles = df["Trimestre"].unique()

with col1:
    filtro_q = st.multiselect("Filtrar por trimestre (Trimestre)", qs_disponibles, default=qs_disponibles)
with col2:
    filtro_mes = st.multiselect("Filtrar por mes", meses_disponibles, default=meses_disponibles)

df_filtrado = df[df["Trimestre"].isin(filtro_q) & df["Mes"].isin(filtro_mes)]

fig = go.Figure()
fig.add_trace(go.Bar(x=df_filtrado["Mes"], y=df_filtrado["Meta"], name='Meta', marker_color='skyblue'))
fig.add_trace(go.Bar(x=df_filtrado["Mes"], y=df_filtrado["Facturado_total"], name='Facturado + Backlog', marker_color='limegreen'))

for i, row in df_filtrado.iterrows():
    if row["GAP_calc"] > 0:
        fig.add_trace(go.Scatter(
            x=[row["Mes"]],
            y=[row["Meta"]],
            mode='markers+text',
            text=[f"-{int(row['GAP_calc']):,}"],
            textposition="top center",
            marker=dict(color="red", size=10),
            showlegend=False
        ))

fig.update_layout(
    barmode='group',
    title="Meta vs Facturado (+Backlog) por Mes",
    yaxis_title="Monto ($.)",
    xaxis_title="Mes",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📌 Resumen")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Meta", f"$ {df_filtrado['Meta'].sum():,.2f}")
kpi2.metric("Total Facturado", f"$ {df_filtrado['Facturado'].sum():,.2f}")
kpi3.metric("Total Backlog", f"$ {df_filtrado['Fac_backlog'].sum():,.2f}")
kpi4.metric("GAP Total", f"$ {df_filtrado['GAP_calc'].sum():,.2f}")
