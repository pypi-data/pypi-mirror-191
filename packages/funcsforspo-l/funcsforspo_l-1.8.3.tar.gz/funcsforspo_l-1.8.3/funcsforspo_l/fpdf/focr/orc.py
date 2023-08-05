"""
    ## DIREITOS RESERVADOS / RIGHTS RESERVED / DERECHOS RESERVADOS

    ## https://online2pdf.com/pt/converter-pdf-para-txt-com-ocr

    Esse robô envia o PDF para o site https://online2pdf.com/pt/converter-pdf-para-txt-com-ocr
        e recupera um arquivo txt com o ocr
    
    Args:
        file_pdf (str): Caminho do arquivo
        dir_exit (str, optional): Local de saída do arquivo TXT. Defaults to `'output'`.
        get_text_into_code (bool, optional): Retorna o texto do pdf no código. Defaults to True.
        headless (bool, optional): executa como headless. Defaults to `True`.
        prints (bool, optional): Mostra o acompanhamento do OCR. Defaults to `True`.
        
    Use:
        >>> text = faz_ocr_em_pdf('MyPDF.pdf')
        >>> print(text)
        
    """
from __future__ import annotations
from funcsforspo_l.fpdf.focr.__ocr_online import GetTextPDF
from funcsforspo_l.fpython.functions_for_py import *

def faz_ocr_em_pdf(file_pdf: str, dir_exit: str='output', get_text_into_code: bool=True, headless: bool=True, prints=False) -> str:
    """
    ## DIREITOS RESERVADOS / RIGHTS RESERVED / DERECHOS RESERVADOS

    ## https://online2pdf.com/pt/converter-pdf-para-txt-com-ocr

    Esse robô envia o PDF para o site https://online2pdf.com/pt/converter-pdf-para-txt-com-ocr
        e recupera um arquivo txt com o ocr
    
    Args:
        file_pdf (str): Caminho do arquivo
        dir_exit (str, optional): Local de saída do arquivo TXT. Defaults to `'output'`.
        get_text_into_code (bool, optional): Retorna o texto do pdf no código. Defaults to True.
        headless (bool, optional): executa como headless. Defaults to `True`.
        prints (bool, optional): Mostra o acompanhamento do OCR. Defaults to `True`.
        
    Use:
        >>> text = faz_ocr_em_pdf('MyPDF.pdf')
        >>> print(text)
        
    """
    
    bot = GetTextPDF(file_pdf=file_pdf, dir_exit=dir_exit, get_text_into_code=get_text_into_code, headless=headless, prints=prints)
    if get_text_into_code:
        return bot.recupera_texto()

def faz_ocr_em_pdf_offline(path_pdf: str, export_from_file_txt: str=False) -> str:
    """Converte pdf(s) em texto com pypdf
    
    ### pip install pypdf
    
    ## Atenção, só funciona corretamente em PDF's que o texto é selecionável!
    
    Use:
        ...
    
    Args:
        path_pdf (str): caminho do pdf
        export_from_file_txt (bool | str): passar um caminho de arquivo txt para o texto sair

    Returns:
        str: texto do PDF
    """
    
    text = []
    from pypdf import PdfReader

    reader = PdfReader(path_pdf)
    pages = reader.pages
    for page in pages:
        text.append(page.extract_text())
    else:
        text = transforma_lista_em_string(text)
        
        if export_from_file_txt:
            with open('extraction_pdf.txt', 'w', encoding='utf-8') as f:
                f.write(text)
        return text
