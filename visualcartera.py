import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from PIL import Image  # Necesario si vas a ajustar el tamaño o usar rutas locales



st.set_page_config(page_title="Dashboard de Llamadas de Cartera", layout="wide")
# Mostrar logo
col1, col2 = st.columns([4, 1])  # más espacio para el título

with col1:
    st.title("📞 Dashboard de Llamadas de Cartera")

with col2:
    image = Image.open("images/CUN-1200X1200.png")  # o solo "CUN-1200X1200.png" si está en la raíz
    st.image(image, width=200) 
#st.title("📞 Dashboard de Llamadas de Cartera")

# ==========================
# Cargar datos desde archivos CSV
# ==========================
df_puntaje = pd.read_csv("data/puntaje_promedio_por_asesor.csv")
df_detalle = pd.read_csv("data/promedio_conteo_por_categoria.csv")
df_sentimiento = pd.read_csv("data/sentimiento_general.csv")
df_polaridad_asesor = pd.read_csv("data/polaridad_por_asesor.csv")
df_resultados = pd.read_csv("data/resultados_por_asesor.csv")


# ==========================
# 1. Puntaje promedio total por asesor
# ==========================
 # Puedes ajustar el tamaño con width
st.subheader("🎯 Puntaje Promedio Total por Asesor")

fig1 = px.bar(
    df_puntaje.sort_values("puntaje_promedio", ascending=False),
    x="asesor",
    y="puntaje_promedio",
    text="puntaje_promedio",
    color="puntaje_promedio",
    color_continuous_scale=[  # Gama más oscura de verdes
        "#c7e9c0","#a1d99b","#41ab5d","#74c476","#004b23"   
    ],
    labels={"puntaje_promedio": "Puntaje Promedio", "asesor": "Asesor"},
    title=""
)

fig1.update_traces(texttemplate='%{text:.2%}', textposition='outside')

fig1.update_layout(
    height=800,
    yaxis_tickformat=".0%",
    xaxis=dict(
        tickfont=dict(size=14, color="black", family="Arial ")  # ⬅️ Estilo fuerte para asesores
    ),
    font=dict(family="Arial", size=12, color="black")
)

st.plotly_chart(fig1, use_container_width=True)


# ==========================
# 2. Promedio de Conteo por Categoría y Asesor
# ==========================
st.subheader("🔍 Promedio de Conteo por Categoría y Asesor")

pivot = df_detalle.pivot(index="asesor", columns="categoria", values="promedio_conteo")

fig2 = go.Figure(data=go.Heatmap(
    z=pivot.values,
    x=pivot.columns,
    y=pivot.index,
    colorscale=[
        [0.0, "#c7e9c0"],
        [0.2, "#a1d99b"],
        [0.4, "#74c476"],
        [0.6, "#41ab5d"],
        [0.8, "#238b45"],
        [1.0, "#006d2c"]
    ],
    showscale=True,
    colorbar=dict(title="Conteo Promedio"),
    zmin=0,
    zmax=2,
    hovertemplate='Categoría: %{x}<br>Asesor: %{y}<br>Conteo: %{z}<extra></extra>'
))

fig2.update_layout(
    height=600,
    yaxis=dict(
        tickfont=dict(size=14, color="black", family="Arial")
    ),
    font=dict(family="Arial", size=12, color="black")
)

st.plotly_chart(fig2, use_container_width=True)



# ==========================
# 3 y 4. Indicadores de Polaridad y Subjectividad
# ==========================
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔍 Polaridad Promedio General de las Llamadas")
    polaridad_total = df_sentimiento["polarity"].mean()
    fig3 = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=polaridad_total,
        delta={'reference': 0},
        gauge={
            'axis': {'range': [-1, 1]},
            'bar': {'color': 'green'},
            'steps': [
                {'range': [-1, -0.3], 'color': '#c7e9c0'},
                {'range': [-0.3, 0.3], 'color': '#a1d99b'},
                {'range': [0.3, 1], 'color': '#31a354'}
            ],
            'threshold': {'line': {'color': "black", 'width': 2}, 'thickness': 0.75, 'value': polaridad_total}
        }
    ))
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("🔍 Subjectividad Promedio General de las Llamadas")
    subjectividad_total = df_sentimiento["subjectivity"].mean()
    fig4 = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=subjectividad_total,
        delta={'reference': 0.5},
        gauge={
            'axis': {'range': [0, 1]},
            'bar': {'color': 'green'},
            'steps': [
                {'range': [0, 0.3], 'color': '#e5f5e0'},
                {'range': [0.3, 0.7], 'color': '#a1d99b'},
                {'range': [0.7, 1], 'color': '#31a354'}
            ],
            'threshold': {'line': {'color': "black", 'width': 2}, 'thickness': 0.75, 'value': subjectividad_total}
        }
    ))
    st.plotly_chart(fig4, use_container_width=True)

# ==========================
# 5. Polaridad promedio por asesor (barra horizontal)
# ==========================
st.subheader("📊 Promedio de Polaridad por Asesor (CUN)")

fig5 = px.bar(
    df_polaridad_asesor,
    x="polarity",
    y="asesor",
    orientation='h',
    color="polarity",
    color_continuous_scale="Greens",
    text="polarity",
    labels={"polarity": "Polaridad", "asesor": "Asesor"},
    title=""
)

fig5.update_traces(texttemplate='%{text:.2f}', textposition='outside')

fig5.update_layout(
    height=600,
    yaxis=dict(
        tickfont=dict(size=14, color="black", family="Arial")  # ⬅️ Negrita simulada
    ),
    font=dict(family="Arial", size=10,color="black")
)

st.plotly_chart(fig5, use_container_width=True)

# ==========================
# 6. Análisis Detallado por Asesor
# ==========================
st.subheader("🗂️ Análisis Detallado por Asesor")

requisitos = {
    "saludo": (1, 0.05),
    "indagacion": (4, 0.20),
    "programas": (3, 0.15),
    "argumentacion": (20, 0.30),
    "objecion": (4, 0.20),
    "cierre": (3, 0.20)
}

# Verificamos que el dataframe no esté vacío
if df_resultados.empty:
    st.warning("No hay datos disponibles para mostrar el análisis detallado por asesor.")
else:
    for asesor, grupo in df_resultados.groupby("asesor"):
        with st.expander(f"👤 {asesor} — {len(grupo)} llamadas"):
            for _, fila in grupo.iterrows():
                st.markdown(f"**📄 Archivo:** `{fila['archivo']}`")
                for cat, (minimo, _) in requisitos.items():
                    conteo = fila.get(cat, 0)
                    ok = fila.get(f"{cat}_ok", "❌")
                    icon = "✅" if ok == "✅" else "❌"
                    st.markdown(f"- **{cat.capitalize()}:** {conteo} {icon}")
                res_icon = "✅" if fila.get("efectiva", "❌") == "✅" else "❌"
                st.markdown(f"**🎯 Resultado:** {res_icon} — _Puntaje:_ {fila.get('puntaje', 0):.1f}%")
                st.markdown("---")
