"""
Copa do Mundo — Dashboard
Consultas avançadas (não-triviais) e visualizações com Plotly.
Inclui: LEFT JOIN, GROUP BY, SUM, COUNT, AVG, TIMESTAMPDIFF, CASE WHEN, COALESCE.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from db_connection import fetch_dataframe

st.set_page_config(page_title="Dashboard — Copa do Mundo", page_icon="📊", layout="wide")

with open("style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("# 📊 Dashboard")
st.markdown("Visualizações gráficas e consultas avançadas — LEFT JOIN, GROUP BY, TIMESTAMPDIFF, agregações")
st.markdown("---")

# Plotly theme helper
PLOTLY_LAYOUT = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#b0b8d1", family="Inter", size=12),
    title_font=dict(color="#d4af37", family="Montserrat", size=18),
    legend=dict(font=dict(color="#b0b8d1")),
    margin=dict(l=20, r=20, t=50, b=20),
)

GOLD = "#d4af37"
GOLD_LIGHT = "#f0d060"
BLUE = "#3949ab"
GREEN = "#4caf50"
RED = "#ef5350"
YELLOW = "#fdd835"


# ============================================================
# 1. Total de Gols por Seleção
# SUM + CASE WHEN + LEFT JOIN + GROUP BY
# ============================================================
st.markdown("### ⚽ Total de Gols por Seleção")
try:
    df_gols = fetch_dataframe("""
        SELECT s.nome_selecao,
               COALESCE(SUM(CASE
                   WHEN p.id_selecao_1 = s.id_selecao THEN p.quantidade_gols_selecao_1
                   WHEN p.id_selecao_2 = s.id_selecao THEN p.quantidade_gols_selecao_2
                   ELSE 0 END), 0) AS total_gols
        FROM selecoes s
        LEFT JOIN partidas p ON s.id_selecao = p.id_selecao_1 OR s.id_selecao = p.id_selecao_2
        GROUP BY s.id_selecao, s.nome_selecao
        ORDER BY total_gols DESC
    """)

    if not df_gols.empty:
        fig = px.bar(
            df_gols, x="total_gols", y="nome_selecao",
            orientation="h",
            title="Total de Gols por Seleção",
            labels={"total_gols": "Gols", "nome_selecao": "Seleção"},
            color="total_gols",
            color_continuous_scale=[[0, BLUE], [0.5, GOLD], [1, GOLD_LIGHT]],
        )
        fig.update_layout(**PLOTLY_LAYOUT)
        fig.update_layout(coloraxis_showscale=False, yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("📄 Ver consulta SQL"):
            st.code("""SELECT s.nome_selecao,
       COALESCE(SUM(CASE
           WHEN p.id_selecao_1 = s.id_selecao THEN p.quantidade_gols_selecao_1
           WHEN p.id_selecao_2 = s.id_selecao THEN p.quantidade_gols_selecao_2
           ELSE 0 END), 0) AS total_gols
FROM selecoes s
LEFT JOIN partidas p ON s.id_selecao = p.id_selecao_1
                     OR s.id_selecao = p.id_selecao_2
GROUP BY s.id_selecao, s.nome_selecao
ORDER BY total_gols DESC""", language="sql")
    else:
        st.info("Sem dados de partidas disponíveis.")
except Exception as e:
    st.error(f"Erro: {e}")

st.markdown("---")

# ============================================================
# 2 e 3 lado a lado
# ============================================================
col_a, col_b = st.columns(2)

# 2. Cartões por Jogador (Stacked)
# SUM + CASE WHEN + COUNT + INNER JOIN + GROUP BY
with col_a:
    st.markdown("### 🟨 Cartões por Jogador")
    try:
        df_cartoes = fetch_dataframe("""
            SELECT j.nome_jogador,
                   SUM(CASE WHEN c.cor_cartao = 'Amarelo' THEN 1 ELSE 0 END) AS amarelos,
                   SUM(CASE WHEN c.cor_cartao = 'Vermelho' THEN 1 ELSE 0 END) AS vermelhos,
                   COUNT(c.`id_cartao`) AS total
            FROM jogadores j
            INNER JOIN `cartoes` c ON j.id_jogador = c.id_jogador
            GROUP BY j.id_jogador, j.nome_jogador
            ORDER BY total DESC
        """)

        if not df_cartoes.empty:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=df_cartoes["nome_jogador"], x=df_cartoes["amarelos"],
                name="Amarelos", orientation="h",
                marker_color=YELLOW,
            ))
            fig.add_trace(go.Bar(
                y=df_cartoes["nome_jogador"], x=df_cartoes["vermelhos"],
                name="Vermelhos", orientation="h",
                marker_color=RED,
            ))
            fig.update_layout(**PLOTLY_LAYOUT, barmode="stack", title="Cartões por Jogador")
            fig.update_layout(yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sem cartões registrados.")
    except Exception as e:
        st.error(f"Erro: {e}")

# 3. Média de Capacidade por País
# AVG + COUNT + GROUP BY
with col_b:
    st.markdown("### 🏟️ Média de Capacidade por País")
    try:
        df_cap = fetch_dataframe("""
            SELECT pais,
                   ROUND(AVG(capacidade)) AS media_capacidade,
                   COUNT(*) AS qtd_estadios
            FROM estadios
            GROUP BY pais
            ORDER BY media_capacidade DESC
        """)

        if not df_cap.empty:
            fig = px.bar(
                df_cap, x="pais", y="media_capacidade",
                title="Capacidade Média dos Estádios por País",
                labels={"media_capacidade": "Capacidade Média", "pais": "País"},
                color="media_capacidade",
                color_continuous_scale=[[0, BLUE], [1, GREEN]],
                text="qtd_estadios",
            )
            fig.update_traces(texttemplate="%{text} estádio(s)", textposition="outside")
            fig.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sem estádios cadastrados.")
    except Exception as e:
        st.error(f"Erro: {e}")

st.markdown("---")

# ============================================================
# 4. Distribuição de Idade dos Jogadores
# TIMESTAMPDIFF + LEFT JOIN
# ============================================================
st.markdown("### 🎂 Distribuição de Idade dos Jogadores")
st.caption("Consulta não-trivial: `TIMESTAMPDIFF(YEAR, data_nascimento, CURDATE())`")

try:
    df_idade = fetch_dataframe("""
        SELECT j.nome_jogador,
               TIMESTAMPDIFF(YEAR, j.data_nascimento, CURDATE()) AS idade,
               j.posicao,
               s.nome_selecao
        FROM jogadores j
        LEFT JOIN selecoes s ON j.id_selecao = s.id_selecao
        ORDER BY idade
    """)

    if not df_idade.empty:
        col_c, col_d = st.columns(2)
        with col_c:
            fig = px.histogram(
                df_idade, x="idade",
                title="Histograma de Idades",
                labels={"idade": "Idade", "count": "Jogadores"},
                color_discrete_sequence=[GOLD],
                nbins=10,
            )
            fig.update_layout(**PLOTLY_LAYOUT)
            st.plotly_chart(fig, use_container_width=True)

        with col_d:
            fig = px.box(
                df_idade, x="posicao", y="idade",
                title="Idade por Posição",
                labels={"idade": "Idade", "posicao": "Posição"},
                color="posicao",
                color_discrete_sequence=[GOLD, BLUE, GREEN, RED, GOLD_LIGHT],
            )
            fig.update_layout(**PLOTLY_LAYOUT)
            st.plotly_chart(fig, use_container_width=True)

        with st.expander("📊 Tabela de Idades"):
            df_display = df_idade.copy()
            df_display.columns = ["Jogador", "Idade", "Posição", "Seleção"]
            st.dataframe(df_display, use_container_width=True, hide_index=True)

        with st.expander("📄 Ver consulta SQL"):
            st.code("""SELECT j.nome_jogador,
       TIMESTAMPDIFF(YEAR, j.data_nascimento, CURDATE()) AS idade,
       j.posicao, s.nome_selecao
FROM jogadores j
LEFT JOIN selecoes s ON j.id_selecao = s.id_selecao
ORDER BY idade""", language="sql")
    else:
        st.info("Sem jogadores cadastrados.")
except Exception as e:
    st.error(f"Erro: {e}")

st.markdown("---")

# ============================================================
# 5 e 6 lado a lado
# ============================================================
col_e, col_f = st.columns(2)

# 5. Partidas por Estádio (Donut)
# LEFT JOIN + COUNT + GROUP BY
with col_e:
    st.markdown("### 🏟️ Partidas por Estádio")
    try:
        df_part_est = fetch_dataframe("""
            SELECT e.nome_estadio,
                   COUNT(p.id_partida) AS total_partidas
            FROM estadios e
            LEFT JOIN partidas p ON e.id_estadio = p.id_estadio
            GROUP BY e.id_estadio, e.nome_estadio
        """)

        if not df_part_est.empty:
            fig = px.pie(
                df_part_est, values="total_partidas", names="nome_estadio",
                title="Distribuição de Partidas por Estádio",
                hole=0.4,
                color_discrete_sequence=[GOLD, BLUE, GREEN, GOLD_LIGHT, "#7c4dff", "#00bcd4"],
            )
            fig.update_layout(**PLOTLY_LAYOUT)
            fig.update_traces(textfont=dict(color="#ffffff"))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sem dados disponíveis.")
    except Exception as e:
        st.error(f"Erro: {e}")

# 6. Seleções por Continente (Pie)
# COUNT + GROUP BY
with col_f:
    st.markdown("### 🌍 Seleções por Continente")
    try:
        df_cont = fetch_dataframe("""
            SELECT continente, COUNT(*) AS total
            FROM selecoes
            GROUP BY continente
            ORDER BY total DESC
        """)

        if not df_cont.empty:
            fig = px.pie(
                df_cont, values="total", names="continente",
                title="Distribuição de Seleções por Continente",
                color_discrete_sequence=[GOLD, BLUE, GREEN, RED, GOLD_LIGHT, "#7c4dff"],
            )
            fig.update_layout(**PLOTLY_LAYOUT)
            fig.update_traces(textfont=dict(color="#ffffff"))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sem seleções cadastradas.")
    except Exception as e:
        st.error(f"Erro: {e}")

st.markdown("---")

# ============================================================
# 7. Jogadores por Seleção
# LEFT JOIN + COUNT + GROUP BY
# ============================================================
st.markdown("### 👥 Jogadores por Seleção")
try:
    df_jog_sel = fetch_dataframe("""
        SELECT s.nome_selecao,
               COUNT(j.id_jogador) AS total_jogadores
        FROM selecoes s
        LEFT JOIN jogadores j ON s.id_selecao = j.id_selecao
        GROUP BY s.id_selecao, s.nome_selecao
        ORDER BY total_jogadores DESC
    """)

    if not df_jog_sel.empty:
        fig = px.bar(
            df_jog_sel, x="nome_selecao", y="total_jogadores",
            title="Total de Jogadores por Seleção",
            labels={"total_jogadores": "Jogadores", "nome_selecao": "Seleção"},
            color="total_jogadores",
            color_continuous_scale=[[0, BLUE], [0.5, GOLD], [1, GOLD_LIGHT]],
            text="total_jogadores",
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Sem seleções cadastradas.")
except Exception as e:
    st.error(f"Erro: {e}")

st.markdown("---")

# ============================================================
# Resumo das Consultas Não-Triviais
# ============================================================
st.markdown("### 📝 Consultas Não-Triviais Utilizadas")
st.markdown(
    """
| # | Consulta | Técnicas SQL |
|---|---|---|
| 1 | Total de Gols por Seleção | `SUM`, `CASE WHEN`, `COALESCE`, `LEFT JOIN`, `GROUP BY` |
| 2 | Cartões por Jogador | `SUM`, `CASE WHEN`, `COUNT`, `INNER JOIN`, `GROUP BY` |
| 3 | Média de Capacidade por País | `AVG`, `ROUND`, `COUNT`, `GROUP BY` |
| 4 | Distribuição de Idade | `TIMESTAMPDIFF`, `CURDATE()`, `LEFT JOIN` |
| 5 | Partidas por Estádio | `LEFT JOIN`, `COUNT`, `GROUP BY` |
| 6 | Seleções por Continente | `COUNT`, `GROUP BY` |
| 7 | Jogadores por Seleção | `LEFT JOIN`, `COUNT`, `GROUP BY` |
"""
)

# Footer
st.markdown("---")
st.markdown(
    """
<div style="text-align: center; color: #6b7394; font-size: 0.8rem; padding: 1rem 0;">
    📊 Dashboard — Consultas avançadas com LEFT JOIN, GROUP BY, TIMESTAMPDIFF e funções de agregação
</div>
""",
    unsafe_allow_html=True,
)
