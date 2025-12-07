# AEM Documentation MCP Server | Servidor MCP de Documentação AEM

<div align="center">

[![English](https://img.shields.io/badge/lang-English-blue.svg)](README-en.md)
[![Português](https://img.shields.io/badge/lang-Português-green.svg)](README-pt-BR.md)

</div>

---

## 🌍 Language | Idioma

Choose your preferred language to read the documentation:

Escolha seu idioma preferido para ler a documentação:

### 📖 Documentation | Documentação

- **[English Documentation](README-en.md)** - Full documentation in English
- **[Documentação em Português](README-pt-BR.md)** - Documentação completa em português

---

## 🚀 Quick Start | Início Rápido

### Model Context Protocol (MCP) server for Adobe Experience Manager (AEM) Documentation

This MCP server provides tools to access Adobe AEM documentation and related resources from the AEM ecosystem, converting them to markdown format for easy consumption by AI assistants.

### Servidor Model Context Protocol (MCP) para Documentação do Adobe Experience Manager (AEM)

Este servidor MCP fornece ferramentas para acessar a documentação do Adobe AEM e recursos relacionados do ecossistema AEM, convertendo-os para formato markdown para fácil consumo por assistentes de IA.

---

## ✨ Key Features | Principais Funcionalidades

- 🔍 **Search Experience League** | **Buscar no Experience League**
- 📚 **Read Documentation** from multiple sources | **Ler Documentação** de múltiplas fontes
- 🛠️ **Get Available Services** (30+ AEM resources) | **Obter Serviços Disponíveis** (mais de 30 recursos AEM)
- 🐳 **Docker Support** | **Suporte Docker**
- 📦 **UVX Installation** | **Instalação via UVX**

---

## 📦 Installation | Instalação

> **⚠️ Important | Importante**: Package not yet published to PyPI. Use Docker for now.  
> O pacote ainda não está publicado no PyPI. Use Docker por enquanto.

### Using Docker (Recommended) | Usando Docker (Recomendado)

```bash
# Build the image | Construa a imagem
cd aem_documentation_mcp_server
docker build -t aem-docs-mcp-server:latest .
```

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

### Using UVX (When published to PyPI) | Usando UVX (Quando publicado no PyPI)

**Note | Nota**: Package not yet published to PyPI. Use Docker for now.
O pacote ainda não está publicado no PyPI. Use Docker por enquanto.

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

---

## 👤 Author | Autor

**Salomão Santos**
- 📧 Email: salomaosantos777@gmail.com
- 🐙 GitHub: [@salomao-santos](https://github.com/salomao-santos)

---

## 📄 License | Licença

Apache License 2.0

---

## 🔗 Links

- **Repository | Repositório**: [github.com/salomao-santos/adobe-experience-manager-mcps](https://github.com/salomao-santos/adobe-experience-manager-mcps)
- **Issues | Problemas**: [Bug Tracker](https://github.com/salomao-santos/adobe-experience-manager-mcps/issues)

---

<div align="center">

**[Read Full Documentation | Leia a Documentação Completa](README-en.md)**

**[Ler Documentação Completa em Português](README-pt-BR.md)**

</div>
