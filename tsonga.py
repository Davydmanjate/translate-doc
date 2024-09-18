import os
import PyPDF2
from googletrans import Translator
from gtts import gTTS

def extrair_texto_pdf(caminho_arquivo):
    with open(caminho_arquivo, 'rb') as arquivo:
        leitor = PyPDF2.PdfReader(arquivo)
        texto = ""
        for pagina in leitor.pages:
            texto += pagina.extract_text()
    return texto

def traduzir_e_converter_para_audio(texto, nome_arquivo, idioma_origem='pt', idioma_destino='en'):
    tradutor = Translator()
    
    # Traduzir o texto
    traducao = tradutor.translate(texto, src=idioma_origem, dest=idioma_destino)
    texto_traduzido = traducao.text
    
    # Converter o texto traduzido diretamente para áudio
    tts = gTTS(text=texto_traduzido, lang=idioma_destino)
    tts.save(nome_arquivo)

def processar_documentos(pasta_entrada, pasta_saida, idioma_origem='pt', idioma_destino='en'):
    # Criar pasta de saída se não existir
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)
    
    # Processar todos os arquivos PDF na pasta de entrada
    for arquivo in os.listdir(pasta_entrada):
        if arquivo.lower().endswith('.pdf'):
            caminho_entrada = os.path.join(pasta_entrada, arquivo)
            nome_arquivo_saida = os.path.splitext(arquivo)[0] + '.mp3'
            caminho_saida = os.path.join(pasta_saida, nome_arquivo_saida)
            
            print(f"Processando: {arquivo}")
            
            # Extrair texto do PDF
            texto = extrair_texto_pdf(caminho_entrada)
            
            # Traduzir e converter para áudio
            traduzir_e_converter_para_audio(texto, caminho_saida, idioma_origem, idioma_destino)
            
            print(f"Concluído: {nome_arquivo_saida}")

def main():
    pasta_entrada = "o"  # Pasta contendo os documentos PDF
    pasta_saida = "audios_traduzidos"  # Pasta para salvar os arquivos de áudio
    
    # Idioma de origem e destino
    idioma_origem = 'pt'  # Português
    idioma_destino = 'en'  # Inglês
    
    processar_documentos(pasta_entrada, pasta_saida, idioma_origem, idioma_destino)
    print("Todos os documentos foram processados.")

if __name__ == "__main__":
    main()