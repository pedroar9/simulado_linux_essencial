import streamlit as st
import random
import time
import re
import json
import os
import pandas as pd
from datetime import date, datetime
import pytz

# --- Configuracoes de hora     ---  
fuso_brasilia = pytz.timezone("America/Sao_Paulo")
agora = datetime.now(fuso_brasilia)
data_atual = agora.today().strftime("%d/%m/%Y")


# --- Questions Data ---
questions_data = [
    {
        "question": "Qual comando exibe informações sobre o uso de disco do sistema?",
        "options": ["df", "du", "lsblk", "mount"],
        "answer": "df",
        "explanation": "`df` mostra o espaço em disco utilizado e disponível nas partições montadas."
    },
    {
        "question": "Qual comando compacta arquivos em um tarball?",
        "options": ["tar", "zip", "archive", "bundle"],
        "answer": "tar",
        "explanation": "`tar` é utilizado para criar e extrair arquivos compactados do tipo tarball."
    },
    {
        "question": "Qual comando exibe o manual do sistema para um comando específico?",
        "options": ["help", "man", "info", "doc"],
        "answer": "man",
        "explanation": "`man` mostra as páginas de manual para comandos e utilitários do sistema."
    },
    {
        "question": "Qual arquivo armazena informações de montagem automática no sistema?",
        "options": ["/etc/fstab", "/etc/auto.conf", "/mnt/config", "/etc/mount"],
        "answer": "/etc/fstab",
        "explanation": "`/etc/fstab` define os sistemas de arquivos a serem montados automaticamente na inicialização."
    },
    {
        "question": "O que faz o comando `ls`?",
        "options": ["Remove arquivos", "Lista arquivos e diretórios", "Cria arquivos", "Move arquivos"],
        "answer": "Lista arquivos e diretórios",
        "explanation": "`ls` lista o conteúdo de diretórios."
    },
    {
        "question": "Qual diretório representa o ponto de montagem para dispositivos removíveis?",
        "options": ["/media", "/mnt", "/run", "/dev"],
        "answer": "/media",
        "explanation": "`/media` é usado para montar automaticamente dispositivos como pendrives e HDs externos."
    },
    {
        "question": "Qual comando é usado para ver o conteúdo de um arquivo texto?",
        "options": ["cat", "ls", "cd", "touch"],
        "answer": "cat",
        "explanation": "`cat` exibe o conteúdo de arquivos no terminal."
    },
    {
        "question": "Qual comando exibe o nome do diretório atual?",
        "options": ["pwd", "cwd", "dir", "whereami"],
        "answer": "pwd",
        "explanation": "`pwd` mostra o caminho completo do diretório de trabalho atual."
    },
    {
        "question": "Qual comando é usado para obter permissões de superusuário temporariamente?",
        "options": ["sudo", "su", "admin", "root"],
        "answer": "sudo",
        "explanation": "`sudo` permite executar comandos como superusuário de forma controlada."
    },
    {
        "question": "Qual comando é utilizado para atualizar os pacotes no Debian/Ubuntu?",
        "options": ["apt update", "yum update", "update", "pkg update"],
        "answer": "apt update",
        "explanation": "`apt update` atualiza a lista de pacotes disponíveis no Debian/Ubuntu."
    },
    {
        "question": "O que representa o diretório `/etc` no Linux?",
        "options": ["Arquivos de usuário", "Arquivos temporários", "Arquivos de configuração", "Bibliotecas do sistema"],
        "answer": "Arquivos de configuração",
        "explanation": "O diretório `/etc` contém arquivos de configuração do sistema."
    },
    {
        "question": "Qual comando cria um novo diretório no Linux?",
        "options": ["mkdir", "mkfolder", "createdir", "newdir"],
        "answer": "mkdir",
        "explanation": "`mkdir` é usado para criar novos diretórios."
    },
    {
        "question": "Qual comando termina um processo pelo seu PID?",
        "options": ["kill", "stop", "terminate", "end"],
        "answer": "kill",
        "explanation": "`kill` envia sinais para processos, como o sinal de término (SIGTERM)."
    },
    {
        "question": "Qual comando é utilizado para alterar o dono de um arquivo no Linux?",
        "options": ["chmod", "chown", "usermod", "own"],
        "answer": "chown",
        "explanation": "`chown` é usado para alterar o dono e/ou grupo de arquivos e diretórios."
    },
    {
        "question": "O que o comando `echo` faz no terminal?",
        "options": ["Cria arquivos", "Imprime texto", "Apaga arquivos", "Lista arquivos"],
        "answer": "Imprime texto",
        "explanation": "`echo` imprime mensagens no terminal ou o valor de variáveis."
    },
    {
        "question": "Qual comando permite agendar tarefas no Linux?",
        "options": ["at", "cron", "schedule", "timejob"],
        "answer": "cron",
        "explanation": "`cron` é utilizado para agendar tarefas recorrentes no sistema Linux."
    },
    {
        "question": "Qual diretório contém os dispositivos do sistema como discos e terminais?",
        "options": ["/dev", "/proc", "/etc", "/var"],
        "answer": "/dev",
        "explanation": "`/dev` contém arquivos especiais que representam dispositivos do sistema."
    },
    {
        "question": "Qual extensão de arquivo é normalmente usada para scripts de shell?",
        "options": [".sh", ".bash", ".run", ".cmd"],
        "answer": ".sh",
        "explanation": "Scripts de shell geralmente usam a extensão `.sh`."
    },
    {
        "question": "Qual comando é utilizado para verificar o caminho completo de um comando?",
        "options": ["where", "path", "which", "locate"],
        "answer": "which",
        "explanation": "`which` mostra o caminho do executável que será executado para um comando."
    },
    {
        "question": "Qual comando é usado para mudar permissões de arquivos?",
        "options": ["chmod", "chperm", "perms", "chattr"],
        "answer": "chmod",
        "explanation": "`chmod` altera as permissões de leitura, escrita e execução de arquivos e diretórios."
    },
    {
        "question": "Qual comando mostra a quantidade de espaço usada por um diretório?",
        "options": ["du", "df", "ls", "size"],
        "answer": "du",
        "explanation": "`du` exibe o uso de espaço de diretórios e arquivos."
    },
    {
        "question": "Qual comando mostra os processos em execução no sistema?",
        "options": ["top", "list", "ps", "jobs"],
        "answer": "ps",
        "explanation": "`ps` exibe os processos ativos no momento em que o comando é executado."
    },
    {
        "question": "Qual comando exibe as variáveis de ambiente atuais?",
        "options": ["set", "env", "printenv", "export"],
        "answer": "env",
        "explanation": "`env` mostra o ambiente atual e as variáveis disponíveis no shell."
    },
    {
        "question": "Qual é a função do arquivo `/etc/passwd`?",
        "options": ["Armazenar senhas dos usuários", "Configurar o bash", "Definir permissões", "Armazenar informações dos usuários"],
        "answer": "Armazenar informações dos usuários",
        "explanation": "`/etc/passwd` contém informações básicas dos usuários, como login, UID, GID e diretório home."
    },
    {
        "question": "Qual comando é usado para visualizar o conteúdo compactado de um arquivo `.gz`?",
        "options": ["gzip -d", "tar -xvzf", "zcat", "extract"],
        "answer": "zcat",
        "explanation": "`zcat` permite visualizar o conteúdo de arquivos compactados com gzip sem descompactá-los."
    },
    {
        "question": "Qual comando é usado para comprimir arquivos com gzip?",
        "options": ["zip", "compress", "gzip", "gz"],
        "answer": "gzip",
        "explanation": "`gzip` é usado para comprimir arquivos em formato `.gz`."
    },
    {
        "question": "Qual comando é usado para desligar o sistema?",
        "options": ["halt", "poweroff", "shutdown", "off"],
        "answer": "shutdown",
        "explanation": "`shutdown` é utilizado para desligar ou reiniciar o sistema de forma segura."
    },
    {
        "question": "Qual comando verifica conectividade com um host remoto?",
        "options": ["ping", "connect", "netcheck", "host"],
        "answer": "ping",
        "explanation": "`ping` envia pacotes ICMP para testar a conectividade com outro host."
    },
    {
        "question": "O que significa o caminho relativo `../`?",
        "options": ["Diretório raiz", "Diretório atual", "Diretório pai", "Diretório temporário"],
        "answer": "Diretório pai",
        "explanation": "`../` representa o diretório pai (nível acima na hierarquia)."
    },
    {
        "question": "O que faz o comando `touch` no Linux?",
        "options": ["Edita arquivos", "Move arquivos", "Cria arquivos vazios", "Apaga arquivos"],
        "answer": "Cria arquivos vazios",
        "explanation": "`touch` é usado para criar arquivos vazios ou atualizar o timestamp de arquivos existentes."
    }
]

# --- Configuracoes da aplicacao ---
st.set_page_config(
    page_title="Simulado da Certificação Linux Essentials",
    page_icon="🐧",
    layout="wide",
    initial_sidebar_state="auto"
)

# --- Definição das cores do tema ---
primary_color = "#347AB6"
secondary_color = "#79A6DC"
background_color = "#F0F8FF"
text_color = "#333333"

# --- CSS para o tema azul ---
custom_css = f"""
<style>
    /* ----------------------------- TIPOGRAFIA ----------------------------- */
    section.main h1, .block-container h1 {{
        font-size: 2.2em;
    }}
    section.main h2, .block-container h2 {{
        font-size: 1.6em;
    }}
    section.main h3, .block-container h3 {{
        font-size: 1.3em;
    }}

    /* ----------------------------- BOTÕES ----------------------------- */
    .stButton>button {{
        background-color: {primary_color};
        color: white;
        border-radius: 10px; /* Aumentado para um look mais rebuscado */
        border: none;
        padding: 12px 24px; /* Padding maior para destaque */
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Sombra sutil */
        transition: all 0.3s ease; /* Transição suave */
        font-size: 1em;
    }}

    .stButton>button:hover {{
        background-color: {secondary_color};
        transform: translateY(-2px); /* Efeito de elevação */
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }}
    .stButton>button:active {{
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }}

    .stButton>button[kind="secondary"], 
    .stButton>button[kind="secondary"]:focus {{
        background-color: #D3D3D3;
        color: #333333;
    }}
    .stButton>button[kind="secondary"]:hover {{
        background-color: #BEBEBE;
        color: #333333;
    }}

    /* Tema Dark */
    .st-emotion-cache-13k62yr .stButton>button,
    body[color-scheme="dark"] .stButton>button {{
        background-color: #4A90E2; /* Tom mais escuro de azul para contraste */
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }}
    .st-emotion-cache-13k62yr .stButton>button:hover,
    body[color-scheme="dark"] .stButton>button:hover {{
        background-color: #63A4FF;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
    }}
    .st-emotion-cache-13k62yr .stButton>button[kind="secondary"],
    body[color-scheme="dark"] .stButton>button[kind="secondary"]:focus {{
        background-color: #555555;
        color: #E0E0E0;
    }}
    .st-emotion-cache-13k62yr .stButton>button[kind="secondary"]:hover,
    body[color-scheme="dark"] .stButton>button[kind="secondary"]:hover {{
        background-color: #6E6E6E;
        color: #E0E0E0;
    }}

    .stButton {{
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }}
    /* Alinha os botões quando aparecem juntos */
    .stButton + .stButton {{
    margin-top: 0 !important;
    }}

    /* ----------------------------- FORMULÁRIO DE CADASTRO ----------------------------- */
    div[data-testid="stForm"] {{
        border: 1px solid {secondary_color};
        border-radius: 10px;
        padding: 1rem 1rem 0.5rem 1rem;
    }}
    body[data-theme="dark"] div[data-testid="stForm"] {{
        border-color: #4A5464 !important;
    }}

    /* ----------------------------- DATAFRAME (RANKING) ----------------------------- */
    /* Cor de fundo da linha ao passar o mouse (hover) */
    div[data-testid="stDataFrame"] .glide-table-body .glide-row:hover {{
        background-color: #E7F1FF !important;
    }}
    /* Cor do texto da linha ao passar o mouse (hover) */
    div[data-testid="stDataFrame"] .glide-table-body .glide-row:hover .glide-cell {{
        color: #000000 !important;
    }}
    /* Tema Dark para o DataFrame */
    body[data-theme="dark"] div[data-testid="stDataFrame"] .glide-table-body .glide-row:hover {{
        background-color: #2C3440 !important;
    }}
    body[data-theme="dark"] div[data-testid="stDataFrame"] .glide-table-body .glide-row:hover .glide-cell {{
        color: #FAFAFA !important;
    }}

    /* ----------------------------- RADIO ----------------------------- */
    .stRadio > label p {{
        font-size: 1.05em !important;
    }}
    body[data-theme="dark"] .stRadio > label p,
    body.dark .stRadio > label p {{
        color: #FAFAFA !important;
    }}
    body[data-theme="light"] .stRadio > label p,
    body.light .stRadio > label p {{
        color: #333333 !important;
    }}
    div[data-baseweb="radio"] > label {{
    margin-bottom: 6px !important;
    }}

    /* ----------------------------- TEXTOS DAS QUESTÕES ----------------------------- */
    .quiz-question-text {{
        font-size: 1.2em;
        color: inherit;
        margin-bottom: 10px !important; 
        line-height: 1.1;
    }}
    body[data-theme="dark"] .quiz-question-text, 
    body.dark .quiz-question-text,
    body[data-theme="dark"] .quiz-question-text strong, 
    body.dark .quiz-question-text strong {{
        color: #FAFAFA !important; 
    }}

    /* ----------------------------- CAIXA DE EXPLICAÇÃO ----------------------------- */
    .explanation-box {{
        border: 1px solid {secondary_color};
        background-color: #E7F1FF;
        padding: 15px;
        border-radius: 5px;
        margin-top: 10px !important';
        line-height: 1.6;
        color: {text_color};
    }}
    body[data-theme="dark"] .explanation-box,
    body.dark .explanation-box {{
        background-color: #2C3440 !important;
        border-color: #4A5464 !important;
        color: #FAFAFA !important;
    }}

    /* ----------------------------- RESULTADO ----------------------------- */
    .score-display {{
        font-size: 1.5em;
        font-weight: bold;
        color: {primary_color};
        text-align: center;
        margin-top: 10px !important;
    }}

    .timer-display {{
        font-size: 1.1em;
        font-weight: bold;
        color: {primary_color};
        padding: 10px;
        border: 1px solid {secondary_color};
        border-radius: 5px;
        background-color: #E7F1FF;
        text-align: center;
    }}

    /* ----------------------------- BLOCOS DE CÓDIGO ----------------------------- */
    .quiz-question-text pre,
    .explanation-box pre {{
        background-color: #282c34 !important;
        color: #abb2bf !important;
        padding: 0.6em !important;
        margin: 0.5em !important;
        border-radius: 5px !important;
        overflow-x: auto !important;
        white-space: pre !important;
        font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace !important;
        font-size: 0.95em !important;
        line-height: 1.6 !important;
        border: 1px solid #3e4451;
    }}

    .quiz-question-text pre code,
    .explanation-box pre code {{
        display: block !important;
        padding: 0 !important;
        margin: 0 !important;
        white-space: pre !important;
        border: none !important;
    }}

    .quiz-question-text p > code,
    .quiz-question-text li > code,
    .explanation-box p > code,
    .explanation-box li > code {{
        padding: 0.1em 0.4em !important;
        margin: 0 0.2em !important;
        display: inline-block !important;
        white-space: pre-wrap !important;
        vertical-align: baseline !important;
    }}

    /* ----------------------------- SYNTAX HIGHLIGHTING ----------------------------- */
    .quiz-question-text pre .c1, .explanation-box pre .c1,
    .quiz-question-text pre .cm, .explanation-box pre .cm {{
        color: #5c6370 !important; font-style: italic !important;
    }}
    .quiz-question-text pre .k, .explanation-box pre .k,
    .quiz-question-text pre .kn, .explanation-box pre .kn {{
        color: #c678dd !important;
    }}
    .quiz-question-text pre .nb, .explanation-box pre .nb,
    .quiz-question-text pre .nc, .explanation-box pre .nc {{
        color: #e5c07b !important;
    }}
    .quiz-question-text pre .nf, .explanation-box pre .nf {{
        color: #61afef !important;
    }}
    .quiz-question-text pre .s1, .explanation-box pre .s1,
    .quiz-question-text pre .s2, .explanation-box pre .s2 {{
        color: #98c379 !important;
    }}
    .quiz-question-text pre .mi, .explanation-box pre .mi,
    .quiz-question-text pre .mf, .explanation-box pre .mf {{
        color: #d19a66 !important;
    }}
    .quiz-question-text pre .bp, .explanation-box pre .bp,
    .quiz-question-text pre .o, .explanation-box pre .o {{
        color: #56b6c2 !important;
    }}
    .quiz-question-text pre .p, .explanation-box pre .p,
    .quiz-question-text pre .n, .explanation-box pre .n {{
        color: #abb2bf !important;
    }}

    /* ----------------------------- RODAPÉ ----------------------------- */
    .rodape-container {{
        position: static;
        width: 100%;
        margin-top: 2rem;
        padding: 0;
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
    }}
    body[data-theme="dark"] .rodape-container,
    body.st-dark .rodape-container {{
        background-color: #1a1c23 !important;
        border: 1px solid #33353b !important;
    }}

    /* Forçar herança do tema dark do contêiner pai */
    .st-emotion-cache-13k62yr .rodape-container,
    body[color-scheme="dark"] .rodape-container,
    body[data-theme="dark"] .rodape-container,
    body.dark .rodape-container,
    body.st-dark .rodape-container {{
        background-color: #1a1c23 !important;
        border: 1px solid #33353b !important;
    }}
    .st-emotion-cache-13k62yr .rodape-container *,
    body[color-scheme="dark"] .rodape-container *,
    body[data-theme="dark"] .rodape-container *,
    body.dark .rodape-container *,
    body.st-dark .rodape-container * {{
        background-color: #1a1c23 !important;
    }}
    .rodape {{
        margin: 0 auto;
        max-width: 900px;
        text-align: center;
        font-size: 0.7em;
        padding: 10px 1.5rem;
        color: #333333;
        box-sizing: border-box;
    }}
    body[data-theme="dark"] .rodape,
    body.st-dark .rodape {{
        background-color: transparent !important;
        color: #FAFAFA !important;
    }}
    .st-emotion-cache-13k62yr .rodape,
    body[color-scheme="dark"] .rodape,
    body[data-theme="dark"] .rodape,
    body.dark .rodape,
    body.st-dark .rodape {{
        color: #abb2bf !important;
    }}
    .rodape .linha {{
        margin: 5px 0;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
    }}
    .rodape .links {{
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 5px;
    }}
    .rodape .links a {{
        text-decoration: none;
        transition: transform 0.3s ease;
    }}
    .rodape .links a:hover {{
        transform: scale(1.1);
    }}
    @media (max-width: 768px) {{
        .rodape-container {{
            margin-top: 2rem;
        }}
        section.main h1, .block-container h1 {{
            font-size: 1.2em !important;
        }}
        .main h2 {{
            font-size: 1.2em !important;
        }}
        .main h3 {{
            font-size: 1em !important;
        }}
        .rodape {{
            font-size: 0.75em;
        }}
        .rodape .links {{
            flex-direction: row;  /* mantém horizontal no mobile */
        }}
        /* Remove espaçamento excessivo entre os botões */
        .st-emotion-cache-ocqkz7 {{
        margin-top: 0 !important;
        gap: 0.2rem !important; /* ou 0.2rem se quiser ainda mais próximo */
        }}

</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# --- Aqui ficam as variáveis globais do SIMULADO como numeros de perguntas, limite de tempo e porcetagem de aprovado ---
NUM_QUESTIONS_PER_QUIZ = 40
QUIZ_TIME_LIMIT_MINUTES = 60
PASSING_PERCENTAGE = 76

RANKING_FILE = 'ranking.json'

# --- Funções ---
def initialize_quiz_session():
    # Garante uma nova semente aleatória a cada inicialização para máxima variedade das perguntas
    random.seed(time.time_ns())

    if len(questions_data) >= NUM_QUESTIONS_PER_QUIZ:
        selected_questions = random.sample(questions_data, NUM_QUESTIONS_PER_QUIZ)
    else:
        selected_questions = random.sample(questions_data, len(questions_data))
    
    st.session_state.questions_to_ask = selected_questions
    st.session_state.total_quiz_questions = len(selected_questions)
    st.session_state.current_question_index = 0
    st.session_state.score = 0
    st.session_state.user_answers = [None] * len(selected_questions)
    st.session_state.answer_submitted = False
    st.session_state.quiz_started = False
    st.session_state.quiz_completed = False
    st.session_state.quiz_start_time = 0.0
    st.session_state.time_up = False
    st.session_state.ranking_updated = False
    # Não limpa o user_info para que o usuário continue logado para novas tentativas
    if "user_info" not in st.session_state:
        st.session_state.user_info = {}

def load_ranking():
    if not os.path.exists(RANKING_FILE):
        return []
    try:
        with open(RANKING_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_ranking(ranking_data):
    with open(RANKING_FILE, 'w', encoding='utf-8') as f:
        json.dump(ranking_data, f, indent=4, ensure_ascii=False)

def add_to_ranking(user_data, score, time_seconds, total_questions_quiz, questions_answered):
    ranking = load_ranking()
    new_entry = {
        "name": user_data.get("name", "Anônimo"),
        "email": user_data.get("email", ""),
        "city": user_data.get("city", ""),
        "country": user_data.get("country", ""),
        "score": score,
        "questions_answered": questions_answered,
        "time_seconds": int(time_seconds),
        "date": datetime.now().strftime("%d-%m-%Y %H:%M"),
        "total_questions": total_questions_quiz 
    }
    ranking.append(new_entry)
    # Ordena por pontos (desc) e depois por tempo (asc)
    ranking.sort(key=lambda x: (-x['score'], x['time_seconds']))
    top_10 = ranking[:10]
    save_ranking(top_10)

def display_question(question_data, current_idx, total_questions):
    # Título geral do simulado
    st.markdown("""            

    ### 🐧 Simulado da certificação Linux Essentials

    """)

    st.markdown(
        f"<div class='quiz-question-text'><strong>Pergunta {current_idx + 1}/{total_questions}:</strong></div>", 
        unsafe_allow_html=True)

    question_text = question_data['question']

    # Pré-processar para blocos de código "cercados" por ```python ... ```
    # Regex para encontrar ```python ... ``` e substituir por <pre><code class="language-python">...</code></pre>
    # A flag re.DOTALL faz com que '.' corresponda também a quebras de linha
    question_text = re.sub(
        r'```python\s*\n(.*?)\n\s*```',
        r'<pre><code class="language-python">\1</code></pre>',
        question_text,
        flags=re.DOTALL
    )
    # Pré-processar para código inline (envolvido por crases simples)
    question_text = re.sub(r'`([^`]+)`', r'<code>\1</code>', question_text)

    st.markdown(f"<div class='quiz-question-text'>{question_text}</div>", unsafe_allow_html=True)
    original_options = list(question_data['options']) # Garante que é uma lista

    def format_option_for_display(opt_str):
        # Substitui múltiplos espaços por &nbsp; para correta renderização no HTML
        # Trata de 2 a 5 espaços consecutivos. Pode ser expandido se necessário.
        s = opt_str
        s = s.replace("     ", "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;") # 5 espaços
        s = s.replace("    ", "&nbsp;&nbsp;&nbsp;&nbsp;")   # 4 espaços
        s = s.replace("   ", "&nbsp;&nbsp;&nbsp;")      # 3 espaços
        s = s.replace("  ", "&nbsp;&nbsp;")         # 2 espaços
        return s

    display_options = [format_option_for_display(opt) for opt in original_options]
    
    # Determina o índice para st.radio com base na resposta original armazenada
    current_user_original_answer = st.session_state.user_answers[current_idx]
    radio_index = None
    if st.session_state.answer_submitted and current_user_original_answer is not None:
        try:
            # Encontra o índice da resposta original nas opções originais
            original_answer_index = original_options.index(current_user_original_answer)
            radio_index = original_answer_index # st.radio usará este índice com display_options
        except ValueError:
            # Caso a resposta armazenada não esteja nas opções originais (improvável com dados consistentes)
            radio_index = None

    # st.radio usa unsafe_allow_html implicitamente para as opções se elas contiverem HTML simples como &nbsp;
    user_choice_display_value = st.radio(
        "Escolha sua resposta:",
        options=display_options, # Usa as opções formatadas para exibição
        index=radio_index,
        key=f"q_radio_{current_idx}",
        disabled=st.session_state.answer_submitted
    )

    # Mapeia a escolha de exibição de volta para o valor da opção original
    if user_choice_display_value is not None:
        selected_display_index = display_options.index(user_choice_display_value)
        user_selected_original_option = original_options[selected_display_index]
        return user_selected_original_option
    return None

def display_timer_and_handle_timeout():
    if st.session_state.quiz_started and not st.session_state.quiz_completed and st.session_state.quiz_start_time > 0:
        timer_placeholder = st.sidebar.empty()
        current_time = time.time()
        elapsed = current_time - st.session_state.quiz_start_time
        time_limit_sec = QUIZ_TIME_LIMIT_MINUTES * 60

        if elapsed >= time_limit_sec:
            if not st.session_state.time_up:
                st.session_state.time_up = True
                st.session_state.quiz_completed = True
                timer_placeholder.error("⏰ Tempo Esgotado!")
                st.warning("⏰ Seu tempo para o quiz esgotou! Verificando resultados...")
                st.experimental_rerun()
            return

        remaining_time = time_limit_sec - elapsed
        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)
        timer_placeholder.markdown(
            f"<div class='timer-display'>⏳ Tempo Restante: {minutes:02d}:{seconds:02d}</div>", 
            unsafe_allow_html=True
        )

        display_ranking_sidebar()
        time.sleep(1)
        st.rerun()

def display_ranking_sidebar():
    st.sidebar.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    with st.sidebar.expander("🏆 Top 10 Ranking", expanded=False):
        ranking_data = load_ranking()
        if not ranking_data:
            st.write("O ranking ainda está vazio. Seja o primeiro a pontuar!")
        else:
            # Calcula a porcentagem para cada entrada
            for entry in ranking_data:
                total_q = entry.get('total_questions', NUM_QUESTIONS_PER_QUIZ) # Usa NUM_QUESTIONS_PER_QUIZ como fallback
                entry['percentage'] = (entry['score'] / total_q) * 100 if total_q > 0 else 0

            df = pd.DataFrame(ranking_data)
            # Formata o tempo para exibição
            df['Tempo'] = df['time_seconds'].apply(lambda s: f"{int(s // 60):02d}:{int(s % 60):02d}")
            # Formata a porcentagem para exibição
            df['Porcentagem'] = df['percentage'].apply(lambda p: f"{int(p)}%")
            # Seleciona e renomeia colunas para exibição
            df_display = df[['name', 'Porcentagem', 'Tempo', 'city', 'country']]
            df_display.columns = ["Nome", "Acerto", "Tempo", "Cidade", "País"]
            # Define o índice para começar em 1 (para o ranking)
            df_display.index = range(1, len(df_display) + 1)
            st.dataframe(df_display, use_container_width=True)

def show_results_page():
    score = st.session_state.score
    total = st.session_state.total_quiz_questions
    final_time_seconds = time.time() - st.session_state.quiz_start_time
    user_info = st.session_state.get("user_info", {})
    pct = (score / total) * 100 if total > 0 else 0

    if pct >= PASSING_PERCENTAGE:
        st.header("🎉 Simulado Concluído! 🎉")
    else:
        st.header("👎🏾 Simulado Concluído! 👎🏾")

    if st.session_state.get("time_up", False):
        st.warning("⏰ Seu tempo para o simulado esgotou!")

    # Garante que o ranking seja atualizado apenas uma vez por quiz
    if not st.session_state.get("ranking_updated", False):
        questions_answered = sum(1 for answer in st.session_state.user_answers if answer is not None)
        add_to_ranking(user_info, score, final_time_seconds, total, questions_answered)
        st.session_state.ranking_updated = True

    display_ranking_sidebar()

    st.markdown(f"<p class='score-display'>Você acertou {score} de {total} questões. ({pct:.1f}%)</p>", unsafe_allow_html=True)
    
    if pct >= PASSING_PERCENTAGE:
        st.success("✅ Parabéns! Você foi aprovado no simulado da certificação PCEP!")
        st.balloons()  # balões só para APROVADOS
        st.markdown("<div class='centered-gif-mobile'>", unsafe_allow_html=True)
        st.image("https://imagens.net.br/wp-content/uploads/2024/06/os-melhores-gifs-de-parabens-para-qualquer-ocasiao-1.gif", width=300)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.error("❌ Você não atingiu a pontuação mínima para aprovação. Tente novamente!")
        st.snow() # emojis de gelor para REPROVADOS
        st.markdown("<div class='centered-gif-mobile'>", unsafe_allow_html=True)
        st.image("https://media1.tenor.com/m/gw207uCZe_MAAAAC/estuda-porra-evelyn-castro.gif", width=300)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("📖 Revisar apenas as questões respondidas"):
        any_answered = False
        if not st.session_state.questions_to_ask:
            st.write("Nenhuma questão para revisar.")
        else:
            for i, q_data_original in enumerate(st.session_state.questions_to_ask):
                user_answer_for_this_q = st.session_state.user_answers[i]

                if user_answer_for_this_q is not None:  # Usuário respondeu a esta pergunta
                    any_answered = True
                    st.markdown(f"**Pergunta {i + 1}:**") # Usa o índice original da pergunta
                    st.markdown(q_data_original['question'], unsafe_allow_html=True)
                    st.markdown(f"**Sua resposta:** {user_answer_for_this_q}")

                    if user_answer_for_this_q == q_data_original["answer"]:
                        st.markdown(f"**Resultado:** ✅ Correto")
                    else:
                        st.markdown(f"**Resultado:** ❌ Incorreto")
                        st.markdown(f"**Resposta correta:** {q_data_original['answer']}")

                    st.markdown(
                        f"<div class='explanation-box'><strong>🧠 Explicação:</strong><br>{q_data_original.get('explanation', 'Nenhuma explicação disponível.')}</div>",
                        unsafe_allow_html=True
                    )
                    st.markdown("---")
            
            if not any_answered and st.session_state.questions_to_ask:
              st.write("Você não respondeu a nenhuma questão.")

    if st.button("Reiniciar Simulado ♻️"):
        initialize_quiz_session()
        st.session_state.quiz_started = False
        st.session_state.quiz_completed = False
        st.rerun()

# --- Inicializar estado do simulado ---
if "questions_to_ask" not in st.session_state:
    initialize_quiz_session()

# --- Interface principal do simulado ---
if not st.session_state.quiz_started:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px;">
            <img src="https://firebrand.training/media/nzgnw4md/linux-l.svg" width="65"/>
            <h1 style="margin: 0;">Simulado da certificação Linux Essentials</h1>
            <img src="https://www.certificacaolinux.com.br/wp-content/uploads/2019/04/linux-essentials.jpg.webp" alt="Linux Essentials Logo" width="65"/>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
### 📢 Sobre a Certificação Linux Essentials 🐧:
                
Este simulado é baseado na prova oficial **Linux Essentials – LPI 010-160**, oferecida pela [LPI (Linux Professional Institute)](https://www.lpi.org/pt-br/our-certifications/linux-essentials-overview/).

---
                
📝 **Formato da Prova Oficial:**
- 🔢 **Número de questões:** 40  
- 🧠 **Tipo de questões:** Múltipla escolha (com uma ou mais corretas) e correspondência (matching)
- ⏰ **Tempo para realização:** 60 minutos  
- ✅ **Nota mínima para aprovação:** 500 de 800 pontos possíveis (Isso geralmente equivale a cerca de 75% de acertos, mas o valor pode variar))  
- 📌 **Aplicação:** Online via OnVUE ou presencial em centros de teste **VUE**
- 🌍 **Idiomas disponíveis:** Inglês, Português, Espanhol, Alemão, Francês, entre outros

---
                
🧠 Utilize este simulado para testar seus conhecimentos e se preparar para a certificação real!

""")
    
    display_ranking_sidebar() # Exibe o ranking na página inicial
    with st.expander("👤 Cadastro para o Top 10 Ranking (Opcional)"):
        with st.form("registration_form"):
            name = st.text_input("Nome")
            email = st.text_input("Email")
            city = st.text_input("Cidade")
            country = st.text_input("País")
            submitted = st.form_submit_button("Salvar Cadastro")
            if submitted and name: # Nome é obrigatório para o cadastro
                st.session_state.user_info = {
                    "name": name, "email": email, "city": city, "country": country
                }
                st.success(f"Olá, {name}! Você está cadastrado para o ranking.")

    if st.session_state.get("user_info", {}).get("name"):
        st.info(f"✅ Logado como **{st.session_state.user_info['name']}**. Seu resultado será registrado no ranking se estiver no Top 10.")

    if st.button("🚀 Iniciar Simulado"):
        st.session_state.quiz_started = True
        st.session_state.quiz_start_time = time.time()
        st.rerun()

elif st.session_state.quiz_completed:
    show_results_page()

else:
    current_idx = st.session_state.current_question_index
    total_questions = st.session_state.total_quiz_questions
    current_question = st.session_state.questions_to_ask[current_idx]

    # --- Barra de Progresso ---
    # O progresso e o texto devem refletir a questão atual (índice + 1)
    progress_value = (current_idx + 1) / total_questions
    st.markdown(
        f"<div class='progress-text'>{current_idx + 1} / {total_questions}</div>", 
        unsafe_allow_html=True
    )
    st.progress(progress_value)
    # --- Fim da Barra de Progresso ---
    user_choice = display_question(current_question, current_idx, total_questions)

    # Criar um placeholder para a área de feedback (sucesso/erro e explicação)
    feedback_placeholder = st.empty()
    # Criar um placeholder para os botões de ação após o feedback
    initial_action_buttons_placeholder = st.empty()
    # Criar um placeholder para os botões de ação após o feedback
    action_buttons_placeholder = st.empty()

    if not st.session_state.answer_submitted:
        # Botões "Confirmar e Avançar" e "Finalizar Simulado" DENTRO do placeholder inicial
        with initial_action_buttons_placeholder.container():
            col1, col2 = st.columns([3, 1.1]) # Ajuste a proporção conforme necessário
            with col1:
                if st.button("Confirmar e Avançar ❯", key=f"confirm_next_{current_idx}", use_container_width=True):
                    if user_choice is not None:  # Usuário selecionou uma resposta
                        st.session_state.answer_submitted = True
                        st.session_state.user_answers[current_idx] = user_choice
                        if user_choice == current_question["answer"]:
                            st.session_state.score += 1
                        initial_action_buttons_placeholder.empty() # Limpa estes botões
                        # Não avança o índice ainda, apenas reroda para mostrar o feedback
                        st.rerun()
                    else:  # Usuário não selecionou, considera como "pulada" e avança
                        st.session_state.user_answers[current_idx] = None # Marca como não respondida
                        if current_idx < total_questions - 1:
                            st.session_state.current_question_index += 1
                            # st.session_state.answer_submitted permanece False
                        else:
                            st.session_state.quiz_completed = True
                        initial_action_buttons_placeholder.empty() # Limpa estes botões
                        st.rerun()
            with col2:
                if st.button("Finalizar Simulado 🏁", key="finalizar_quiz_main", use_container_width=True):
                    st.session_state.quiz_completed = True
                    initial_action_buttons_placeholder.empty() # Limpa estes botões
                    if hasattr(st.session_state, 'timer_placeholder'): # Garante que o placeholder do timer existe
                        st.session_state.timer_placeholder.empty() # Limpa o timer também ao finalizar
                    else:
                        st.sidebar.empty() # Tenta limpar a sidebar se o placeholder específico não foi definido
                    st.rerun()
    else:
        # Resposta já foi submetida (answer_submitted is True), mostrar feedback DENTRO do placeholder
        with feedback_placeholder.container(): # Usar .container() para agrupar múltiplos elementos no placeholder
            correct_answer = current_question["answer"]
            user_answer_for_current_q = st.session_state.user_answers[current_idx]

            if user_answer_for_current_q == correct_answer:
                st.success("✅ Resposta correta!")
            else:
                st.error(f"❌ Resposta incorreta! A resposta correta é: **{correct_answer}**")

            st.markdown(
                f"<div class='explanation-box'><strong>🧠 Explicação:</strong><br>{current_question.get('explanation', 'Nenhuma explicação disponível.')}</div><br>",
                unsafe_allow_html=True
            )


        # Botões após o feedback DENTRO do placeholder de botões de ação
        with action_buttons_placeholder.container():
            col1, col2 = st.columns([3, 1.1])
            with col1:
                if current_idx < total_questions - 1:
                    if st.button("Próxima Pergunta ➡️", key=f"next_question_{current_idx}", use_container_width=True):
                        st.session_state.current_question_index += 1
                        st.session_state.answer_submitted = False  # Reset para a próxima pergunta
                        initial_action_buttons_placeholder.empty() # Garante que os botões iniciais não reapareçam indevidamente
                        feedback_placeholder.empty() # Limpa o feedback anterior
                        action_buttons_placeholder.empty() # Limpa estes botões
                        st.rerun()
                else: # Última pergunta já respondida e feedback mostrado
                    if st.button("Ver Resultado Final 🏁", key="finish_quiz_final_feedback", use_container_width=True):
                        st.session_state.quiz_completed = True
                        feedback_placeholder.empty()
                        action_buttons_placeholder.empty()
                        st.rerun()
            with col2:
                if st.button("Finalizar Simulado 🏁", key="finalizar_quiz_feedback", use_container_width=True):
                    st.session_state.quiz_completed = True
                    feedback_placeholder.empty()
                    action_buttons_placeholder.empty()
                    if hasattr(st.session_state, 'timer_placeholder'):
                        st.session_state.timer_placeholder.empty()
                    else:
                        st.sidebar.empty()
                    st.rerun()

display_timer_and_handle_timeout()

# --- Rodapé com informações do desenvolvedor e versão ---
st.markdown(
    f"""
    <div class="rodape-container">
      <div class="rodape">
          <div class="linha"> 👨🏾‍💻 <b>Desenvolvido por:</b></div>
          <div class="links">
              <a href="https://github.com/pedroar9/" target="_blank">
                  <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white">
              </a>
              <a href="https://www.linkedin.com/in/pedrocarlos-assis/" target="_blank">
                  <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white">
              </a>         
          </div>  
          <div class="linha"> <br> </div>
          <div class="linha">⚙️ <b>Versão:</b> 1.0.1</div> 
          <div class="linha">🗓️ <b>Build:</b> {data_atual}</div>        
      </div>
    </div>
    """,
    unsafe_allow_html=True
)