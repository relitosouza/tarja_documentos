# ... (Padrões de Regex de EMAIL, CPF, etc. permanecem os mesmos) ...

def redact_pdf(input_path: str, output_path: str, redact_email: bool, redact_cpf: bool, redact_address: bool, redact_rg: bool, redact_phone: bool, custom_terms_list: list):
    """
    Abre um arquivo PDF e aplica a redação baseada nos argumentos booleanos e termos personalizados.
    
    :param custom_terms_list: Lista de strings fornecidas pelo usuário para redação.
    """
    
    # 1. Montar a lista de padrões com base nas flags
    pii_patterns_to_use = []
    
    if redact_email:
        pii_patterns_to_use.append((REGEX_EMAIL, "EMAIL"))
    
    if redact_cpf:
        pii_patterns_to_use.append((REGEX_CPF, "CPF"))
        
    if redact_rg:
        pii_patterns_to_use.append((REGEX_RG, "RG"))

    if redact_phone:
        pii_patterns_to_use.append((REGEX_PHONE, "TELEFONE")) 
        
    if redact_address:
        pii_patterns_to_use.append((REGEX_ADDRESS_TERMS, "ENDEREÇO"))
        pii_patterns_to_use.append((REGEX_CEP, "CEP"))


    if not pii_patterns_to_use and not custom_terms_list:
        print("Aviso: Nenhuma opção de redação selecionada na função.")
        
    try:
        doc = fitz.open(input_path)
    except Exception as e:
        raise IOError(f"Não foi possível abrir o PDF: {e}")

    # Itera por todas as páginas
    for page in doc:
        redact_areas = []
        text = page.get_text("text")

        # 2. Busca por padrões de PII ativados (Regex)
        for pattern, pii_type in pii_patterns_to_use:
            
            for match in re.finditer(pattern, text, re.IGNORECASE):
                matching_text = match.group(0)
                
                rects = page.search_for(matching_text) 
                
                for rect in rects:
                    redact_areas.append(rect)
        
        # 3. Busca por termos personalizados (Strings exatas)
        if custom_terms_list:
            for term in custom_terms_list:
                # Remove espaços em branco extras e garante que o termo não está vazio
                clean_term = term.strip()
                if clean_term:
                    # Busca a string exata fornecida pelo usuário
                    rects = page.search_for(clean_term) 
                    for rect in rects:
                        redact_areas.append(rect)

        # 4. Adicionar e Aplicar Redações
        for rect in redact_areas:
            page.add_redact_annot(rect, fill=(0, 0, 0))

        page.apply_redactions()

    # 5. Salvar o PDF redigido
    doc.save(output_path, garbage=4, deflate=True)
    doc.close()
