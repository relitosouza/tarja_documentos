import fitz # PyMuPDF
import re
import os

# --- Expressões Regulares (Regex) para PII ---
# Padrão 1: Endereço de Email (Ex: usuario@dominio.com)
REGEX_EMAIL = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# Padrão 2: CPF (Ex: 000.000.000-00)
REGEX_CPF = r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b'

# Padrão 3: RG (Registro Geral)
REGEX_RG = r'\b\d{1,2}\.?\d{3}\.?\d{3}-?\d{1}X?\b'

# Padrão 4: Celular Brasileiro (Ex: (00) 90000-0000, 00 900000000) - NOVO PADRÃO
# Este padrão é complexo e deve ser testado:
# (DDI opcional) (DDD opcional) 9 + 8 dígitos
REGEX_PHONE = r'(?:\+\d{1,3}\s?)?\(?\d{2}\)?[\s-]?9?\d{4}-?\d{4}\b'

# Padrão 5: CEP (Ex: 00000-000)
REGEX_CEP = r'\b\d{5}-?\d{3}\b'

# Padrão 6: Termos Comuns de Endereço (Rua, Av, Travessa, etc.)
REGEX_ADDRESS_TERMS = r'\b(?:Rua|Av(?:enida)?|Travessa|Alameda|Praça|Estrada|Beco|Servidão)\s+[A-Z][a-zà-ú\s]{3,},\s*\d+'


def redact_pdf(input_path: str, output_path: str, redact_email: bool, redact_cpf: bool, redact_address: bool, redact_rg: bool, redact_phone: bool):
    """
    Abre um arquivo PDF e aplica a redação baseada nos argumentos booleanos.
    
    :param input_path: Caminho para o arquivo PDF de entrada.
    :param output_path: Caminho para o arquivo PDF de saída redigido.
    :param redact_email: Se emails devem ser redigidos.
    :param redact_cpf: Se CPFs devem ser redigidos.
    :param redact_address: Se endereços (incluindo CEP) devem ser redigidos.
    :param redact_rg: Se números de RG devem ser redigidos.
    :param redact_phone: Se números de telefone/celular devem ser redigidos.
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
        pii_patterns_to_use.append((REGEX_PHONE, "TELEFONE")) # NOVO
        
    if redact_address:
        # Endereços usam dois padrões (o termo e o CEP)
        pii_patterns_to_use.append((REGEX_ADDRESS_TERMS, "ENDEREÇO"))
        pii_patterns_to_use.append((REGEX_CEP, "CEP"))


    if not pii_patterns_to_use:
        print("Aviso: Nenhuma opção de redação selecionada na função.")
        
    try:
        doc = fitz.open(input_path)
    except Exception as e:
        raise IOError(f"Não foi possível abrir o PDF: {e}")

    # Itera por todas as páginas
    for page in doc:
        redact_areas = []
        text = page.get_text("text")

        # 2. Buscar por padrões de PII ativados
        for pattern, pii_type in pii_patterns_to_use:
            
            # re.finditer busca todas as ocorrências do padrão no texto da página
            for match in re.finditer(pattern, text, re.IGNORECASE):
                matching_text = match.group(0)
                
                # Encontrar os retângulos (Rects) para o texto encontrado
                rects = page.search_for(matching_text) 
                
                for rect in rects:
                    redact_areas.append(rect)
                        
        # 3. Adicionar e Aplicar Redações
        for rect in redact_areas:
            # Marca a área para remoção com uma caixa preta (0, 0, 0)
            page.add_redact_annot(rect, fill=(0, 0, 0))

        # Remove fisicamente o texto e transforma as anotações em caixas pretas
        page.apply_redactions()

    # 4. Salvar o PDF redigido
    doc.save(output_path, garbage=4, deflate=True)
    doc.close()
