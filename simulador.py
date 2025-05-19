import streamlit as st
from datetime import datetime, date
import math

st.set_page_config(page_title="Simulador de Portabilidade de Crédito", layout="centered")
st.title("📊 Simulador de Portabilidade de Crédito")

# Entradas do usuário
saldo_devedor = st.number_input("Saldo Devedor Atual (R$):", min_value=0.0, step=100.0)
taxa_juros = st.number_input("Nova Taxa de Juros Mensal (%):", min_value=0.0, step=0.01) / 100
prazo = st.number_input("Novo Prazo (meses):", min_value=1, step=1)
valor_liberado = st.number_input("Deseja liberar um valor adicional? (R$):", min_value=0.0, step=100.0)
data_primeira_parcela = st.date_input("Data da 1ª Parcela:", min_value=date.today())

# Cálculo do IOF com base apenas no valor liberado
dias_ate_primeira_parcela = (data_primeira_parcela - date.today()).days
iof_fixo = valor_liberado * 0.0038
iof_dia = valor_liberado * (0.000082 * dias_ate_primeira_parcela)
iof_total = iof_fixo + iof_dia

# Total financiado com IOF incluso
valor_total_financiado = saldo_devedor + valor_liberado + iof_total

# Cálculo da nova parcela
if taxa_juros > 0:
    parcela = valor_total_financiado * (taxa_juros * math.pow(1 + taxa_juros, prazo)) / (math.pow(1 + taxa_juros, prazo) - 1)
else:
    parcela = valor_total_financiado / prazo

# Valor total a pagar
valor_total_a_pagar = parcela * prazo

# Exibição dos resultados
st.subheader("Resultado:")
st.write(f"📅 Dias até a 1ª parcela: {dias_ate_primeira_parcela} dias")
st.write(f"✅ Valor Liberado: R$ {valor_liberado:,.2f}")
st.write(f"📌 IOF Fixo: R$ {iof_fixo:,.2f}")
st.write(f"📌 IOF Diário: R$ {iof_dia:,.2f}")
st.write(f"💸 IOF Total: R$ {iof_total:,.2f}")
st.write(f"💰 Nova Parcela: R$ {parcela:,.2f}")
st.write(f"📈 Total Financiado (com IOF): R$ {valor_total_financiado:,.2f}")
st.write(f"📊 Valor Total a Pagar (somando todas as parcelas): R$ {valor_total_a_pagar:,.2f}")

