# GitHub Copilot MCP Configuration

Este projeto está configurado para usar o MCP Server de Documentação AEM com o GitHub Copilot.

## Configuração Automática

O servidor MCP está configurado em `.github/copilot-instructions.json` e será carregado automaticamente pelo GitHub Copilot quando você abrir este projeto.

## Configuração Manual (Alternativa)

Se preferir configurar manualmente:

1. Abra o VS Code
2. Pressione `Ctrl+Shift+P` (ou `Cmd+Shift+P` no Mac)
3. Digite "Preferences: Open User Settings (JSON)"
4. Adicione a seguinte configuração:

```json
{
  "github.copilot.chat.mcp.enabled": true,
  "github.copilot.chat.mcp.servers": {
    "aem-documentation": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "aem-docs-mcp-server:latest"
      ]
    }
  }
}
```

## Usando o MCP Server

Depois de configurado, você pode usar o servidor MCP no GitHub Copilot Chat:

### Ferramentas Disponíveis

1. **read_documentation** - Lê e converte documentação AEM para Markdown
   ```
   @workspace Leia a documentação de https://experienceleague.adobe.com/docs/experience-manager-cloud-service/content/assets/overview.html
   ```

2. **search_experience_league** - Busca na Adobe Experience League
   ```
   @workspace Busque tutoriais sobre AEM Assets
   ```

3. **get_available_services** - Lista serviços AEM disponíveis
   ```
   @workspace Quais serviços AEM estão disponíveis?
   ```

## Testando a Configuração

Para verificar se o MCP server está funcionando:

1. Abra o GitHub Copilot Chat
2. Digite: `@workspace list available services`
3. O servidor deve retornar uma lista de 30+ serviços AEM

## Construindo a Imagem Docker

Se você ainda não construiu a imagem Docker:

```bash
cd aem_documentation_mcp_server
docker build -t aem-docs-mcp-server:latest .
```

## Verificando a Imagem

```bash
docker images | grep aem-docs-mcp-server
```

## Testando o Servidor Diretamente

```bash
# Testar se o servidor está funcionando
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | docker run --rm -i aem-docs-mcp-server:latest
```

## Troubleshooting

### Erro: "Image not found"
- Execute o build da imagem Docker primeiro

### Erro: "MCP server not responding"
- Verifique se o Docker está rodando
- Verifique os logs: `docker logs <container_id>`

### Servidor não aparece no Copilot
- Reinicie o VS Code
- Verifique as configurações do Copilot
- Verifique se MCP está habilitado nas configurações

## Recursos Adicionais

- **Documentação:** Veja `README.md` para mais detalhes
- **Configuração:** Arquivo de configuração em `.github/copilot-instructions.json`
- **Performance:** Veja `PERFORMANCE_IMPROVEMENTS.md` para otimizações aplicadas
