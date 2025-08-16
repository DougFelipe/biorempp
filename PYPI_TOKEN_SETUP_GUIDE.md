# 🔐 Configuração do Token PyPI para CI/CD - BioRemPP

## 📋 Guia Completo de Configuração

### 1️⃣ Criação do Token no PyPI Test

#### Passo 1: Criar conta no PyPI Test
1. Acesse: https://test.pypi.org/
2. Crie uma conta ou faça login
3. Verifique seu email

#### Passo 2: Gerar Token da API
1. Faça login no PyPI Test
2. Vá para: **Account Settings** → **API tokens**
3. Clique em **"Add API token"**
4. Configure o token:
   - **Token name**: `biorempp-ci-test`
   - **Scope**:
     - Se primeiro upload: **"Entire account"**
     - Se projeto já existe: **"Project: biorempp"**
5. Clique em **"Add token"**
6. **⚠️ IMPORTANTE**: Copie o token imediatamente (começa com `pypi-`)
7. O token será algo como: `pypi-AgEIcHlwaS5vcmcCJGFhYWFhYWFhLWJiYmItY2NjYy1kZGRkLWVlZWVlZWVlZWVlZQACKlszLCI0Il0gW10gWyJmb28iXQAABiABBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB`

### 2️⃣ Configuração do Token no GitHub

#### Passo 1: Adicionar Secret no Repositório
1. Vá para seu repositório GitHub: `https://github.com/DougFelipe/biorempp`
2. Clique em **"Settings"** (na barra superior do repo)
3. No menu lateral esquerdo: **"Secrets and variables"** → **"Actions"**
4. Clique em **"New repository secret"**
5. Configure:
   - **Name**: `PYPI_TEST_TOKEN`
   - **Secret**: Cole o token completo do PyPI Test (inclui `pypi-`)
6. Clique em **"Add secret"**

#### Passo 2: (Opcional) Token para PyPI Produção
Para publicação em produção futura:
1. Repita o processo em https://pypi.org/
2. Crie secret: `PYPI_TOKEN`

### 3️⃣ Estrutura dos Secrets Configurados

```yaml
# Secrets necessários no GitHub Actions:
PYPI_TEST_TOKEN=pypi-AgEIcHlwaS5vcmcCJGFh...  # Para test.pypi.org
PYPI_TOKEN=pypi-AgEIcHlwaS5vcmcCJGFh...       # Para pypi.org (produção)
```

### 4️⃣ Verificação da Configuração

#### Como testar se está funcionando:
1. Faça um commit no branch `develop` ou `main`
2. Verifique o workflow em: **Actions** tab no GitHub
3. O job `test-publish` deve executar após os testes
4. Verifique em https://test.pypi.org/project/biorempp/ se o pacote foi publicado

### 5️⃣ Workflow Adicionado

O workflow `ci.yml` agora inclui:

```yaml
test-publish:
  needs: test
  runs-on: ubuntu-latest
  if: github.ref == 'refs/heads/develop' || github.ref == 'refs/heads/main'

  steps:
  - uses: actions/checkout@v4
    with:
      fetch-depth: 0  # Para versionamento correto

  - name: Set up Python
    uses: actions/setup-python@v4
    with:
      python-version: "3.10"

  - name: Install build dependencies
    run: |
      python -m pip install --upgrade pip
      pip install build twine

  - name: Build package
    run: python -m build

  - name: Validate package with twine
    run: twine check dist/*

  - name: Publish to PyPI Test
    env:
      TWINE_USERNAME: __token__
      TWINE_PASSWORD: ${{ secrets.PYPI_TEST_TOKEN }}
    run: twine upload --repository testpypi dist/* --verbose
```

### 6️⃣ Funcionalidades Implementadas

✅ **Triggers**: Executa em pushes para `develop` e `main`
✅ **Dependências**: Só executa após testes passarem
✅ **Build**: Cria wheel e source distribution
✅ **Validação**: Verifica integridade com `twine check`
✅ **Upload**: Publica no PyPI Test automaticamente
✅ **Segurança**: Usa token da API ao invés de usuário/senha

### 7️⃣ Próximos Passos Recomendados

#### Para Produção (PyPI real):
1. Configure `PYPI_TOKEN` para https://pypi.org/
2. Modifique o workflow de release para incluir upload para PyPI produção
3. Configure release apenas em tags ou main branch

#### Melhorias Futuras:
- Adicionar verificação de versão antes do upload
- Implementar strategy para evitar uploads duplicados
- Configurar notificações de sucesso/falha

### 8️⃣ Troubleshooting

#### Erro comum: "403 Forbidden"
- **Causa**: Token inválido ou sem permissões
- **Solução**: Regenerar token com scope correto

#### Erro: "File already exists"
- **Causa**: Versão já publicada
- **Solução**: Incrementar versão no código

#### Erro: "Invalid or non-existent authentication"
- **Causa**: Secret não configurado corretamente
- **Solução**: Verificar nome do secret no GitHub

### 9️⃣ Comandos Manuais para Teste Local

```bash
# Instalar dependências
pip install build twine

# Build local
python -m build

# Verificar pacote
twine check dist/*

# Upload manual para teste (com seu token)
twine upload --repository testpypi dist/* --verbose
```

---

## ✅ Checklist de Configuração

- [ ] Conta criada no test.pypi.org
- [ ] Token gerado no PyPI Test
- [ ] Secret `PYPI_TEST_TOKEN` adicionado no GitHub
- [ ] Workflow testado com commit
- [ ] Pacote aparece em test.pypi.org
- [ ] (Opcional) Configuração para PyPI produção

**🎯 Resultado**: Após esta configuração, a cada push para `develop` ou `main`, se os testes passarem, uma nova versão será automaticamente publicada no PyPI Test!
