"""
Copa do Mundo — CRUD Jogadores
Inclui cálculo de idade via TIMESTAMPDIFF (consulta não-trivial).
"""

import streamlit as st
import datetime
from db_connection import fetch_all, fetch_dataframe, execute_query, get_next_id, get_flag_url

st.set_page_config(page_title="Jogadores — Copa do Mundo", page_icon="⚽", layout="wide")

with open("style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("# ⚽ Jogadores")
st.markdown("Gerenciamento dos jogadores das seleções — com idade calculada automaticamente")
st.markdown("---")

POSICOES = ["Goleiro", "Zagueiro", "Lateral", "Meio-campista", "Atacante"]

tab1, tab2, tab3, tab4 = st.tabs(["📋 Listar", "➕ Adicionar", "✏️ Editar", "🗑️ Deletar"])

# ============================================================
# READ — Listar Jogadores (com TIMESTAMPDIFF para idade)
# ============================================================
with tab1:
    try:
        # Consulta não-trivial: TIMESTAMPDIFF + LEFT JOIN
        query = """
            SELECT j.id_jogador, j.nome_jogador, j.posicao, j.numero_camisa,
                   j.data_nascimento,
                   TIMESTAMPDIFF(YEAR, j.data_nascimento, CURDATE()) AS idade,
                   s.nome_selecao
            FROM jogadores j
            LEFT JOIN selecoes s ON j.id_selecao = s.id_selecao
            ORDER BY j.nome_jogador
        """

        # Filtros
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            selecoes_list = fetch_all("SELECT id_selecao, nome_selecao FROM selecoes ORDER BY nome_selecao")
            sel_names = ["Todas"] + [s["nome_selecao"] for s in selecoes_list]
            filtro_selecao = st.selectbox("Filtrar por Seleção:", sel_names, key="filtro_sel_jog")
        with col_f2:
            filtro_posicao = st.selectbox("Filtrar por Posição:", ["Todas"] + POSICOES, key="filtro_pos_jog")

        df = fetch_dataframe(query)

        if not df.empty:
            # Aplicar filtros
            if filtro_selecao != "Todas":
                df = df[df["nome_selecao"] == filtro_selecao]
            if filtro_posicao != "Todas":
                df = df[df["posicao"] == filtro_posicao]

            if not df.empty:
                # Exibir como cards estilizados
                for _, row in df.iterrows():
                    flag_url = get_flag_url(row["nome_selecao"], 40)
                    flag_img = f'<img src="{flag_url}" style="width:30px;height:20px;border-radius:2px;vertical-align:middle;margin-right:6px;" />' if flag_url else ""

                    st.markdown(
                        f"""<div class="player-card">
<div class="player-number">#{row["numero_camisa"]}</div>
<div class="player-info">
<div class="player-name">{row["nome_jogador"]}</div>
<div class="player-detail">
{flag_img} {row["nome_selecao"]} &nbsp;|&nbsp; 
🎯 {row["posicao"]} &nbsp;|&nbsp; 
🎂 {row["idade"]} anos &nbsp;|&nbsp;
📅 {row["data_nascimento"]}
</div>
</div>
</div>""",
                        unsafe_allow_html=True,
                    )

                # Tabela detalhada
                with st.expander("📊 Ver tabela completa"):
                    df_display = df.copy()
                    df_display.columns = ["ID", "Nome", "Posição", "Camisa", "Nascimento", "Idade", "Seleção"]
                    st.dataframe(df_display, use_container_width=True, hide_index=True)

                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total de Jogadores", len(df))
                with col2:
                    st.metric("Idade Média", f"{df['idade'].mean():.1f} anos")
                with col3:
                    st.metric("Jogador Mais Jovem", f"{df['idade'].min()} anos")
            else:
                st.info("Nenhum jogador encontrado com os filtros selecionados.")
        else:
            st.info("📭 Nenhum jogador cadastrado ainda.")
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")

# ============================================================
# CREATE — Adicionar Jogador
# ============================================================
with tab2:
    try:
        selecoes = fetch_all("SELECT id_selecao, nome_selecao FROM selecoes ORDER BY nome_selecao")
        if selecoes:
            with st.form("form_add_jogador", clear_on_submit=True):
                st.markdown("### ➕ Novo Jogador")
                nome = st.text_input("Nome do Jogador *", placeholder="Ex: Neymar Jr.")
                col1, col2 = st.columns(2)
                with col1:
                    posicao = st.selectbox("Posição *", POSICOES)
                with col2:
                    numero = st.number_input("Número da Camisa *", min_value=1, max_value=99, value=10, step=1)
                col3, col4 = st.columns(2)
                with col3:
                    data_nasc = st.date_input(
                        "Data de Nascimento *",
                        value=datetime.date(2000, 1, 1),
                        min_value=datetime.date(1970, 1, 1),
                        max_value=datetime.date.today(),
                    )
                with col4:
                    sel_options = {s["nome_selecao"]: s["id_selecao"] for s in selecoes}
                    selecao_nome = st.selectbox("Seleção *", list(sel_options.keys()))

                submitted = st.form_submit_button("✅ Adicionar Jogador")
                if submitted:
                    if nome:
                        try:
                            next_id = get_next_id("jogadores", "id_jogador")
                            execute_query(
                                "INSERT INTO jogadores (id_jogador, nome_jogador, posicao, numero_camisa, data_nascimento, id_selecao) VALUES (%s, %s, %s, %s, %s, %s)",
                                (next_id, nome.strip(), posicao, numero, data_nasc, sel_options[selecao_nome]),
                            )
                            st.success(f"✅ Jogador **{nome}** adicionado com sucesso!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Erro ao adicionar: {e}")
                    else:
                        st.warning("⚠️ Preencha o nome do jogador.")
        else:
            st.warning("⚠️ Cadastre pelo menos uma seleção antes de adicionar jogadores.")
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")

# ============================================================
# UPDATE — Editar Jogador
# ============================================================
with tab3:
    try:
        jogadores = fetch_all(
            """
            SELECT j.*, s.nome_selecao
            FROM jogadores j
            LEFT JOIN selecoes s ON j.id_selecao = s.id_selecao
            ORDER BY j.nome_jogador
        """
        )
        selecoes = fetch_all("SELECT id_selecao, nome_selecao FROM selecoes ORDER BY nome_selecao")

        if jogadores and selecoes:
            options = {f"{j['nome_jogador']} — {j['nome_selecao']}": j for j in jogadores}
            selected = st.selectbox("Selecione o jogador para editar:", list(options.keys()), key="edit_jog_select")
            jog = options[selected]

            with st.form("form_edit_jogador"):
                st.markdown(f"### ✏️ Editando: {jog['nome_jogador']}")
                nome = st.text_input("Nome do Jogador", value=jog["nome_jogador"])
                col1, col2 = st.columns(2)
                with col1:
                    pos_idx = POSICOES.index(jog["posicao"]) if jog["posicao"] in POSICOES else 0
                    posicao = st.selectbox("Posição", POSICOES, index=pos_idx)
                with col2:
                    numero = st.number_input("Número da Camisa", value=int(jog["numero_camisa"]), min_value=1, max_value=99, step=1)
                col3, col4 = st.columns(2)
                with col3:
                    data_val = jog["data_nascimento"]
                    if not isinstance(data_val, datetime.date):
                        data_val = datetime.date(2000, 1, 1)
                    data_nasc = st.date_input("Data de Nascimento", value=data_val)
                with col4:
                    sel_options = {s["nome_selecao"]: s["id_selecao"] for s in selecoes}
                    sel_names = list(sel_options.keys())
                    current_sel = jog.get("nome_selecao", sel_names[0])
                    sel_idx = sel_names.index(current_sel) if current_sel in sel_names else 0
                    selecao_nome = st.selectbox("Seleção", sel_names, index=sel_idx)

                submitted = st.form_submit_button("💾 Salvar Alterações")
                if submitted:
                    try:
                        execute_query(
                            "UPDATE jogadores SET nome_jogador=%s, posicao=%s, numero_camisa=%s, data_nascimento=%s, id_selecao=%s WHERE id_jogador=%s",
                            (nome.strip(), posicao, numero, data_nasc, sel_options[selecao_nome], jog["id_jogador"]),
                        )
                        st.success("✅ Jogador atualizado com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro ao atualizar: {e}")
        else:
            st.info("📭 Nenhum jogador ou seleção cadastrada.")
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")

# ============================================================
# DELETE — Deletar Jogador
# ============================================================
with tab4:
    try:
        jogadores = fetch_all(
            """
            SELECT j.*, s.nome_selecao
            FROM jogadores j
            LEFT JOIN selecoes s ON j.id_selecao = s.id_selecao
            ORDER BY j.nome_jogador
        """
        )
        if jogadores:
            options = {f"{j['nome_jogador']} — {j['nome_selecao']} (#{j['numero_camisa']})": j for j in jogadores}
            selected = st.selectbox("Selecione o jogador para deletar:", list(options.keys()), key="del_jog_select")
            jog = options[selected]

            st.warning(f"⚠️ Tem certeza que deseja deletar o jogador **{jog['nome_jogador']}**?")
            st.caption("Jogadores vinculados a cartões não podem ser deletados.")

            if st.button("🗑️ Confirmar Exclusão", key="btn_del_jogador"):
                try:
                    execute_query("DELETE FROM jogadores WHERE id_jogador = %s", (jog["id_jogador"],))
                    st.success("✅ Jogador deletado com sucesso!")
                    st.rerun()
                except Exception as e:
                    if "foreign key" in str(e).lower() or "constraint" in str(e).lower():
                        st.error("❌ Não é possível deletar este jogador pois ele possui cartões vinculados.")
                    else:
                        st.error(f"❌ Erro ao deletar: {e}")
        else:
            st.info("📭 Nenhum jogador cadastrado para deletar.")
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
