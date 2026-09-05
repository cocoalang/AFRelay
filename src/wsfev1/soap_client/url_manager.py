import os

# Environment is selected with the ARCA_ENV variable (set in .env, passed through
# docker-compose.yml): "production" selects ARCA production, anything else (or unset)
# selects testing/homologation. Kept as an env var instead of a hardcoded flag so that
# switching environment stays an operational task and not a code change.
IS_WSFE_PRODUCTION = os.getenv("ARCA_ENV", "").strip().lower() == "production"

def get_wsfe_url() -> str:
    if IS_WSFE_PRODUCTION:
        return "https://servicios1.afip.gov.ar/wsfev1/service.asmx"
    else:
        return "https://wswhomo.afip.gov.ar/wsfev1/service.asmx"
