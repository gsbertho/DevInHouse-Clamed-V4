import streamlit as st
import pandas as pd
from src.utils.postgres_utils import criar_conexao
import seaborn as sns
import matplotlib.pyplot as plt

#configurar nome na aba e layout
st.set_page_config(
    page_title="📊 Dashboard de Vendas",
    layout="wide"
)

#título do dashboard
st.title("📊 Dashboard de Vendas e Market Share")

# =========================
# CARREGAMENTO DOS DADOS
# =========================

@st.cache_data
def load_data(sql: str) -> pd.DataFrame:
    """
    Executa uma consulta SQL no PostgreSQL e retorna os resultados
    como um DataFrame pandas.

    Args:
        sql (str): Query SQL a ser executada.

    Returns:
        pd.DataFrame: DataFrame contendo os dados retornados pela consulta.
    """

    conn = criar_conexao()

    try:
        df = pd.read_sql(sql, conn)
    finally:
        conn.close()

    return df

sql_dim_produto = "select * from silver.dim_produto"
sql_dim_filial = "select * from silver.dim_filial"
sql_vendas = "select * from gold.vw_vendas_mensais"
sql_share = "select * from gold.vw_market_share_mensal"

#explorar queries independentes da camada gold
sql_vendas_produtos = """
SELECT
    date_trunc('month', v.data) :: date AS mes
  , v.empresa
  , f.brick
  , p.nome_produto
  , p.categoria
  , SUM(v.volume) AS total_volume
FROM silver.fato_vendas v
JOIN silver.dim_produto p
  ON v.produto_id = p.produto_id
JOIN silver.dim_filial f
  ON v.filial_id = f.filial_id
GROUP BY 1, 2, 3, 4, 5;
"""

df_vendas = load_data(sql_vendas)
df_share = load_data(sql_share)
df_dim_produto = load_data(sql_dim_produto)
df_dim_filial = load_data(sql_dim_filial)
df_vendas_produtos = load_data(sql_vendas_produtos)

# =========================
# CRIAR FUNCOES AUX
# =========================

def format_inteiro_br(valor):
    return f"{valor:,.0f}".replace(",", ".")

def format_monetario_br(valor):
    return f"R$ {valor:,.2f}".replace(",", "x").replace(".", ",").replace("x", ".")

# =========================
# FILTROS
# =========================

#valores únicos para os filtros
#meses
un_meses = sorted(df_vendas["mes"].unique())

#categorias
un_categorias = sorted(df_dim_produto["categoria"].unique())

#bricks
un_bricks = sorted(df_dim_filial["brick"].unique())


st.sidebar.header("Filtros")

mes = st.sidebar.multiselect(
    "Mês",
    options=un_meses,
    default=un_meses
)

categoria = st.sidebar.multiselect(
    "Categoria",
    options=un_categorias,
    default=un_categorias
)

brick = st.sidebar.multiselect(
    "Brick",
    options=un_bricks,
    default=un_bricks
)


#aplicando filtros no df_vendas
df_vendas = df_vendas[
    (df_vendas["brick"].isin(brick)) &
    (df_vendas["categoria"].isin(categoria)) &
    (df_vendas["mes"].isin(mes))
]

#aplicando filtros no df_share
df_share = df_share[
    (df_share["brick"].isin(brick)) &
    (df_share["categoria"].isin(categoria)) &
    (df_share["mes"].isin(mes))
]

#aplicando filtros no df_vendas_produtos
df_vendas_produtos = df_vendas_produtos[
    (df_vendas_produtos["brick"].isin(brick)) &
    (df_vendas_produtos["categoria"].isin(categoria)) &
    (df_vendas_produtos["mes"].isin(mes))
]

# =========================
# KPIs
# =========================

st.subheader("KPIs")

col1, col2, col3 = st.columns([1, 2, 1])

# criar métricas baseadas na tabela vendas
#pré filtrar df_vendas
df_clamed = df_vendas[df_vendas["empresa"] == "Clamed"]
df_conc = df_vendas[df_vendas["empresa"] == "Concorrente"]

#volume
vol_clamed = df_clamed["total_volume"].sum()
vol_conc = df_conc["total_volume"].sum()
vol_mercado = df_vendas["total_volume"].sum()

#receita
rec_clamed = df_clamed["total_receita"].sum()
rec_conc = df_conc["total_receita"].sum()
rec_mercado = df_vendas["total_receita"].sum()

#gap de preço médio percentual
preco_medio_clamed = (
    rec_clamed / vol_clamed if vol_clamed != 0 else 0 
)

preco_medio_conc = (
    rec_conc / vol_conc if vol_conc != 0 else 0 
)

gap_perc = (
    preco_medio_clamed / preco_medio_conc - 1 if preco_medio_conc != 0 else 0
)

gap_abs = preco_medio_clamed - preco_medio_conc

# =========================
# KPI 1 - share
# =========================

#Market Share Clamed
share_clamed_vol = (
    vol_clamed / vol_mercado if vol_mercado != 0 else 0
)

share_clamed_rec = (
    rec_clamed / rec_mercado if rec_mercado != 0 else 0
)

with col1:
    st.text("Market Share Clamed")

    st.metric("por volume", f"{share_clamed_vol:.2%}")
    st.metric("por receita", f"{share_clamed_rec:.2%}")

# =========================
# KPI 2 - totais
# =========================

with col2:
    st.text("Totais Mercado")

    subcol1, subcol2 = st.columns(2)

    with subcol1:
        st.metric("volume conc", format_inteiro_br(vol_conc))
        st.metric("volume clamed", format_inteiro_br(vol_clamed))

    with subcol2:
        st.metric("receita conc", format_monetario_br(rec_conc))
        st.metric("receita clamed", format_monetario_br(rec_clamed))


# =========================
# KPI 3 - GAP PREÇO MÉDIO
# =========================

with col3:
    st.text("Gap de Preço Médio")
    st.metric("Percentual", f"{gap_perc:.2%}")
    st.metric("Absoluto", format_monetario_br(gap_abs))

# =========================
# Análise de potencial de crescimento por brick
# =========================

#filtra apenas Clamed pois dados de mercado se repetem para cada chave e agrupa
df_potencial_brick = df_share[df_share['empresa'] == "Clamed"].groupby('brick').agg({
    'total_volume' : 'sum',
    'total_mercado_volume' : 'sum'
})

#renomear colunas para facilitar entendimento no dashboard
df_potencial_brick.rename(columns={
    "total_volume": "volume_clamed",
    "total_mercado_volume": "volume_mercado"
}, inplace=True)

#criar coluna de volume em potencial (volume concorrentes)
df_potencial_brick['volume_concorrente (alvo)'] = (
    df_potencial_brick['volume_mercado'] -
    df_potencial_brick['volume_clamed']
)

#criar coluna share clamed
df_potencial_brick['share_clamed'] = df_potencial_brick['volume_clamed'] / df_potencial_brick['volume_mercado']

#ordenar do menor pro maior share
df_potencial_brick.sort_values(by='share_clamed', ascending=True, inplace=True)

st.subheader("Bricks com maior potencial de crescimento em volume")
st.text('Verifica os top 5 bricks com menor participação da clamed em volume e apresenta volume dos concorrentes')
st.dataframe(
    df_potencial_brick.head().style.format({
        "share_clamed": "{:.2%}",
        "volume_clamed": lambda x: f"{x:,.0f}".replace(",", "."),
        "volume_mercado": lambda x: f"{x:,.0f}".replace(",", "."),
        "volume_concorrente (alvo)": lambda x: f"{x:,.0f}".replace(",", ".")
    })
)

# =========================
# Gráfico de evolução de volume
# =========================

st.subheader("Evolução de Volume")

df_plot = (
    df_vendas
    .groupby(["mes", "empresa"])["total_volume"]
    .sum()
    .reset_index()
    .sort_values("mes")
)

fig, ax = plt.subplots(figsize=(10, 5))

for empresa in df_plot["empresa"].unique():
    df_temp = df_plot[df_plot["empresa"] == empresa]

    ax.plot(
        df_temp["mes"],
        df_temp["total_volume"],
        marker="o",
        label=empresa
    )

ax.set_title("Evolução de Volume - Clamed vs Concorrência")
ax.set_xlabel("Mês")
ax.set_ylabel("Volume")
ax.legend()

st.pyplot(fig)

# =========================
# HEATMAP (simples)
# =========================

# agregação
df_heat = (
    df_vendas
    .groupby(["brick", "empresa"])["total_volume"]
    .sum()
    .reset_index()
)

# pivot
pivot = df_heat.pivot(
    index="brick",
    columns="empresa",
    values="total_volume"
).fillna(0)

# ordenar por volume total
pivot = pivot.loc[pivot.sum(axis=1).sort_values(ascending=False).index]

# plot
fig, ax = plt.subplots(figsize=(6, 6))

sns.heatmap(
    pivot,
    cmap="Blues",
    linewidths=0.3,
    annot=True,
    fmt=".0f",         # inteiro (sem decimal)
    cbar=True,
    ax=ax
)

ax.set_title("Volume por Brick (Clamed vs Concorrente)")
ax.set_xlabel("")
ax.set_ylabel("")

#exibir
st.subheader("Volume por Brick")    
st.pyplot(fig)

# =========================
# TABELA completa - view share
# =========================

st.subheader("Tabela Detalhada - Market Share com crescimento MOM")
st.text("Análise detalhada por brick, categoria e mês")
st.dataframe(
    df_share
    .sort_values(by=["brick", "categoria", "mes", "empresa"])
    .style.format({
        # percentuais
        "share_volume": "{:.2%}",
        "share_receita": "{:.2%}",
        "mom_volume": "{:.2%}",
        "mom_receita": "{:.2%}",

        # volumes 
        "total_volume": lambda x: f"{x:,.0f}".replace(",", "."),
        "total_mercado_volume": lambda x: f"{x:,.0f}".replace(",", "."),
        
        # receitas
        "total_receita": lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        "total_mercado_receita": lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
    })
)


# =========================
# Gráfico TOP 10 produtos
# =========================

# agregação por produto + empresa
df_p = (
    df_vendas_produtos
    .groupby(["nome_produto", "empresa"])["total_volume"]
    .sum()
    .reset_index()
)

# pivot
pivot = df_p.pivot(
    index="nome_produto",
    columns="empresa",
    values="total_volume"
).fillna(0)

# top 10 produtos por volume total
pivot["total"] = pivot.sum(axis=1)
pivot = pivot.sort_values("total", ascending=False).head(10)

# plot
fig, ax = plt.subplots(figsize=(10, 5))

pivot[["Clamed", "Concorrente"]].plot(
    kind="bar",
    ax=ax
)

ax.set_title("Top 10 Produtos - Volume (Clamed vs Concorrente)")
ax.set_ylabel("Volume")
ax.set_xlabel("Produto")
ax.tick_params(axis='x', rotation=45)

# exibir
st.subheader("Análise por produtos")
st.text("Top 10 produtos em volume no mercado")
st.pyplot(fig)

# =========================
# Tabela geral produtos
# =========================

# agregação por produto + empresa
df_prod = (
    df_vendas_produtos
    .groupby(["nome_produto", "empresa"])["total_volume"]
    .sum()
    .reset_index()
)

# pivot
df_prod = df_prod.pivot(
    index="nome_produto",
    columns="empresa",
    values="total_volume"
).fillna(0)

# renomear
df_prod = df_prod.rename(columns={
    "Clamed": "volume_clamed",
    "Concorrente": "volume_conc"
})

# criar share
df_prod["share_clamed"] = (
    df_prod["volume_clamed"] / (df_prod["volume_clamed"] + df_prod["volume_conc"])
)

# resetar índice para virar coluna
df_prod = df_prod.reset_index()

# exibir
st.subheader("Tabela detalhada produtos")
st.dataframe(
    df_prod
        .style.format({
        "volume_clamed":  lambda x: f"{x:,.0f}".replace(",", "."),
        "volume_conc":  lambda x: f"{x:,.0f}".replace(",", "."),
        "share_clamed": "{:.2%}"
        })
    )