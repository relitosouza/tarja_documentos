import fitz # PyMuPDF
import re
import os

# --- Expressões Regulares (Regex) para PII ---

# Padrão 1: Endereço de Email
REGEX_EMAIL = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# Padrão 2: CPF (11 dígitos)
REGEX_CPF = r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b'

# Padrão 3: RG (Registro Geral) - Permite 1 ou 2 dígitos no final (ex: -02)
REGEX_RG = r'\b\d{1,2}\.?\d{3}\.?\d{3}-?\d{1,2}X?\b'

# Padrão 4: Celular Brasileiro - Permite 4 ou 5 dígitos na primeira parte (ex: (11) 98182-4903)
REGEX_PHONE = r'(?:\+\d{1,3}\s?)?\(?\d{2}\)?[\s-]?\d{4,5}-?\d{4}\b'

# Padrão 5: CEP
REGEX_CEP = r'\b\d{5}-?\d{3}\b'

# Padrão 6: Termos Comuns de Endereço - Mais permissivo para pontuação e caixa alta.
REGEX_ADDRESS_TERMS = r'\b(?:RUA|AVENIDA|TRAVESSA|ALAMEDA|PRAÇA|ESTRADA|BECO|SERVIDÃO|R\.|AV\.)\b[\s\.,]*[\w\s\-\.\/]*\s+\d{2,4}\b'


def redact_pdf(input_path: str, output_path: str, redact_email: bool, redact_cpf: bool, redact_address: bool, redact_rg: bool, redact_phone: bool, custom_terms_list: list):
    """
    Abre um arquivo PDF e aplica a redação baseada nos argumentos booleanos e termos personalizados.
    """
    
    # 1. Montar a lista de padrões (Regex) com base nas flags
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
