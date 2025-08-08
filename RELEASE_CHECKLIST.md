# ✅ Checklist de Release - BioRemPP

Use este checklist para garantir que todos os passos foram seguidos antes de cada release.

## 📋 Preparação (Antes do Release)

### Código e Testes
- [ ] Todos os testes estão passando (`pytest tests/`)
- [ ] Código está em compliance com Flake8 (`flake8 src/`)
- [ ] Cobertura de testes adequada (`pytest --cov=biorempp`)
- [ ] Sem TODOs ou FIXMEs críticos no código
- [ ] Funcionalidades documentadas

### Documentação
- [ ] README.md atualizado com novas funcionalidades
- [ ] CHANGELOG.md com todas as mudanças da versão
- [ ] Exemplos e notebooks funcionando
- [ ] Docstrings atualizadas

### Configuração
- [ ] pyproject.toml com versão correta
- [ ] Dependências atualizadas no pyproject.toml
- [ ] Classificadores adequados configurados
- [ ] Entry points configurados corretamente

### Metadados
- [ ] LICENSE.txt presente e correto
- [ ] AUTHORS.md atualizado
- [ ] CONTRIBUTING.md atualizado

## 🔨 Build Local

### Preparação do Ambiente
- [ ] Ambiente virtual limpo criado
- [ ] Ferramentas de build instaladas (`pip install build twine`)
- [ ] Limpeza de builds anteriores

### Execução do Build
- [ ] Build executado com sucesso (`python scripts/build_release.py`)
- [ ] Arquivos .whl e .tar.gz gerados
- [ ] Validação com twine passou (`twine check dist/*`)
- [ ] Tamanho dos arquivos razoável (< 50MB)

## 🧪 TestPyPI

### Upload
- [ ] Credenciais TestPyPI configuradas (~/.pypirc)
- [ ] Upload para TestPyPI bem-sucedido (`twine upload --repository testpypi dist/*`)
- [ ] Página do projeto aparece no TestPyPI

### Testes
- [ ] Instalação do TestPyPI funciona
- [ ] Import do pacote funciona
- [ ] CLI funciona (`biorempp --help`)
- [ ] Funcionalidades básicas testadas
- [ ] Testes com dados reais executados

### Comando de Teste
```bash
# Testar instalação
pip install -i https://test.pypi.org/simple/ biorempp

# Testar funcionalidade
python -c "import biorempp; print('OK')"
biorempp --help
echo ">K00001" | biorempp --input - --database biorempp
```

## 🚀 PyPI Oficial

### Verificações Finais
- [ ] Todos os testes no TestPyPI passaram
- [ ] Versão está correta e não conflita
- [ ] Documentação final revisada
- [ ] Confirmação de que está pronto para produção

### Release
- [ ] Tag criada no Git (`git tag v1.0.0`)
- [ ] Tag enviada para GitHub (`git push origin v1.0.0`)
- [ ] Upload para PyPI oficial (`twine upload dist/*`)
- [ ] Instalação do PyPI oficial testada (`pip install biorempp`)

## 📚 Pós-Release

### GitHub
- [ ] Release criado no GitHub com notas de release
- [ ] Assets (arquivos de distribuição) anexados
- [ ] Release notes elaboradas

### Documentação
- [ ] Documentação oficial atualizada
- [ ] Notebooks demonstrativos funcionando
- [ ] Links de instalação testados

### Comunicação
- [ ] Anúncio em canais relevantes (se aplicável)
- [ ] README badges atualizados
- [ ] Próximos passos documentados

## 🔧 Comandos de Referência

### Build Completo
```bash
# Build automatizado
python scripts/build_release.py

# Ou manual
python -m build
twine check dist/*
```

### TestPyPI
```bash
# Upload
twine upload --repository testpypi dist/*

# Teste
pip install -i https://test.pypi.org/simple/ biorempp
```

### PyPI Oficial
```bash
# Upload
twine upload dist/*

# Teste
pip install biorempp
```

### Release com Tag
```bash
# Criar release
python scripts/release.py 1.0.0 --description "Descrição do release"

# Ou manual
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin v1.0.0
```

## 📊 Métricas de Sucesso

Após cada release, verificar:

- [ ] Download count no PyPI
- [ ] Issues reportados
- [ ] Feedback dos usuários
- [ ] Performance da instalação
- [ ] Compatibilidade em diferentes ambientes

## 🆘 Troubleshooting

### Problemas Comuns
- **"Package already exists"** → Incrementar versão
- **"Invalid wheel"** → Verificar MANIFEST.in
- **"Command not found"** → Verificar entry points
- **"Import error"** → Verificar estrutura de packages

### Logs e Debug
```bash
# Upload com logs detalhados
twine upload --verbose dist/*

# Build com logs
python -m build --verbose

# Testar wheel
pip install dist/*.whl --force-reinstall
```

---

**📝 Nota:** Salve este checklist e use para cada release. Marque os itens conforme completa para não esquecer nenhum passo importante!
