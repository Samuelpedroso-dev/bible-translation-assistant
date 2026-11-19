# Roteiro

## Feito
Interface de chat, diagramação em PDF paralelo, gerador de caderno do Colab, tradução local com CTranslate2, diário automático, pesquisa web simples, esqueleto do agente de navegador.

## Arquitetura do agente
O NLLB só traduz. A camada de agente tem três partes.
1. Navegador real com Playwright, que abre páginas, lê texto, clica e digita.
2. Planejador, um LLM local pequeno via Ollama que escolhe o próximo passo em JSON. É opcional.
3. Diário, que registra cada passo para documentar e postar.

## Próximos passos
Treinar Dinka e Kabyle com o Novo Testamento completo, medir chrF++, rascunhar Rute e Jonas, conseguir validação com falantes nativos, ampliar o agente de pesquisa, adicionar mais idiomas.
