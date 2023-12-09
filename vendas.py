import locale

import pandas as pd
import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards


# funcao para carregar dados
@st.cache_data
def carregar_dados():
    df = pd.read_excel("Vendas.xlsx")
    return df


locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")


def main():
    # Configurações de página
    st.set_page_config(page_title="Vendas", layout="wide", page_icon="💸")
    # Título
    st.title("Dashboard de Vendas ✅")

    # carregar dados
    df = carregar_dados()

    # filtror por ano
    ano_filtrado = st.sidebar.selectbox(
        "Selecione o ano:", ["Todos", *df["Ano"].unique()]
    )

    # aplicar filtro se não selecionar todos
    if ano_filtrado != "Todos":
        df_filtrado = df[df["Ano"] == ano_filtrado]
    else:
        df_filtrado = df

    total_custo = df_filtrado["Custo"].sum()
    total_custo_formatado = locale.currency(total_custo, grouping=True)

    total_lucro = df_filtrado["Lucro"].sum()
    total_lucro_formatado = locale.currency(total_lucro, grouping=True)

    total_clientes_ativos = df_filtrado["ID Cliente"].nunique()

    # criando colunas dos card
    col1, col2, col3 = st.columns(3)

    # metricas dos cards
    with col1:
        st.metric("Custo Total", total_custo_formatado)

    with col2:
        st.metric("Lucro Total", total_lucro_formatado)

    with col3:
        st.metric("Total de Clientes Ativos", total_clientes_ativos)
        style_metric_cards(border_left_color="purple")

    # stylezando o cards com as metricas
    st.markdown(
        """
    <style>
    [data-testid="stMetricValue"] {
        font-size: 18px;
        color: rgba(0,0,0,0,)
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
    # dfs para os graficos
    produtos_marca = (
        df.groupby("Marca")["Quantidade"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    lucro_por_categoria = (
        df.groupby("Categoria")["Lucro"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    import plotly.express as px

    # criando 2 colunas para os graficos
    col1, col2 = st.columns(2)

    # grafico 1 de produtos vendidos por marca
    fig = px.bar(
        produtos_marca,
        x="Quantidade",
        y="Marca",
        orientation="h",
        title="Produtos Vendidos por Marca",
        color="Marca",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        text="Quantidade",
    )

    # centralizar o titulo
    fig.update_layout(title_x=0.1)

    col1.plotly_chart(fig, use_container_width=True)

    # grafico 2 lucro por categoria pizza
    fig1 = px.pie(
        lucro_por_categoria,
        values="Lucro",
        names="Categoria",
        title="Lucro por Categoria",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        hole=0.6,
    )

    # centralizar o titulo
    fig1.update_layout(title_x=0.1)

    col2.plotly_chart(fig1, use_container_width=True)

    # df para o grafico 3
    lucro_mes_categoria = (
        df.groupby(["mes_ano", "Categoria"])["Lucro"].sum().reset_index()
    )

    # grafico 3 lucro x mes x categoria
    fig2 = px.line(
        lucro_mes_categoria,
        x="mes_ano",
        y="Lucro",
        title="Lucro x Mês x Categoria",
        color="Categoria",
        markers=True,
    )
    st.plotly_chart(fig2)


if __name__ == "__main__":
    main()
