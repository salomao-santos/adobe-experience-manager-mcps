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

"""Tests for models module."""

import pytest

from aemlabs.aem_documentation_mcp_server.models import (
    DocumentationResult,
    ServiceInfo,
)


class TestDocumentationResult:
    """Tests for DocumentationResult model."""

    def test_documentation_result_creation(self):
        """Test creating a DocumentationResult."""
        result = DocumentationResult(
            url='https://example.com',
            content='Test content',
            content_length=12,
            title='Test Title',
        )
        
        assert result.url == 'https://example.com'
        assert result.content == 'Test content'
        assert result.title == 'Test Title'
        assert result.content_length == 12

    def test_documentation_result_with_metadata(self):
        """Test DocumentationResult without optional fields."""
        result = DocumentationResult(
            url='https://example.com',
            content='Test content',
            content_length=12,
        )
        
        assert result.content_length == 12
        assert result.title is None


class TestServiceInfo:
    """Tests for ServiceInfo model."""

    def test_service_info_creation(self):
        """Test creating a ServiceInfo."""
        service = ServiceInfo(
            name='Test Service',
            url='https://example.com',
            description='Test description',
            category='cloud-service',
        )
        
        assert service.name == 'Test Service'
        assert service.url == 'https://example.com'
        assert service.description == 'Test description'
        assert service.category == 'cloud-service'

    def test_service_info_validation(self):
        """Test ServiceInfo validation."""
        # Should not raise error for valid data
        service = ServiceInfo(
            name='Valid Name',
            url='https://valid.url',
            description='Valid description',
            category='apis',
        )
        assert service is not None
