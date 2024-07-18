# youtube_video_downloader.py

import os
import re
import string
from pytube import cipher
from pytube import YouTube
from pytube.exceptions import VideoUnavailable

from pytube.innertube import _default_clients

_default_clients[ "ANDROID"][ "context"]["client"]["clientVersion"] = "19.08.35" 
_default_clients["IOS"]["context"]["client"]["clientVersion"] = "19.08.35" 
_default_clients[ "ANDROID_EMBED"][ "context"][ "client"]["clientVersion"] = "19.08.35" 
_default_clients[ "IOS_EMBED"][ "context"]["client"]["clientVersion"] = "19.08.35" 
_default_clients["IOS_MUSIC"][ "context"]["client"]["clientVersion"] = "6.41" 
_default_clients[ "ANDROID_MUSIC"] = _default_clients[ "ANDROID_CREATOR" ]


def get_throttling_function_name(js: str) -> str:
    """Extract the name of the function that computes the throttling parameter.

    :param str js:
        The contents of the base.js asset file.
    :rtype: str
    :returns:
        The name of the function used to compute the throttling parameter.
    """
    function_patterns = [
        r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&\s*'
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])?\([a-z]\)',
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])\([a-z]\)',
    ]
    #logger.debug('Finding throttling function name')
    for pattern in function_patterns:
        regex = re.compile(pattern)
        function_match = regex.search(js)
        if function_match:
            #logger.debug("finished regex search, matched: %s", pattern)
            if len(function_match.groups()) == 1:
                return function_match.group(1)
            idx = function_match.group(2)
            if idx:
                idx = idx.strip("[]")
                array = re.search(
                    r'var {nfunc}\s*=\s*(\[.+?\]);'.format(
                        nfunc=re.escape(function_match.group(1))),
                    js
                )
                if array:
                    array = array.group(1).strip("[]").split(",")
                    array = [x.strip() for x in array]
                    return array[int(idx)]

    raise cipher.RegexMatchError(
        caller="get_throttling_function_name", pattern="multiple"
    )

cipher.get_throttling_function_name = get_throttling_function_name


special_chars = "!@#$%^&*()+={}[]|\\:;\"'<>,.?/"
trans_table = str.maketrans(dict.fromkeys(special_chars, "-"))


def download_videos(video_urls, download_path):
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    for url in video_urls:
        try:
            yt = YouTube(url)
            title = yt.title.translate(trans_table)+'.mp4'
            # Sélectionne le flux vidéo avec la meilleure résolution
            stream = yt.streams.get_highest_resolution()
            print(f"Downloading: {title} from {url}")
            stream.download(output_path=download_path, filename=title)
            print(f"Downloaded: {title}")
        except VideoUnavailable:
            print(f"Video unavailable: {url}")
        except Exception as e:
            print(f"Failed to download from {url}: {e}")

if __name__ == "__main__":
    # Liste d'URLs de vidéos YouTube
    video_urls = [
    "https://www.youtube.com/watch?v=wR6lRmUNCZc",
    "https://www.youtube.com/watch?v=86ZQA-WP_CE",
    ]
    download_path = './videos_YouTube'
    
    download_videos(video_urls, download_path)
