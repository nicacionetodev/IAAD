"""
Copa do Mundo — CRUD Partidas
Exibição de placares estilo Copa com bandeiras dos países.
"""

import streamlit as st
import datetime
from db_connection import fetch_all, fetch_dataframe, execute_query, get_next_id, get_flag_url

st.set_page_config(page_title="Partidas — Copa do Mundo", page_icon="🏆", layout="wide")

with open("style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("# 🏆 Partidas")
st.markdown("Gerenciamento das partidas — com placar e bandeiras estilo Copa do Mundo")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["📋 Listar", "➕ Adicionar", "✏️ Editar", "🗑️ Deletar"])


def get_partidas_completas():
    """Busca partidas com JOINs completos."""
    return fetch_all("""
        SELECT p.*,
               s1.nome_selecao AS selecao_1_nome,
               s2.nome_selecao AS selecao_2_nome,
               sv.nome_selecao AS vencedor_nome,
               e.nome_estadio,
               e.cidade
        FROM partidas p
        LEFT JOIN selecoes s1 ON p.id_selecao_1 = s1.id_selecao
        LEFT JOIN selecoes s2 ON p.id_selecao_2 = s2.id_selecao
        LEFT JOIN selecoes sv ON p.vencedor = sv.id_selecao
        LEFT JOIN estadios e ON p.id_estadio = e.id_estadio
        ORDER BY p.data_partida DESC, p.id_partida DESC
    """)


# ============================================================
# READ — Listar Partidas (estilo Copa com bandeiras)
# ============================================================
with tab1:
    try:
        partidas = get_partidas_completas()
        if partidas:
            st.metric("Total de Partidas", len(partidas))
            st.markdown("")

            for partida in partidas:
                flag1 = get_flag_url(partida["selecao_1_nome"], 80)
                flag2 = get_flag_url(partida["selecao_2_nome"], 80)

                data = partida["data_partida"]
                data_str = data.strftime("%d/%m/%Y") if hasattr(data, "strftime") else str(data)

                resultado = "⚖️ Empate" if partida["vencedor"] is None else f"🏆 {partida.get('vencedor_nome', '')}"

                flag1_img = f'<img src="{flag1}" alt="{partida["selecao_1_nome"]}">' if flag1 else ""
                flag2_img = f'<img src="{flag2}" alt="{partida["selecao_2_nome"]}">' if flag2 else ""

                st.markdown(
                    f"""<div class="match-card">
<div class="team">
{flag1_img}
<span class="team-name">{partida["selecao_1_nome"]}</span>
</div>
<div style="text-align: center;">
<div class="score">{partida["quantidade_gols_selecao_1"]} × {partida["quantidade_gols_selecao_2"]}</div>
<div class="match-info">📍 {partida.get("nome_estadio", "N/A")} — {partida.get("cidade", "N/A")}</div>
<div class="match-info">📅 {data_str} &nbsp;|&nbsp; {resultado}</div>
</div>
<div class="team">
{flag2_img}
<span class="team-name">{partida["selecao_2_nome"]}</span>
</div>
</div>""",
                    unsafe_allow_html=True,
                )

            # Tabela
            with st.expander("📊 Ver tabela completa"):
                df = fetch_dataframe("""
                    SELECT p.id_partida, p.data_partida,
                           s1.nome_selecao AS 'Seleção 1',
                           p.quantidade_gols_selecao_1 AS 'Gols 1',
                           p.quantidade_gols_selecao_2 AS 'Gols 2',
                           s2.nome_selecao AS 'Seleção 2',
                           IFNULL(sv.nome_selecao, 'Empate') AS 'Resultado',
                           e.nome_estadio AS 'Estádio'
                    FROM partidas p
                    LEFT JOIN selecoes s1 ON p.id_selecao_1 = s1.id_selecao
                    LEFT JOIN selecoes s2 ON p.id_selecao_2 = s2.id_selecao
                    LEFT JOIN selecoes sv ON p.vencedor = sv.id_selecao
                    LEFT JOIN estadios e ON p.id_estadio = e.id_estadio
                    ORDER BY p.data_partida DESC
                """)
                st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("📭 Nenhuma partida cadastrada ainda.")
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")

# ============================================================
# CREATE — Adicionar Partida
# ============================================================
with tab2:
    try:
        selecoes = fetch_all("SELECT id_selecao, nome_selecao FROM selecoes ORDER BY nome_selecao")
        estadios = fetch_all("SELECT id_estadio, nome_estadio, cidade FROM estadios ORDER BY nome_estadio")

        if selecoes and estadios:
            with st.form("form_add_partida", clear_on_submit=True):
                st.markdown("### ➕ Nova Partida")

                data_partida = st.date_input("Data da Partida *", value=datetime.date.today())

                est_options = {f"{e['nome_estadio']} — {e['cidade']}": e["id_estadio"] for e in estadios}
                estadio_nome = st.selectbox("Estádio *", list(est_options.keys()))

                col1, col2 = st.columns(2)
                sel_options = {s["nome_selecao"]: s["id_selecao"] for s in selecoes}
                sel_names = list(sel_options.keys())
                with col1:
                    selecao_1 = st.selectbox("Seleção 1 *", sel_names, key="add_sel1")
                with col2:
                    selecao_2 = st.selectbox("Seleção 2 *", sel_names, index=min(1, len(sel_names) - 1), key="add_sel2")

                col3, col4 = st.columns(2)
                with col3:
                    gols_1 = st.number_input("Gols Seleção 1", min_value=0, max_value=20, value=0, step=1)
                with col4:
                    gols_2 = st.number_input("Gols Seleção 2", min_value=0, max_value=20, value=0, step=1)

                vencedor_options = ["Empate"] + sel_names
                vencedor_nome = st.selectbox("Vencedor", vencedor_options)

                submitted = st.form_submit_button("✅ Adicionar Partida")
                if submitted:
                    if selecao_1 == selecao_2:
                        st.error("❌ As seleções devem ser diferentes!")
                    else:
                        try:
                            next_id = get_next_id("partidas", "id_partida")
                            vencedor_id = None if vencedor_nome == "Empate" else sel_options.get(vencedor_nome)
                            execute_query(
                                """INSERT INTO partidas
                                   (id_partida, data_partida, id_estadio, id_selecao_1, id_selecao_2,
                                    quantidade_gols_selecao_1, quantidade_gols_selecao_2, vencedor)
                                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                                (next_id, data_partida, est_options[estadio_nome],
                                 sel_options[selecao_1], sel_options[selecao_2],
                                 gols_1, gols_2, vencedor_id),
                            )
                            st.success(f"✅ Partida **{selecao_1} vs {selecao_2}** adicionada com sucesso!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Erro ao adicionar: {e}")
        else:
            st.warning("⚠️ Cadastre seleções e estádios antes de adicionar partidas.")
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")

# ============================================================
# UPDATE — Editar Partida
# ============================================================
with tab3:
    try:
        partidas = get_partidas_completas()
        selecoes = fetch_all("SELECT id_selecao, nome_selecao FROM selecoes ORDER BY nome_selecao")
        estadios = fetch_all("SELECT id_estadio, nome_estadio, cidade FROM estadios ORDER BY nome_estadio")

        if partidas and selecoes and estadios:
            options = {}
            for p in partidas:
                data_str = p["data_partida"].strftime("%d/%m/%Y") if hasattr(p["data_partida"], "strftime") else str(p["data_partida"])
                label = f"{p['selecao_1_nome']} vs {p['selecao_2_nome']} — {data_str}"
                options[label] = p

            selected = st.selectbox("Selecione a partida para editar:", list(options.keys()), key="edit_partida_select")
            partida = options[selected]

            with st.form("form_edit_partida"):
                st.markdown(f"### ✏️ Editando: {partida['selecao_1_nome']} vs {partida['selecao_2_nome']}")

                data_val = partida["data_partida"]
                if not isinstance(data_val, datetime.date):
                    data_val = datetime.date.today()
                data_partida = st.date_input("Data da Partida", value=data_val)

                est_options = {f"{e['nome_estadio']} — {e['cidade']}": e["id_estadio"] for e in estadios}
                est_names = list(est_options.keys())
                current_est = next((k for k, v in est_options.items() if v == partida["id_estadio"]), est_names[0])
                est_idx = est_names.index(current_est) if current_est in est_names else 0
                estadio_nome = st.selectbox("Estádio", est_names, index=est_idx)

                sel_options = {s["nome_selecao"]: s["id_selecao"] for s in selecoes}
                sel_names = list(sel_options.keys())

                col1, col2 = st.columns(2)
                with col1:
                    s1_idx = sel_names.index(partida["selecao_1_nome"]) if partida["selecao_1_nome"] in sel_names else 0
                    selecao_1 = st.selectbox("Seleção 1", sel_names, index=s1_idx, key="edit_sel1")
                with col2:
                    s2_idx = sel_names.index(partida["selecao_2_nome"]) if partida["selecao_2_nome"] in sel_names else 0
                    selecao_2 = st.selectbox("Seleção 2", sel_names, index=s2_idx, key="edit_sel2")

                col3, col4 = st.columns(2)
                with col3:
                    gols_1 = st.number_input("Gols Seleção 1", value=int(partida["quantidade_gols_selecao_1"]), min_value=0, step=1)
                with col4:
                    gols_2 = st.number_input("Gols Seleção 2", value=int(partida["quantidade_gols_selecao_2"]), min_value=0, step=1)

                vencedor_options = ["Empate"] + sel_names
                current_venc = partida.get("vencedor_nome", "Empate") or "Empate"
                v_idx = vencedor_options.index(current_venc) if current_venc in vencedor_options else 0
                vencedor_nome = st.selectbox("Vencedor", vencedor_options, index=v_idx)

                submitted = st.form_submit_button("💾 Salvar Alterações")
                if submitted:
                    try:
                        vencedor_id = None if vencedor_nome == "Empate" else sel_options.get(vencedor_nome)
                        execute_query(
                            """UPDATE partidas SET data_partida=%s, id_estadio=%s,
                               id_selecao_1=%s, id_selecao_2=%s,
                               quantidade_gols_selecao_1=%s, quantidade_gols_selecao_2=%s,
                               vencedor=%s WHERE id_partida=%s""",
                            (data_partida, est_options[estadio_nome],
                             sel_options[selecao_1], sel_options[selecao_2],
                             gols_1, gols_2, vencedor_id, partida["id_partida"]),
                        )
                        st.success("✅ Partida atualizada com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro ao atualizar: {e}")
        else:
            st.info("📭 Nenhuma partida cadastrada para editar.")
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")

# ============================================================
# DELETE — Deletar Partida
# ============================================================
with tab4:
    try:
        partidas = get_partidas_completas()
        if partidas:
            options = {}
            for p in partidas:
                data_str = p["data_partida"].strftime("%d/%m/%Y") if hasattr(p["data_partida"], "strftime") else str(p["data_partida"])
                label = f"{p['selecao_1_nome']} {p['quantidade_gols_selecao_1']}×{p['quantidade_gols_selecao_2']} {p['selecao_2_nome']} — {data_str}"
                options[label] = p

            selected = st.selectbox("Selecione a partida para deletar:", list(options.keys()), key="del_partida_select")
            partida = options[selected]

            st.warning(f"⚠️ Tem certeza que deseja deletar esta partida?")
            st.caption("Partidas com cartões vinculados não podem ser deletadas.")

            if st.button("🗑️ Confirmar Exclusão", key="btn_del_partida"):
                try:
                    execute_query("DELETE FROM partidas WHERE id_partida = %s", (partida["id_partida"],))
                    st.success("✅ Partida deletada com sucesso!")
                    st.rerun()
                except Exception as e:
                    if "foreign key" in str(e).lower() or "constraint" in str(e).lower():
                        st.error("❌ Não é possível deletar esta partida pois ela possui cartões vinculados.")
                    else:
                        st.error(f"❌ Erro ao deletar: {e}")
        else:
            st.info("📭 Nenhuma partida cadastrada para deletar.")
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
