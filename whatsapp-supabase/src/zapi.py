from typing import Literal, Optional
import os, httpx, json
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

ZStatus = Literal["SENT", "ERROR"]

class ZApiClient:
    def __init__(self) -> None:
        base = os.getenv("ZAPI_BASE_URL", "https://api.z-api.io").rstrip("/")
        instance = os.environ["ZAPI_INSTANCE"]
        token = os.environ["ZAPI_TOKEN"]
        # Aceita base completa ou só domínio
        if "/instances/" in base and "/token/" in base:
            self.url = base
        else:
            self.url = f"{base}/instances/{instance}/token/{token}/send-text"

        self.client_token: Optional[str] = os.getenv("ZAPI_CLIENT_TOKEN") or None
        self._client = httpx.Client(timeout=20)

    @retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, max=4),
        retry=retry_if_exception_type(httpx.HTTPError),
    )
    def send_text(self, phone_e164: str, message: str) -> ZStatus:
        headers = {}
        if self.client_token:
            headers["Client-Token"] = self.client_token  # header exigido se segurança estiver ativa

        payload = {"phone": phone_e164, "message": message}
        r = self._client.post(self.url, json=payload, headers=headers)

        # Se a Z-API devolver 4xx/5xx, capturamos o corpo para diagnóstico
        if r.status_code >= 400:
            try:
                detail = r.json()
            except Exception:
                detail = {"raw": r.text}
            # Anexe a mensagem detalhada à exceção HTTP
            raise httpx.HTTPStatusError(
                f"{r.status_code} while calling Z-API: {json.dumps(detail, ensure_ascii=False)}",
                request=r.request,
                response=r,
            )

        # 2xx: interpretar sucesso
        try:
            data = r.json()
        except Exception:
            return "ERROR"

        ok = bool(
            data.get("sent")
            or data.get("success")
            or data.get("queueNumber")
            or data.get("messageId")
            or data.get("zaapId")
        )
        return "SENT" if ok else "ERROR"
