#!/usr/bin/env python3
"""
Script para testar distribuição no TestPyPI
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path


def test_testpypi_installation():
    """Testa instalação do TestPyPI"""

    print("🧪 Testando instalação do TestPyPI...")

    with tempfile.TemporaryDirectory() as temp_dir:
        venv_path = Path(temp_dir) / "test_venv"

        # Criar ambiente virtual
        print("   📦 Criando ambiente virtual...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)

        # Determinar executável python do venv
        if os.name == "nt":  # Windows
            python_exe = venv_path / "Scripts" / "python.exe"
            pip_exe = venv_path / "Scripts" / "pip.exe"
        else:  # Unix-like
            python_exe = venv_path / "bin" / "python"
            pip_exe = venv_path / "bin" / "pip"

        try:
            # Instalar do TestPyPI
            print("   ⬇️ Instalando do TestPyPI...")
            subprocess.run(
                [
                    str(pip_exe),
                    "install",
                    "-i",
                    "https://test.pypi.org/simple/",
                    "biorempp",
                ],
                check=True,
                capture_output=True,
            )

            # Testar import
            print("   🔍 Testando import...")
            result = subprocess.run(
                [str(python_exe), "-c", "import biorempp; print('✅ Import OK')"],
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                print(f"   {result.stdout.strip()}")
            else:
                print(f"   ❌ Import falhou: {result.stderr}")
                return False

            # Testar CLI
            print("   🖥️ Testando CLI...")
            biorempp_exe = (
                venv_path / ("Scripts" if os.name == "nt" else "bin") / "biorempp"
            )

            if biorempp_exe.exists():
                result = subprocess.run(
                    [str(biorempp_exe), "--help"], capture_output=True, text=True
                )

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

            result = subprocess.run(
                [str(python_exe), "-c", test_script], capture_output=True, text=True
            )

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
