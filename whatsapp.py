import urllib.parse

def preparar_link_whatsapp(texto):
    # Formata o texto para ser enviado via URL do WhatsApp
    return f"https://wa.me/?text={urllib.parse.quote(texto)}"
