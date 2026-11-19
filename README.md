# Tradutor Bíblico Assistido

Motor de rascunho de tradução bíblica para idiomas que só têm o Novo Testamento. Base é o NLLB 200 da Meta, livre e gratuito, ajustado com o Novo Testamento do idioma alinhado ao inglês WEB (domínio público). Roda na sua máquina sem chave de API.

Todo texto gerado é rascunho. Nada é tradução final sem revisão de falantes nativos e tradutores qualificados.

## Como usar
1. pip install -r requirements.txt
2. git clone https://github.com/christos-c/bible-corpus dados/bible-corpus
3. python app.py e abra o endereço mostrado
4. No chat digite preparar dinka, depois treinar dinka. Abra o caderno gerado no Colab com GPU T4 e execute tudo
5. Baixe o zip, descompacte em modelos/dik_Latn, digite importar modelo dinka, confira os números, digite aprovar dinka
6. Digite traduzir Rute para dinka. Saem um PDF paralelo e um TSV em saida

## Limites
O NLLB é um tradutor, não um agente. A pesquisa vem de um módulo de busca simples. Treino precisa de GPU, a tradução roda na CPU. O texto inglês de origem é a WEB, pois a ESV não permite tradução para outros idiomas sem licença.

## Símbolo
assets/simbolo.png é a cruz de Jerusalém enviada pelo autor. A imagem veio de banco de imagens com marca d'água e precisa de licença ou substituição antes de qualquer publicação.
