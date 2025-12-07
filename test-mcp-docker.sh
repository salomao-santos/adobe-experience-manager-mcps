#!/bin/bash
# Test script for AEM Documentation MCP Server

echo "=== Testing AEM Documentation MCP Server via Docker ==="
echo ""

# Test 1: Initialize
echo "Test 1: Initializing MCP Server..."
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{"roots":{"listChanged":true},"sampling":{}},"clientInfo":{"name":"test-client","version":"1.0.0"}}}' | timeout 3 docker run --rm -i aem-docs-mcp-server:latest 2>/dev/null | head -1
echo ""

# Test 2: List tools (in a new container, needs initialization)
echo "Test 2: Listing available tools..."
(
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{"roots":{"listChanged":true},"sampling":{}},"clientInfo":{"name":"test-client","version":"1.0.0"}}}'
sleep 0.5
echo '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'
) | timeout 5 docker run --rm -i aem-docs-mcp-server:latest 2>/dev/null | grep -A 50 '"method":"tools/list"' | head -20
echo ""

# Test 3: Get available services
echo "Test 3: Getting available services..."
(
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{"roots":{"listChanged":true},"sampling":{}},"clientInfo":{"name":"test-client","version":"1.0.0"}}}'
sleep 0.5
echo '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_available_services","arguments":{}}}'
) | timeout 5 docker run --rm -i aem-docs-mcp-server:latest 2>/dev/null | grep -A 30 'AEM Assets' | head -15
echo ""

echo "=== Docker Image Info ==="
docker images | grep aem-docs-mcp-server
echo ""

echo "=== Test Complete ==="
echo "MCP Server is ready to use with GitHub Copilot!"
echo "Configuration file: .github/copilot-instructions.json"
