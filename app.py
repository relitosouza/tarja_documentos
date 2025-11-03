import os
from flask import Flask, request, render_template, send_from_directory, redirect, url_for, flash
from werkzeug.utils import secure_filename
from utils.redact import redact_pdf


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024 # 50 MB
app.secret_key = 'troque_esta_chave_por_uma_sena_secreta'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/redact', methods=['POST'])
def redact_route():
    if 'file' not in request.files:
        flash('Nenhum arquivo enviado')
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        flash('Nenhum arquivo selecionado')
        return redirect(url_for('index'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)
        output_filename = filename.rsplit('.', 1)[0] + '_redacted.pdf'
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        try:
            redact_pdf(input_path, output_path)
        except Exception as e:
            flash(f'Erro ao processar PDF: {e}')
            return redirect(url_for('index'))
        return render_template('result.html', filename=output_filename)
    else:
        flash('Formato de arquivo não permitido. Use PDF.')
        return redirect(url_for('index'))


@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)