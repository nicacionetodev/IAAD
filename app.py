"""
Copa do Mundo — Sistema CRUD
Página principal com visão geral e partidas recentes.
"""

import streamlit as st

st.set_page_config(
    page_title="Copa do Mundo — Sistema CRUD",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded",
)

with open("style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


with st.sidebar:
    
    with st.expander(" Conexão MySQL"):
        from db_connection import DB_CONFIG, save_db_config, test_connection
        host_sb = st.text_input("Host", value=DB_CONFIG.get("host", "localhost"), key="sb_host")
        port_sb = st.number_input("Porta", value=int(DB_CONFIG.get("port", 3306)), step=1, key="sb_port")
        user_sb = st.text_input("Usuário", value=DB_CONFIG.get("user", "root"), key="sb_user")
        pwd_sb = st.text_input("Senha", value=DB_CONFIG.get("password", ""), type="password", key="sb_pwd")
        
        if st.button(" Salvar & Recarregar", key="btn_save_config_sidebar", use_container_width=True):
            try:
                # Testar se credenciais funcionam
                test_connection(host_sb, port_sb, user_sb, pwd_sb)
                save_db_config(host_sb, port_sb, user_sb, pwd_sb, DB_CONFIG.get("database", "Copa_do_Mundo"))
                st.success("Configurações salvas!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro de conexão: {e}")

        st.markdown("---")
        if st.button(" Recriar Banco de Dados", key="btn_reset_db_sidebar", use_container_width=True, type="secondary"):
            try:
                from db_connection import init_database
                with st.spinner("Apagando e recriando banco de dados..."):
                    init_database(host_sb, port_sb, user_sb, pwd_sb)
                    save_db_config(host_sb, port_sb, user_sb, pwd_sb, "Copa_do_Mundo")
                st.success("Banco de dados reinicializado e populado!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao recriar: {e}")
                




st.markdown(
    """
<div class="hero-section">
    <div class="hero-title">🏆 Copa do Mundo 2026</div>
    <div class="hero-divider"></div>
    <div class="hero-subtitle">Sistema de Gerenciamento — FIFA World Cup</div>
    <div class="hero-subtitle" style="font-size: 0.9rem; margin-top: 0.3rem; color: #6b7394;">
        USA • México • Canadá
    </div>
</div>
""",
    unsafe_allow_html=True,
)


try:
    from db_connection import fetch_all, get_flag_url

    st.markdown("### Visão Geral")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        total = fetch_all("SELECT COUNT(*) as total FROM selecoes")
        st.metric("🌍 Seleções", total[0]["total"])
    with col2:
        total = fetch_all("SELECT COUNT(*) as total FROM jogadores")
        st.metric("⚽ Jogadores", total[0]["total"])
    with col3:
        total = fetch_all("SELECT COUNT(*) as total FROM estadios")
        st.metric("🏟️ Estádios", total[0]["total"])
    with col4:
        total = fetch_all("SELECT COUNT(*) as total FROM partidas")
        st.metric("🏆 Partidas", total[0]["total"])
    with col5:
        total = fetch_all("SELECT COUNT(*) as total FROM `cartoes`")
        st.metric("🟨 Cartões", total[0]["total"])

    st.markdown("---")

    st.markdown("### 🏟️ Partidas Recentes")

    partidas = fetch_all(
        """
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
        ORDER BY p.data_partida DESC
        LIMIT 6
    """
    )

    if partidas:
        for partida in partidas:
            flag1 = get_flag_url(partida["selecao_1_nome"], 80)
            flag2 = get_flag_url(partida["selecao_2_nome"], 80)

            # Formatar data
            data = partida["data_partida"]
            if hasattr(data, "strftime"):
                data_str = data.strftime("%d/%m/%Y")
            else:
                data_str = str(data)

            # Resultado
            if partida["vencedor"] is None:
                resultado = "Empate"
            else:
                resultado = f"Vencedor: {partida.get('vencedor_nome', '')}"

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
    else:
        st.info("Nenhuma partida registrada ainda.")

   
    st.markdown("---")
    st.markdown("### 🏅 Ranking de Títulos")

    selecoes = fetch_all(
        """
        SELECT nome_selecao, titulos, continente
        FROM selecoes
        WHERE titulos > 0
        ORDER BY titulos DESC
    """
    )

    if selecoes:
        cols = st.columns(len(selecoes))
        for i, sel in enumerate(selecoes):
            flag_url = get_flag_url(sel["nome_selecao"], 80)
            with cols[i]:
                st.markdown(
                    f"""
                <div class="stat-card">
                    <img src="{flag_url}" style="width: 56px; height: 38px; border-radius: 4px; margin-bottom: 0.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.3);" />
                    <div class="stat-value">{sel["titulos"]}</div>
                    <div class="stat-label">{sel["nome_selecao"]}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

except Exception as e:
    st.markdown("---")
    st.error(
        "⚠️ **Não foi possível conectar ao banco de dados MySQL.**\n\n"
        "Por favor, verifique se o serviço do MySQL está rodando e configure os dados de conexão abaixo."
    )
    
    from db_connection import DB_CONFIG, save_db_config, test_connection, init_database
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("### ⚙️ Configurações de Acesso")
        host_input = st.text_input("MySQL Host", value=DB_CONFIG.get("host", "localhost"), key="setup_host")
        port_input = st.number_input("MySQL Porta", value=int(DB_CONFIG.get("port", 3306)), step=1, key="setup_port")
        user_input = st.text_input("MySQL Usuário", value=DB_CONFIG.get("user", "root"), key="setup_user")
        pwd_input = st.text_input("MySQL Senha", value=DB_CONFIG.get("password", ""), type="password", key="setup_pwd")
        
        btn_connect = st.button(" Testar e Salvar Conexão", use_container_width=True)
        if btn_connect:
            try:

                test_connection(host_input, port_input, user_input, pwd_input)
                save_db_config(host_input, port_input, user_input, pwd_input, "Copa_do_Mundo")
                st.success(" Conectado ao MySQL com sucesso! Salvando configurações...")
                st.rerun()
            except Exception as conn_err:
                st.error(f" Falha de conexão: {conn_err}")
                
    with col_c2:
        st.markdown("###  Inicialização Automática do Banco")
        st.markdown(
            "Se você ainda não criou o banco de dados `Copa_do_Mundo` ou as tabelas, clique no botão abaixo para "
            "criar o schema, triggers e carregar os dados de exemplo automaticamente."
        )
        btn_init = st.button(" Inicializar Banco de Dados (Copa_do_Mundo)", use_container_width=True, type="primary")
        if btn_init:
            try:
                with st.spinner("Criando banco de dados, tabelas, triggers e carregando dados iniciais..."):
                    init_database(host_input, port_input, user_input, pwd_input)
                    save_db_config(host_input, port_input, user_input, pwd_input, "Copa_do_Mundo")
                st.success(" Banco de dados inicializado com sucesso!")
                st.rerun()
            except Exception as init_err:
                st.error(f"❌ Erro ao inicializar banco: {init_err}")
                
    st.markdown("---")
    with st.expander(" Detalhes técnicos do erro atual"):
        st.code(str(e))


st.markdown("---")

