# ... (início do app.py) ...

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
        
        # Captura das opções de redação do formulário
        redact_email = 'email' in request.form
        redact_cpf = 'cpf' in request.form
        redact_rg = 'rg' in request.form
        redact_address = 'address' in request.form
        redact_phone = 'phone' in request.form
        
        # NOVO: Captura e processa os termos personalizados
        custom_terms_string = request.form.get('custom_terms', '')
        custom_terms_list = [term.strip() for term in custom_terms_string.split(',') if term.strip()]
        # FIM NOVO

        # Verifica se pelo menos uma opção ou um termo personalizado foi fornecido
        if not (redact_email or redact_cpf or redact_rg or redact_address or redact_phone or custom_terms_list):
             flash('Selecione pelo menos uma opção de redação ou digite termos personalizados.')
             return redirect(url_for('index'))

        try:
            # Chamada da função com TODAS as flags + a nova lista de termos
            redact_pdf(input_path, output_path, redact_email, redact_cpf, redact_address, redact_rg, redact_phone, custom_terms_list)
        except Exception as e:
            flash(f'Erro ao processar PDF: {e}')
            return redirect(url_for('index'))
            
        return render_template('result.html', filename=output_filename)
    else:
        flash('Formato de arquivo não permitido. Use PDF.')
        return redirect(url_for('index'))

# ... (fim do app.py) ...
