import gradio as gr
import pandas as pd
import os
from datetime import datetime

ARQUIVO_CSV = "pacientes.csv"
COLUNAS = ["data_hora", "nome", "idade", "telefone", "convenio", "prioridade", "motivo"]

def cadastrar_paciente(nome_paciente, idade_paciente, telefone_paciente, convenio_selecionado, nivel_prioridade, motivo_consulta):
    nova_linha = {
        "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nome": nome_paciente,
        "idade": idade_paciente,
        "telefone": telefone_paciente,
        "convenio": convenio_selecionado,
        "prioridade": nivel_prioridade,
        "motivo": motivo_consulta,
    }
    novo_registro = pd.DataFrame([nova_linha], columns=COLUNAS)
    if os.path.exists(ARQUIVO_CSV):
        novo_registro.to_csv(ARQUIVO_CSV, mode="a", header=False, index=False)
    else:
        novo_registro.to_csv(ARQUIVO_CSV, mode="w", header=True, index=False)
    tabela_atualizada = pd.read_csv(ARQUIVO_CSV).tail(5)
    return "Paciente cadastrado com sucesso!", tabela_atualizada

with gr.Blocks() as interface_clinica:
    gr.Markdown("## Cadastro de Pacientes - Recepção")
    campo_nome = gr.Textbox(label="Nome do paciente")
    campo_idade = gr.Number(label="Idade", precision=0)
    campo_telefone = gr.Textbox(label="Telefone de contato")
    campo_convenio = gr.Dropdown(
        ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"],
        label="Convênio",
        value="Particular"
    )
    campo_prioridade = gr.Slider(1, 5, value=1, step=1, label="Prioridade do atendimento (1 a 5)")
    campo_motivo = gr.Textbox(label="Motivo da consulta / observações", lines=3)
    botao_cadastrar = gr.Button("Cadastrar")
    mensagem_status = gr.Textbox(label="Status", interactive=False)
    tabela_pacientes = gr.Dataframe(label="Últimos pacientes cadastrados")

    botao_cadastrar.click(
        cadastrar_paciente,
        [campo_nome, campo_idade, campo_telefone, campo_convenio, campo_prioridade, campo_motivo],
        [mensagem_status, tabela_pacientes]
    )

interface_clinica.launch()
