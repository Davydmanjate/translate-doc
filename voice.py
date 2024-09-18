import PyPDF2
from googletrans import Translator
from gtts import gTTS
import os

# Função para extrair texto de um PDF
def extrair_texto_pdf(caminho_arquivo):
    if not os.path.exists(caminho_arquivo):
        raise FileNotFoundError(f"O arquivo '{caminho_arquivo}' não foi encontrado.")
    
    with open(caminho_arquivo, 'rb') as file:
        leitor_pdf = PyPDF2.PdfReader(file)
        texto = ""
        for page in leitor_pdf.pages:
            texto += page.extract_text()
        return texto

# Função para detectar o idioma original e traduzir o texto para o idioma escolhido
def traduzir_texto(texto, idioma_destino):
    tradutor = Translator()
    # Detectar o idioma do texto original
    deteccao_idioma = tradutor.detect(texto)
    idioma_origem = deteccao_idioma.lang
    print(f"Idioma detectado: {idioma_origem}")
    
    # Traduzir para o idioma destino
    traducao = tradutor.translate(texto, src=idioma_origem, dest=idioma_destino)
    return traducao.text

# Função para converter texto traduzido em áudio
def converter_texto_para_audio(texto, nome_arquivo_audio="saida.mp3", idioma='pt'):
    tts = gTTS(text=texto, lang=idioma)
    tts.save(nome_arquivo_audio)
    print(f"Áudio salvo como {nome_arquivo_audio}")

# Função principal para ler da pasta "doc", traduzir e gerar o áudio
def traduzir_documento_para_audio(nome_arquivo_pdf, idioma_destino):
    # Diretório base do sistema
    diretorio_base = r"D:\App\Voice"
    pasta_docs = os.path.join(diretorio_base, "doc")  # Pasta onde os documentos serão armazenados
    caminho_arquivo = os.path.join(pasta_docs, nome_arquivo_pdf)
    
    if not os.path.exists(caminho_arquivo):
        raise FileNotFoundError(f"O arquivo '{caminho_arquivo}' não foi encontrado na pasta 'doc'.")
    
    # 1. Extrair texto do PDF
    texto = extrair_texto_pdf(caminho_arquivo)
    
    # 2. Traduzir o texto para o idioma escolhido
    texto_traduzido = traduzir_texto(texto, idioma_destino)
    
    # 3. Converter para áudio no idioma escolhido
    nome_arquivo_audio = os.path.join(diretorio_base, nome_arquivo_pdf.replace(".pdf", ".mp3"))
    converter_texto_para_audio(texto_traduzido, nome_arquivo_audio=nome_arquivo_audio, idioma=idioma_destino)

# Função para exibir opções de idioma e retornar o código do idioma escolhido
def escolher_idioma_destino():
    print("Escolha o idioma para tradução:")
    print("1. Português")
    print("2. Inglês")
    print("3. Francês")
    print("4. Espanhol")
    print("5. Tsonga (língua local)")
    
    opcao = input("Digite o número da opção desejada: ")
    
    if opcao == '1':
        return 'pt'  # Português
    elif opcao == '2':
        return 'en'  # Inglês
    elif opcao == '3':
        return 'fr'  # Francês
    elif opcao == '4':
        return 'es'  # Espanhol
    elif opcao == '5':
        return 'ts'  # Tsonga (língua local)
    else:
        print("Opção inválida! O idioma padrão será Português.")
        return 'pt'

# Exemplo de uso
nome_arquivo_pdf = "espanhol.pdf"  # Nome do documento na pasta 'doc'
idioma_destino = escolher_idioma_destino()  # Solicita ao usuário que escolha o idioma
traduzir_documento_para_audio(nome_arquivo_pdf, idioma_destino)  # Traduz e gera áudio
