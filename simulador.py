import streamlit as st
from datetime import date
import math
import pandas as pd
import io

st.set_page_config(page_title="Simulador de Portabilidade de Crédito", layout="centered")

def formatar_reais(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

st.image("https://github.com/Jean-Sabino/simulador-portabilidade/blob/main/logo_sicoob.png?raw=true", width=180)

st.markdown("<h1 style='text-align: center; color: #004d40;'>📊 Simulador de Portabilidade de Crédito</h1>", unsafe_allow_html=True)
st.markdown("---")

tabs = st.tabs(["📌 Simular valor da parcela", "📌 Simular valor liberado com base na parcela desejada"])

# ---------- TELA 1: Simular valor da parcela ----------
with tabs[0]:
    st.subheader("🔢 Informações do Empréstimo")
    col1, col2 = st.columns(2)
    with col1:
        saldo_devedor = st.number_input("💰 Saldo Devedor Atual (R$):", min_value=0.0, step=100.0, key="sd1")
        valor_liberado = st.number_input("💸 Valor do Contrato Novo ou do Troco (R$):", min_value=0.0, step=100.0)
    with col2:
        taxa_juros = st.number_input("📉 Nova Taxa de Juros Mensal (%):", min_value=0.0, step=0.01, key="tj1") / 100
        prazo = st.number_input("📆 Prazo (meses):", min_value=1, step=1, key="pz1")
        data_primeira_parcela = st.date_input("📅 Data da 1ª Parcela:", min_value=date.today(), key="dp1")

    observacoes = st.text_area("📝 Observações adicionais (opcional):", placeholder="Digite anotações relevantes para essa simulação...")

    if st.button("🚀 Calcular Simulação", key="btn1"):
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
        st.subheader("📄 Resultado da Simulação")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"📅 Dias até a 1ª parcela: `{dias_ate_primeira_parcela}`")
            st.write(f"📌 IOF sobre `{dias_iof}` dias")
            st.write(f"💸 IOF Fixo: {formatar_reais(iof_fixo)}")
            st.write(f"💸 IOF Diário: {formatar_reais(iof_dia)}")
            st.write(f"💰 IOF Total: {formatar_reais(iof_total)}")
        with col2:
            st.write(f"💼 Valor Total Financiado: {formatar_reais(valor_total_financiado)}")
            st.success(f"📆 Parcelas: {prazo}x de {formatar_reais(parcela)}")
            st.info(f"📊 Total a Pagar: {formatar_reais(valor_total_a_pagar)}")

        # Exportar Excel
        df_resultado = pd.DataFrame({
            "Descrição": ["Saldo Devedor", "Valor Liberado", "IOF Fixo", "IOF Diário", "IOF Total",
                          "Total Financiado", "Parcela", "Total a Pagar", "Prazo (meses)", "Data 1ª Parcela", "Observações"],
            "Valor": [saldo_devedor, valor_liberado, iof_fixo, iof_dia, iof_total,
                      valor_total_financiado, parcela, valor_total_a_pagar, prazo, str(data_primeira_parcela), observacoes]
        })

        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df_resultado.to_excel(writer, index=False, sheet_name="Simulação")
            writer.close()
            st.download_button("📥 Baixar Resultado em Excel", buffer.getvalue(), file_name="simulacao_parcela.xlsx")

# ---------- TELA 2: Simular valor liberado ----------
with tabs[1]:
    st.subheader("🔢 Informações da Parcela Desejada")
    col1, col2 = st.columns(2)
    with col1:
        parcela_desejada = st.number_input("💵 Valor da Parcela Desejada (R$):", min_value=0.0, step=50.0)
    with col2:
        taxa_juros = st.number_input("📉 Nova Taxa de Juros Mensal (%):", min_value=0.0, step=0.01, key="tj2") / 100
        prazo = st.number_input("📆 Prazo (meses):", min_value=1, step=1, key="pz2")
        data_primeira_parcela = st.date_input("📅 Data da 1ª Parcela:", min_value=date.today(), key="dp2")

    observacoes2 = st.text_area("📝 Observações adicionais (opcional):", key="obs2", placeholder="Digite anotações relevantes para essa simulação...")

    if st.button("🚀 Calcular Simulação", key="btn2"):
        saldo_devedor = 0.0
        dias_ate_primeira_parcela = (data_primeira_parcela - date.today()).days
        dias_iof = min(365, prazo * 30)

        if taxa_juros > 0:
            fator = (1 - math.pow(1 + taxa_juros, -prazo)) / taxa_juros
        else:
            fator = prazo

        valor_total_financiado = parcela_desejada * fator
        valor_base_iof = valor_total_financiado - saldo_devedor
        iof_fixo = valor_base_iof * 0.0038
        iof_dia = valor_base_iof * (0.000082 * dias_iof)
        iof_total = iof_fixo + iof_dia
        valor_liberado = valor_base_iof - iof_total
        parcela = parcela_desejada
        valor_total_a_pagar = parcela * prazo

        # Resultados
        st.subheader("📄 Resultado da Simulação")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"📅 Dias até a 1ª parcela: `{dias_ate_primeira_parcela}`")
            st.write(f"📌 IOF sobre `{dias_iof}` dias")
            st.write(f"💸 IOF Fixo: {formatar_reais(iof_fixo)}")
            st.write(f"💸 IOF Diário: {formatar_reais(iof_dia)}")
            st.write(f"💰 IOF Total: {formatar_reais(iof_total)}")
        with col2:
            st.write(f"💼 Valor Total Financiado: {formatar_reais(valor_total_financiado)}")
            st.success(f"📆 Parcelas: {prazo}x de {formatar_reais(parcela)}")
            st.info(f"📊 Total a Pagar: {formatar_reais(valor_total_a_pagar)}")
            st.warning(f"🔓 Valor que pode ser liberado: {formatar_reais(valor_liberado)}")

        # Exportar Excel
        df_resultado2 = pd.DataFrame({
            "Descrição": ["Parcela Desejada", "IOF Fixo", "IOF Diário", "IOF Total",
                          "Valor Total Financiado", "Valor Liberado", "Total a Pagar", "Prazo (meses)", "Data 1ª Parcela", "Observações"],
            "Valor": [parcela_desejada, iof_fixo, iof_dia, iof_total,
                      valor_total_financiado, valor_liberado, valor_total_a_pagar, prazo, str(data_primeira_parcela), observacoes2]
        })

        buffer2 = io.BytesIO()
        with pd.ExcelWriter(buffer2, engine='xlsxwriter') as writer:
            df_resultado2.to_excel(writer, index=False, sheet_name="Simulação")
            writer.close()
            st.download_button("📥 Baixar Resultado em Excel", buffer2.getvalue(), file_name="simulacao_valor_liberado.xlsx")

