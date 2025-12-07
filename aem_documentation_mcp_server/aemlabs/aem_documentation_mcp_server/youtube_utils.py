# Copyright 2024-2025 Salomão Santos (salomaosantos777@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""YouTube utilities for extracting video transcripts."""

import re
from typing import Optional
from urllib.parse import parse_qs, urlparse


def extract_video_id(url: str) -> Optional[str]:
    """Extract YouTube video ID from URL.

    Args:
        url: YouTube URL

    Returns:
        Video ID if found, None otherwise
    """
    # Parse URL
    parsed = urlparse(url)

    # youtube.com/watch?v=VIDEO_ID
    if parsed.netloc in ['www.youtube.com', 'youtube.com']:
        if parsed.path == '/watch':
            query = parse_qs(parsed.query)
            return query.get('v', [None])[0]
        # youtube.com/embed/VIDEO_ID
        elif parsed.path.startswith('/embed/'):
            return parsed.path.split('/')[2]
        # youtube.com/v/VIDEO_ID
        elif parsed.path.startswith('/v/'):
            return parsed.path.split('/')[2]

    # youtu.be/VIDEO_ID
    elif parsed.netloc in ['youtu.be', 'www.youtu.be']:
        return parsed.path.lstrip('/')

    return None


def get_youtube_transcript_url(video_id: str) -> str:
    """Get YouTube video page URL for transcript extraction.

    Args:
        video_id: YouTube video ID

    Returns:
        YouTube video URL
    """
    return f'https://www.youtube.com/watch?v={video_id}'


def extract_transcript_from_html(html: str) -> Optional[str]:
    """Extract transcript from YouTube HTML page.

    This attempts to extract captions/subtitles from the YouTube page HTML.
    Note: This is a basic implementation and may not work for all videos.

    Args:
        html: Raw HTML from YouTube video page

    Returns:
        Transcript text if found, None otherwise
    """
    try:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, 'html.parser')

        # Try to find transcript in various locations
        # YouTube embeds transcript data in JSON within script tags
        scripts = soup.find_all('script')

        for script in scripts:
            if script.string and 'captionTracks' in script.string:
                # This is a simplified approach
                # In production, you'd want to properly parse the JSON
                # and extract the caption URL, then fetch and parse the captions
                return 'Transcript extraction from YouTube requires additional parsing. Video ID found in page.'

        return None

    except Exception:
        return None


def is_youtube_url(url: str) -> bool:
    """Check if URL is a YouTube URL.

    Args:
        url: URL to check

    Returns:
        True if YouTube URL, False otherwise
    """
    parsed = urlparse(url)
    return parsed.netloc in [
        'www.youtube.com',
        'youtube.com',
        'youtu.be',
        'www.youtu.be',
        'm.youtube.com',
    ]
