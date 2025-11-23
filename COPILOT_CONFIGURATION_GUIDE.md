# 🚀 Configuração Completa do MCP Server para GitHub Copilot

## ✅ Status da Configuração

- **Imagem Docker:** `aem-docs-mcp-server:latest` (111MB)
- **Servidor:** ✅ Funcionando
- **Configuração:** `.github/copilot-instructions.json`
- **Testes:** ✅ Passando

---

## 📋 Pré-requisitos

- ✅ Docker instalado e rodando
- ✅ VS Code com GitHub Copilot instalado
- ✅ Imagem Docker construída: `aem-docs-mcp-server:latest`

---

## 🔧 Passo a Passo - Configuração GitHub Copilot

### Opção 1: Configuração Automática (Recomendado)

Este projeto já contém a configuração em `.github/copilot-instructions.json`.

**Para ativar:**

1. Abra este projeto no VS Code
2. O GitHub Copilot detectará automaticamente a configuração
3. Reinicie o VS Code se necessário

### Opção 2: Configuração Manual Global

Se preferir configurar globalmente para todos os projetos:

1. Pressione `Ctrl+Shift+P` (Windows/Linux) ou `Cmd+Shift+P` (Mac)
2. Digite: `Preferences: Open User Settings (JSON)`
3. Adicione esta configuração:

```json
{
  "github.copilot.chat.mcp.enabled": true,
  "github.copilot.chat.mcp.servers": {
    "aem-documentation": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "aem-docs-mcp-server:latest"]
    }
  }
}
```

4. Salve e reinicie o VS Code

---

## 🧪 Testando a Configuração

### Teste 1: Verificar Servidor

```bash
# Executar script de teste
./test-mcp-docker.sh
```

**Resultado esperado:** Mensagens de sucesso mostrando inicialização do servidor

### Teste 2: Verificar no Copilot Chat

1. Abra o GitHub Copilot Chat (ícone no sidebar)
2. Digite um dos seguintes comandos:

```
@workspace Quais serviços AEM estão disponíveis?
```

```
@workspace Liste os serviços de documentação AEM
```

```
@workspace Busque tutoriais sobre AEM Assets
```

**Resultado esperado:** O Copilot deve usar o MCP server e retornar informações sobre serviços AEM

---

## 🎯 Ferramentas Disponíveis

### 1. `get_available_services`
Lista todos os 30+ serviços AEM com URLs e categorias.

**Exemplo de uso no Copilot:**
```
@workspace Liste todos os serviços AEM disponíveis
@workspace Quais são as ferramentas do AEM Cloud Service?
@workspace Mostre os serviços de integração do AEM
```

### 2. `read_documentation`
Lê e converte documentação AEM de URLs suportadas para Markdown.

**Exemplo de uso no Copilot:**
```
@workspace Leia https://experienceleague.adobe.com/docs/experience-manager-cloud-service/content/assets/overview.html

@workspace Resuma a documentação de https://developer.adobe.com/experience-manager/reference-materials/

@workspace Extraia informações de https://github.com/adobe/aem-core-wcm-components
```

**Domínios suportados:**
- `experienceleague.adobe.com` - Documentação principal
- `developer.adobe.com` - APIs e referências
- `helpx.adobe.com` - Ajuda Adobe
- `docs.adobe.com` - Documentação técnica
- `github.com/*` - Qualquer repositório GitHub
- `*.github.io` - GitHub Pages
- `sling.apache.org` - Apache Sling
- `adapt.to` - Conferências adaptTo()
- `youtube.com` - Vídeos (com transcrição)

### 3. `search_experience_league`
Busca na Adobe Experience League com filtros avançados.

**Exemplo de uso no Copilot:**
```
@workspace Busque tutoriais sobre AEM Assets

@workspace Procure documentação de AEM Cloud Manager para desenvolvedores

@workspace Encontre cursos sobre AEM Sites
```

**Filtros disponíveis:**
- **Tipos de conteúdo:** docs, tutorials, videos, courses
- **Produtos:** 30+ produtos AEM (Assets, Sites, Forms, etc.)
- **Funções:** admin, developer, user, architect, business-practitioner

---

## 📝 Exemplos de Uso Completo

### Exemplo 1: Pesquisa e Leitura
```
Usuário: @workspace Preciso aprender sobre AEM Assets Cloud Service

Copilot (usando MCP):
1. Usa search_experience_league para encontrar docs
2. Retorna URL: https://experienceleague.adobe.com/docs/...
3. Usa read_documentation para ler o conteúdo
4. Apresenta resumo em Markdown
```

### Exemplo 2: Exploração de Serviços
```
Usuário: @workspace Quais ferramentas de integração o AEM oferece?

Copilot (usando MCP):
1. Usa get_available_services
2. Filtra categoria "Integrations"
3. Lista: Analytics, Target, Campaign, Workfront, Creative Cloud
```

### Exemplo 3: Documentação Técnica
```
Usuário: @workspace Como configurar replicação no AEM?

Copilot (usando MCP):
1. Busca docs sobre replicação
2. Lê documentação relevante
3. Extrai passos de configuração
4. Fornece exemplos de código
```

---

## 🔍 Verificação de Problemas

### Problema: "MCP server not found"

**Solução:**
```bash
# Verificar se a imagem existe
docker images | grep aem-docs-mcp-server

# Se não existir, construir novamente
cd aem_documentation_mcp_server
docker build -t aem-docs-mcp-server:latest .
```

### Problema: "Server not responding"

**Solução:**
```bash
# Testar manualmente
./test-mcp-docker.sh

# Verificar logs
docker logs <container_id>
```

### Problema: "Copilot não usa o MCP"

**Solução:**
1. Verificar se MCP está habilitado nas configurações
2. Reiniciar VS Code
3. Verificar se `.github/copilot-instructions.json` existe
4. Tentar configuração manual global

---

## 📊 Informações Técnicas

### Servidor MCP

- **Nome:** aemlabs.aem-documentation-mcp-server
- **Versão:** 1.22.0
- **Protocolo:** MCP 2024-11-05
- **Transporte:** stdio (via Docker)

### Performance

- **Tempo de resposta:** 210-1810ms
- **Parsing HTML:** 10ms (média) com lxml
- **Validação URL:** <0.01ms (com cache)
- **Tamanho da imagem:** 111MB

### Limitações

- Não extrai texto de PDFs automaticamente (fornece instruções)
- Transcrições de YouTube requerem acesso manual
- Documentação privada não é acessível

---

## 🎓 Recursos Adicionais

### Documentação

- **README.md** - Documentação completa do projeto
- **PERFORMANCE_IMPROVEMENTS.md** - Otimizações aplicadas
- **SECURITY_ANALYSIS.md** - Análise de segurança
- **PROJECT_STATUS.md** - Status geral do projeto

### Scripts

- **test-mcp-docker.sh** - Script de teste do servidor
- **Dockerfile** - Configuração da imagem Docker

### Configuração

- **.github/copilot-instructions.json** - Configuração MCP local

---

## ✅ Checklist de Configuração

- [ ] Docker instalado e rodando
- [ ] Imagem `aem-docs-mcp-server:latest` construída
- [ ] VS Code com GitHub Copilot instalado
- [ ] Arquivo `.github/copilot-instructions.json` presente
- [ ] Script `test-mcp-docker.sh` executado com sucesso
- [ ] VS Code reiniciado após configuração
- [ ] Teste no Copilot Chat realizado com sucesso

---

## 🎉 Próximos Passos

Agora você pode:

1. ✅ Usar o Copilot para pesquisar documentação AEM
2. ✅ Ler e converter docs para Markdown automaticamente
3. ✅ Explorar 30+ serviços AEM
4. ✅ Buscar tutoriais, vídeos e cursos
5. ✅ Acessar GitHub, Apache Sling e adaptTo()

**Experimente agora no Copilot Chat:**
```
@workspace Quais são os principais serviços do AEM Cloud?
```

---

**Autor:** Salomão Santos  
**Email:** salomaosantos777@gmail.com  
**Versão:** 0.4.0  
**Data:** 23 de Novembro de 2025
