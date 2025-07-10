import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# Leer archivo Excel
st.set_page_config(layout="wide", page_title="Dashboard Ventas 2025")
st.title("📊 Dashboard de Ventas | 2025")

# Leer Excel
@st.cache_data
def cargar_datos():
    df = pd.read_excel("Ventas-PROMELSA.xlsx", sheet_name="data1")
    df["Facturado_total"] = df["Facturado"]
    df["GAP_calc"] = df["Meta"] - df["Facturado_total"]
    return df

df = cargar_datos()

# Filtros
meses_disponibles = df["Mes"].unique()

filtro_mes = st.multiselect("Filtrar por mes", meses_disponibles, default=meses_disponibles)

df_filtrado = df[df["Mes"].isin(filtro_mes)]

# --- Gráfico 1: Meta vs Facturado + GAP
fig1 = go.Figure()
fig1.add_trace(go.Bar(x=df_filtrado["Mes"], y=df_filtrado["Meta"], name='Meta', marker_color='skyblue'))
fig1.add_trace(go.Bar(x=df_filtrado["Mes"], y=df_filtrado["Facturado_total"], name='Facturado', marker_color='limegreen'))

for i, row in df_filtrado.iterrows():
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

fig1.update_layout(
    barmode='group',
    title="Meta vs Facturado (+Backlog) por Mes",
    yaxis_title="Monto ($.)",
    xaxis_title="Mes",
    height=400
)

# --- Gráficos de marcador de posición (pendientes de personalizar)
def placeholder_grafico(n):
    return go.Figure().update_layout(title=f"Gráfico {n} (pendiente)", height=300)

fig2 = placeholder_grafico(2)
fig3 = placeholder_grafico(3)
fig4 = placeholder_grafico(4)
fig5 = placeholder_grafico(5)
fig6 = placeholder_grafico(6)
fig7 = placeholder_grafico(7)
fig8 = placeholder_grafico(8)
fig9 = placeholder_grafico(9)

# --- Mostrar 9 gráficos (3 columnas x 3 filas)

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

# --- KPIs resumen
st.markdown("---")
st.subheader("📌 Resumen")
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Total Meta", f"$ {df_filtrado['Meta'].sum():,.2f}")
kpi2.metric("Total Facturado", f"$ {df_filtrado['Facturado'].sum():,.2f}")
kpi3.metric("GAP Total", f"$ {df_filtrado['GAP_calc'].sum():,.2f}")
