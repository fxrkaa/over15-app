import streamlit as st

def calcular_media_gols(jogos):
    return sum(g1 + g2 for g1, g2 in jogos) / len(jogos) if jogos else 0

def estimar_chance_over_15(media):
    if media < 1:
        return 0.25
    elif media < 2:
        return 0.55
    elif media < 3:
        return 0.75
    else:
        return 0.90

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

st.title("Analisador de Over 1.5 Gols")

time1 = st.text_input("Nome do Time 1", value="Alemanha")
jogos1 = entrada_de_jogos(time1)

time2 = st.text_input("Nome do Time 2", value="Eslovênia")
jogos2 = entrada_de_jogos(time2)

if st.button("Analisar"):
    media1 = calcular_media_gols(jogos1)
    media2 = calcular_media_gols(jogos2)
    media_total = (media1 + media2) / 2
    chance = estimar_chance_over_15(media_total)

    st.markdown("### Resultado")
    st.write(f"{time1} - Média de gols: {media1:.2f}")
    st.write(f"{time2} - Média de gols: {media2:.2f}")
    st.write(f"Média combinada: {media_total:.2f}")
    st.success(f"Chance estimada de Over 1.5 gols: **{chance*100:.2f}%**")
import streamlit as st
import re

st.title("Analisador de Over 1.5 Gols com Texto")

st.write("Cole os resultados recentes em formato simples, como por exemplo:")
st.code("""
Germany 3-3 France
Scotland 2-0 Denmark
Albania 0-1 Georgia
Croatia 1-1 Italy
""", language="text")

entrada = st.text_area("Cole aqui os resultados dos últimos jogos", height=200)

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

def estimar_chance_over_15(media):
    if media < 1:
        return 0.25
    elif media < 2:
        return 0.55
    elif media < 3:
        return 0.75
    else:
        return 0.90

jogos = parse_jogos(entrada)

if jogos:
    st.success(f"{len(jogos)} jogos reconhecidos.")
    time1 = st.text_input("Nome do Time 1 (exato como aparece)", value=jogos[-1][0])
    time2 = st.text_input("Nome do Time 2 (exato como aparece)", value=jogos[-1][3])

    if st.button("Analisar Probabilidade"):
        num_jogos, media = calcular_estatisticas(jogos, time1, time2)
        chance = estimar_chance_over_15(media)
        st.markdown("### Resultado")
        st.write(f"Número de jogos analisados: {num_jogos}")
        st.write(f"Média de gols por jogo envolvendo {time1} ou {time2}: {media:.2f}")
        st.success(f"Chance estimada de Over 1.5 gols: **{chance*100:.2f}%**")

