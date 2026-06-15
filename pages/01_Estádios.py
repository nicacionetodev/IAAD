"""
Copa do Mundo — CRUD Estádios
"""

import streamlit as st
from db_connection import fetch_all, fetch_dataframe, execute_query, get_next_id

st.set_page_config(page_title="Estádios — Copa do Mundo", page_icon="🏟️", layout="wide")

with open("style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("# 🏟️ Estádios")
st.markdown("Gerenciamento dos estádios da Copa do Mundo")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["📋 Listar", "➕ Adicionar", "✏️ Editar", "🗑️ Deletar"])

# ============================================================
# READ — Listar Estádios
# ============================================================
with tab1:
    try:
        df = fetch_dataframe("SELECT id_estadio, nome_estadio, cidade, pais, capacidade FROM estadios ORDER BY nome_estadio")
        if not df.empty:
            df.columns = ["ID", "Nome do Estádio", "Cidade", "País", "Capacidade"]
            st.dataframe(df, use_container_width=True, hide_index=True)

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total de Estádios", len(df))
            with col2:
                st.metric("Capacidade Média", f"{int(df['Capacidade'].mean()):,}".replace(",", "."))
        else:
            st.info("📭 Nenhum estádio cadastrado ainda.")
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")

# ============================================================
# CREATE — Adicionar Estádio
# ============================================================
with tab2:
    with st.form("form_add_estadio", clear_on_submit=True):
        st.markdown("### ➕ Novo Estádio")
        nome = st.text_input("Nome do Estádio *", placeholder="Ex: Maracanã")
        col1, col2 = st.columns(2)
        with col1:
            cidade = st.text_input("Cidade *", placeholder="Ex: Rio de Janeiro")
        with col2:
            pais = st.text_input("País *", placeholder="Ex: Brasil")
        capacidade = st.number_input("Capacidade *", min_value=1000, max_value=200000, value=50000, step=1000)

        submitted = st.form_submit_button("✅ Adicionar Estádio")
        if submitted:
            if nome and cidade and pais:
                try:
                    next_id = get_next_id("estadios", "id_estadio")
                    execute_query(
                        "INSERT INTO estadios (id_estadio, nome_estadio, cidade, pais, capacidade) VALUES (%s, %s, %s, %s, %s)",
                        (next_id, nome.strip(), cidade.strip(), pais.strip(), capacidade),
                    )
                    st.success(f"✅ Estádio **{nome}** adicionado com sucesso! (ID: {next_id})")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao adicionar: {e}")
            else:
                st.warning("⚠️ Preencha todos os campos obrigatórios.")

# ============================================================
# UPDATE — Editar Estádio
# ============================================================
with tab3:
    try:
        estadios = fetch_all("SELECT * FROM estadios ORDER BY nome_estadio")
        if estadios:
            options = {f"{e['nome_estadio']} — {e['cidade']}, {e['pais']}": e for e in estadios}
            selected = st.selectbox("Selecione o estádio para editar:", list(options.keys()), key="edit_estadio_select")
            estadio = options[selected]

            with st.form("form_edit_estadio"):
                st.markdown(f"### ✏️ Editando: {estadio['nome_estadio']}")
                nome = st.text_input("Nome do Estádio", value=estadio["nome_estadio"])
                col1, col2 = st.columns(2)
                with col1:
                    cidade = st.text_input("Cidade", value=estadio["cidade"])
                with col2:
                    pais = st.text_input("País", value=estadio["pais"])
                capacidade = st.number_input("Capacidade", value=int(estadio["capacidade"]), min_value=1000, max_value=200000, step=1000)

                submitted = st.form_submit_button("💾 Salvar Alterações")
                if submitted:
                    try:
                        execute_query(
                            "UPDATE estadios SET nome_estadio=%s, cidade=%s, pais=%s, capacidade=%s WHERE id_estadio=%s",
                            (nome.strip(), cidade.strip(), pais.strip(), capacidade, estadio["id_estadio"]),
                        )
                        st.success("✅ Estádio atualizado com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro ao atualizar: {e}")
        else:
            st.info("📭 Nenhum estádio cadastrado para editar.")
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")

# ============================================================
# DELETE — Deletar Estádio
# ============================================================
with tab4:
    try:
        estadios = fetch_all("SELECT * FROM estadios ORDER BY nome_estadio")
        if estadios:
            options = {f"{e['nome_estadio']} — {e['cidade']}, {e['pais']}": e for e in estadios}
            selected = st.selectbox("Selecione o estádio para deletar:", list(options.keys()), key="del_estadio_select")
            estadio = options[selected]

            st.warning(f"⚠️ Tem certeza que deseja deletar o estádio **{estadio['nome_estadio']}** ({estadio['cidade']}, {estadio['pais']})?")
            st.caption("Esta ação não pode ser desfeita. Estádios vinculados a partidas não podem ser deletados.")

            if st.button("🗑️ Confirmar Exclusão", key="btn_del_estadio"):
                try:
                    execute_query("DELETE FROM estadios WHERE id_estadio = %s", (estadio["id_estadio"],))
                    st.success("✅ Estádio deletado com sucesso!")
                    st.rerun()
                except Exception as e:
                    if "foreign key" in str(e).lower() or "constraint" in str(e).lower():
                        st.error("❌ Não é possível deletar este estádio pois ele está vinculado a partidas existentes.")
                    else:
                        st.error(f"❌ Erro ao deletar: {e}")
        else:
            st.info("📭 Nenhum estádio cadastrado para deletar.")
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
