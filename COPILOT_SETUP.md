# GitHub Copilot MCP Configuration

Este projeto está configurado para usar o MCP Server de Documentação AEM com o GitHub Copilot.

## Configuração Automática

O servidor MCP está configurado em `.github/copilot-instructions.json` com **duas opções de execução**:

1. **UVX (Ativo por padrão)** - Execução via Python/UV
2. **Docker (Desativado)** - Execução via container Docker

## Escolhendo o Modo de Execução

### Opção 1: UVX (Recomendado) ✅

**Pré-requisitos:**
- Instale `uv`: https://docs.astral.sh/uv/getting-started/installation/
- Python 3.10+ será instalado automaticamente pelo `uv`

**Vantagens:**
- ✅ Mais rápido (sem overhead de container)
- ✅ Menor uso de memória
- ✅ Atualizações automáticas via `@latest`
- ✅ Não requer Docker instalado

**Já está ativo!** Veja `.github/copilot-instructions.json`

### Opção 2: Docker

**Pré-requisitos:**
- Docker instalado e em execução
- Build da imagem: `cd aem_documentation_mcp_server && docker build -t aem-docs-mcp-server:latest .`

**Para ativar Docker:**
Edite `.github/copilot-instructions.json` e troque os valores de `disabled` entre as duas configurações.

## Configuração Manual (VS Code Settings)

Se preferir configurar manualmente no VS Code:

1. Abra o VS Code
2. Pressione `Ctrl+Shift+P` (ou `Cmd+Shift+P` no Mac)
3. Digite "Preferences: Open User Settings (JSON)"
4. Adicione a seguinte configuração:

**Para UVX:**

```json
{
  "github.copilot.chat.mcp.enabled": true,
  "github.copilot.chat.mcp.servers": {
    "aem-documentation-uvx": {
      "command": "uvx",
      "args": ["aemlabs.aem-documentation-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      }
    }
  }
}
```

**Para Docker:**

```json
{
  "github.copilot.chat.mcp.enabled": true,
  "github.copilot.chat.mcp.servers": {
    "aem-documentation-docker": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "aem-docs-mcp-server:latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      }
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

1. Abra o GitHub Copilot Chat no VS Code
2. Digite: `@workspace list available services`
3. O servidor deve retornar uma lista de 30+ serviços AEM

## Instalação de Pré-requisitos

### Para UVX (modo ativo):

```bash
# Instalar uv (escolha um método)
# Linux/macOS:
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell):
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Python será instalado automaticamente quando você executar uvx pela primeira vez
```

### Para Docker (modo alternativo):

```bash
# Construir a imagem Docker
cd aem_documentation_mcp_server
docker build -t aem-docs-mcp-server:latest .

# Verificar a imagem
docker images | grep aem-docs-mcp-server
```

## Troubleshooting

### UVX Mode

**Erro: "uv not found"**
- Instale o `uv` seguindo as instruções acima
- Reinicie o terminal/VS Code após a instalação

**Erro: "MCP server not responding"**
- Verifique se o `uv` está no PATH: `which uv` (Linux/macOS) ou `where uv` (Windows)
- Teste manualmente: `uvx aemlabs.aem-documentation-mcp-server@latest`

### Docker Mode

**Erro: "Image not found"**
- Execute o build da imagem Docker primeiro

**Erro: "Docker not running"**
- Inicie o Docker Desktop ou o daemon do Docker

**Erro: "MCP server not responding"**
- Verifique se o Docker está rodando: `docker ps`
- Verifique os logs: `docker logs <container_id>`

### Geral

**Servidor não aparece no Copilot**
- Reinicie o VS Code completamente
- Verifique se o arquivo `.github/copilot-instructions.json` existe
- Verifique se `"disabled": false` está configurado no modo escolhido
- Verifique as configurações do Copilot: GitHub Copilot → MCP deve estar habilitado

## Recursos Adicionais

- **Documentação:** Veja `README.md` para mais detalhes
- **Configuração:** Arquivo de configuração em `.github/copilot-instructions.json`
- **Performance:** Veja `PERFORMANCE_IMPROVEMENTS.md` para otimizações aplicadas
