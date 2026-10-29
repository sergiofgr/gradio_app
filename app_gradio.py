import os
from datetime import datetime

import gradio as gr
import pandas as pd

PASTA_PROJETO = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_CSV = os.path.join(PASTA_PROJETO, "pacientes.csv")

COLUNAS = ["timestamp", "nome", "idade", "convenio", "prioridade", "motivo"]
CONVENIOS = ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"]


def ultimos_pacientes(n=5):
    if os.path.exists(ARQUIVO_CSV):
        return pd.read_csv(ARQUIVO_CSV).tail(n)
    return pd.DataFrame(columns=COLUNAS)


def cadastrar_paciente(nome, idade, convenio, prioridade, motivo):
    if not nome or not nome.strip():
        return "⚠️ Informe o nome do paciente.", ultimos_pacientes()
    if idade is None or idade < 0 or idade > 130:
        return "⚠️ Informe uma idade válida.", ultimos_pacientes()
    if not convenio:
        return "⚠️ Selecione o convênio.", ultimos_pacientes()

    linha = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nome": nome.strip(),
        "idade": int(idade),
        "convenio": convenio,
        "prioridade": int(prioridade),
        "motivo": (motivo or "").strip(),
    }
    novo = pd.DataFrame([linha], columns=COLUNAS)
    existe = os.path.exists(ARQUIVO_CSV)
    novo.to_csv(
        ARQUIVO_CSV,
        mode="a" if existe else "w",
        header=not existe,
        index=False,
        encoding="utf-8",
    )
    return "✅ Paciente cadastrado com sucesso!", ultimos_pacientes()


with gr.Blocks(title="Cadastro de Pacientes") as demo:
    gr.Markdown("## Cadastro de Pacientes")
    nome = gr.Textbox(label="Nome do paciente")
    idade = gr.Number(label="Idade", precision=0, minimum=0, maximum=130)
    convenio = gr.Dropdown(CONVENIOS, label="Convênio", value="Particular")
    prioridade = gr.Slider(1, 5, value=1, step=1, label="Prioridade do atendimento (5 = urgente)")
    motivo = gr.Textbox(label="Motivo da consulta / observações", lines=3)
    botao = gr.Button("Cadastrar", variant="primary")
    saida_msg = gr.Textbox(label="Status", interactive=False)
    tabela = gr.Dataframe(label="Últimos pacientes cadastrados", value=ultimos_pacientes)

    botao.click(
        cadastrar_paciente,
        [nome, idade, convenio, prioridade, motivo],
        [saida_msg, tabela],
    )

if __name__ == "__main__":
    demo.launch()

