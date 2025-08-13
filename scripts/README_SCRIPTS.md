# 🚀 Scripts de Automação PyPI - Guia Rápido

Este conjunto de scripts automatiza completamente o processo de submissão de pacotes Python para PyPI e TestPyPI.

## 📋 Scripts Principais

### 🎯 **Script Principal: `pypi_manager.py`**
**Menu interativo que coordena todos os outros scripts**

```bash
# Executar o menu principal
python scripts/pypi_manager.py

# Ações diretas
python scripts/pypi_manager.py --setup          # Configurar .pypirc
python scripts/pypi_manager.py --test-upload    # Upload para TestPyPI
python scripts/pypi_manager.py --status         # Ver status
```

### 🔧 **`create_pypirc.py`** - Criação do arquivo .pypirc
```bash
# Modo interativo (recomendado)
python scripts/create_pypirc.py --interactive

# Com tokens específicos
python scripts/create_pypirc.py --testpypi-token "pypi-SEU_TOKEN"
```

### 🧪 **`upload_to_testpypi.py`** - Upload automático para TestPyPI
```bash
# Upload completo
python scripts/upload_to_testpypi.py

# Opções avançadas
python scripts/upload_to_testpypi.py --skip-build --verbose
```

## ⚡ Início Rápido

### 1️⃣ **Primeira vez** (configuração)
```bash
# Execute o menu principal
python scripts/pypi_manager.py

# Escolha opção 2: Configurar .pypirc
# Escolha opção 6: Instalar ferramentas (se necessário)
```

### 2️⃣ **Para cada release**
```bash
# 1. Atualizar versão no pyproject.toml
# 2. Commitar alterações
# 3. Upload para TestPyPI
python scripts/pypi_manager.py
# Escolha opção 3: Upload para TestPyPI

# 4. Testar instalação
pip install --index-url https://test.pypi.org/simple/ biorempp

# 5. Upload para PyPI oficial (se tudo OK)
python scripts/pypi_manager.py
# Escolha opção 4: Upload para PyPI oficial
```

## 🎯 Funcionalidades dos Scripts

### `pypi_manager.py` - Script Maestro
- ✅ **Menu interativo** com todas as opções
- ✅ **Verificação de status** completa
- ✅ **Coordenação** de outros scripts
- ✅ **Documentação** integrada
- ✅ **Instalação** automática de ferramentas

### `create_pypirc.py` - Configurador do .pypirc
- ✅ **Modo interativo** com input seguro
- ✅ **Validação automática** de tokens
- ✅ **Backup automático** de arquivos existentes
- ✅ **Permissões de segurança** automáticas
- ✅ **Suporte multiplataforma**

### `upload_to_testpypi.py` - Uploader TestPyPI
- ✅ **Workflow completo** automatizado
- ✅ **Verificação de pré-requisitos**
- ✅ **Build e upload** automáticos
- ✅ **Instruções de instalação** detalhadas
- ✅ **Saída colorida** e informativa

## 🔗 Tokens Necessários

### TestPyPI (obrigatório para testes)
1. Acesse: https://test.pypi.org/manage/account/#api-tokens
2. Clique "Add API token"
3. Nome: `biorempp-test`
4. Escopo: "Entire account"

### PyPI (para produção)
1. Acesse: https://pypi.org/manage/account/#api-tokens
2. Clique "Add API token"
3. Nome: `biorempp-prod`
4. Escopo: "Entire account" (primeiro upload) ou "Specific project"

## 📁 Arquivos de Apoio

| Arquivo | Finalidade |
|---------|------------|
| `.pypirc_template` | Template base do .pypirc |
| `configure_pypi.py` | Script alternativo (inglês) |
| `DOCUMENTACAO_SCRIPTS_PYPI.md` | Documentação completa |
| `PYPI_SETUP_GUIDE.md` | Guia em inglês |

## 🛠️ Pré-requisitos

```bash
# Ferramentas necessárias
pip install build twine

# Para Python < 3.11
pip install tomli
```

## 🎨 Interface do Menu Principal

```
============================================================
                 GERENCIADOR DE UPLOAD PYPI                
============================================================

Opções Disponíveis:
1. 📊 Ver status da configuração
2. 🔧 Configurar .pypirc (criar/editar tokens)
3. 🧪 Upload para TestPyPI
4. 🚀 Upload para PyPI oficial
5. 📚 Ver documentação
6. 🛠️  Instalar ferramentas necessárias
0. ❌ Sair

Escolha uma opção (0-6):
```

## 🔒 Segurança

- ❌ **Nunca** commite `.pypirc` no git
- ✅ **Sempre** teste no TestPyPI primeiro
- ✅ **Use** tokens específicos por projeto
- ✅ **Revogue** tokens antigos regularmente

## 🐛 Solução Rápida de Problemas

| Problema | Solução |
|----------|---------|
| Erro de autenticação | `python scripts/pypi_manager.py` → opção 2 |
| Ferramentas não encontradas | `python scripts/pypi_manager.py` → opção 6 |
| Pacote já existe | Incrementar versão no `pyproject.toml` |
| Build falha | Verificar estrutura do projeto |

## 📞 Suporte

- 📖 **Documentação completa**: `scripts/DOCUMENTACAO_SCRIPTS_PYPI.md`
- 🌐 **Guia em inglês**: `scripts/PYPI_SETUP_GUIDE.md`
- 🔧 **Status do sistema**: `python scripts/pypi_manager.py --status`

---

**💡 Dica**: Execute `python scripts/pypi_manager.py` para começar imediatamente!
