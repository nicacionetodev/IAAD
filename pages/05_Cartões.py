"""
Copa do Mundo — CRUD Cartões
Com indicação de expulsão via trigger MySQL.
"""

import streamlit as st
from db_connection import fetch_all, execute_query, get_next_id

st.set_page_config(page_title="Cartões — Copa do Mundo", page_icon="🟨", layout="wide")

with open("style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("# 🟨 Cartões")
st.markdown("Gerenciamento de cartões — com detecção automática de expulsão via trigger MySQL")
st.markdown("---")

st.info(
    "💡 **Trigger ativo:** Ao inserir um cartão, o MySQL verifica automaticamente:\n"
    "- 🔴 **Vermelho** → Expulsão direta\n"
    "- 🟡🟡 **Segundo Amarelo** na mesma partida → Expulsão automática\n\n"
    "O campo `expulso` é preenchido automaticamente pelo trigger `trg_verificar_expulsao`."
)

tab1, tab2, tab3, tab4 = st.tabs(["📋 Listar", "➕ Adicionar", "✏️ Editar", "🗑️ Deletar"])


def get_cartoes_completos():
    """Busca cartões com JOINs completos."""
    return fetch_all("""
        SELECT c.`id_cartao`, c.id_partida, c.id_jogador, c.cor_cartao, c.minuto, c.expulso,
               j.nome_jogador, j.numero_camisa,
               s.nome_selecao,
               s1.nome_selecao AS selecao_1_nome,
               s2.nome_selecao AS selecao_2_nome,
               p.data_partida
        FROM `cartoes` c
        LEFT JOIN jogadores j ON c.id_jogador = j.id_jogador
        LEFT JOIN selecoes s ON j.id_selecao = s.id_selecao
        LEFT JOIN partidas p ON c.id_partida = p.id_partida
        LEFT JOIN selecoes s1 ON p.id_selecao_1 = s1.id_selecao
        LEFT JOIN selecoes s2 ON p.id_selecao_2 = s2.id_selecao
        ORDER BY c.id_partida, c.minuto
    """)


def get_partidas_select():
    """Busca partidas formatadas para selectbox."""
    return fetch_all("""
        SELECT p.id_partida, p.data_partida,
               s1.nome_selecao AS sel1, s2.nome_selecao AS sel2
        FROM partidas p
        LEFT JOIN selecoes s1 ON p.id_selecao_1 = s1.id_selecao
        LEFT JOIN selecoes s2 ON p.id_selecao_2 = s2.id_selecao
        ORDER BY p.data_partida DESC
    """)


def get_jogadores_select():
    """Busca jogadores formatados para selectbox."""
    return fetch_all("""
        SELECT j.id_jogador, j.nome_jogador, j.numero_camisa, s.nome_selecao
        FROM jogadores j
        LEFT JOIN selecoes s ON j.id_selecao = s.id_selecao
        ORDER BY j.nome_jogador
    """)


# ============================================================
# READ — Listar Cartões
# ============================================================
with tab1:
    try:
        cartoes = get_cartoes_completos()
        if cartoes:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de Cartões", len(cartoes))
            with col2:
                amarelos = sum(1 for c in cartoes if c["cor_cartao"] == "Amarelo")
                st.metric("🟡 Amarelos", amarelos)
            with col3:
                vermelhos = sum(1 for c in cartoes if c["cor_cartao"] == "Vermelho")
                st.metric("🔴 Vermelhos", vermelhos)

            st.markdown("---")

            for cartao in cartoes:
                card_class = "card-yellow" if cartao["cor_cartao"] == "Amarelo" else "card-red"
                data_str = cartao["data_partida"].strftime("%d/%m/%Y") if hasattr(cartao["data_partida"], "strftime") else str(cartao["data_partida"])
                partida_str = f"{cartao.get('selecao_1_nome', 'N/A')} vs {cartao.get('selecao_2_nome', 'N/A')}"
                expelled_html = '<span class="expelled-badge">EXPULSO</span>' if cartao["expulso"] else ""

                st.markdown(
                    f"""<div class="player-card">
<div style="min-width: 40px; text-align: center;">
<span class="{card_class}"></span>
</div>
<div class="player-info" style="flex: 1;">
<div class="player-name">
{cartao["nome_jogador"]} <span style="color:#6b7394;font-weight:400;font-size:0.85rem;">(#{cartao.get("numero_camisa", "")})</span>
{expelled_html}
</div>
<div class="player-detail">
🌍 {cartao.get("nome_selecao", "N/A")} &nbsp;|&nbsp;
⚽ {partida_str} &nbsp;|&nbsp;
⏱️ {cartao["minuto"]}' &nbsp;|&nbsp;
📅 {data_str}
</div>
</div>
</div>""",
                    unsafe_allow_html=True,
                )
        else:
            st.info("📭 Nenhum cartão registrado ainda.")
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")

# ============================================================
# CREATE — Adicionar Cartão (trigger define expulso!)
# ============================================================
with tab2:
    try:
        partidas_sel = get_partidas_select()
        jogadores_sel = get_jogadores_select()

        if partidas_sel and jogadores_sel:
            with st.form("form_add_cartao", clear_on_submit=True):
                st.markdown("### ➕ Novo Cartão")
                st.caption("O campo **expulso** será definido automaticamente pelo trigger MySQL.")

                part_options = {}
                for p in partidas_sel:
                    data_str = p["data_partida"].strftime("%d/%m/%Y") if hasattr(p["data_partida"], "strftime") else str(p["data_partida"])
                    label = f"{p['sel1']} vs {p['sel2']} — {data_str}"
                    part_options[label] = p["id_partida"]
                partida_nome = st.selectbox("Partida *", list(part_options.keys()))

                jog_options = {f"{j['nome_jogador']} — {j['nome_selecao']} (#{j['numero_camisa']})": j["id_jogador"] for j in jogadores_sel}
                jogador_nome = st.selectbox("Jogador *", list(jog_options.keys()))

                col1, col2 = st.columns(2)
                with col1:
                    cor = st.selectbox("Cor do Cartão *", ["Amarelo", "Vermelho"])
                with col2:
                    minuto = st.number_input("Minuto *", min_value=1, max_value=120, value=45, step=1)

                submitted = st.form_submit_button("✅ Adicionar Cartão")
                if submitted:
                    try:
                        next_id = get_next_id("cartoes", "id_cartao")
                        execute_query(
                            "INSERT INTO `cartoes` (`id_cartao`, id_partida, id_jogador, cor_cartao, minuto) VALUES (%s, %s, %s, %s, %s)",
                            (next_id, part_options[partida_nome], jog_options[jogador_nome], cor, minuto),
                        )
                        # Verificar se foi expulso (definido pelo trigger)
                        result = fetch_all(
                            "SELECT expulso FROM `cartoes` WHERE `id_cartao` = %s", (next_id,)
                        )
                        if result and result[0]["expulso"]:
                            st.error(f"🔴 EXPULSO! O jogador foi expulso {'(cartão vermelho direto)' if cor == 'Vermelho' else '(segundo cartão amarelo)'}!")
                        else:
                            st.success(f"✅ Cartão {cor} registrado com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro ao adicionar: {e}")
        else:
            st.warning("⚠️ Cadastre partidas e jogadores antes de adicionar cartões.")
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")

# ============================================================
# UPDATE — Editar Cartão
# ============================================================
with tab3:
    try:
        cartoes = get_cartoes_completos()
        if cartoes:
            options = {}
            for c in cartoes:
                data_str = c["data_partida"].strftime("%d/%m/%Y") if hasattr(c["data_partida"], "strftime") else str(c["data_partida"])
                partida_str = f"{c.get('selecao_1_nome', '')} vs {c.get('selecao_2_nome', '')}"
                label = f"{c['cor_cartao']} — {c['nome_jogador']} ({partida_str}, {c['minuto']}')"
                options[label] = c

            selected = st.selectbox("Selecione o cartão para editar:", list(options.keys()), key="edit_cartao_select")
            cartao = options[selected]

            with st.form("form_edit_cartao"):
                st.markdown(f"### ✏️ Editando cartão de: {cartao['nome_jogador']}")
                st.caption("Após edição, o campo **expulso** será recalculado manualmente (trigger só funciona no INSERT).")

                col1, col2 = st.columns(2)
                with col1:
                    cor_idx = 0 if cartao["cor_cartao"] == "Amarelo" else 1
                    cor = st.selectbox("Cor do Cartão", ["Amarelo", "Vermelho"], index=cor_idx)
                with col2:
                    minuto = st.number_input("Minuto", value=int(cartao["minuto"]), min_value=1, max_value=120, step=1)

                submitted = st.form_submit_button("💾 Salvar Alterações")
                if submitted:
                    try:
                        # Atualizar cartão
                        execute_query(
                            "UPDATE `cartoes` SET cor_cartao = %s, minuto = %s WHERE `id_cartao` = %s",
                            (cor, minuto, cartao["id_cartao"]),
                        )

                        # Recalcular expulso manualmente
                        expulso = 0
                        if cor == "Vermelho":
                            expulso = 1
                        elif cor == "Amarelo":
                            # Contar amarelos do mesmo jogador na mesma partida (excluindo este)
                            count = fetch_all(
                                """SELECT COUNT(*) AS cnt FROM `cartoes`
                                   WHERE id_jogador = %s AND id_partida = %s
                                   AND cor_cartao = 'Amarelo' AND `id_cartao` != %s""",
                                (cartao["id_jogador"], cartao["id_partida"], cartao["id_cartao"]),
                            )
                            if count and count[0]["cnt"] >= 1:
                                expulso = 1

                        execute_query(
                            "UPDATE `cartoes` SET expulso = %s WHERE `id_cartao` = %s",
                            (expulso, cartao["id_cartao"]),
                        )

                        st.success("✅ Cartão atualizado com sucesso!")
                        if expulso:
                            st.warning("🔴 Jogador marcado como EXPULSO.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro ao atualizar: {e}")
        else:
            st.info("📭 Nenhum cartão cadastrado para editar.")
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")

# ============================================================
# DELETE — Deletar Cartão
# ============================================================
with tab4:
    try:
        cartoes = get_cartoes_completos()
        if cartoes:
            options = {}
            for c in cartoes:
                data_str = c["data_partida"].strftime("%d/%m/%Y") if hasattr(c["data_partida"], "strftime") else str(c["data_partida"])
                partida_str = f"{c.get('selecao_1_nome', '')} vs {c.get('selecao_2_nome', '')}"
                expelled_str = " [EXPULSO]" if c["expulso"] else ""
                label = f"{c['cor_cartao']} — {c['nome_jogador']} ({partida_str}, {c['minuto']}'){expelled_str}"
                options[label] = c

            selected = st.selectbox("Selecione o cartão para deletar:", list(options.keys()), key="del_cartao_select")
            cartao = options[selected]

            st.warning(f"⚠️ Tem certeza que deseja deletar o cartão **{cartao['cor_cartao']}** de **{cartao['nome_jogador']}**?")

            if st.button("🗑️ Confirmar Exclusão", key="btn_del_cartao"):
                try:
                    execute_query("DELETE FROM `cartoes` WHERE `id_cartao` = %s", (cartao["id_cartao"],))
                    st.success("✅ Cartão deletado com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao deletar: {e}")
        else:
            st.info("📭 Nenhum cartão cadastrado para deletar.")
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
