import streamlit as st
import math

st.set_page_config(page_title="Simulador de Portabilidade de Crédito", layout="centered")
st.title("📊 Simulador de Portabilidade de Crédito")

col1, col2 = st.columns(2)
with col1:
    saldo_devedor = st.number_input("Saldo Devedor Atual (R$):", min_value=0.0, step=100.0, format="%.2f")
    prazo = st.number_input("Novo Prazo (meses):", min_value=1, step=1)
with col2:
    taxa_juros = st.number_input("Nova Taxa de Juros Mensal (%):", min_value=0.0, step=0.01, format="%.2f") / 100
    valor_liberado = st.number_input("Valor Adicional Liberado (R$):", min_value=0.0, step=100.0, format="%.2f")

st.markdown("""
**IOF (aplicado somente sobre o valor adicional liberado):**

- 0,38% fixo  
- 0,01118% ao dia  
- + 0,0082% ao dia se prazo > 365 dias  
""")

if st.button("Calcular"):
    prazo_dias = prazo * 30  # aproximação do prazo em dias

    # IOF fixo sobre valor adicional liberado
    iof_fixo = valor_liberado * 0.0038

    # IOF diário sobre valor adicional liberado
    iof_diario = valor_liberado * 0.0001118 * prazo_dias

    # IOF diário adicional para prazo > 365 dias
    iof_diario_adicional = 0
    if prazo_dias > 365:
        iof_diario_adicional = valor_liberado * 0.000082 * prazo_dias

    # Total IOF
    iof_total = iof_fixo + iof_diario + iof_diario_adicional

    # Total financiado (saldo devedor + valor liberado + IOF sobre valor liberado)
    valor_total_financiado = saldo_devedor + valor_liberado + iof_total

    # Cálculo da parcela
    if taxa_juros > 0:
        parcela = valor_total_financiado * (taxa_juros * math.pow(1 + taxa_juros, prazo)) / (math.pow(1 + taxa_juros, prazo) - 1)
    else:
        parcela = valor_total_financiado / prazo

    valor_total_a_pagar = parcela * prazo

    st.subheader("Resultado:")
    st.write(f"✅ Valor Liberado: R$ {valor_liberado:,.2f}")
    st.write(f"📌 IOF Fixo (0,38%): R$ {iof_fixo:,.2f}")
    st.write(f"📌 IOF Diário (0,01118% x {prazo_dias} dias): R$ {iof_diario:,.2f}")
    if iof_diario_adicional > 0:
        st.write(f"📌 IOF Diário Adicional (0,0082% x {prazo_dias} dias): R$ {iof_diario_adicional:,.2f}")
    st.write(f"📌 **IOF Total:** R$ {iof_total:,.2f}")
    st.write(f"📈 Total Financiado (com IOF): R$ {valor_total_financiado:,.2f}")
    st.write(f"💰 Nova Parcela: R$ {parcela:,.2f}")
    st.write(f"💸 Valor Total a Pagar (soma de todas as parcelas): R$ {valor_total_a_pagar:,.2f}")
