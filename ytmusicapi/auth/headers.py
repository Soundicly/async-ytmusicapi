import orjson
import os
from typing import Dict, Optional

import aiohttp
from requests.structures import CaseInsensitiveDict

from ytmusicapi.auth.browser import is_browser
from ytmusicapi.auth.oauth import YTMusicOAuth, is_oauth, is_custom_oauth
from ytmusicapi.helpers import initialize_headers


def load_headers_file(auth: str) -> Dict:
    if os.path.isfile(auth):
        with open(auth) as json_file:
            input_json = orjson.loads(json_file.read())
    else:
        input_json = orjson.loads(auth)

    return input_json


async def prepare_headers(
    session: aiohttp.ClientSession,
    proxy: Optional[str] = None,
    input_dict: Optional[CaseInsensitiveDict] = None,
) -> Dict:
    if input_dict:

        if is_oauth(input_dict):
            oauth = YTMusicOAuth(session, proxy)
            headers = await oauth.load_headers(dict(input_dict), input_dict['filepath'])

        elif is_browser(input_dict):
            headers = input_dict

        elif is_custom_oauth(input_dict):
            headers = input_dict

        else:
            raise Exception(
                "Could not detect credential type. "
                "Please ensure your oauth or browser credentials are set up correctly.")

    else:  # no authentication
        headers = initialize_headers()

    return headers
