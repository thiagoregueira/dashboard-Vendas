import pandas as pd
import streamlit as st


# funcao para carregar dados
@st.cache_data
def carregar_dados():
    df = pd.read_excel("Vendas.xlsx")
    return df


def negative_color(val):
    if val < 0:
        color = "red"
    else:
        color = "black"
    return f"color: {color}"


def main():
    # configuração da pagina
    st.set_page_config(layout="wide", page_icon="🎢")

    # carregar os dados
    df = carregar_dados()

    st.header("Acompanhamento Mensal 📅")
    MoM = df.groupby("mes_ano")["Lucro"].sum().reset_index()
    MoM["LM"] = MoM["Lucro"].shift(1)
    MoM["Variação"] = MoM["Lucro"] - MoM["LM"]
    MoM["% Variação"] = MoM["Variação"] / MoM["LM"] * 100
    MoM["% Variação"] = MoM["% Variação"].map("{:.2f}%".format)
    MoM["% Variação"] = MoM["% Variação"].replace("nan%", "")

    df_styled = (
        MoM.style.format(
            {"LM": "R${:.2f}", "Lucro": "R${:.2f}", "Variação": "{:20,.2f}"}
        )
        .hide(axis="index")
        .applymap(negative_color, subset=["Variação"])
    )

    st.write(df_styled, use_container_width=True)


if __name__ == "__main__":
    main()
