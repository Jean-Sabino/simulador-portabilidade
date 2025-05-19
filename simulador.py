import streamlit as st
from datetime import datetime, date
import math
import locale

# Define o locale para formato monetário brasileiro
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

st.set_page_config(page_title="Simulador de Portabilidade de Crédito", layout="centered")

# Exibe a logo diretamente do GitHub
st.image("https://github.com/Jean-Sabino/simulador-portabilidade/blob/main/logo_sicoob.png?raw=true", width=200)

st.markdown("<h1 style='text-align: center;'>📊 Simulador de Portabilidade de Crédito</h1>", unsafe_allow_html=True)
st.markdown("---")

# Entradas do usuário
st.header("🔢 Informações do Empréstimo")
saldo_devedor = st.number_input("Saldo Devedor Atual (R$):", min_value=0.0, step=100.0)
taxa_juros = st.number_input("Nova Taxa de Juros Mensal (%):", min_value=0.0, step=0.01) / 100
prazo = st.number_input("Novo Prazo (meses):", min_value=1, step=1)
valor_liberado = st.number_input("Deseja liberar um valor adicional? (R$):", min_value=0.0, step=100.0)
data_primeira_parcela = st.date_input("Data da 1ª Parcela:", min_value=date.today())

# Verifica se os dados estão completos para simular
if saldo_devedor > 0 and prazo > 0:
    # Cálculo do IOF
    dias_ate_primeira_parcela = (data_primeira_parcela - date.today()).days
    dias_iof = min(365, prazo * 30)  # Limita a 365 dias
    iof_fixo = valor_liberado * 0.0038
    iof_dia = valor_liberado * (0.000082 * dias_iof)
    iof_total = iof_fixo + iof_dia

    # Valor total financiado
    valor_total_financiado = saldo_devedor + valor_liberado + iof_total

    # Cálculo da parcela
    if taxa_juros > 0:
        parcela = valor_total_financiado * (taxa_juros * math.pow(1 + taxa_juros, prazo)) / (math.pow(1 + taxa_juros, prazo) - 1)
    else:
        parcela = valor_total_financiado / prazo

    valor_total_a_pagar = parcela * prazo

    # Exibição dos resultados
    st.markdown("---")
    st.header("📄 Resultado da Simulação")
    st.write(f"📅 Dias até a 1ª parcela: `{dias_ate_primeira_parcela}` dias")
    st.write(f"📌 IOF calculado sobre `{dias_iof}` dias de operação")
    st.write(f"💸 IOF Fixo: {locale.currency(iof_fixo, grouping=True)}")
    st.write(f"💸 IOF Diário: {locale.currency(iof_dia, grouping=True)}")
    st.write(f"💰 IOF Total: {locale.currency(iof_total, grouping=True)}")
    st.write(f"💼 Valor Total Financiado: {locale.currency(valor_total_financiado, grouping=True)}")

    st.success(f"📆 {prazo}x de {locale.currency(parcela, grouping=True)}")
    st.info(f"📊 Total a Pagar: {locale.currency(valor_total_a_pagar, grouping=True)}")
else:
    st.warning("Por favor, insira um saldo devedor e prazo válidos para realizar a simulação.")




