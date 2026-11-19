import os, glob
import gradio as gr
from bibletrans.chat import responder, AJUDA
from bibletrans import diario
SIMB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "simbolo.png")
def enviar(msg, hist, arqs):
    t, f = responder(msg)
    hist = (hist or []) + [{"role": "user", "content": msg}, {"role": "assistant", "content": t}]
    return "", hist, list(dict.fromkeys((arqs or []) + f))
def ver_diario():
    return "\n".join("%s  %s" % (e.get("quando", ""), e.get("evento", "")) for e in diario.ler()[-50:]) or "Diário vazio."
with gr.Blocks(title="Tradutor Bíblico Assistido") as app:
    with gr.Row():
        if os.path.exists(SIMB):
            gr.Image(SIMB, width=90, show_label=False, interactive=False, container=False)
        gr.Markdown("## Tradutor Bíblico Assistido\nRascunhos de máquina. Sempre validar com falantes nativos.")
    with gr.Tab("Chat"):
        ch = gr.Chatbot(value=[{"role": "assistant", "content": AJUDA}], height=440)
        tx = gr.Textbox(placeholder="Digite um comando ou ajuda", show_label=False)
        fl = gr.Files(label="Arquivos gerados")
        tx.submit(enviar, [tx, ch, fl], [tx, ch, fl])
    with gr.Tab("Diário"):
        bt = gr.Button("Atualizar"); sd = gr.Textbox(lines=18, label="Últimos eventos")
        bt.click(ver_diario, None, sd)
if __name__ == "__main__":
    app.launch()
