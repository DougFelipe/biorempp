# 📦 Guia Completo de Distribuição - BioRemPP

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Estrutura de Arquivos para Produção](#estrutura-de-arquivos-para-produção)
3. [Configuração de Build](#configuração-de-build)
4. [Processo de Build Local](#processo-de-build-local)
5. [Teste no TestPyPI](#teste-no-testpypi)
6. [Distribuição no PyPI Oficial](#distribuição-no-pypi-oficial)
7. [Versionamento e Tags](#versionamento-e-tags)
8. [Automação com GitHub Actions](#automação-com-github-actions)
9. [Checklist de Produção](#checklist-de-produção)
10. [Troubleshooting](#troubleshooting)

---

## 🎯 Visão Geral

### O que é Distribuição de Pacotes Python?

A distribuição de pacotes Python permite que outros usuários instalem seu software via `pip install`. O processo envolve:

- **Build**: Compilação do código em formatos distribuíveis (.whl e .tar.gz)
- **Upload**: Envio para repositórios (TestPyPI → PyPI)
- **Versionamento**: Controle de versões semântico
- **Testes**: Validação em ambiente isolado

### Fluxo de Distribuição Recomendado

```mermaid
graph TD
    A[Desenvolvimento Local] → B[Build Local]
    B → C[Teste Local]
    C → D[Upload TestPyPI]
    D → E[Teste TestPyPI]
    E → F[Upload PyPI Oficial]
    F → G[Release GitHub]
    G → H[Documentação]
```

---

## 📁 Estrutura de Arquivos para Produção

### Arquivos Essenciais para Distribuição

```
biorempp/
├── 📦 ARQUIVOS DE BUILD (obrigatórios)
│   ├── setup.py                    # ✅ Configuração principal
│   ├── pyproject.toml              # ✅ Configuração moderna
│   ├── setup.cfg                   # ✅ Configuração adicional
│   ├── MANIFEST.in                 # ✅ Arquivos inclusos
│   └── requirements.txt            # ✅ Dependências
│
├── 📄 METADADOS (obrigatórios)
│   ├── README.md                   # ✅ Descrição principal
│   ├── LICENSE.txt                 # ✅ Licença
│   ├── AUTHORS.md                  # ✅ Autores
│   ├── CHANGELOG.md                # ✅ Histórico de mudanças
│   └── CONTRIBUTING.md             # ✅ Guia de contribuição
│
├── 🐍 CÓDIGO FONTE (core)
│   ├── src/biorempp/              # ✅ Código principal
│   │   ├── __init__.py            # ✅ Módulo principal
│   │   ├── main.py                # ✅ CLI entry point
│   │   ├── pipelines/             # ✅ Lógica principal
│   │   ├── cli/                   # ✅ Interface CLI
│   │   ├── data/                  # ✅ Dados incorporados
│   │   ├── utils/                 # ✅ Utilitários
│   │   └── metadata/              # ✅ Versão e metadados
│   │       └── version.py
│
├── 🧪 TESTES (recomendados)
│   ├── tests/                     # ✅ Testes automatizados
│   └── conftest.py                # ✅ Configuração pytest
│
├── 📚 DOCUMENTAÇÃO (recomendados)
│   ├── docs/                      # ✅ Documentação completa
│   └── notebooks/                 # ✅ Exemplos práticos
│
└── ⚙️ CONFIGURAÇÃO (opcionais)
    ├── tox.ini                    # ✅ Testes multi-ambiente
    ├── .github/workflows/         # ✅ CI/CD
    └── Dockerfile                 # ✅ Containerização
```

### Arquivos que NÃO devem ir para produção

```
❌ NÃO INCLUIR:
├── __pycache__/                   # Cache Python
├── *.pyc                          # Bytecode compilado
├── .pytest_cache/                 # Cache pytest
├── .git/                          # Controle de versão
├── .venv/ ou venv/                # Ambiente virtual
├── .env                           # Variáveis de ambiente
├── .DS_Store                      # Arquivos sistema macOS
├── Thumbs.db                      # Arquivos sistema Windows
├── *.egg-info/                    # Metadados de build antigos
├── build/                         # Diretório de build temporário
├── dist/                          # Distribuições anteriores
└── .idea/ ou .vscode/             # Configurações IDE
```

---

## ⚙️ Configuração de Build

### 1. pyproject.toml (Configuração Principal)

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel", "setuptools-scm"]
build-backend = "setuptools.build_meta"

[project]
name = "biorempp"
dynamic = ["version"]
description = "Biological Remediation Pathway Predictor"
readme = "README.md"
license = {file = "LICENSE.txt"}
authors = [
    {name = "Douglas Felipe", email = "douglas@biorempp.org"}
]
maintainers = [
    {name = "Douglas Felipe", email = "douglas@biorempp.org"}
]
keywords = ["bioinformatics", "remediation", "pathway", "analysis"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Scientific/Engineering :: Bio-Informatics",
]
requires-python = ">=3.8"
dependencies = [
    "pandas>=1.3.0",
    "numpy>=1.20.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=6.0",
    "pytest-cov",
    "flake8",
    "black",
    "isort",
    "mypy",
]
docs = [
    "sphinx",
    "sphinx-rtd-theme",
    "myst-parser",
]
test = [
    "pytest>=6.0",
    "pytest-cov",
    "tox",
]

[project.urls]
Homepage = "https://github.com/DougFelipe/biorempp"
Documentation = "https://biorempp.readthedocs.io"
Repository = "https://github.com/DougFelipe/biorempp.git"
Issues = "https://github.com/DougFelipe/biorempp/issues"
Changelog = "https://github.com/DougFelipe/biorempp/blob/main/CHANGELOG.md"

[project.scripts]
biorempp = "biorempp.main:main"

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
biorempp = ["data/*.csv", "data/*.txt"]

[tool.setuptools_scm]
write_to = "src/biorempp/metadata/version.py"
version_scheme = "post-release"
local_scheme = "node-and-date"
```

### 2. MANIFEST.in (Arquivos Adicionais)

```ini
# Documentação
include README.md
include LICENSE.txt
include AUTHORS.md
include CHANGELOG.md
include CONTRIBUTING.md

# Configuração
include pyproject.toml
include setup.cfg
include requirements.txt
include tox.ini

# Dados
recursive-include src/biorempp/data *.csv *.txt

# Testes (opcionais na distribuição)
recursive-include tests *.py
include conftest.py

# Documentação
recursive-include docs *.md *.rst *.txt
recursive-include notebooks *.ipynb

# Excluir arquivos desnecessários
global-exclude *.pyc
global-exclude *.pyo
global-exclude *.egg-info
global-exclude __pycache__
global-exclude .git
global-exclude .pytest_cache
prune build
prune dist
```

### 3. setup.cfg (Configuração de Ferramentas)

```ini
[metadata]
name = biorempp
author = Douglas Felipe
author_email = douglas@biorempp.org
description = Biological Remediation Pathway Predictor
long_description = file: README.md
long_description_content_type = text/markdown
url = https://github.com/DougFelipe/biorempp
project_urls =
    Bug Tracker = https://github.com/DougFelipe/biorempp/issues
    Documentation = https://biorempp.readthedocs.io
    Source Code = https://github.com/DougFelipe/biorempp
classifiers =
    Development Status :: 4 - Beta
    Intended Audience :: Science/Research
    License :: OSI Approved :: MIT License
    Operating System :: OS Independent
    Programming Language :: Python :: 3
    Programming Language :: Python :: 3.8
    Programming Language :: Python :: 3.9
    Programming Language :: Python :: 3.10
    Programming Language :: Python :: 3.11
    Programming Language :: Python :: 3.12
    Topic :: Scientific/Engineering :: Bio-Informatics

[options]
package_dir =
    = src
packages = find:
python_requires = >=3.8
install_requires =
    pandas>=1.3.0
    numpy>=1.20.0

[options.packages.find]
where = src

[options.package_data]
biorempp = data/*.csv, data/*.txt

[options.entry_points]
console_scripts =
    biorempp = biorempp.main:main

[options.extras_require]
dev =
    pytest>=6.0
    pytest-cov
    flake8
    black
    isort
    mypy
docs =
    sphinx
    sphinx-rtd-theme
    myst-parser
test =
    pytest>=6.0
    pytest-cov
    tox

# Configuração de ferramentas
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude =
    .git,
    __pycache__,
    build,
    dist,
    *.egg-info

[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

---

## 🔨 Processo de Build Local

### 1. Preparação do Ambiente

```bash
# Criar ambiente virtual limpo
python -m venv build_env
source build_env/bin/activate  # Linux/Mac
# ou
build_env\Scripts\activate     # Windows

# Atualizar ferramentas de build
pip install --upgrade pip
pip install --upgrade setuptools wheel build twine
```

### 2. Script Automatizado de Build

Crie o arquivo `scripts/build_release.py`:

```python
#!/usr/bin/env python3
"""
Script automatizado para build de release do BioRemPP
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import tempfile


class ReleaseBuilder:
    def __init__(self, project_root=None):
        self.project_root = Path(project_root or os.getcwd())
        self.build_dir = self.project_root / "build"
        self.dist_dir = self.project_root / "dist"

    def clean_previous_builds(self):
        """Remove builds anteriores"""
        print("🧹 Limpando builds anteriores...")

        dirs_to_clean = [
            self.build_dir,
            self.dist_dir,
            self.project_root / "src" / "biorempp.egg-info"
        ]

        for dir_path in dirs_to_clean:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"   ✅ Removido: {dir_path}")

    def validate_project_structure(self):
        """Valida estrutura do projeto"""
        print("🔍 Validando estrutura do projeto...")

        required_files = [
            "pyproject.toml",
            "README.md",
            "LICENSE.txt",
            "src/biorempp/__init__.py",
            "src/biorempp/main.py"
        ]

        missing_files = []
        for file_path in required_files:
            full_path = self.project_root / file_path
            if not full_path.exists():
                missing_files.append(file_path)
            else:
                print(f"   ✅ {file_path}")

        if missing_files:
            print(f"   ❌ Arquivos obrigatórios não encontrados:")
            for file_path in missing_files:
                print(f"      - {file_path}")
            return False

        return True

    def run_tests(self):
        """Executa testes antes do build"""
        print("🧪 Executando testes...")

        try:
            result = subprocess.run([
                sys.executable, "-m", "pytest", "tests/", "-v"
            ], cwd=self.project_root, capture_output=True, text=True)

            if result.returncode == 0:
                print("   ✅ Todos os testes passaram")
                return True
            else:
                print(f"   ❌ Testes falharam:")
                print(result.stdout)
                print(result.stderr)
                return False

        except FileNotFoundError:
            print("   ⚠️ pytest não encontrado - pulando testes")
            return True

    def build_distributions(self):
        """Constrói as distribuições wheel e source"""
        print("📦 Construindo distribuições...")

        try:
            # Build usando python -m build
            result = subprocess.run([
                sys.executable, "-m", "build"
            ], cwd=self.project_root, capture_output=True, text=True)

            if result.returncode == 0:
                print("   ✅ Build concluído com sucesso")

                # Listar arquivos gerados
                if self.dist_dir.exists():
                    print("   📄 Arquivos gerados:")
                    for file_path in self.dist_dir.glob("*"):
                        size_mb = file_path.stat().st_size / (1024 * 1024)
                        print(f"      - {file_path.name} ({size_mb:.2f} MB)")

                return True
            else:
                print(f"   ❌ Build falhou:")
                print(result.stdout)
                print(result.stderr)
                return False

        except FileNotFoundError:
            print("   ❌ Ferramenta 'build' não encontrada")
            print("   💡 Instale com: pip install build")
            return False

    def validate_distributions(self):
        """Valida as distribuições geradas"""
        print("🔍 Validando distribuições...")

        if not self.dist_dir.exists():
            print("   ❌ Diretório dist/ não encontrado")
            return False

        # Verificar se temos wheel e source distribution
        wheel_files = list(self.dist_dir.glob("*.whl"))
        source_files = list(self.dist_dir.glob("*.tar.gz"))

        if not wheel_files:
            print("   ❌ Arquivo .whl não encontrado")
            return False

        if not source_files:
            print("   ❌ Arquivo .tar.gz não encontrado")
            return False

        print(f"   ✅ Wheel: {wheel_files[0].name}")
        print(f"   ✅ Source: {source_files[0].name}")

        # Validar com twine
        try:
            result = subprocess.run([
                "twine", "check", str(self.dist_dir / "*")
            ], capture_output=True, text=True)

            if result.returncode == 0:
                print("   ✅ Validação twine passou")
                return True
            else:
                print(f"   ❌ Validação twine falhou:")
                print(result.stdout)
                print(result.stderr)
                return False

        except FileNotFoundError:
            print("   ⚠️ twine não encontrado - validação pulada")
            return True

    def build_release(self, run_tests=True):
        """Executa processo completo de build"""
        print("🚀 INICIANDO BUILD DE RELEASE")
        print("=" * 50)

        steps = [
            ("Limpeza", self.clean_previous_builds),
            ("Validação", self.validate_project_structure),
        ]

        if run_tests:
            steps.append(("Testes", self.run_tests))

        steps.extend([
            ("Build", self.build_distributions),
            ("Validação Final", self.validate_distributions)
        ])

        for step_name, step_func in steps:
            print(f"\n📋 {step_name}...")
            if not step_func():
                print(f"\n❌ FALHA na etapa: {step_name}")
                return False

        print("\n🎉 BUILD CONCLUÍDO COM SUCESSO!")
        print("=" * 50)
        print("📦 Arquivos prontos para distribuição:")

        for file_path in self.dist_dir.glob("*"):
            print(f"   📄 {file_path}")

        print("\n💡 Próximos passos:")
        print("   1. Testar no TestPyPI: twine upload --repository testpypi dist/*")
        print("   2. Testar instalação: pip install -i https://test.pypi.org/simple/ biorempp")
        print("   3. Upload final: twine upload dist/*")

        return True


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Build release do BioRemPP")
    parser.add_argument("--no-tests", action="store_true",
                       help="Pular execução de testes")
    parser.add_argument("--project-root",
                       help="Diretório raiz do projeto")

    args = parser.parse_args()

    builder = ReleaseBuilder(args.project_root)
    success = builder.build_release(run_tests=not args.no_tests)

    sys.exit(0 if success else 1)
```

### 3. Executar Build

```bash
# Usando o script automatizado
python scripts/build_release.py

# Ou manualmente
python -m build

# Verificar distribuições
twine check dist/*
```

---

## 🧪 Teste no TestPyPI

### 1. Configuração de Credenciais

#### Criar conta no TestPyPI
1. Acesse: https://test.pypi.org/account/register/
2. Confirme email
3. Configure 2FA (recomendado)

#### Configurar API Token
1. Acesse: https://test.pypi.org/manage/account/#api-tokens
2. Clique em "Add API token"
3. Nome: `biorempp-token`
4. Escopo: `Entire account` (para primeiro upload)

#### Configurar ~/.pypirc

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-your-actual-api-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-testpypi-token-here
```

### 2. Upload para TestPyPI

```bash
# Upload para TestPyPI
twine upload --repository testpypi dist/*

# Verificar upload
# Acesse: https://test.pypi.org/project/biorempp/
```

### 3. Teste de Instalação

```bash
# Criar ambiente virtual limpo
python -m venv test_install
source test_install/bin/activate  # Linux/Mac
# ou
test_install\Scripts\activate     # Windows

# Instalar do TestPyPI
pip install -i https://test.pypi.org/simple/ biorempp

# Testar funcionalidade básica
python -c "import biorempp; print('Import OK')"
biorempp --help

# Testar com dados
echo ">K00001\n>K00002" > test_data.txt
biorempp --input test_data.txt --database biorempp

# Limpar ambiente
deactivate
rm -rf test_install
```

### 4. Script de Teste Automatizado

Crie `scripts/test_distribution.py`:

```python
#!/usr/bin/env python3
"""
Script para testar distribuição no TestPyPI
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path


def test_testpypi_installation():
    """Testa instalação do TestPyPI"""

    print("🧪 Testando instalação do TestPyPI...")

    with tempfile.TemporaryDirectory() as temp_dir:
        venv_path = Path(temp_dir) / "test_venv"

        # Criar ambiente virtual
        print("   📦 Criando ambiente virtual...")
        subprocess.run([
            sys.executable, "-m", "venv", str(venv_path)
        ], check=True)

        # Determinar executável python do venv
        if os.name == 'nt':  # Windows
            python_exe = venv_path / "Scripts" / "python.exe"
            pip_exe = venv_path / "Scripts" / "pip.exe"
        else:  # Unix-like
            python_exe = venv_path / "bin" / "python"
            pip_exe = venv_path / "bin" / "pip"

        try:
            # Instalar do TestPyPI
            print("   ⬇️ Instalando do TestPyPI...")
            subprocess.run([
                str(pip_exe), "install",
                "-i", "https://test.pypi.org/simple/",
                "biorempp"
            ], check=True, capture_output=True)

            # Testar import
            print("   🔍 Testando import...")
            result = subprocess.run([
                str(python_exe), "-c", "import biorempp; print('✅ Import OK')"
            ], capture_output=True, text=True)

            if result.returncode == 0:
                print(f"   {result.stdout.strip()}")
            else:
                print(f"   ❌ Import falhou: {result.stderr}")
                return False

            # Testar CLI
            print("   🖥️ Testando CLI...")
            biorempp_exe = venv_path / ("Scripts" if os.name == 'nt' else "bin") / "biorempp"

            if biorempp_exe.exists():
                result = subprocess.run([
                    str(biorempp_exe), "--help"
                ], capture_output=True, text=True)

                if result.returncode == 0:
                    print("   ✅ CLI funcionando")
                else:
                    print(f"   ⚠️ CLI com problemas: {result.stderr}")
            else:
                print("   ⚠️ Executável CLI não encontrado")

            # Teste funcional básico
            print("   ⚙️ Testando funcionalidade...")
            test_script = """
import biorempp
from biorempp.pipelines import run_biorempp_processing_pipeline
import tempfile
import os

# Criar arquivo de teste
with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
    f.write('>K00001\\n>K00002\\n>K00003\\n')
    test_file = f.name

try:
    # Teste básico
    with tempfile.TemporaryDirectory() as output_dir:
        result = run_biorempp_processing_pipeline(
            input_file=test_file,
            database='biorempp',
            output_dir=output_dir,
            quiet=True
        )
    print('✅ Teste funcional OK')
except Exception as e:
    print(f'⚠️ Teste funcional com problemas: {e}')
finally:
    os.unlink(test_file)
"""

            result = subprocess.run([
                str(python_exe), "-c", test_script
            ], capture_output=True, text=True)

            if result.returncode == 0:
                print(f"   {result.stdout.strip()}")
            else:
                print(f"   ⚠️ Teste funcional: {result.stderr}")

            print("   🎉 Teste de instalação concluído!")
            return True

        except subprocess.CalledProcessError as e:
            print(f"   ❌ Erro durante teste: {e}")
            return False


if __name__ == "__main__":
    success = test_testpypi_installation()
    sys.exit(0 if success else 1)
```

---

## 🏷️ Versionamento e Tags

### 1. Estratégia de Versionamento

Usar **Semantic Versioning (SemVer)**:

```
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]

Exemplos:
- 1.0.0        # Release estável
- 1.0.1        # Bug fix
- 1.1.0        # Nova funcionalidade
- 2.0.0        # Breaking changes
- 1.0.0-alpha.1 # Pre-release
- 1.0.0-beta.2  # Beta
- 1.0.0-rc.1    # Release candidate
```

### 2. Configuração Automática com setuptools-scm

O `setuptools-scm` gera versões automaticamente a partir de tags Git:

```python
# src/biorempp/metadata/version.py (gerado automaticamente)
# coding: utf-8
__version__ = "1.0.0"
```

### 3. Script de Release

Crie `scripts/release.py`:

```python
#!/usr/bin/env python3
"""
Script para criar releases com versionamento automático
"""

import subprocess
import sys
from pathlib import Path


def create_release(version, description=""):
    """Cria release com tag e push"""

    print(f"🏷️ Criando release {version}...")

    # Validar formato da versão
    import re
    version_pattern = r'^\d+\.\d+\.\d+(-[\w\.]+)?$'
    if not re.match(version_pattern, version):
        print(f"❌ Formato de versão inválido: {version}")
        print("💡 Use formato: MAJOR.MINOR.PATCH[-PRERELEASE]")
        return False

    try:
        # Verificar se estamos na branch correta
        result = subprocess.run([
            "git", "branch", "--show-current"
        ], capture_output=True, text=True, check=True)

        current_branch = result.stdout.strip()
        print(f"📍 Branch atual: {current_branch}")

        # Verificar se não há mudanças não commitadas
        result = subprocess.run([
            "git", "status", "--porcelain"
        ], capture_output=True, text=True, check=True)

        if result.stdout.strip():
            print("❌ Há mudanças não commitadas")
            print("💡 Commit todas as mudanças antes do release")
            return False

        # Criar tag
        tag_message = f"Release {version}"
        if description:
            tag_message += f": {description}"

        subprocess.run([
            "git", "tag", "-a", f"v{version}", "-m", tag_message
        ], check=True)

        print(f"✅ Tag v{version} criada")

        # Push tag
        subprocess.run([
            "git", "push", "origin", f"v{version}"
        ], check=True)

        print(f"✅ Tag v{version} enviada para origin")

        print(f"🎉 Release {version} criado com sucesso!")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Erro durante release: {e}")
        return False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Criar release")
    parser.add_argument("version", help="Versão do release (ex: 1.0.0)")
    parser.add_argument("--description", help="Descrição do release")

    args = parser.parse_args()

    success = create_release(args.version, args.description)
    sys.exit(0 if success else 1)
```

### 4. Fluxo de Release Completo

```bash
# 1. Preparar código
git add .
git commit -m "Prepare for release v1.0.0"

# 2. Criar release
python scripts/release.py 1.0.0 --description "Initial stable release"

# 3. Build com nova versão
python scripts/build_release.py

# 4. Upload para TestPyPI
twine upload --repository testpypi dist/*

# 5. Testar
python scripts/test_distribution.py

# 6. Upload para PyPI oficial
twine upload dist/*
```

---

## 🤖 Automação com GitHub Actions

### 1. Workflow de CI/CD

Crie `.github/workflows/release.yml`:

```yaml
name: Build and Release

on:
  push:
    tags:
      - 'v*'
  workflow_dispatch:
    inputs:
      test_only:
        description: 'Test only (upload to TestPyPI)'
        required: false
        default: 'false'

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, "3.10", "3.11", "3.12"]

    steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .[test]

    - name: Run tests
      run: |
        pytest tests/ -v --cov=biorempp --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      if: matrix.python-version == '3.11'

  build:
    needs: test
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.11"

    - name: Install build dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine

    - name: Build distributions
      run: python -m build

    - name: Check distributions
      run: twine check dist/*

    - name: Upload build artifacts
      uses: actions/upload-artifact@v3
      with:
        name: distributions
        path: dist/

  publish-testpypi:
    needs: build
    runs-on: ubuntu-latest
    if: github.event.inputs.test_only == 'true' || contains(github.ref, 'alpha') || contains(github.ref, 'beta')

    steps:
    - name: Download artifacts
      uses: actions/download-artifact@v3
      with:
        name: distributions
        path: dist/

    - name: Publish to TestPyPI
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        repository_url: https://test.pypi.org/legacy/
        password: ${{ secrets.TEST_PYPI_API_TOKEN }}

  publish-pypi:
    needs: build
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && startsWith(github.ref, 'refs/tags/v') && !contains(github.ref, 'alpha') && !contains(github.ref, 'beta')

    steps:
    - name: Download artifacts
      uses: actions/download-artifact@v3
      with:
        name: distributions
        path: dist/

    - name: Publish to PyPI
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        password: ${{ secrets.PYPI_API_TOKEN }}

  create-release:
    needs: [publish-pypi]
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && startsWith(github.ref, 'refs/tags/v')

    steps:
    - uses: actions/checkout@v4

    - name: Create GitHub Release
      uses: actions/create-release@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        tag_name: ${{ github.ref }}
        release_name: Release ${{ github.ref }}
        body: |
          🚀 **BioRemPP ${{ github.ref_name }}**

          ## 📦 Installation
          ```bash
          pip install biorempp
          ```

          ## 📋 Changes
          See [CHANGELOG.md](CHANGELOG.md) for detailed changes.

          ## 📚 Documentation
          - [Documentation](https://biorempp.readthedocs.io)
          - [Examples](https://github.com/DougFelipe/biorempp/tree/main/notebooks)
        draft: false
        prerelease: ${{ contains(github.ref, 'alpha') || contains(github.ref, 'beta') || contains(github.ref, 'rc') }}
```

### 2. Configurar Secrets

No GitHub, vá para Settings → Secrets → Actions:

```
TEST_PYPI_API_TOKEN = pypi-xxxxx (token do TestPyPI)
PYPI_API_TOKEN = pypi-xxxxx (token do PyPI oficial)
```

---

## ✅ Checklist de Produção

### Antes do Release

- [ ] **Código**
  - [ ] Todos os testes passando
  - [ ] Cobertura de testes > 80%
  - [ ] Documentação atualizada
  - [ ] Sem TODOs ou FIXMEs críticos

- [ ] **Metadados**
  - [ ] README.md atualizado
  - [ ] CHANGELOG.md com mudanças
  - [ ] LICENSE.txt correto
  - [ ] Versão atualizada

- [ ] **Configuração**
  - [ ] pyproject.toml completo
  - [ ] Dependências corretas
  - [ ] Entry points configurados
  - [ ] Classificadores adequados

- [ ] **Build**
  - [ ] Build local bem-sucedido
  - [ ] Validação twine OK
  - [ ] Tamanho razoável (< 50MB)

### Durante o Release

- [ ] **TestPyPI**
  - [ ] Upload bem-sucedido
  - [ ] Instalação teste OK
  - [ ] Funcionalidades básicas OK
  - [ ] CLI funcionando

- [ ] **PyPI Oficial**
  - [ ] Upload bem-sucedido
  - [ ] Página do projeto OK
  - [ ] Downloads funcionando

### Após o Release

- [ ] **GitHub**
  - [ ] Tag criada
  - [ ] Release notes publicadas
  - [ ] Assets anexados

- [ ] **Documentação**
  - [ ] Docs atualizadas
  - [ ] Exemplos funcionando
  - [ ] Colab notebook atualizado

---

## 🔧 Troubleshooting

### Problemas Comuns

#### 1. "Package already exists"
```bash
# Erro: File already exists
# Solução: Incrementar versão
python scripts/release.py 1.0.1
```

#### 2. "Invalid distribution format"
```bash
# Erro: Invalid wheel/tar.gz
# Solução: Verificar MANIFEST.in e pyproject.toml
twine check dist/*
```

#### 3. "Import error after installation"
```bash
# Erro: ModuleNotFoundError
# Solução: Verificar estrutura de packages
[tool.setuptools.packages.find]
where = ["src"]
```

#### 4. "CLI command not found"
```bash
# Erro: biorempp command not found
# Solução: Verificar entry points
[project.scripts]
biorempp = "biorempp.main:main"
```

#### 5. "Missing data files"
```bash
# Erro: Data files not included
# Solução: Configurar package_data
[tool.setuptools.package-data]
biorempp = ["data/*.csv", "data/*.txt"]
```

### Debug de Distribuições

```bash
# Extrair e examinar wheel
unzip -l dist/biorempp-*.whl

# Examinar tar.gz
tar -tzf dist/biorempp-*.tar.gz

# Testar instalação em ambiente limpo
python -m venv debug_env
source debug_env/bin/activate
pip install dist/biorempp-*.whl
python -c "import biorempp; print(biorempp.__file__)"
```

### Logs e Diagnósticos

```bash
# Upload com logs detalhados
twine upload --verbose dist/*

# Build com logs
python -m build --verbose

# Teste com logs
pytest -v -s --tb=long
```

---

## 📚 Recursos Adicionais

### Documentação Oficial
- [Python Packaging Guide](https://packaging.python.org/)
- [PyPI Help](https://pypi.org/help/)
- [setuptools Documentation](https://setuptools.pypa.io/)

### Ferramentas Úteis
- [check-manifest](https://github.com/mgedmin/check-manifest) - Verificar MANIFEST.in
- [pyroma](https://github.com/regebro/pyroma) - Verificar metadados
- [wheel](https://wheel.readthedocs.io/) - Manipular wheels

### Templates e Exemplos
- [PyPA Sample Project](https://github.com/pypa/sampleproject)
- [Cookiecutter PyPackage](https://github.com/audreyfeldroy/cookiecutter-pypackage)

---

**🎯 Próximos Passos Recomendados:**

1. **Configurar estrutura** - Organizar arquivos conforme este guia
2. **Testar build local** - Usar script automatizado
3. **Configurar TestPyPI** - Criar conta e testar upload
4. **Implementar CI/CD** - GitHub Actions para automação
5. **Primeira versão beta** - Release 0.1.0-beta.1 no TestPyPI
6. **Documentação completa** - ReadTheDocs + exemplos
7. **Release estável** - Versão 1.0.0 no PyPI oficial

Este guia cobre todo o ciclo de vida de distribuição. Use-o como referência durante o desenvolvimento e releases do BioRemPP! 🚀
