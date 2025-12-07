# Configuração de Servidores MCP Adobe e AWS para Kiro

## Resumo

Este guia configura **6 servidores MCP** no Kiro para acesso a documentação Adobe AEM, AWS, processamento de documentos e pesquisa em repositórios.

**Total de MCPs configurados**: 6 servidores
- **1 servidor Adobe**: AEM Documentation
- **5 servidores AWS**: Documentation, Core, Knowledge, Document Loader e Git Repo Research

---

## Requisitos de Instalação

### Requisitos Obrigatórios

1. **uv** - Gerenciador de pacotes Python rápido
   - Instalação: [Astral](https://docs.astral.sh/uv/getting-started/installation/) ou [GitHub](https://github.com/astral-sh/uv#installation)
   - Comando de instalação: `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - Ou via pip: `pip install uv`
   - Ou via homebrew: `brew install uv`
   - Verificar instalação: `uv --version`

2. **Python 3.10 ou superior** (recomendado: 3.10, 3.11, 3.12 ou 3.13)
   - **Para AEM Documentation MCP**: Python 3.10+ é obrigatório
   - **Para AWS MCPs**: Python 3.12+ é recomendado
   - Instalação via uv: `uv python install 3.10` (ou versão superior)
   - Verificar versão: `python3 --version`

3. **Docker** (opcional - para execução em contêiner)
   - Instalação: [Docker Desktop](https://www.docker.com/products/docker-desktop/)
   - Verificar instalação: `docker --version`
   - **Nota**: Docker é uma alternativa ao uvx para executar os servidores MCP

### Requisitos AWS (Opcionais - apenas para alguns servidores)

1. **AWS CLI configurado** com credenciais que tenham acesso ao Amazon Bedrock
2. **Acesso ao Amazon Bedrock** para modelos de embedding como Titan Embeddings
3. **Variáveis de ambiente AWS**:
   - `AWS_REGION` (exemplo: `us-west-2`)
   - `AWS_PROFILE` (nome do seu perfil AWS)

### Requisitos Opcionais

1. **Token do GitHub** - Para limites de taxa mais altos ao pesquisar repositórios
   - Variável de ambiente: `GITHUB_TOKEN`

---

## Servidores MCP Configurados

> **⚠️ Importante**: O servidor AEM Documentation MCP ainda **não está publicado no PyPI**. Use Docker para desenvolvimento local conforme as instruções abaixo.

## Servidores Adobe

### 1. AEM Documentation MCP Server
**Função**: Acesso à documentação oficial do Adobe Experience Manager (AEM)

**Requisitos Específicos**:
- **Python**: 3.10 ou superior (suporta 3.10, 3.11, 3.12, 3.13)
- **uv**: Versão mais recente
- **Docker** (opcional): Para execução em contêiner

**Recursos**:
- **Busca no Experience League**: Pesquisa na documentação Adobe com filtros avançados (tipo de conteúdo, produtos, funções)
- **Leitura de documentação**: Busca e converte páginas de documentação para formato markdown de:
  - Documentação oficial Adobe (Experience League, Developer, HelpX, Docs)
  - Repositórios GitHub (qualquer organização: Adobe, ACS, Netcentric, etc.)
  - GitHub Pages (sites de documentação *.github.io)
  - Documentação Apache Sling
  - Recursos da conferência adaptTo() (todos os anos: 2011-2025+, incluindo PDFs)
  - Vídeos do YouTube (com orientação de transcrição)
  - Sites corporativos Adobe (Summit, etc.)
- **Serviços disponíveis**: Lista curada de mais de 30 serviços e áreas de documentação AEM
- **Suporte a fragmentos de hash**: Preserva fragmentos de URL para páginas de busca e agendas adaptTo() (#day-1, #day-2, etc.)
- **Detecção de PDF**: Identifica documentos PDF e fornece orientação para download

**Ferramentas Disponíveis**:
1. `search_experience_league` - Busca com filtros avançados
2. `read_documentation` - Converte documentação para markdown
3. `get_available_services` - Lista 30+ recursos AEM

**Configuração via Docker (Recomendado para desenvolvimento local)**:
```json
{
  "mcpServers": {
    "aem-documentation-mcp-server": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "aem-docs-mcp-server:latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": [
        "search_experience_league",
        "read_documentation",
        "get_available_services"
      ]
    }
  }
}
```

**Nota Docker**: Para usar Docker, primeiro construa a imagem:
```bash
cd aem_documentation_mcp_server
docker build -t aem-docs-mcp-server:latest .
```

**Configuração via UVX (Quando publicado no PyPI)**:
```json
{
  "mcpServers": {
    "aemlabs.aem-documentation-mcp-server": {
      "command": "uvx",
      "args": ["aemlabs.aem-documentation-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": [
        "search_experience_league",
        "read_documentation",
        "get_available_services"
      ]
    }
  }
}
```

**Nota**: O pacote ainda não está publicado no PyPI. Use Docker para desenvolvimento local.

**Variáveis de Ambiente Opcionais**:
- `FASTMCP_LOG_LEVEL`: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL) - Padrão: WARNING
- `MCP_USER_AGENT`: User-Agent personalizado para redes corporativas

**Repositório**: [adobe-experience-manager-mcps](https://github.com/salomao-santos/adobe-experience-manager-mcps)
**Autor**: Salomão Santos (salomaosantos777@gmail.com)

---

## Servidores AWS

### 2. AWS Documentation MCP Server
**Função**: Acesso à documentação oficial da AWS

**Recursos**:
- Busca em documentação AWS
- Leitura de páginas de documentação
- Recomendações de conteúdo relacionado

**Configuração**:
```json
{
  "mcpServers": {
    "awslabs.aws-documentation-mcp-server": {
      "command": "uvx",
      "args": ["awslabs.aws-documentation-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR",
        "AWS_DOCUMENTATION_PARTITION": "aws",
        "MCP_USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

---

### 3. Core MCP Server
**Função**: Funcionalidades principais da AWS

**Recursos**:
- Operações básicas AWS
- Integração com serviços AWS

**Configuração**:
```json
{
  "mcpServers": {
    "awslabs.core-mcp-server": {
      "command": "uvx",
      "args": ["awslabs.core-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

---

### 4. AWS Knowledge MCP Server
**Função**: Base de conhecimento AWS via HTTP

**Recursos**:
- Acesso a conhecimento AWS
- Consultas sobre serviços e recursos AWS

**Configuração (Recomendada para Kiro)**:
```json
{
  "mcpServers": {
    "aws-knowledge-mcp-server": {
      "url": "https://knowledge-mcp.global.api.aws",
      "type": "http",
      "disabled": false
    }
  }
}
```

---

### 5. Document Loader MCP Server
**Função**: Processamento de documentos diversos

**Recursos**:
- **Extração de texto PDF**: Usando pdfplumber
- **Processamento de Word**: Converte DOCX/DOC para markdown
- **Leitura de Excel**: Analisa XLSX/XLS e converte para markdown
- **Processamento de PowerPoint**: Extrai conteúdo de PPTX/PPT
- **Carregamento de imagens**: Suporta PNG, JPG, GIF, BMP, TIFF, WEBP

**Configuração**:
```json
{
  "mcpServers": {
    "awslabs.document-loader-mcp-server": {
      "command": "uvx",
      "args": ["awslabs.document-loader-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

---

### 6. Git Repo Research MCP Server (Opcional)
**Função**: Pesquisa e análise de repositórios Git usando embeddings do Amazon Bedrock

**Requisitos adicionais**:
- AWS credentials com acesso ao Bedrock
- Token do GitHub (opcional, mas recomendado)

**Recursos**:
- Pesquisa semântica em repositórios
- Análise de código usando IA
- Embeddings com Amazon Bedrock

**Configuração**:
```json
{
  "mcpServers": {
    "awslabs.git-repo-research-mcp-server": {
      "command": "uvx",
      "args": ["awslabs.git-repo-research-mcp-server@latest"],
      "env": {
        "AWS_PROFILE": "seu-perfil-aws",
        "AWS_REGION": "us-west-2",
        "FASTMCP_LOG_LEVEL": "ERROR",
        "GITHUB_TOKEN": "seu-token-github"
      },
      "disabled": true,
      "autoApprove": []
    }
  }
}
```

**Importante**: Este servidor está **desabilitado por padrão** porque requer:
- Credenciais AWS configuradas com acesso ao Bedrock
- Token do GitHub opcional para limites de taxa mais altos
- Defina `"disabled": false` somente após configurar suas credenciais AWS

**Nota**: Substitua `seu-perfil-aws` e `seu-token-github` pelos seus valores reais.

---

## Configuração Completa no Kiro

### Configuração Completa (Recomendada)

Arquivo: `.kiro/settings/mcp.json`

**Nota**: O servidor AEM usa Docker pois o pacote ainda não está publicado no PyPI.

```json
{
  "mcpServers": {
    "aem-documentation-mcp-server": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "aem-docs-mcp-server:latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": [
        "search_experience_league",
        "read_documentation",
        "get_available_services"
      ]
    },
    "awslabs.aws-documentation-mcp-server": {
      "command": "uvx",
      "args": ["awslabs.aws-documentation-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR",
        "AWS_DOCUMENTATION_PARTITION": "aws",
        "MCP_USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
      },
      "disabled": false,
      "autoApprove": [
        "read_documentation",
        "search_documentation",
        "recommend"
      ]
    },
    "awslabs.core-mcp-server": {
      "command": "uvx",
      "args": ["awslabs.core-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": []
    },
    "aws-knowledge-mcp-server": {
      "url": "https://knowledge-mcp.global.api.aws",
      "type": "http",
      "disabled": false
    },
    "awslabs.document-loader-mcp-server": {
      "command": "uvx",
      "args": ["awslabs.document-loader-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": [
        "read_document",
        "read_image"
      ]
    },
    "awslabs.git-repo-research-mcp-server": {
      "command": "uvx",
      "args": ["awslabs.git-repo-research-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": true,
      "autoApprove": []
    }
  }
}
```

**Importante**: Antes de usar, construa a imagem Docker do AEM:
```bash
cd aem_documentation_mcp_server
docker build -t aem-docs-mcp-server:latest .
```

### Sobre Auto-Aprovação (autoApprove)

As ferramentas listadas em `autoApprove` não exigem confirmação manual a cada uso:
- **AEM**: `search_experience_league`, `read_documentation`, `get_available_services`
- **AWS Docs**: `read_documentation`, `search_documentation`, `recommend`
- **Document Loader**: `read_document`, `read_image`

Você pode adicionar ou remover ferramentas desta lista conforme sua preferência de segurança.

---

## Verificação da Instalação

### 1. Verificar requisitos instalados

```bash
# Verificar uv
uv --version

# Verificar Python (deve ser 3.10+ para AEM, 3.12+ para AWS)
python3 --version

# Verificar uvx
uvx --help

# Verificar Docker (se usar)
docker --version
```

### 2. Validar arquivo de configuração

```bash
# Verificar se o JSON está válido
cat .kiro/settings/mcp.json | python3 -m json.tool
```

### 3. Testar servidores MCP individualmente

```bash
# Testar AEM Documentation
uvx aemlabs.aem-documentation-mcp-server@latest

# Testar AWS Documentation
uvx awslabs.aws-documentation-mcp-server@latest

# Testar Document Loader
uvx awslabs.document-loader-mcp-server@latest

# Testar AEM via Docker (se construiu a imagem)
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' | docker run --rm -i aem-docs-mcp-server:latest
```

### 4. Verificar no Kiro

1. Abra o painel de servidores MCP no Kiro
2. Verifique se os 5-6 servidores estão conectados (1 Adobe + 4-5 AWS)
3. Teste as ferramentas disponíveis:
   - AEM: `search_experience_league`, `read_documentation`, `get_available_services`
   - AWS: Ferramentas específicas de cada servidor
4. Consulte os logs em caso de problemas
5. Use o comando de paleta do Kiro: "MCP: Reconnect Servers" se necessário

---

## Notas Importantes

1. **Versões**: Sempre use `@latest` para obter a versão mais recente dos servidores
2. **Log Level**: Configurado como `ERROR` para reduzir verbosidade. Use `DEBUG` para troubleshooting
3. **Auto Approve**: Lista vazia por padrão. Adicione ferramentas específicas para aprovação automática
4. **Reconexão**: Servidores se reconectam automaticamente após mudanças na configuração
5. **Git Repo Research**: Servidor opcional que requer configuração AWS adicional
6. **AEM Documentation**: Acessa documentação Adobe, GitHub, Apache Sling, adaptTo() e YouTube relacionados ao AEM

---

## Solução de Problemas

### Servidor não conecta
- Verifique se `uv` e `uvx` estão instalados
- Confirme que Python 3.12+ está disponível
- Valide o formato JSON do arquivo de configuração

### Erro de credenciais AWS
- Configure AWS CLI: `aws configure`
- Verifique variáveis de ambiente: `AWS_PROFILE` e `AWS_REGION`
- Confirme acesso ao Bedrock (se usar Git Repo Research)

### Timeout ou lentidão
- Verifique conexão com internet
- Teste conectividade: `curl https://knowledge-mcp.global.api.aws`
- Aumente timeout se necessário

### Problemas com AEM Documentation
- Verifique se `uvx` está instalado e funcionando: `uvx --help`
- Confirme Python 3.10+: `python3 --version`
- Teste conectividade com Experience League: `curl https://experienceleague.adobe.com`
- Para Docker: Verifique se a imagem foi construída: `docker images | grep aem-docs-mcp-server`
- Teste o servidor manualmente: `uvx aemlabs.aem-documentation-mcp-server@latest`
- Consulte o repositório: [adobe-experience-manager-mcps](https://github.com/salomao-santos/adobe-experience-manager-mcps)
- Abra uma issue: [Bug Tracker](https://github.com/salomao-santos/adobe-experience-manager-mcps/issues)

---

## Recursos Adicionais

### Documentação Adobe AEM
- [Experience League - AEM](https://experienceleague.adobe.com/docs/experience-manager.html)
- [AEM Developer Documentation](https://developer.adobe.com/experience-manager/)
- [Conferência adaptTo()](https://adapt.to/)
- [Apache Sling](https://sling.apache.org/)

### Documentação AWS
- [AWS Documentation](https://docs.aws.amazon.com/)
- [AWS Developer Center](https://aws.amazon.com/developer/)
- [Amazon Bedrock](https://aws.amazon.com/bedrock/)

### Repositórios MCP
- [Adobe Experience Manager MCPs](https://github.com/salomao-santos/adobe-experience-manager-mcps)
- [AWS Labs MCP Servers](https://github.com/awslabs)