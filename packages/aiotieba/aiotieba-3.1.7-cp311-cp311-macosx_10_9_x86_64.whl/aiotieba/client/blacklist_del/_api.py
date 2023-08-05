import sys

import yarl

from .._core import WEB_BASE_HOST, HttpCore
from .._helper import log_exception, log_success, pack_web_form_request, parse_json, send_request
from ..exception import TiebaServerError


def parse_body(body: bytes) -> None:
    res_json = parse_json(body)
    if code := res_json['errno']:
        raise TiebaServerError(code, res_json['errmsg'])


async def request(http_core: HttpCore, fname: str, user_id: int) -> bool:
    data = [
        ('word', fname),
        ('tbs', http_core.core._tbs),
        ('list[]', user_id),
        ('ie', 'utf-8'),
    ]

    request = pack_web_form_request(
        http_core,
        yarl.URL.build(scheme="http", host=WEB_BASE_HOST, path="/bawu2/platform/cancelBlack"),
        data,
    )

    log_str = f"fname={fname} user_id={user_id}"
    frame = sys._getframe(1)

    try:
        body = await send_request(request, http_core.connector, read_bufsize=2 * 1024)
        parse_body(body)

    except Exception as err:
        log_exception(frame, err, log_str)
        return False

    log_success(frame, log_str)
    return True
