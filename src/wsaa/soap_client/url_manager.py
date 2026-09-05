
import os

# Environment is selected with the ARCA_ENV variable (set in .env, passed through
# docker-compose.yml): "production" selects ARCA production, anything else (or unset)
# selects testing/homologation. Kept as an env var instead of a hardcoded flag so that
# switching environment stays an operational task and not a code change.
IS_WSAA_PRODUCTION = os.getenv("ARCA_ENV", "").strip().lower() == "production"

def get_wsaa_url() -> str:
    if IS_WSAA_PRODUCTION:
        return "https://wsaa.afip.gov.ar/ws/services/LoginCms"
    else:
        return "https://wsaahomo.afip.gov.ar/ws/services/LoginCms"
