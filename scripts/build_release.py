#!/usr/bin/env python3
"""
Script automatizado para build de release do BioRemPP
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


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
            self.project_root / "src" / "biorempp.egg-info",
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
            "src/biorempp/main.py",
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
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "tests/", "-v"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
            )

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
            result = subprocess.run(
                [sys.executable, "-m", "build"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
            )

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
            result = subprocess.run(
                ["twine", "check", str(self.dist_dir / "*")],
                capture_output=True,
                text=True,
            )

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

        steps.extend(
            [
                ("Build", self.build_distributions),
                ("Validação Final", self.validate_distributions),
            ]
        )

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
        print(
            "   2. Testar instalação: pip install -i https://test.pypi.org/simple/ biorempp"
        )
        print("   3. Upload final: twine upload dist/*")

        return True


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Build release do BioRemPP")
    parser.add_argument(
        "--no-tests", action="store_true", help="Pular execução de testes"
    )
    parser.add_argument("--project-root", help="Diretório raiz do projeto")

    args = parser.parse_args()

    builder = ReleaseBuilder(args.project_root)
    success = builder.build_release(run_tests=not args.no_tests)

    sys.exit(0 if success else 1)
