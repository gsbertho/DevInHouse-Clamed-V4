CREATE SCHEMA IF NOT EXISTS gold;

CREATE OR REPLACE VIEW gold.vw_vendas_mensais AS
SELECT
    date_trunc('month', v.data) :: date AS mes
  ,v.empresa
  ,f.brick
  ,p.categoria
  ,SUM(v.volume) AS total_volume
  ,SUM(v.receita) AS total_receita
  ,ROUND(
        SUM(v.receita) / NULLIF(SUM(v.volume), 0)
    , 2) AS preco_medio
FROM silver.fato_vendas v
INNER JOIN silver.dim_produto p
    ON v.produto_id = p.produto_id
INNER JOIN silver.dim_filial f
    ON v.filial_id = f.filial_id
GROUP BY 1, 2, 3, 4;


CREATE OR REPLACE VIEW gold.vw_market_share_mensal AS
WITH base AS (
    SELECT *
    FROM gold.vw_vendas_mensais
),
calc AS (
    SELECT
        mes
      ,empresa
      ,brick
      ,categoria
      ,total_volume
      ,total_receita
      ,SUM(total_volume) OVER (
            PARTITION BY mes, brick, categoria
        ) AS total_mercado_volume
      ,SUM(total_receita) OVER (
            PARTITION BY mes, brick, categoria
        ) AS total_mercado_receita
    FROM base
)
SELECT
    mes
  ,empresa
  ,brick
  ,categoria
  ,total_volume
  ,total_receita
  ,total_mercado_volume
  ,total_mercado_receita
  ,ROUND(
        total_volume::numeric
        / NULLIF(total_mercado_volume, 0)
    ,4) AS share_volume
  ,ROUND(
        total_receita::numeric
        / NULLIF(total_mercado_receita, 0)
    ,4) AS share_receita
  ,ROUND(
        (
            total_volume
            - LAG(total_volume) OVER (
                PARTITION BY empresa, brick, categoria
                ORDER BY mes
            )
        )::numeric
        / NULLIF(
            LAG(total_volume) OVER (
                PARTITION BY empresa, brick, categoria
                ORDER BY mes
            ),
            0
        )
    ,4) AS mom_volume
  ,ROUND(
        (
            total_receita
            - LAG(total_receita) OVER (
                PARTITION BY empresa, brick, categoria
                ORDER BY mes
            )
        )::numeric
        / NULLIF(
            LAG(total_receita) OVER (
                PARTITION BY empresa, brick, categoria
                ORDER BY mes
            ),
            0
        )
    ,4) AS mom_receita
FROM calc;
