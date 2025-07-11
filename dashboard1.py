import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

# Leer archivo Excel
st.set_page_config(layout="wide", page_title="Dashboard Ventas 2025")

# Obtener año actual y meses hasta la fecha
anio_actual = datetime.now().year
mes_actual_num = datetime.now().month

orden_meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
               'Julio', 'Agosto', 'Setiembre', 'Octubre', 'Noviembre', 'Diciembre']
meses_a_la_fecha = orden_meses[:mes_actual_num]


st.markdown("<h2 style='margin-top:0;'>📊 Dashboard de Ventas | 2025</h2>", unsafe_allow_html=True)

# Leer Excel
@st.cache_data
def cargar_datos():
    df = pd.read_excel("Ventas-PROMELSA.xlsx", sheet_name="meta_fac")
    df["Facturado_total"] = df["Facturado"]
    df["GAP_calc"] = df["Meta"] - df["Facturado_total"]
    return df

df = cargar_datos()

@st.cache_data
def cargar_fac_cli():
    df_cli = pd.read_excel("Ventas-PROMELSA.xlsx", sheet_name="fac_cli")
    df_cli["Año"] = df_cli["Año"].astype(str)
    return df_cli

df_cli = cargar_fac_cli()


df_filtrado = df[(df["Año"] == anio_sel) & (df["Mes"].isin(meses_sel))]


# Calcular KPIs
total_meta = df_filtrado['Meta'].sum()
total_fact = df_filtrado['Facturado'].sum()
total_gap = df_filtrado['GAP_calc'].sum()
avance_pct = (total_fact / total_meta * 100) if total_meta != 0 else 0

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

# KPIs como anotaciones
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

# --- Gráficos de marcador de posición (pendientes de personalizar)
def placeholder_grafico(n):
    return go.Figure().update_layout(title=f"Gráfico {n} (pendiente)", height=300)

# Filtrar base de clientes por año y meses seleccionados
df_cli_filtrado = df_cli[df_cli["Año"] == anio_sel]


# --- Lista de clientes clave a mostrar
clientes_clave = [
    "MINERA BORO MISQUICHILCA S.A.",
    "LA ARENA S.A.",
    "CIA MINERA PODEROSA S.A.",
    "CONSORCIO MINERO HORIZONTE S.A.",
    "MINERA AURÍFERA RETAMAS S.A.",
    "MINERA YANACOCHA S.R.L.",
    "SHAHUINDO S.A.C.",
    "GOLD FIELDS LA CIMA S.A.",
    "MINERA LA ZANJA S.R.L.",
    "CIA MINERA COIMOLACHE SA"
]

# --- Filtrar data base
df_cli_filtrado = df_cli[df_cli["Año"].isin(anios_sel)]
df_largo = df_cli_filtrado.melt(
    id_vars=["razon_social", "Año"],
    value_vars=columnas_meses,
    var_name="Mes",
    value_name="Ventas"
)

# Limpiar nombres
df_largo["Mes"] = df_largo["Mes"].str.replace("vta_", "").str.capitalize()
df_largo["Etiqueta"] = df_largo["Mes"] + " - " + df_largo["Año"]

# Filtrar por meses seleccionados y clientes clave
df_largo = df_largo[df_largo["Mes"].isin(meses_sel)]
df_largo = df_largo[df_largo["razon_social"].isin(clientes_clave)]

# Agrupar por cliente y etiqueta (mes-año)
df_agrupado = df_largo.groupby(["razon_social", "Etiqueta"], as_index=False)["Ventas"].sum()

# Ordenar etiquetas cronológicamente
orden_meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
               'Julio', 'Agosto', 'Setiembre', 'Octubre', 'Noviembre', 'Diciembre']

# Crear columna auxiliar para ordenar etiquetas (año + número de mes)
mes_a_num = {mes: str(i+1).zfill(2) for i, mes in enumerate(orden_meses)}
df_agrupado["orden"] = df_agrupado["Etiqueta"].apply(
    lambda x: x.split(" - ")[1] + "-" + mes_a_num[x.split(" - ")[0]]
)
df_agrupado = df_agrupado.sort_values("orden")

# --- Gráfico
fig2 = go.Figure()

etiquetas_ordenadas = df_agrupado["Etiqueta"].unique()

for etiqueta in etiquetas_ordenadas:
    df_temp = df_agrupado[df_agrupado["Etiqueta"] == etiqueta]
    fig2.add_trace(go.Bar(
        x=df_temp["razon_social"],
        y=df_temp["Ventas"],
        name=etiqueta
    ))

fig2.update_layout(
    barmode='group',
    title=f"Ventas por Cliente - por Mes y Año",
    xaxis_title="Cliente",
    yaxis_title="Monto de Ventas ($)",
    height=600
)

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
