import fitz # PyMuPDF
import re
import os

# --- Expressões Regulares (Regex) para PII ---
# Padrão 1: Endereço de Email
REGEX_EMAIL = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# Padrão 2: CPF (11 dígitos)
# Permite formato XXX.XXX.XXX-XX ou XXXXXXXXXXX
REGEX_CPF = r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b'

# Padrão 3: RG (Registro Geral) - CORRIGIDO
# Permite 1 ou 2 dígitos após o hífen no final (ex: -02)
REGEX_RG = r'\b\d{1,2}\.?\d{3}\.?\d{3}-?\d{1,2}X?\b'

# Padrão 4: Celular Brasileiro
REGEX_PHONE = r'(?:\+\d{1,3}\s?)?\(?\d{2}\)?[\s-]?9?\d{4}-?\d{4}\b'

# Padrão 5: CEP
REGEX_CEP = r'\b\d{5}-?\d{3}\b'

# Padrão 6: Termos Comuns de Endereço
REGEX_ADDRESS_TERMS = r'\b(?:RUA|AVENIDA|TRAVESSA|ALAMEDA|PRAÇA|ESTRADA|BECO|SERVIDÃO|R\.|AV\.)\b[\s\.,]*[\w\s\-\.\/]*\s+\d{2,4}\b'


def redact_pdf(input_path: str, output_path: str, redact_email: bool, redact_cpf: bool, redact_address: bool, redact_rg: bool, redact_phone: bool):
    # ... (O corpo da função permanece o mesmo, utilizando os novos REGEX) ...

    # O corpo da função é mantido
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

    if not pii_patterns_to_use:
        print("Aviso: Nenhuma opção de redação selecionada na função.")
        
    try:
        doc = fitz.open(input_path)
    except Exception as e:
        raise IOError(f"Não foi possível abrir o PDF: {e}")

    for page in doc:
        redact_areas = []
        text = page.get_text("text")

        for pattern, pii_type in pii_patterns_to_use:
            
            for match in re.finditer(pattern, text, re.IGNORECASE):
                matching_text = match.group(0)
                
                rects = page.search_for(matching_text) 
                
                for rect in rects:
                    redact_areas.append(rect)
                        
        for rect in redact_areas:
            page.add_redact_annot(rect, fill=(0, 0, 0))

        page.apply_redactions()

    doc.save(output_path, garbage=4, deflate=True)
    doc.close()
