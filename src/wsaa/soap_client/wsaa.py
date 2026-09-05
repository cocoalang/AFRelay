import logging
from builtins import ConnectionResetError

import httpx
from tenacity import (before_sleep_log, retry, retry_if_exception_type,
                      stop_after_attempt, wait_fixed)

from src.shared.utils.arca_ssl import build_arca_ssl_context
from src.shared.utils.logger import logger
from src.shared.utils.response_management import build_error_response
from src.wsaa.soap_client.url_manager import get_wsaa_url


@retry(
        retry=retry_if_exception_type(( ConnectionResetError, httpx.ConnectError, httpx.TimeoutException )),
        stop=stop_after_attempt(3),
        wait=wait_fixed(0.5),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
async def consult_afip_wsaa(xml: str, client=None) -> dict:

    if client is None:
        client = httpx.AsyncClient(timeout=30.0, verify=build_arca_ssl_context())

    url = get_wsaa_url()
    headers = {
        'Content-Type': 'text/xml; charset=utf-8',
        'SOAPAction': ""
    }

    try:
        response = await client.post(url, content=xml, headers=headers)
        response.raise_for_status()
        
        return {
            "status" : "success",
            "response" : response.text
            }

    except httpx.HTTPStatusError as e:
        return build_error_response("LoginCms", "HTTP Error", str(e))

    except (httpx.ConnectError, httpx.TimeoutException) as e:
        return build_error_response("LoginCms", "Network error", str(e))
    
    except Exception as e:
        logger.error(f"General exception in LoginCms: {e}")
        return build_error_response("LoginCms", "unknown", str(e))

    finally:
        await client.aclose()
