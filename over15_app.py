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
