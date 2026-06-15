"""
Copa do Mundo — CRUD Seleções
"""

import streamlit as st
from db_connection import fetch_all, fetch_dataframe, execute_query, get_next_id, get_flag_url

st.set_page_config(page_title="Seleções — Copa do Mundo", page_icon="🌍", layout="wide")

with open("style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("# 🌍 Seleções")
st.markdown("Gerenciamento das seleções participantes da Copa do Mundo")
st.markdown("---")

CONTINENTES = [
    "América do Sul",
    "Europa",
    "Ásia",
    "África",
    "Oceania",
    "América do Norte e Central",
]

tab1, tab2, tab3, tab4 = st.tabs(["📋 Listar", "➕ Adicionar", "✏️ Editar", "🗑️ Deletar"])

# ============================================================
# READ — Listar Seleções (com bandeiras)
# ============================================================
with tab1:
    try:
        selecoes = fetch_all("SELECT * FROM selecoes ORDER BY nome_selecao")
        if selecoes:
            # Filtro por continente
            continentes_existentes = sorted(set(s["continente"] for s in selecoes))
            filtro = st.selectbox(
                "Filtrar por continente:",
                ["Todos"] + continentes_existentes,
                key="filtro_continente",
            )

            if filtro != "Todos":
                selecoes_filtradas = [s for s in selecoes if s["continente"] == filtro]
            else:
                selecoes_filtradas = selecoes

            # Cards com bandeiras
            cols = st.columns(4)
            for i, sel in enumerate(selecoes_filtradas):
                flag_url = get_flag_url(sel["nome_selecao"], 80)
                with cols[i % 4]:
                    flag_html = f'<img src="{flag_url}" style="width:56px;height:38px;border-radius:4px;box-shadow:0 2px 8px rgba(0,0,0,0.3);" />' if flag_url else ""
                    st.markdown(
                        f"""<div class="stat-card" style="margin-bottom: 1rem;">
{flag_html}
<div style="font-family:'Montserrat',sans-serif;font-weight:700;font-size:1rem;color:#fff;margin-top:0.5rem;">{sel["nome_selecao"]}</div>
<div style="color:#b0b8d1;font-size:0.8rem;">🌎 {sel["continente"]}</div>
<div style="color:#b0b8d1;font-size:0.8rem;">👔 {sel["tecnico"]}</div>
<div style="color:#d4af37;font-weight:700;font-size:0.9rem;margin-top:0.3rem;">🏆 {sel["titulos"]} título(s)</div>
</div>""",
                        unsafe_allow_html=True,
                    )

            # Tabela detalhada
            with st.expander("📊 Ver tabela completa"):
                df = fetch_dataframe("SELECT id_selecao, nome_selecao, continente, tecnico, titulos FROM selecoes ORDER BY nome_selecao")
                df.columns = ["ID", "Seleção", "Continente", "Técnico", "Títulos"]
                st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("📭 Nenhuma seleção cadastrada ainda.")
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")

# ============================================================
# CREATE — Adicionar Seleção
# ============================================================
with tab2:
    with st.form("form_add_selecao", clear_on_submit=True):
        st.markdown("### ➕ Nova Seleção")
        nome = st.text_input("Nome da Seleção *", placeholder="Ex: Brasil")
        continente = st.selectbox("Continente *", CONTINENTES)
        tecnico = st.text_input("Técnico *", placeholder="Ex: Dorival Júnior")
        titulos = st.number_input("Títulos Mundiais", min_value=0, max_value=10, value=0, step=1)

        submitted = st.form_submit_button("✅ Adicionar Seleção")
        if submitted:
            if nome and tecnico:
                try:
                    next_id = get_next_id("selecoes", "id_selecao")
                    execute_query(
                        "INSERT INTO selecoes (id_selecao, nome_selecao, continente, tecnico, titulos) VALUES (%s, %s, %s, %s, %s)",
                        (next_id, nome.strip(), continente, tecnico.strip(), titulos),
                    )
                    st.success(f"✅ Seleção **{nome}** adicionada com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao adicionar: {e}")
            else:
                st.warning("⚠️ Preencha todos os campos obrigatórios.")

# ============================================================
# UPDATE — Editar Seleção
# ============================================================
with tab3:
    try:
        selecoes = fetch_all("SELECT * FROM selecoes ORDER BY nome_selecao")
        if selecoes:
            options = {f"{s['nome_selecao']} ({s['continente']})": s for s in selecoes}
            selected = st.selectbox("Selecione a seleção para editar:", list(options.keys()), key="edit_selecao_select")
            sel = options[selected]

            with st.form("form_edit_selecao"):
                st.markdown(f"### ✏️ Editando: {sel['nome_selecao']}")
                nome = st.text_input("Nome da Seleção", value=sel["nome_selecao"])
                cont_idx = CONTINENTES.index(sel["continente"]) if sel["continente"] in CONTINENTES else 0
                continente = st.selectbox("Continente", CONTINENTES, index=cont_idx)
                tecnico = st.text_input("Técnico", value=sel["tecnico"])
                titulos = st.number_input("Títulos Mundiais", value=int(sel["titulos"]), min_value=0, max_value=10, step=1)

                submitted = st.form_submit_button("💾 Salvar Alterações")
                if submitted:
                    try:
                        execute_query(
                            "UPDATE selecoes SET nome_selecao=%s, continente=%s, tecnico=%s, titulos=%s WHERE id_selecao=%s",
                            (nome.strip(), continente, tecnico.strip(), titulos, sel["id_selecao"]),
                        )
                        st.success("✅ Seleção atualizada com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro ao atualizar: {e}")
        else:
            st.info("📭 Nenhuma seleção cadastrada para editar.")
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")

# ============================================================
# DELETE — Deletar Seleção
# ============================================================
with tab4:
    try:
        selecoes = fetch_all("SELECT * FROM selecoes ORDER BY nome_selecao")
        if selecoes:
            options = {f"{s['nome_selecao']} ({s['continente']})": s for s in selecoes}
            selected = st.selectbox("Selecione a seleção para deletar:", list(options.keys()), key="del_selecao_select")
            sel = options[selected]

            st.warning(f"⚠️ Tem certeza que deseja deletar a seleção **{sel['nome_selecao']}**?")
            st.caption("Seleções vinculadas a jogadores ou partidas não podem ser deletadas.")

            if st.button("🗑️ Confirmar Exclusão", key="btn_del_selecao"):
                try:
                    execute_query("DELETE FROM selecoes WHERE id_selecao = %s", (sel["id_selecao"],))
                    st.success("✅ Seleção deletada com sucesso!")
                    st.rerun()
                except Exception as e:
                    if "foreign key" in str(e).lower() or "constraint" in str(e).lower():
                        st.error("❌ Não é possível deletar esta seleção pois ela possui jogadores ou partidas vinculadas.")
                    else:
                        st.error(f"❌ Erro ao deletar: {e}")
        else:
            st.info("📭 Nenhuma seleção cadastrada para deletar.")
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
