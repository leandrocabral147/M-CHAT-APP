# 🧩 Sistema M-CHAT-R/F - Questionário para Triagem de Autismo

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Flask-2.3.3-green?style=for-the-badge&logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/Bootstrap-5.1.3-purple?style=for-the-badge&logo=bootstrap" alt="Bootstrap">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License">
</p>

Um sistema web completo para aplicação do questionário M-CHAT-R/F (Modified Checklist for Autism in Toddlers, Revised with Follow-Up), instrumento validado para triagem de Transtorno do Espectro Autista (TEA) em crianças.


## ✨ Funcionalidades

- 🧠 **Questionário Completo**: Todas as 20 questões do M-CHAT-R/F com opções Sim/Não
- 📊 **Avaliação Automática**: Sistema de pontuação e classificação de risco integrado
- 📄 **Relatórios em PDF**: Geração de resultados em formato PDF para download
- 📧 **Envio por E-mail**: Opção de enviar resultados diretamente para o e-mail informado
- 🎨 **Interface Responsiva**: Design moderno e acessível com tema de conscientização do autismo
- 📱 **Mobile-Friendly**: Layout adaptável para todos os dispositivos
- ⚡ **Processo Rápido**: Interface intuitiva e de fácil utilização

## 🛠️ Tecnologias Utilizadas

### Backend
- ![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white) Python 3.8+
- ![Flask](https://img.shields.io/badge/Flask-2.3.3-000000?style=flat-square&logo=flask&logoColor=white) Flask 2.3.3

### Frontend
- ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white) HTML5
- ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white) CSS3
- ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black) JavaScript
- ![Bootstrap](https://img.shields.io/badge/Bootstrap-5.1.3-7952B3?style=flat-square&logo=bootstrap&logoColor=white) Bootstrap 5.1.3

### Bibliotecas
- ![ReportLab](https://img.shields.io/badge/ReportLab-PDF_Generation-FF6B6B?style=flat-square) ReportLab (PDF)
- ![Flask-Mail](https://img.shields.io/badge/Flask--Mail-Email_System-DC3545?style=flat-square) Flask-Mail
- ![Bootstrap Icons](https://img.shields.io/badge/Bootstrap_Icons-1.10.0-6F42C1?style=flat-square) Bootstrap Icons

## 📦 Instalação e Configuração

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)

### 🚀 Passo a Passo

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/mchat-system.git
   cd mchat-system
   ```

2. **Crie um ambiente virtual (recomendado)**
   ```bash
   # Linux/Mac
   python -m venv venv
   source venv/bin/activate
   
   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente**
   ```bash
   # Copie o arquivo de exemplo
   cp .env.example .env
   ```
   
   Edite o arquivo `.env` com suas configurações:
   ```env
   SECRET_KEY=sua_chave_secreta_aqui
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=seu_email@gmail.com
   MAIL_PASSWORD=sua_senha_de_app
   MAIL_DEFAULT_SENDER=seu_email@gmail.com
   ```

5. **Execute a aplicação**
   ```bash
   python app.py
   ```

6. **Acesse o sistema**
   Abra seu navegador e visite: `http://localhost:5000`

## 🎯 Como Utilizar

1. **📋 Acesse a Página Inicial** - Navegue até a aba "Teste"
2. **✅ Responda as Perguntas** - Complete todas as 20 questões
3. **📊 Visualize o Resultado** - Veja a classificação automática
4. **📄 Gere o Relatório** - Baixe o PDF ou envie por e-mail
5. **ℹ️ Consulte Informações** - Acesse as abas "Sobre" e "Informações"

## 📋 Estrutura do Projeto

```
mchat-system/
├── 📁 static/               # Arquivos estáticos
│   ├── 📁 css/              # Estilos CSS
│   │   ├── style.css        # Estilos principais
│   │   └── theme.css        # Tema customizado
│   ├── 📁 js/               # JavaScript
│   │   └── script.js        # Funcionalidades frontend
│   └── 📁 images/           # Imagens e ícones
├── 📁 templates/            # Templates HTML
│   ├── base.html            # Template base
│   ├── index.html           # Página inicial
│   ├── sobre.html           # Informações sobre o M-CHAT-R/F
│   ├── informacoes.html     # Informações importantes
│   ├── resultado.html       # Página de resultados
│   └── erro.html            # Página de erro
├── app.py                   # Aplicação principal Flask
├── requirements.txt         # Dependências do projeto
├── .env                     # Variáveis de ambiente
└── README.md                # Este arquivo
```

## ⚙️ Configuração de E-mail

Para configurar o envio de e-mails:

### 📧 Gmail
1. Ative a verificação em duas etapas
2. Gere uma senha de aplicativo
3. Use as credenciais no arquivo `.env`

### 📧 Outlook/Office 365
```env
MAIL_SERVER=smtp.office365.com
MAIL_PORT=587
MAIL_USE_TLS=True
```

### 📧 Outros provedores
Consulte a documentação do seu serviço de e-mail

## 🚀 Deploy em Produção

### Opção 1: Gunicorn (Recomendado)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Opção 2: Waitress (Windows)
```bash
pip install waitress
waitress-serve --port=5000 app:app
```

### Configurações de Produção
```python
# No app.py, adicione:
app.config['DEBUG'] = False
app.config['TESTING'] = False
```

## 📊 Sistema de Pontuação

| Pontuação | Classificação | Recomendação |
|-----------|---------------|--------------|
| 0-2 | 🟢 Baixo risco | Acompanhamento regular |
| 3-7 | 🟡 Risco moderado | Avaliação adicional recomendada |
| 8-20 | 🔴 Alto risco | Encaminhamento urgente |

## ⚠️ Aviso Importante

> **🚨 ATENÇÃO: Este sistema tem caráter informativo e NÃO substitui o diagnóstico profissional.**
> 
> Sempre consulte especialistas qualificados para avaliação e diagnóstico preciso.

## 🤝 Como Contribuir

Contribuições são bem-vindas! Siga estes passos:

1. 🍴 Faça um Fork do projeto
2. 🌿 Crie uma Branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. 💾 Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. 📤 Push para a Branch (`git push origin feature/AmazingFeature`)
5. 🔀 Abra um Pull Request

## 📄 Licença

Distribuído sob licença MIT. Veja o arquivo `LICENSE` para mais informações.

## 👨💻 Desenvolvido por

**Seu Nome** - [@Leandro Cabral](https://github.com/leandrocabral147) - leandrocabral147@gmail.com

## 🌐 Links Úteis

- 🔗 [Documentação Oficial M-CHAT-R/F](https://mchatscreen.com/)
- 🔗 [Site Oficial do Autismo](https://www.autismspeaks.org/)
- 🔗 [Documentação Flask](https://flask.palletsprojects.com/)
- 🔗 [Documentação Bootstrap](https://getbootstrap.com/docs/)

---

<p align="center">
  <strong>💙 Apoie a conscientização sobre o autismo! 💙</strong>
</p>

<p align="center">
  <em>Este projeto visa facilitar o acesso à triagem precoce, contribuindo para o desenvolvimento saudável de crianças.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/seu-usuario/mchat-system?style=social" alt="GitHub stars">
  <img src="https://img.shields.io/github/forks/seu-usuario/mchat-system?style=social" alt="GitHub forks">
</p>
