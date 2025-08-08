#!/usr/bin/env python3
"""
BioRemPP Package Builder

Script automatizado para compilar e distribuir o pacote BioRemPP.
Este script realiza limpeza, testes, construção e validação do pacote.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


class PackageBuilder:
    """Construtor automatizado do pacote BioRemPP."""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.dist_dir = self.project_root / "dist"
        self.build_dir = self.project_root / "build"
        self.egg_info_dir = self.project_root / "src" / "biorempp.egg-info"

    def print_step(self, step_name: str):
        """Imprime o nome da etapa atual."""
        print(f"\n{'='*60}")
        print(f"🔧 {step_name}")
        print(f"{'='*60}")

    def clean_previous_builds(self):
        """Remove builds anteriores."""
        self.print_step("Limpando builds anteriores")

        directories_to_clean = [self.dist_dir, self.build_dir, self.egg_info_dir]

        for directory in directories_to_clean:
            if directory.exists():
                print(f"   Removendo: {directory}")
                shutil.rmtree(directory)
            else:
                print(f"   ✅ Já limpo: {directory}")

    def check_dependencies(self):
        """Verifica se as dependências necessárias estão instaladas."""
        self.print_step("Verificando dependências")

        required_packages = ["build", "twine", "wheel"]
        missing_packages = []

        for package in required_packages:
            try:
                subprocess.run(
                    [sys.executable, "-c", f"import {package}"],
                    check=True,
                    capture_output=True,
                )
                print(f"   ✅ {package}")
            except subprocess.CalledProcessError:
                missing_packages.append(package)
                print(f"   ❌ {package}")

        if missing_packages:
            print(f"\n📦 Instalando dependências ausentes: {missing_packages}")
            subprocess.run([sys.executable, "-m", "pip", "install"] + missing_packages)

    def run_tests(self):
        """Execute testes básicos"""
        print("🔧 Executando testes")
        print("=" * 60)

        try:
            # Teste de importação básica
            import_cmd = (
                "import sys; sys.path.insert(0, 'src'); "
                "import biorempp; print('Importacao bem-sucedida')"
            )
            result = subprocess.run(
                [sys.executable, "-c", import_cmd],
                capture_output=True,
                text=True,
                check=True,
            )

            print("   ✅ Importação do pacote")

            # Teste de linha de comando (se disponível)
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "src.biorempp.main", "--help"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )

                if result.returncode == 0:
                    print("   ✅ Interface de linha de comando")
                else:
                    print("   ⚠️ CLI com problemas (não crítico)")

            except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
                print("   ⚠️ CLI não testável (não crítico)")

            return True

        except subprocess.CalledProcessError as e:
            print(f"   ❌ Erro nos testes: {e}")
            if e.stderr:
                print(f"   Saída do erro: {e.stderr}")
            return False

    def build_package(self):
        """Constrói o pacote."""
        self.print_step("Construindo o pacote")

        try:
            # Construir com build (recomendado pelo PEP 517)
            subprocess.run(
                [sys.executable, "-m", "build"], cwd=self.project_root, check=True
            )

            print("   ✅ Pacote construído com sucesso")

            # Listar arquivos criados
            if self.dist_dir.exists():
                print("\n   📦 Arquivos criados:")
                for file in self.dist_dir.iterdir():
                    size_mb = file.stat().st_size / (1024 * 1024)
                    print(f"      {file.name} ({size_mb:.2f} MB)")

        except subprocess.CalledProcessError as e:
            print(f"   ❌ Erro na construção: {e}")
            return False

        return True

    def validate_package(self):
        """Valida o pacote construído."""
        self.print_step("Validando o pacote")

        try:
            # Verificar se os arquivos foram criados
            if not self.dist_dir.exists():
                print("   ❌ Diretório dist não encontrado")
                return False

            # Listar arquivos gerados
            whl_files = list(self.dist_dir.glob("*.whl"))
            tar_files = list(self.dist_dir.glob("*.tar.gz"))
            dist_files = whl_files + tar_files

            if not dist_files:
                print("   ❌ Nenhum arquivo de distribuição encontrado")
                return False

            # Validar com twine
            subprocess.run(
                [sys.executable, "-m", "twine", "check"] + [str(f) for f in dist_files],
                check=True,
            )

            print("   ✅ Pacote válido")
            return True

        except subprocess.CalledProcessError as e:
            print(f"   ❌ Erro na validação: {e}")
            return False

    def show_upload_instructions(self):
        """Mostra instruções para upload."""
        self.print_step("Instruções de Upload")

        print(
            """
📤 INSTRUÇÕES PARA UPLOAD DO PACOTE:

1. 🔐 Upload para TestPyPI (recomendado para testes):
   python -m twine upload --repository testpypi dist/*

2. 🌐 Upload para PyPI (produção):
   python -m twine upload dist/*

3. 📋 Antes do upload, certifique-se de:
   ✅ Ter conta no PyPI/TestPyPI
   ✅ Configurar credenciais (.pypirc ou variáveis de ambiente)
   ✅ Incrementar versão no pyproject.toml
   ✅ Atualizar CHANGELOG.md

4. 🧪 Para testar instalação do TestPyPI:
   pip install --index-url https://test.pypi.org/simple/ biorempp

5. 📦 Para instalação normal (após upload para PyPI):
   pip install biorempp

6. 🔄 Para desenvolvimento local:
   pip install -e .
        """
        )

    def build(self):
        """Executa o processo completo de build."""
        print("🧬 BioRemPP Package Builder")
        print("=" * 60)

        try:
            # Etapas do build
            self.clean_previous_builds()
            self.check_dependencies()

            if not self.run_tests():
                print("\n❌ Build interrompido devido a falhas nos testes")
                return False

            if not self.build_package():
                print("\n❌ Build interrompido devido a erro na construção")
                return False

            if not self.validate_package():
                print("\n❌ Build interrompido devido a erro na validação")
                return False

            self.show_upload_instructions()

            print(f"\n🎉 Build concluído com sucesso!")
            print(f"📁 Arquivos de distribuição em: {self.dist_dir}")

            return True

        except KeyboardInterrupt:
            print("\n⚠️ Build interrompido pelo usuário")
            return False
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
            return False


if __name__ == "__main__":
    builder = PackageBuilder()
    success = builder.build()
    sys.exit(0 if success else 1)
