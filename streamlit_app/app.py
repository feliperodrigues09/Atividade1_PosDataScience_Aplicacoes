import streamlit as st
import pandas as pd
import os
from datetime import datetime

ARQUIVO_CSV = "pacientes.csv"
COLUNAS = ["data_hora", "nome", "idade", "telefone", "convenio", "prioridade", "motivo"]

st.set_page_config(page_title="Cadastro de Pacientes", layout="centered")
st.title("Cadastro de Pacientes - Recepção")

if "lista_pacientes" not in st.session_state:
    if os.path.exists(ARQUIVO_CSV):
        st.session_state.lista_pacientes = pd.read_csv(ARQUIVO_CSV)
    else:
        st.session_state.lista_pacientes = pd.DataFrame(columns=COLUNAS)

with st.form("formulario_cadastro", clear_on_submit=True):
    nome_paciente = st.text_input("Nome do paciente")
    idade_paciente = st.number_input("Idade", min_value=0, max_value=120, step=1)
    telefone_paciente = st.text_input("Telefone de contato")
    convenio_selecionado = st.selectbox(
        "Convênio",
        ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"]
    )
    nivel_prioridade = st.slider("Prioridade do atendimento (1 a 5)", 1, 5, 1)
    motivo_consulta = st.text_area("Motivo da consulta / observações")
    botao_enviado = st.form_submit_button("Cadastrar")

if botao_enviado:
    nova_linha = {
        "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nome": nome_paciente,
        "idade": int(idade_paciente),
        "telefone": telefone_paciente,
        "convenio": convenio_selecionado,
        "prioridade": int(nivel_prioridade),
        "motivo": motivo_consulta,
    }
    novo_registro = pd.DataFrame([nova_linha], columns=COLUNAS)
    if os.path.exists(ARQUIVO_CSV):
        novo_registro.to_csv(ARQUIVO_CSV, mode="a", header=False, index=False)
    else:
        novo_registro.to_csv(ARQUIVO_CSV, mode="w", header=True, index=False)

    st.session_state.lista_pacientes = pd.concat(
        [st.session_state.lista_pacientes, novo_registro],
        ignore_index=True
    )
    st.success("Paciente cadastrado com sucesso!")

st.subheader("Últimos pacientes cadastrados")
st.dataframe(st.session_state.lista_pacientes.tail(5), use_container_width=True)

dados_csv = st.session_state.lista_pacientes.to_csv(index=False).encode("utf-8")
st.download_button(
    "Baixar CSV",
    dados_csv,
    "pacientes.csv",
    "text/csv"
)
