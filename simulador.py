import streamlit as st
from datetime import date
import math

# Configuração da página
st.set_page_config(page_title="Simulador de Portabilidade de Crédito", layout="centered")

# Função para formatar valores como reais
def formatar_reais(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Logo da cooperativa
st.image("https://github.com/Jean-Sabino/simulador-portabilidade/blob/main/logo_sicoob.png?raw=true", width=180)

# Título centralizado com ícone
st.markdown("<h1 style='text-align: center; color: #004d40;'>📊 Simulador de Portabilidade de Crédito</h1>", unsafe_allow_html=True)
st.markdown("---")

# Bloco de entrada com colunas
st.subheader("🔢 Informações do Empréstimo")

col1, col2 = st.columns(2)
with col1:
    saldo_devedor = st.number_input("💰 Saldo Devedor Atual (R$):", min_value=0.0, step=100.0)
    valor_liberado = st.number_input("💸 Valor de Troco ou Contrato Novo (R$):", min_value=0.0, step=100.0)

with col2:
    taxa_juros = st.number_input("📉 Nova Taxa de Juros Mensal (%):", min_value=0.0, step=0.01) / 100
    prazo = st.number_input("📆 Novo Prazo (meses):", min_value=1, step=1)

data_primeira_parcela = st.date_input("📅 Data da 1ª Parcela:", min_value=date.today())

st.markdown("---")

# Botão para acionar o cálculo
if st.button("🚀 Calcular Simulação"):
    dias_ate_primeira_parcela = (data_primeira_parcela - date.today()).days
    dias_iof = min(365, prazo * 30)

    iof_fixo = valor_liberado * 0.0038
    iof_dia = valor_liberado * (0.000082 * dias_iof)
    iof_total = iof_fixo + iof_dia

    valor_total_financiado = saldo_devedor + valor_liberado + iof_total

    if taxa_juros > 0:
        parcela = valor_total_financiado * (taxa_juros * math.pow(1 + taxa_juros, prazo)) / (math.pow(1 + taxa_juros, prazo) - 1)
    else:
        parcela = valor_total_financiado / prazo

    valor_total_a_pagar = parcela * prazo

    # Resultados
    st.markdown("---")
    st.subheader("📄 Resultado da Simulação")

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"📅 Dias até a 1ª parcela: `{dias_ate_primeira_parcela}`")
        st.write(f"📌 IOF sobre `{dias_iof}` dias de operação")
        st.write(f"💸 IOF Fixo: {formatar_reais(iof_fixo)}")
        st.write(f"💸 IOF Diário: {formatar_reais(iof_dia)}")
        st.write(f"💰 IOF Total: {formatar_reais(iof_total)}")

    with col2:
        st.write(f"💼 Valor Total Financiado: {formatar_reais(valor_total_financiado)}")
        st.success(f"📆 Parcelas: {prazo}x de {formatar_reais(parcela)}")
        st.info(f"📊 Total a Pagar: {formatar_reais(valor_total_a_pagar)}")

    st.markdown("---")
    st.caption("Simulação estimada com base nas informações fornecidas. Consulte sua cooperativa para condições oficiais.")







