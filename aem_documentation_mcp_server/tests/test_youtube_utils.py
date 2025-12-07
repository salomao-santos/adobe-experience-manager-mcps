# Copyright 2024-2025 Salomão Santos
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
"""Tests for YouTube utilities."""

import pytest
from aemlabs.aem_documentation_mcp_server.youtube_utils import (
    extract_video_id,
    is_youtube_url,
    get_youtube_transcript_url,
)


class TestExtractVideoId:
    """Tests for extract_video_id function."""

    def test_youtube_watch_url(self):
        """Test extracting video ID from youtube.com/watch URL."""
        url = 'https://www.youtube.com/watch?v=nJ8QTNQEkD8'
        video_id = extract_video_id(url)
        assert video_id == 'nJ8QTNQEkD8'

    def test_youtube_watch_url_with_params(self):
        """Test extracting video ID from youtube.com/watch URL with extra params."""
        url = 'https://www.youtube.com/watch?v=abc123&t=10s&list=PLxyz'
        video_id = extract_video_id(url)
        assert video_id == 'abc123'

    def test_youtube_embed_url(self):
        """Test extracting video ID from youtube.com/embed URL."""
        url = 'https://www.youtube.com/embed/xyz789'
        video_id = extract_video_id(url)
        assert video_id == 'xyz789'

    def test_youtube_v_url(self):
        """Test extracting video ID from youtube.com/v URL."""
        url = 'https://www.youtube.com/v/def456'
        video_id = extract_video_id(url)
        assert video_id == 'def456'

    def test_youtu_be_url(self):
        """Test extracting video ID from youtu.be URL."""
        url = 'https://youtu.be/ghi012'
        video_id = extract_video_id(url)
        assert video_id == 'ghi012'

    def test_youtu_be_url_with_params(self):
        """Test extracting video ID from youtu.be URL with params."""
        url = 'https://youtu.be/jkl345?t=30'
        video_id = extract_video_id(url)
        assert video_id == 'jkl345'

    def test_youtube_without_www(self):
        """Test extracting video ID from youtube.com URL without www."""
        url = 'https://youtube.com/watch?v=mno678'
        video_id = extract_video_id(url)
        assert video_id == 'mno678'

    def test_invalid_youtube_url(self):
        """Test extracting video ID from invalid YouTube URL."""
        url = 'https://www.youtube.com/user/someuser'
        video_id = extract_video_id(url)
        assert video_id is None

    def test_non_youtube_url(self):
        """Test extracting video ID from non-YouTube URL."""
        url = 'https://vimeo.com/123456789'
        video_id = extract_video_id(url)
        assert video_id is None


class TestIsYoutubeUrl:
    """Tests for is_youtube_url function."""

    def test_youtube_com_url(self):
        """Test detecting youtube.com URL."""
        assert is_youtube_url('https://www.youtube.com/watch?v=test') is True

    def test_youtube_com_without_www(self):
        """Test detecting youtube.com URL without www."""
        assert is_youtube_url('https://youtube.com/watch?v=test') is True

    def test_youtu_be_url(self):
        """Test detecting youtu.be URL."""
        assert is_youtube_url('https://youtu.be/test') is True

    def test_youtu_be_with_www(self):
        """Test detecting youtu.be URL with www."""
        assert is_youtube_url('https://www.youtu.be/test') is True

    def test_non_youtube_url(self):
        """Test detecting non-YouTube URL."""
        assert is_youtube_url('https://vimeo.com/123') is False

    def test_adobe_url(self):
        """Test detecting Adobe URL."""
        assert is_youtube_url('https://experienceleague.adobe.com/docs') is False


class TestGetYoutubeTranscriptUrl:
    """Tests for get_youtube_transcript_url function."""

    def test_get_transcript_url(self):
        """Test generating transcript URL from video ID."""
        url = get_youtube_transcript_url('abc123')
        assert url == 'https://www.youtube.com/watch?v=abc123'

    def test_get_transcript_url_empty_id(self):
        """Test generating transcript URL with empty video ID."""
        url = get_youtube_transcript_url('')
        assert url == 'https://www.youtube.com/watch?v='
