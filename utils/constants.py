import pathlib
import uuid
from urllib.parse import urlparse

from django.conf import settings


def get_extension_from_url(url: str):
    results = urlparse(url)
    filename = results.path.split("/")[-1]
    extension = pathlib.Path(filename).suffixes[-1]
    return extension


def get_file_path(url):
    destination = settings.MEDIA_URL + str(uuid.uuid4())
    extension = get_extension_from_url(url)
    file_path = destination+extension
    return file_path


user_agent_list = [
    'Mozilla/5.0 (Linux; Android 9; Mi A1 Build/PKQ1.180917.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.87 Mobile Safari/537.36 Viber/13.2.0.8',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.1047.0 Safari/537.36 Edg/96.0.1047.0',
    'Mozilla/5.0 (Linux; Android 8.0.0; SM-G611MT) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.116 Mobile Safari/537.36',
    'Mozilla/5.0 (Android 7.1.2; Mobile; rv:68.2.0) Gecko/68.2.0 Firefox/68.2.0',
    'Dalvik/2.1.0 (Linux; U; Android 6.0.1; SM-N915K Build/MMB29K)',
    'Mozilla/5.0 (Linux; Android 5.1.1; SM-J700H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.93 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; SH-02M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.66 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; SM-A107M Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 Mobile Safari/537.36',
    'Dalvik/2.1.0 (Linux; U; Android 6.0.1; HTC Desire 825 Build/MMB29M)',
    'Mozilla/5.0 (Linux; Android 9; W-P611-EEA) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.96 Mobile Safari/537.36'
]
