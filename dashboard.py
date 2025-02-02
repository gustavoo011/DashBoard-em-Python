import streamlit as st #lib que constrói os dashboards
import pandas as pd #manipular arquivos
import plotly.express as px # construção de gráficos

# Objetivos - MENSAIS
# Faturamento por unidade
# Tipo de produto mais vendido
# Desempenho das formas de pagamento
# Avaliação das filiais

st.set_page_config(layout="wide") #config layout

df = pd.read_csv("supermarket_sales.csv", sep=";", decimal=",")

# colocando a coluna date no tipo de dado datetime, pois estava sendo reconhecida como object
df["Date"] = pd.to_datetime(df["Date"])
#df.dtypes
df = df.sort_values(by="Date") #ordenando as dates 

#separando mês e ano
df["Month"] = df["Date"].apply(lambda x: str(x.year)+"-"+ str(x.month))

#sidebar
month = st.sidebar.selectbox("Month", df["Month"].unique())

df_filtrado = df[df["Month"] == month]

#criando as colunas no streamlit - as colunas são como 'divs'
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

#grafico 1
graf_fat= px.bar(df_filtrado, x="Date", y="Total",color="City", title="Faturamento por Dia")
col1.plotly_chart(graf_fat,  use_container_width=True)

#grafico2
graf_prod = px.bar(df_filtrado, x = "Date", y="Product line", color="City", title="Faturamento por tipo de Produto", orientation="h")
col2.plotly_chart(graf_prod,  use_container_width=True)

#grafico3
#agrupamento por city
city_total = df_filtrado.groupby("City")[["Total"]].sum().reset_index()
graf_cit= px.bar(city_total, x="City", y="Total", title="Faturamento por Filial")
col3.plotly_chart(graf_cit,  use_container_width=True)

#grafico4
graf_tip = px.pie(df_filtrado, values="Total", names="Payment", title="Faturamento por tipo de pagamento")
col4.plotly_chart(graf_tip,  use_container_width=True)

#grafico5
city_total = df_filtrado.groupby("City")[["Rating"]].mean().reset_index()
graf_aval= px.bar(df_filtrado, y="Rating",  x="City", title="Avaliação")
col5.plotly_chart(graf_aval, use_container_width=True)