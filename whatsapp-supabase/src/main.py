import logging
import os
from dotenv import load_dotenv
from contacts import fetch_contacts
from zapi import ZApiClient

def setup_logging() -> None:
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=level,
        format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
    )

def render_template(template: str, nome: str) -> str:
    return template.replace("{{nome_contato}}", nome)

def main() -> None:
    load_dotenv()
    setup_logging()
    log = logging.getLogger("runner")
    log.info("Buscando contatos no Supabase...")
    contacts = fetch_contacts(limit=3)
    if not contacts:
        log.error("Nenhum contato encontrado na tabela 'contacts'.")
        raise SystemExit(1)

    template = "Olá, {{nome_contato}}! Mensagem enviada via integração Python + Supabase + Z-API. 🚀"

    zapi = ZApiClient()
    sent = 0
    for c in contacts:
        msg = render_template(template, c["nome"])
        try:
            status = zapi.send_text(c["phone_e164"], msg)
            log.info("Enviado para %s (%s): %s", c["nome"], c["phone_e164"], status)
            if status == "SENT":
                sent += 1
        except Exception as e:
            log.exception("Falha ao enviar para %s (%s): %s", c["nome"], c["phone_e164"], e)

    log.info("Resumo: %d/%d mensagens enviadas com sucesso.", sent, len(contacts))

if __name__ == "__main__":
    main()
