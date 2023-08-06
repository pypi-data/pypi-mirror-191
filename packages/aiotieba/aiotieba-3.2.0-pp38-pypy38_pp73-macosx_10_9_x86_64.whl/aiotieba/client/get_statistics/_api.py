from typing import Dict, List

import yarl

from .._core import HttpCore
from .._helper import pack_form_request, parse_json, send_request
from ..const import APP_BASE_HOST, APP_SECURE_SCHEME
from ..exception import TiebaServerError

field_names = [
    'view',
    'thread',
    'new_member',
    'post',
    'sign_ratio',
    'average_time',
    'average_times',
    'recommend',
]


def null_ret_factory() -> Dict[str, List[int]]:
    return {field_name: [] for field_name in field_names}


def parse_body(body: bytes) -> Dict[str, List[int]]:
    res_json = parse_json(body)
    if code := int(res_json['error_code']):
        raise TiebaServerError(code, res_json['error_msg'])

    data = res_json['data']
    stat = {
        field_name: [int(item['value']) for item in reversed(data_i['group'][1]['values'])]
        for field_name, data_i in zip(field_names, data)
    }

    return stat


async def request(http_core: HttpCore, fid: int) -> Dict[str, List[int]]:
    data = [
        ('BDUSS', http_core.core._BDUSS),
        ('_client_version', http_core.core.main_version),
        ('forum_id', fid),
    ]

    request = pack_form_request(
        http_core,
        yarl.URL.build(scheme=APP_SECURE_SCHEME, host=APP_BASE_HOST, path="/c/f/forum/getforumdata"),
        data,
    )

    __log__ = "fid={fid}"  # noqa: F841

    body = await send_request(request, http_core.connector, read_bufsize=4 * 1024)
    return parse_body(body)
