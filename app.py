from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from flask_mail import Mail, Message
import os
from datetime import datetime
from dotenv import load_dotenv
import io
import base64
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.barcharts import VerticalBarChart

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)

# Configurações básicas
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-key-changeme-in-production'

# Configurações de e-mail
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', 'False') == 'False'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', app.config['MAIL_USERNAME'])

mail = Mail(app)

# Perguntas do M-CHAT-R/F
perguntas = [
    "1. Se você aponta para algo do outro lado do cômodo, seu filho olha para ele?",
    "2. Você já se perguntou se seu filho pode ser surdo?",
    "3. Seu filho brinca de faz-de-conta?",
    "4. Seu filho gosta de subir em coisas?",
    "5. Seu filho faz movimentos incomuns com os dedos perto dos olhos?",
    "6. Seu filho aponta com o dedo para pedir algo ou para conseguir ajuda?",
    "7. Seu filho aponta com o dedo para mostrar algo interessante a você?",
    "8. Seu filho está interessado em outras crianças?",
    "9. Seu filho mostra coisas para você trazendo-as ou segurando-as para que você veja?",
    "10. Seu filho responde quando você chama ele pelo nome?",
    "11. Quando você sorri para seu filho, ele sorri de volta?",
    "12. Seu filho fica chateado com barulhos do dia a dia?",
    "13. Seu filho anda?",
    "14. Seu filho olha para você nos olhos quando você está falando com ele ou se vestindo?",
    "15. Seu filho tenta copiar o que você faz?",
    "16. Se você vira a cabeça para olhar para algo, seu filho olha em volta para ver o que é?",
    "17. Seu filho tenta fazer você olhar para ele?",
    "18. Seu filho entende quando você fala para ele fazer algo?",
    "19. Se algo novo acontece, seu filho olha para o seu rosto para ver como você se sente?",
    "20. Seu filho gosta de atividades de movimento?"
]

# Respostas que indicam risco (de acordo com o M-CHAT-R/F)
respostas_risco = {
    0: "NÃO",   # Para a pergunta 1, resposta "NÃO" indica risco
    1: "SIM",   # Para a pergunta 2, resposta "SIM" indica risco
    2: "NÃO",   # Para a pergunta 3, resposta "NÃO" indica risco
    3: "NÃO",   # E assim por diante...
    4: "SIM",
    5: "NÃO",
    6: "NÃO",
    7: "NÃO",
    8: "NÃO",
    9: "NÃO",
    10: "NÃO",
    11: "SIM",
    12: "NÃO",
    13: "NÃO",
    14: "NÃO",
    15: "NÃO",
    16: "NÃO",
    17: "NÃO",
    18: "NÃO",
    19: "NÃO"
}

@app.route('/')
def index():
    return render_template('index.html', perguntas=perguntas)

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/informacoes')
def informacoes():
    return render_template('informacoes.html')

@app.route('/avaliar', methods=['POST'])
def avaliar():
    respostas = []
    pontuacao = 0
    
    for i in range(len(perguntas)):
        resposta = request.form.get(f'pergunta_{i}', '')
        respostas.append(resposta)
        
        # Verificar se a resposta indica risco
        if resposta == respostas_risco[i]:
            pontuacao += 1
    
    # Classificação de acordo com o M-CHAT-R/F
    if pontuacao <= 2:
        classificacao = "Baixo risco"
        recomendacao = "Não é necessário nenhuma ação específica. Continue monitorando o desenvolvimento da criança."
        cor_classificacao = "success"
    elif pontuacao <= 7:
        classificacao = "Risco moderado"
        recomendacao = "Recomenda-se aplicar o Questionário de Follow-up (M-CHAT-R/F) e, se indicado, encaminhar para avaliação especializada."
        cor_classificacao = "warning"
    else:
        classificacao = "Alto risco"
        recomendacao = "Recomenda-se encaminhamento imediato para avaliação diagnóstica especializada."
        cor_classificacao = "danger"
    
    # Dados para o resultado
    dados = {
        'pontuacao': pontuacao,
        'classificacao': classificacao,
        'recomendacao': recomendacao,
        'cor_classificacao': cor_classificacao,
        'perguntas': perguntas,
        'respostas': respostas,
        'data': datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    
    return render_template('resultado.html', **dados)

def create_pdf_with_reportlab(nome, pontuacao, classificacao, recomendacao, data):
    """Cria PDF usando apenas ReportLab"""
    try:
        # Criar buffer para o PDF
        pdf_buffer = io.BytesIO()
        
        # Criar documento
        doc = SimpleDocTemplate(pdf_buffer, pagesize=A4,
                               rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=72)
        
        styles = getSampleStyleSheet()
        
        # Estilos customizados
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#4a90e2'),
            spaceAfter=20,
            alignment=1  # Center
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.gray,
            alignment=1,
            spaceAfter=30
        )
        
        # Conteúdo do PDF
        story = []
        
        # Título
        story.append(Paragraph("M-CHAT-R/F - RESULTADO", title_style))
        story.append(Paragraph(f"Relatório gerado em: {data}", subtitle_style))
        
        # Informações do paciente
        story.append(Paragraph(f"<b>Nome:</b> {nome}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Linha separadora
        story.append(Spacer(1, 12))
        story.append(Drawing(400, 1))
        sep_line = Drawing(400, 1)
        sep_line.add(Rect(0, 0, 400, 1, fillColor=colors.HexColor('#4a90e2'), strokeColor=colors.HexColor('#4a90e2')))
        story.append(sep_line)
        story.append(Spacer(1, 20))
        
        # Resultado - Título
        story.append(Paragraph("RESULTADO DA AVALIAÇÃO", ParagraphStyle(
            'ResultTitle',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#343a40'),
            spaceAfter=15
        )))
        
        # Determinar cor baseado na classificação
        if classificacao == "Baixo risco":
            bg_color = colors.HexColor('#d4edda')
            text_color = colors.HexColor('#155724')
            border_color = colors.HexColor('#c3e6cb')
        elif classificacao == "Risco moderado":
            bg_color = colors.HexColor('#fff3cd')
            text_color = colors.HexColor('#856404')
            border_color = colors.HexColor('#ffeaa7')
        else:
            bg_color = colors.HexColor('#f8d7da')
            text_color = colors.HexColor('#721c24')
            border_color = colors.HexColor('#f5c6cb')
        
        # Tabela de resultados
        result_data = [
            ['Pontuação', f'{pontuacao}/20'],
            ['Classificação', classificacao],
            ['Recomendação', recomendacao]
        ]
        
        result_table = Table(result_data, colWidths=[100, 250])
        result_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
            ('BACKGROUND', (1, 1), (1, 1), bg_color),
            ('TEXTCOLOR', (1, 1), (1, 1), text_color),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a90e2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6'))
        ]))
        
        story.append(result_table)
        story.append(Spacer(1, 30))
        
        # Interpretação dos resultados
        interpretacao_text = """
        <b>Interpretação dos Resultados:</b><br/>
        • <b>0-2 pontos (Baixo risco):</b> Não é necessário nenhuma ação específica.<br/>
        • <b>3-7 pontos (Risco moderado):</b> Recomenda-se aplicar o Questionário de Follow-up.<br/>
        • <b>8-20 pontos (Alto risco):</b> Recomenda-se encaminhamento para avaliação especializada.
        """
        
        story.append(Paragraph(interpretacao_text, styles['Normal']))
        story.append(Spacer(1, 30))
        
        # Nota importante
        note_style = ParagraphStyle(
            'NoteStyle',
            parent=styles['Italic'],
            fontSize=10,
            textColor=colors.gray,
            alignment=1,
            spaceBefore=20
        )
        
        story.append(Paragraph("<i>Este é um relatório gerado automaticamente e não substitui a avaliação de um profissional qualificado. Consulte sempre um especialista para diagnóstico preciso.</i>", note_style))
        
        # Construir PDF
        doc.build(story)
        
        # Retornar dados do PDF
        pdf_data = pdf_buffer.getvalue()
        pdf_buffer.close()
        
        return pdf_data
        
    except Exception as e:
        # Fallback: criar PDF simples se o método anterior falhar
        try:
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer, pagesize=letter)
            width, height = letter
            
            # Título
            c.setFont("Helvetica-Bold", 16)
            c.setFillColor(colors.HexColor('#4a90e2'))
            c.drawString(72, height - 72, "M-CHAT-R/F - RESULTADO")
            
            # Data
            c.setFont("Helvetica", 10)
            c.setFillColor(colors.gray)
            c.drawString(72, height - 90, f"Relatório gerado em: {data}")
            
            # Nome
            c.setFont("Helvetica-Bold", 12)
            c.setFillColor(colors.black)
            c.drawString(72, height - 120, f"Nome: {nome}")
            
            # Resultados
            c.setFont("Helvetica-Bold", 14)
            c.drawString(72, height - 160, "RESULTADO DA AVALIAÇÃO")
            
            c.setFont("Helvetica", 12)
            c.drawString(72, height - 190, f"Pontuação: {pontuacao}/20")
            c.drawString(72, height - 210, f"Classificação: {classificacao}")
            
            # Recomendação
            c.drawString(72, height - 240, "Recomendação:")
            text_object = c.beginText(72, height - 260)
            text_object.setFont("Helvetica", 10)
            text_object.setTextOrigin(72, height - 260)
            text_object.setLeading(14)
            
            # Quebrar texto da recomendação em linhas
            words = recomendacao.split()
            line = ""
            for word in words:
                if c.stringWidth(line + word, "Helvetica", 10) < 400:
                    line += word + " "
                else:
                    text_object.textLine(line)
                    line = word + " "
            if line:
                text_object.textLine(line)
                
            c.drawText(text_object)
            
            # Nota
            c.setFont("Helvetica-Oblique", 8)
            c.setFillColor(colors.gray)
            c.drawString(72, 72, "Este é um relatório gerado automaticamente e não substitui a avaliação de um profissional qualificado.")
            
            c.save()
            pdf_data = pdf_buffer.getvalue()
            pdf_buffer.close()
            
            return pdf_data
            
        except Exception as fallback_error:
            raise Exception(f"Erro ao gerar PDF: {str(fallback_error)}")

@app.route('/gerar_pdf', methods=['POST'])
def gerar_pdf():
    # Recuperar dados do formulário
    nome = request.form.get('nome', '')
    email = request.form.get('email', '')
    pontuacao = request.form.get('pontuacao', '')
    classificacao = request.form.get('classificacao', '')
    recomendacao = request.form.get('recomendacao', '')
    data = request.form.get('data', '')
    
    # Gerar PDF
    try:
        pdf_data = create_pdf_with_reportlab(nome, pontuacao, classificacao, recomendacao, data)
    except Exception as e:
        return render_template('erro.html', mensagem=f"Erro ao gerar PDF: {str(e)}")
    
    # Salvar PDF temporariamente
    filename = f"mchat_resultado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join('static', 'temp', filename)
    
    # Criar diretório se não existir
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'wb') as f:
        f.write(pdf_data)
    
    # Enviar por e-mail se solicitado
    if email and request.form.get('enviar_email') == 'sim':
        try:
            # Verificar se o e-mail está configurado
            if not all([app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']]):
                flash('Serviço de e-mail não configurado. O PDF foi gerado, mas não foi enviado por e-mail.', 'warning')
            else:
                msg = Message(
                    subject="Resultado do Questionário M-CHAT-R/F",
                    sender=app.config['MAIL_DEFAULT_SENDER'],
                    recipients=[email]
                )
                
                # Corpo do e-mail
                msg.body = f"""
                Prezado(a),
                
                Segue em anexo o resultado do questionário M-CHAT-R/F realizado em {data}.
                
                Pontuação: {pontuacao}/20
                Classificação: {classificacao}
                
                {recomendacao}
                
                Atenciosamente,
                Equipe M-CHAT-R/F
                """
                
                msg.html = f"""
                <html>
                <body>
                    <h2>Resultado do Questionário M-CHAT-R/F</h2>
                    <p>Prezado(a),</p>
                    <p>Segue em anexo o resultado do questionário M-CHAT-R/F realizado em <strong>{data}</strong>.</p>
                    
                    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0;">
                        <h3>Resumo do Resultado</h3>
                        <p><strong>Pontuação:</strong> {pontuacao}/20<br>
                        <strong>Classificação:</strong> {classificacao}</p>
                        <p><strong>Recomendação:</strong><br>{recomendacao}</p>
                    </div>
                    
                    <p><em>Este é um relatório automático e não substitui a avaliação de um profissional qualificado.</em></p>
                    
                    <p>Atenciosamente,<br>
                    <strong>Equipe M-CHAT-R/F</strong></p>
                </body>
                </html>
                """
                
                # Anexar o PDF
                with open(filepath, 'rb') as f:
                    msg.attach(filename, "application/pdf", f.read())
                
                # Enviar o e-mail
                mail.send(msg)
                flash('E-mail enviado com sucesso! Verifique sua caixa de entrada.', 'success')
                
        except Exception as e:
            error_msg = f"Erro ao enviar e-mail: {str(e)}"
            print(error_msg)
            flash('Erro ao enviar e-mail. O PDF foi gerado e pode ser baixado.', 'danger')
    
    # Oferecer para baixar o PDF
    return send_file(filepath, as_attachment=True, download_name=filename)

def check_email_config():
    """Verifica se as configurações de e-mail estão definidas"""
    required_configs = ['MAIL_SERVER', 'MAIL_PORT', 'MAIL_USERNAME', 'MAIL_PASSWORD']
    for config in required_configs:
        if not app.config.get(config) or app.config[config] in ['', 'seu_email@gmail.com', 'sua_senha_de_app']:
            return False, f"Configuração de e-mail {config} não está definida corretamente"
    return True, "Configurações de e-mail OK"

if __name__ == '__main__':
    # Criar diretório temporário se não existir
    if not os.path.exists('static/temp'):
        os.makedirs('static/temp', exist_ok=True)
    
    app.run(debug=True)