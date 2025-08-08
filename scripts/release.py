#!/usr/bin/env python3
"""
Script para criar releases com versionamento automático
"""

import re
import subprocess
import sys


def create_release(version, description=""):
    """Cria release com tag e push"""

    print(f"🏷️ Criando release {version}...")

    # Validar formato da versão
    version_pattern = r"^\d+\.\d+\.\d+(-[\w\.]+)?$"
    if not re.match(version_pattern, version):
        print(f"❌ Formato de versão inválido: {version}")
        print("💡 Use formato: MAJOR.MINOR.PATCH[-PRERELEASE]")
        return False

    try:
        # Verificar se estamos na branch correta
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=True,
        )

        current_branch = result.stdout.strip()
        print(f"📍 Branch atual: {current_branch}")

        # Verificar se não há mudanças não commitadas
        result = subprocess.run(
            ["git", "status", "--porcelain"], capture_output=True, text=True, check=True
        )

        if result.stdout.strip():
            print("❌ Há mudanças não commitadas")
            print("💡 Commit todas as mudanças antes do release")
            return False

        # Criar tag
        tag_message = f"Release {version}"
        if description:
            tag_message += f": {description}"

        subprocess.run(
            ["git", "tag", "-a", f"v{version}", "-m", tag_message], check=True
        )

        print(f"✅ Tag v{version} criada")

        # Push tag
        subprocess.run(["git", "push", "origin", f"v{version}"], check=True)

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
