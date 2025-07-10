import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# Leer archivo Excel
st.set_page_config(layout="wide", page_title="Dashboard Ventas 2025")
st.markdown("<h3 style='margin-top:-52;'>📊 Dashboard de Ventas | 2025</h3>", unsafe_allow_html=True)

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

# Calcular KPIs
meta_total = df_filtrado['Meta'].sum()
fact_total = df_filtrado['Facturado'].sum()
gap_total = df_filtrado['GAP_calc'].sum()
avance_pct = (fact_total / meta_total * 100) if meta_total != 0 else 0

# --- Gráfico 1: Meta vs Facturado + GAP resaltado, % de avance y KPIs dentro del gráfico
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

# Agregar KPIs como anotaciones al costado de la leyenda (incluye % avance)
kpi_text = (
    f"<b>Total Meta</b><br>$ {meta_total:,.2f}" +
    f"<br><b>Total Facturado</b><br>$ {fact_total:,.2f}" +
    f"<br><b>GAP Total</b><br><span style='color:{'red' if gap_total > 0 else 'blue'};'>$ {gap_total:,.2f}</span>" +
    f"<br><b>Avance</b><br>{avance_pct:.1f}%"
)

fig1.add_annotation(
    text=kpi_text,
    xref="paper", yref="paper",
    x=1.28, y=0.5,
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
    margin=dict(r=250)  # más espacio a la derecha para anotaciones
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

# --- Mostrar 6 gráficos (2 columnas x 3 filas)
def mostrar_fila(fig_a, fig_b):
    col1, col2 = st.columns(2)
    with col1: st.plotly_chart(fig_a, use_container_width=True)
    with col2: st.plotly_chart(fig_b, use_container_width=True)

# st.markdown("## 🔹 Fila 1")
mostrar_fila(fig1, fig2)

st.markdown("## 🔹 Fila 2")
mostrar_fila(fig3, fig4)

st.markdown("## 🔹 Fila 3")
mostrar_fila(fig5, fig6)
