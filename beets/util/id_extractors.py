# This file is part of beets.
# Copyright 2016, Adrian Sampson.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

"""Helpers around the extraction of album/track ID's from metadata sources."""

import re

# Spotify IDs consist of 22 alphanumeric characters
# (zero-left-padded base62 representation of randomly generated UUID4)
spotify_id_regex = {
    "pattern": r"(^|open\.spotify\.com/{}/)([0-9A-Za-z]{{22}})",
    "match_group": 2,
}

deezer_id_regex = {
    "pattern": r"(^|deezer\.com/)([a-z]*/)?({}/)?(\d+)",
    "match_group": 4,
}

beatport_id_regex = {
    "pattern": r"(^|beatport\.com/(?:track|release)/.+/)(\d+)(?:$|/)",
    "match_group": 2,
}

# A note on Bandcamp: There is no such thing as a Bandcamp album or artist ID,
# the URL can be used as the identifier. The Bandcamp metadata source plugin
# works that way - https://github.com/snejus/beetcamp. Bandcamp album
# URLs usually look like: https://nameofartist.bandcamp.com/album/nameofalbum


def extract_discogs_id_regex(album_id):
    """Returns the Discogs_id or None."""
    # Discogs-IDs are simple integers. In order to avoid confusion with
    # other metadata plugins, we only look for very specific formats of the
    # input string:
    # - plain integer, optionally wrapped in brackets and prefixed by an
    #   'r', as this is how discogs displays the release ID on its webpage.
    # - legacy url format: discogs.com/<name of release>/release/<id>
    # - legacy url short format: discogs.com/release/<id>
    # - current url format: discogs.com/release/<id>-<name of release>
    # See #291, #4080 and #4085 for the discussions leading up to these
    # patterns.
    # Regex has been tested here https://regex101.com/r/TOu7kw/1

    for pattern in [
        r"^\[?r?(?P<id>\d+)\]?$",
        r"discogs\.com/release/(?P<id>\d+)-?",
        r"discogs\.com/[^/]+/release/(?P<id>\d+)",
    ]:
        match = re.search(pattern, album_id)
        if match:
            return int(match.group("id"))

    return None

# Lifted from https://gist.github.com/rodrigoborgesdeoliveira/987683cfbfcc8d800192da1e73adc486
def get_youtube_video_id_by_url(url):
    regex = r"^((https?://(?:www\.)?(?:m\.)?youtube\.com))/((?:oembed\?url=https?%3A//(?:www\.)youtube.com/watch\?(?:v%3D)(?P<video_id_1>[\w\-]{10,20})&format=json)|(?:attribution_link\?a=.*watch(?:%3Fv%3D|%3Fv%3D)(?P<video_id_2>[\w\-]{10,20}))(?:%26feature.*))|(https?:)?(\/\/)?((www\.|m\.)?youtube(-nocookie)?\.com\/((watch)?\?(app=desktop&)?(feature=\w*&)?v=|embed\/|v\/|e\/)|youtu\.be\/)(?P<video_id_3>[\w\-]{10,20})"
    match = re.match(regex, url, re.IGNORECASE)
    if match:
        return (
            match.group("video_id_1")
            or match.group("video_id_2")
            or match.group("video_id_3")
        )
    else:
        return None