# Servidor MCP de Documentação AEM

Servidor Model Context Protocol (MCP) para Documentação do Adobe Experience Manager (AEM)

Este servidor MCP fornece ferramentas para acessar a documentação do Adobe AEM e recursos relacionados do ecossistema AEM, convertendo-os para formato markdown para fácil consumo por assistentes de IA.

## Funcionalidades

- **Buscar no Experience League**: Busque na documentação Adobe com filtros avançados (tipo de conteúdo, produtos, funções)
- **Ler Documentação**: Busque e converta páginas de documentação para formato markdown de:
  - Documentação Oficial Adobe (Experience League, Developer, HelpX, Docs)
  - Repositórios GitHub (qualquer organização: Adobe, ACS, Netcentric, etc.)
  - GitHub Pages (sites de documentação *.github.io)
  - Documentação Apache Sling
  - Recursos da conferência adaptTo() (todos os anos: 2011-2025+, incluindo PDFs)
  - Vídeos do YouTube (com orientação de transcrição)
  - Sites Adobe Business (Summit, etc.)
- **Obter Serviços Disponíveis**: Obtenha uma lista curada de mais de 30 serviços e áreas de documentação AEM
- **Suporte a Fragmentos Hash**: Preserva fragmentos de URL para páginas de busca e cronogramas adaptTo() (#day-1, #day-2, etc.)
- **Detecção de PDF**: Identifica documentos PDF e fornece orientação de download

## Pré-requisitos

### Requisitos de Instalação

1. **Python**: Versão 3.10 ou mais recente
   - Instale usando `uv python install 3.10` (ou 3.11, 3.12, 3.13)
   
2. **uv**: Versão mais recente da [Astral](https://docs.astral.sh/uv/getting-started/installation/)
   - Instale via: `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - Ou via pip: `pip install uv`
   - Ou via homebrew: `brew install uv`

3. **Docker** (opcional): Para implantação em contêiner
   - Instale do [Docker Desktop](https://www.docker.com/products/docker-desktop/)

## Instalação

> **⚠️ Importante**: O pacote `aemlabs.aem-documentation-mcp-server` ainda **não está publicado no PyPI**. Use Docker para desenvolvimento local até a publicação oficial.

Você pode executar o servidor MCP usando **Docker** (recomendado para desenvolvimento local) ou **UVX** (quando publicado no PyPI). Escolha o método que melhor se adapta ao seu ambiente.

### Opção 1: Usando Docker (Recomendado para desenvolvimento local)

Primeiro, construa a imagem Docker:

```bash
cd aem_documentation_mcp_server
docker build -t aem-docs-mcp-server:latest .
```

Depois configure o servidor MCP:

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

### Opção 2: Usando UVX (Quando publicado no PyPI)

**Nota**: O pacote ainda não está publicado no PyPI. Esta opção estará disponível em breve.

Configure o servidor MCP na configuração do seu cliente MCP:

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

### Sobre Auto-Aprovação (autoApprove)

As ferramentas listadas em `autoApprove` não exigem confirmação manual a cada uso:
- `search_experience_league` - Busca na documentação
- `read_documentation` - Leitura de páginas de documentação
- `get_available_services` - Lista de serviços disponíveis

Você pode adicionar ou remover ferramentas desta lista conforme sua preferência de segurança.

### Alternando Entre Docker e UVX

Para alternar entre os modos, defina `"disabled": true` no modo que você não quer usar e `"disabled": false` no que você quer ativar.

### Instalação para Desenvolvimento

Clone o repositório e instale em modo de desenvolvimento:

```bash
git clone https://github.com/salomao-santos/adobe-experience-manager-mcps.git
cd adobe-experience-manager-mcps/aem_documentation_mcp_server
uv venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
uv pip install -e .
```

## Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `FASTMCP_LOG_LEVEL` | Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL) | `WARNING` |
| `MCP_USER_AGENT` | String User-Agent personalizada para requisições HTTP | Padrão baseado em Chrome |

### Suporte a Redes Corporativas

Para ambientes corporativos com servidores proxy ou firewalls que bloqueiam certas strings User-Agent:

```json
{
  "env": {
    "MCP_USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
  }
}
```

## Uso Básico

Exemplos:

- "Busque no Experience League por documentação sobre 'sling models'"
- "Busque tutoriais de componentes AEM para desenvolvedores"
- "Obtenha os serviços AEM disponíveis"
- "Consulte a documentação sobre introdução ao AEM Cloud Service"
- "Leia a documentação do AEM 6.5 e explique os principais recursos"
- "Mostre-me o README do GitHub do AEM Project Archetype"
- "Obtenha documentação sobre Apache Sling Models"
- "Quais são as sessões do adaptTo() 2024 no dia 1?"
- "Quais foram as sessões do adaptTo() 2012?"
- "Forneça orientação sobre como acessar a transcrição do YouTube para o vídeo XYZ"

## Ferramentas

### search_experience_league

Busque na documentação do Adobe Experience League com filtros avançados.

```python
search_experience_league(
    query: str,
    content_types: List[str] = ['Documentation'],
    products: List[str] = None,
    roles: List[str] = None,
    include_all_aem_products: bool = False
) -> str
```

**Parâmetros**:
- `query`: Termo de busca (ex: 'sling models', 'desenvolvimento de componentes')
- `content_types`: Filtrar por tipo (Documentation, Tutorial, Troubleshooting, API Reference, etc.)
- `products`: Filtrar por produtos Adobe (ex: 'Experience Manager', 'Experience Manager|as a Cloud Service')
- `roles`: Filtrar por função do usuário (Developer, Admin, User, Leader, etc.)
- `include_all_aem_products`: Incluir automaticamente todas as variantes AEM (Cloud Service, 6.5, Assets, Sites, etc.)

**Exemplos**:
```python
# Buscar documentação sobre sling models
search_experience_league(query='sling models', content_types=['Documentation'])

# Buscar tutoriais de componentes para desenvolvedores
search_experience_league(
    query='components',
    content_types=['Tutorial'],
    roles=['Developer']
)

# Buscar em todos os produtos AEM
search_experience_league(
    query='authentication',
    include_all_aem_products=True
)
```

### read_documentation

Busca páginas de documentação do ecossistema AEM e converte para formato markdown.

```python
read_documentation(url: str, max_length: int = 10000, start_index: int = 0) -> str
```

**Domínios Suportados**:
- **Adobe Oficial**: experienceleague.adobe.com (incluindo páginas /search), developer.adobe.com, helpx.adobe.com, docs.adobe.com, business.adobe.com
- **GitHub**: github.com/* (qualquer organização), *.github.io (GitHub Pages)
- **Apache Sling**: sling.apache.org
- **Eventos da Comunidade**: adapt.to (todos os anos: 2011-2025+, incluindo fragmentos hash como #day-1 e PDFs)
- **Recursos de Vídeo**: youtube.com, youtu.be (fornece orientação de acesso a transcrições)

**Recursos Especiais**:
- URLs do YouTube: Fornece informações do vídeo e orientação sobre acesso a transcrições
- Arquivos PDF: Detecta documentos PDF (ex: apresentações adaptTo()) e fornece instruções de download
- Páginas de busca: Preserva fragmentos hash com parâmetros de busca
- Páginas adaptTo(): Preserva fragmentos hash para navegação por dia (#day-1, #day-2, etc.)
- Suporte a paginação para documentos longos via `start_index` e `max_length`
- Extração automática de conteúdo com seletores específicos da plataforma
- Rastreamento de sessão para análises

### get_available_services

Obtém uma lista curada de serviços e áreas de documentação do ecossistema AEM.

```python
get_available_services() -> List[ServiceInfo]
```

Retorna mais de 30 recursos incluindo:
- **AEM Core**: Cloud Service, 6.5, APIs de Desenvolvedor
- **Repositórios GitHub**: Project Archetype, Core WCM Components, ACS AEM Commons, Netcentric Tools
- **Fundação**: Apache Sling Models, Servlets, Eventing
- **Comunidade**: adaptTo() 2025, 2024, 2023, Arquivos históricos (2011-2019)
- **Business**: Adobe Summit
- **Vídeo**: Canais do YouTube (Adobe Developers, AEM User Group)

## Arquitetura

O servidor é construído usando FastMCP e segue as melhores práticas para desenvolvimento de servidores MCP:

- `server.py` - Servidor FastMCP principal com definições de ferramentas
- `server_utils.py` - Utilitários compartilhados para requisições HTTP e validação de URL
- `util.py` - Utilitários de extração HTML e conversão Markdown
- `models.py` - Modelos de dados Pydantic
- `search_utils.py` - Funcionalidade de busca no Experience League
- `youtube_utils.py` - Manipulação de vídeos do YouTube

## Desenvolvimento

### Executando Testes

```bash
# Instalar dependências de desenvolvimento
uv pip install -e ".[dev]"

# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=aemlabs

# Executar testes ao vivo (faz requisições HTTP reais)
pytest --run-live
```

### Qualidade de Código

```bash
# Formatar código
ruff format .

# Verificar código
ruff check .

# Verificação de tipos
pyright
```

## Imagem Docker

A imagem Docker é otimizada para uso em produção:
- **Imagem Base**: Python 3.13 Alpine
- **Tamanho**: ~112MB
- **Build multi-estágio**: Separa dependências de build e runtime
- **Usuário não-root**: Executa como usuário sem privilégios para segurança
- **Otimizações**: Compilação de bytecode, dependências mínimas

## Licença

Apache License 2.0 - Veja o arquivo [LICENSE](aem_documentation_mcp_server/LICENSE) para detalhes

## Autor

**Salomão Santos**
- Email: salomaosantos777@gmail.com
- GitHub: [@salomao-santos](https://github.com/salomao-santos)

## Repositório

Este projeto está disponível publicamente em:
- **Homepage**: https://github.com/salomao-santos/adobe-experience-manager-mcps
- **Documentação**: https://github.com/salomao-santos/adobe-experience-manager-mcps/blob/main/README.md
- **Código Fonte**: https://github.com/salomao-santos/adobe-experience-manager-mcps.git
- **Rastreador de Bugs**: https://github.com/salomao-santos/adobe-experience-manager-mcps/issues

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para enviar um Pull Request.

## Suporte

Para problemas e questões, por favor abra uma issue no [repositório GitHub](https://github.com/salomao-santos/adobe-experience-manager-mcps/issues).
