import streamlit as st
import re
from collections import defaultdict

st.set_page_config(page_title="Analisador Over 1.5", layout="centered")
st.title("⚽ Analisador de Probabilidades para Over 1.5 Gols")

tabs = st.tabs(["🔢 Entrada Manual", "📋 Texto Livre", "📊 Análise Completa"])

# Funções comuns
def estimar_chance_over_15(media):
    if media < 1:
        return 0.25
    elif media < 2:
        return 0.55
    elif media < 3:
        return 0.75
    else:
        return 0.90

# Tab 1 - Entrada Manual
with tabs[0]:
    def entrada_de_jogos(nome_time):
        st.subheader(f"Jogos de {nome_time}")
        num_jogos = st.number_input(f"Número de jogos recentes para {nome_time}", min_value=1, max_value=10, value=3)
        jogos = []
        for i in range(num_jogos):
            col1, col2 = st.columns(2)
            with col1:
                g1 = st.number_input(f"Gols do {nome_time} no jogo {i+1}", min_value=0, key=f"{nome_time}_g1_{i}")
            with col2:
                g2 = st.number_input(f"Gols do adversário no jogo {i+1}", min_value=0, key=f"{nome_time}_g2_{i}")
            jogos.append((g1, g2))
        return jogos

    time1 = st.text_input("Nome do Time 1", value="Alemanha")
    jogos1 = entrada_de_jogos(time1)

    time2 = st.text_input("Nome do Time 2", value="Eslovênia")
    jogos2 = entrada_de_jogos(time2)

    if st.button("Analisar", key="manual_analysis"):
        media1 = sum(g1 + g2 for g1, g2 in jogos1) / len(jogos1)
        media2 = sum(g1 + g2 for g1, g2 in jogos2) / len(jogos2)
        media_total = (media1 + media2) / 2
        chance = estimar_chance_over_15(media_total)

        st.markdown("### Resultado")
        st.write(f"{time1} - Média de gols: {media1:.2f}")
        st.write(f"{time2} - Média de gols: {media2:.2f}")
        st.write(f"Média combinada: {media_total:.2f}")
        st.success(f"Chance estimada de Over 1.5 gols: **{chance*100:.2f}%**")

# Tab 2 - Texto Livre
with tabs[1]:
    st.markdown("Cole os resultados recentes em formato simples:")
    st.code("Germany 3-3 France\nScotland 2-0 Denmark", language="text")
    entrada = st.text_area("Resultados dos jogos", height=200, key="text_input")

    def parse_jogos(texto):
        padrao = re.compile(r"([A-Za-z]+)\s(\d+)[-–](\d+)\s([A-Za-z]+)")
        jogos = []
        for linha in texto.strip().split("\n"):
            m = padrao.search(linha)
            if m:
                time1, g1, g2, time2 = m.groups()
                jogos.append((time1.strip(), int(g1), int(g2), time2.strip()))
        return jogos

    def calcular_estatisticas(jogos, time1, time2):
        total_gols = []
        for j in jogos:
            if j[0] in [time1, time2] or j[3] in [time1, time2]:
                total_gols.append(j[1] + j[2])
        if not total_gols:
            return 0, 0.0
        media = sum(total_gols) / len(total_gols)
        return len(total_gols), media

    jogos = parse_jogos(entrada)

    if jogos:
        st.success(f"{len(jogos)} jogos reconhecidos.")
        time1 = st.text_input("Time 1", value=jogos[-1][0], key="text_time1")
        time2 = st.text_input("Time 2", value=jogos[-1][3], key="text_time2")

        if st.button("Analisar Probabilidade", key="text_analysis"):
            num_jogos, media = calcular_estatisticas(jogos, time1, time2)
            chance = estimar_chance_over_15(media)
            st.markdown("### Resultado")
            st.write(f"Número de jogos analisados: {num_jogos}")
            st.write(f"Média de gols: {media:.2f}")
            st.success(f"Chance estimada de Over 1.5 gols: **{chance*100:.2f}%**")

# Tab 3 - Análise Completa
with tabs[2]:
    st.markdown("Cole os resultados recentes no formato:")
    st.code("Germany 3-3 France\nScotland 2-0 Denmark", language="text")
    entrada = st.text_area("Resultados dos últimos jogos", height=200, key="full_text")

    def stats_por_time(jogos):
        stats = defaultdict(lambda: {'jogos': 0, 'gols_marcados': 0, 'gols_sofridos': 0, 'vitorias': 0, 'empates': 0, 'derrotas': 0})
        for t1, g1, g2, t2 in jogos:
            stats[t1]['jogos'] += 1
            stats[t2]['jogos'] += 1
            stats[t1]['gols_marcados'] += g1
            stats[t1]['gols_sofridos'] += g2
            stats[t2]['gols_marcados'] += g2
            stats[t2]['gols_sofridos'] += g1
            if g1 > g2:
                stats[t1]['vitorias'] += 1
                stats[t2]['derrotas'] += 1
            elif g2 > g1:
                stats[t2]['vitorias'] += 1
                stats[t1]['derrotas'] += 1
            else:
                stats[t1]['empates'] += 1
                stats[t2]['empates'] += 1
        return stats

    def probabilidade(valor, total):
        return valor / total if total else 0

    def estimar_mercados(time1, time2, stats):
        media_total = (stats[time1]['gols_marcados'] + stats[time1]['gols_sofridos'] +
                       stats[time2]['gols_marcados'] + stats[time2]['gols_sofridos']) /                       (stats[time1]['jogos'] + stats[time2]['jogos'])

        over15 = 0.55 + min(0.35, (media_total - 2.0) * 0.2)
        btts = 0.4 + min(0.4, abs(stats[time1]['gols_marcados'] - stats[time1]['gols_sofridos']) * 0.05)
        chance_vitoria1 = probabilidade(stats[time1]['vitorias'], stats[time1]['jogos'])
        chance_vitoria2 = probabilidade(stats[time2]['vitorias'], stats[time2]['jogos'])
        chance_empate = (probabilidade(stats[time1]['empates'], stats[time1]['jogos']) +
                         probabilidade(stats[time2]['empates'], stats[time2]['jogos'])) / 2

        return {
            'Over 1.5 gols': over15,
            'Ambas Marcam (BTTS)': btts,
            f"{time1} vence": chance_vitoria1,
            f"{time2} vence": chance_vitoria2,
            "Empate": chance_empate
        }, media_total

    jogos = parse_jogos(entrada)

    if jogos:
        st.success(f"{len(jogos)} jogos reconhecidos.")
        time1 = st.text_input("Time 1", value=jogos[-1][0], key="full_time1")
        time2 = st.text_input("Time 2", value=jogos[-1][3], key="full_time2")

        if st.button("Analisar Confronto", key="full_analysis"):
            stats = stats_por_time(jogos)
            mercados, media = estimar_mercados(time1, time2, stats)

            st.markdown("### 📊 Estatísticas do confronto")
            st.write(f"Média de gols combinados por jogo: **{media:.2f}**")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**{time1}**")
                st.json(stats[time1])
            with col2:
                st.markdown(f"**{time2}**")
                st.json(stats[time2])

            st.markdown("### 🎯 Probabilidades Estimadas:")
            for mercado, prob in mercados.items():
                st.write(f"- **{mercado}**: {prob*100:.1f}%")
