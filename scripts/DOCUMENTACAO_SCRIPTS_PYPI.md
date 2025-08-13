# Scripts de Automação PyPI - Documentação

Este diretório contém scripts especializados para automatizar o processo de submissão de pacotes Python para PyPI e TestPyPI.

## 📁 Visão Geral dos Scripts

### 1. `create_pypirc.py` - Criador do arquivo .pypirc
**Finalidade**: Cria e configura automaticamente o arquivo `.pypirc` com tokens de autenticação.

### 2. `upload_to_testpypi.py` - Upload automatizado para TestPyPI
**Finalidade**: Automatiza todo o workflow de upload para TestPyPI, incluindo build, verificação e upload.

### 3. Arquivos de apoio:
- `.pypirc_template` - Template base do arquivo .pypirc
- `configure_pypi.py` - Script de configuração alternativo (inglês)
- `PYPI_SETUP_GUIDE.md` - Guia completo em inglês

## 🔧 Script 1: `create_pypirc.py`

### Descrição
Script inteligente que cria o arquivo `.pypirc` automaticamente, com validação de tokens, backup de arquivos existentes e configuração de permissões.

### Características
- ✅ Modo interativo com input seguro de tokens
- ✅ Validação automática de tokens
- ✅ Backup automático de arquivos existentes
- ✅ Configuração automática de permissões (Unix)
- ✅ Suporte multiplataforma (Windows/Linux/Mac)
- ✅ Interface colorida e amigável

### Uso Básico

```bash
# Modo interativo (recomendado)
python scripts/create_pypirc.py --interactive

# Apenas token TestPyPI (para testes)
python scripts/create_pypirc.py --testpypi-token "pypi-SEU_TOKEN_TESTPYPI"

# Ambos os tokens
python scripts/create_pypirc.py \
    --pypi-token "pypi-SEU_TOKEN_PYPI" \
    --testpypi-token "pypi-SEU_TOKEN_TESTPYPI"

# Sobrescrever arquivo existente
python scripts/create_pypirc.py --interactive --force

# Ver onde o arquivo será criado
python scripts/create_pypirc.py --show-path
```

### Parâmetros

| Parâmetro | Descrição | Obrigatório |
|-----------|-----------|-------------|
| `--interactive` | Modo interativo para inserir tokens | Não |
| `--pypi-token` | Token do PyPI oficial | Não |
| `--testpypi-token` | Token do TestPyPI | Não |
| `--force` | Sobrescreve arquivo existente | Não |
| `--show-path` | Mostra caminho do arquivo | Não |

### Exemplo de Saída

```
🔧 PyPI Configuration Creator
===================================

🔐 Interactive PyPI Configuration
========================================

This will help you create a .pypirc file with your PyPI tokens.
You can get tokens from:
  PyPI: https://pypi.org/manage/account/#api-tokens
  TestPyPI: https://test.pypi.org/manage/account/#api-tokens

Note: Tokens will be hidden as you type

Enter your TestPyPI token (required): [hidden input]
Do you want to add PyPI production token now? [y/N]: y
Enter your PyPI production token: [hidden input]

✅ .pypirc file created successfully at: /home/user/.pypirc
✅ File permissions set to 600 (owner read/write only)

🎉 Configuration Complete!

📦 Ready to Upload:
# Test upload (recommended first):
python scripts/upload_to_testpypi.py
```

## 🚀 Script 2: `upload_to_testpypi.py`

### Descrição
Script completo que automatiza todo o processo de upload para TestPyPI, desde a limpeza dos builds anteriores até as instruções de instalação.

### Características
- ✅ Verificação automática de pré-requisitos
- ✅ Limpeza automática de builds anteriores
- ✅ Build automático do pacote
- ✅ Verificação de integridade com twine
- ✅ Upload automático para TestPyPI
- ✅ Instruções detalhadas de instalação
- ✅ Modo dry-run para simulação
- ✅ Saída colorida e informativa

### Uso Básico

```bash
# Upload completo (recomendado)
python scripts/upload_to_testpypi.py

# Usar builds existentes (pular build)
python scripts/upload_to_testpypi.py --skip-build

# Modo verbose (mais detalhes)
python scripts/upload_to_testpypi.py --verbose

# Simulação (não faz alterações)
python scripts/upload_to_testpypi.py --dry-run
```

### Parâmetros

| Parâmetro | Descrição | Obrigatório |
|-----------|-----------|-------------|
| `--skip-build` | Pula etapa de build (usa dist/ existente) | Não |
| `--verbose` | Saída mais detalhada | Não |
| `--dry-run` | Simula operação sem executar | Não |

### Fluxo de Execução

1. **Verificação de Pré-requisitos**
   - Verifica se está no diretório correto (pyproject.toml)
   - Valida configuração do .pypirc
   - Confirma disponibilidade de ferramentas (build, twine)

2. **Limpeza de Builds Anteriores**
   - Remove diretório dist/ existente
   - Garante build limpo

3. **Build do Pacote**
   - Executa `python -m build`
   - Cria arquivos wheel e source distribution

4. **Verificação de Integridade**
   - Executa `twine check dist/*`
   - Valida metadados e estrutura

5. **Upload para TestPyPI**
   - Executa `twine upload --repository testpypi dist/*`
   - Upload automático usando credenciais do .pypirc

6. **Instruções de Instalação**
   - Mostra URLs do pacote no TestPyPI
   - Fornece comandos de instalação
   - Sugere comandos de teste

### Exemplo de Saída

```
🚀 TestPyPI Upload Script for biorempp
==================================================

[Step 1] Checking prerequisites
✅ Found pyproject.toml
✅ .pypirc configuration: Configuration looks good
✅ build is available
✅ twine is available

[Step 2] Cleaning previous builds
  → Removing existing dist/ directory
✅ Cleaned dist/ directory

[Step 3] Building package
  → Building package with python -m build
✅ Package built successfully

[Step 4] Checking package integrity
  → Checking package integrity with twine
✅ Package integrity check passed

[Step 5] Uploading to TestPyPI
  → Uploading to TestPyPI
✅ Upload completed successfully

[Step 6] Upload complete!

🎉 Upload Successful!

Package Information:
  Name: biorempp
  Version: 0.5.0

🔗 TestPyPI URLs:
  Package page: https://test.pypi.org/project/biorempp/
  Specific version: https://test.pypi.org/project/biorempp/0.5.0/

📦 Installation Commands:
  # Install from TestPyPI
  pip install --index-url https://test.pypi.org/simple/ biorempp

  # Install specific version
  pip install --index-url https://test.pypi.org/simple/ biorempp==0.5.0

🧪 Testing Commands:
  # Test the installation
  python -c "import biorempp; print(biorempp.__version__)"

  # Test CLI (if available)
  python -m biorempp --help
```

## 🔗 Workflow Completo Recomendado

### 1. Configuração Inicial (uma vez)

```bash
# Criar arquivo .pypirc
python scripts/create_pypirc.py --interactive

# Verificar configuração
python scripts/create_pypirc.py --show-path
```

### 2. Para Cada Release

```bash
# 1. Atualizar versão no pyproject.toml
# 2. Commit das alterações
# 3. Upload para TestPyPI
python scripts/upload_to_testpypi.py

# 4. Testar instalação do TestPyPI
pip install --index-url https://test.pypi.org/simple/ biorempp

# 5. Se tudo estiver OK, upload para PyPI oficial
twine upload --repository pypi dist/*
```

## 🛠️ Pré-requisitos

### Ferramentas Necessárias
```bash
# Instalar ferramentas de build e upload
pip install build twine

# Para Python < 3.11 (leitura de pyproject.toml)
pip install tomli
```

### Tokens Necessários
- **TestPyPI**: https://test.pypi.org/manage/account/#api-tokens
- **PyPI**: https://pypi.org/manage/account/#api-tokens

### Estrutura do Projeto
- `pyproject.toml` configurado corretamente
- Projeto committado no git (recomendado)
- Working directory limpo

## 🔒 Segurança e Boas Práticas

### Tokens
- ✅ Use tokens ao invés de senha
- ✅ Crie tokens específicos por projeto (após primeiro upload)
- ✅ Use escopo "Entire account" apenas para primeiro upload
- ✅ Revogue tokens antigos regularmente
- ❌ Nunca commite o arquivo .pypirc

### Arquivos
```bash
# Configurar permissões corretas (Unix)
chmod 600 ~/.pypirc

# Adicionar ao .gitignore
echo ".pypirc" >> .gitignore
```

### Workflow de Segurança
1. Sempre teste no TestPyPI primeiro
2. Verifique o pacote instalado funciona
3. Só então faça upload para PyPI oficial
4. Não é possível sobrescrever versões no PyPI

## 🐛 Solução de Problemas

### Erro: "File already exists"
```bash
# Limpar builds anteriores
rm -rf dist/
python scripts/upload_to_testpypi.py
```

### Erro: "Invalid authentication"
```bash
# Verificar configuração
python scripts/create_pypirc.py --show-path
cat ~/.pypirc  # Verificar tokens

# Recriar .pypirc
python scripts/create_pypirc.py --interactive --force
```

### Erro: "Package already exists"
```bash
# Incrementar versão no pyproject.toml
# Exemplo: 0.5.0 -> 0.5.1
```

### Erro: "Command not found"
```bash
# Instalar ferramentas
pip install build twine
```

## 📋 Checklist de Release

- [ ] Versão atualizada no `pyproject.toml`
- [ ] Changelog atualizado
- [ ] Testes passando
- [ ] Código committado
- [ ] `.pypirc` configurado
- [ ] Upload para TestPyPI realizado
- [ ] Instalação do TestPyPI testada
- [ ] Upload para PyPI oficial realizado
- [ ] Release/tag criado no GitHub

## 🔄 Scripts Relacionados

### Scripts Legacy (compatibilidade)
- `pypirc_example` - Exemplo em português
- `setup_pypirc.py` - Script anterior de configuração

### Scripts Atuais (recomendados)
- `create_pypirc.py` - **Criação do .pypirc**
- `upload_to_testpypi.py` - **Upload para TestPyPI**

### Guias e Documentação
- `PYPI_SETUP_GUIDE.md` - Guia completo em inglês
- `README_PYPI_SETUP.md` - Documentação em português
