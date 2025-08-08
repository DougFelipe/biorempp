#!/usr/bin/env python3
"""
Script completo para gerenciar todo o processo de distribuição
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def main():
    """Função principal do script de distribuição"""

    parser = argparse.ArgumentParser(
        description="Gerenciador completo de distribuição BioRemPP"
    )

    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")

    # Comando build
    build_parser = subparsers.add_parser("build", help="Construir distribuições")
    build_parser.add_argument(
        "--no-tests", action="store_true", help="Pular execução de testes"
    )

    # Comando release
    release_parser = subparsers.add_parser("release", help="Criar release com tag")
    release_parser.add_argument("version", help="Versão (ex: 1.0.0)")
    release_parser.add_argument("--description", help="Descrição do release")

    # Comando test-pypi
    test_parser = subparsers.add_parser("test-pypi", help="Upload para TestPyPI")

    # Comando publish
    publish_parser = subparsers.add_parser("publish", help="Upload para PyPI oficial")

    # Comando full-release
    full_parser = subparsers.add_parser(
        "full-release", help="Processo completo de release"
    )
    full_parser.add_argument("version", help="Versão (ex: 1.0.0)")
    full_parser.add_argument("--description", help="Descrição do release")
    full_parser.add_argument(
        "--skip-testpypi",
        action="store_true",
        help="Pular TestPyPI e ir direto para PyPI",
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Executar comando
    if args.command == "build":
        return run_build(skip_tests=args.no_tests)
    elif args.command == "release":
        return run_release(args.version, args.description)
    elif args.command == "test-pypi":
        return run_test_pypi()
    elif args.command == "publish":
        return run_publish()
    elif args.command == "full-release":
        return run_full_release(
            args.version, args.description, skip_testpypi=args.skip_testpypi
        )

    return 1


def run_build(skip_tests=False):
    """Executa build das distribuições"""
    from build_release import ReleaseBuilder

    builder = ReleaseBuilder()
    success = builder.build_release(run_tests=not skip_tests)
    return 0 if success else 1


def run_release(version, description=None):
    """Cria release com tag"""
    from release import create_release

    success = create_release(version, description or "")
    return 0 if success else 1


def run_test_pypi():
    """Upload para TestPyPI"""
    print("🧪 Fazendo upload para TestPyPI...")

    try:
        result = subprocess.run(
            ["twine", "upload", "--repository", "testpypi", "dist/*"], check=True
        )

        print("✅ Upload para TestPyPI concluído!")
        print("💡 Teste a instalação com:")
        print("   pip install -i https://test.pypi.org/simple/ biorempp")
        return 0

    except subprocess.CalledProcessError as e:
        print(f"❌ Falha no upload para TestPyPI: {e}")
        return 1
    except FileNotFoundError:
        print("❌ twine não encontrado. Instale com: pip install twine")
        return 1


def run_publish():
    """Upload para PyPI oficial"""
    print("🚀 Fazendo upload para PyPI oficial...")

    # Confirmação
    response = input("⚠️ Tem certeza que quer publicar no PyPI oficial? (y/N): ")
    if response.lower() != "y":
        print("Operação cancelada.")
        return 1

    try:
        result = subprocess.run(["twine", "upload", "dist/*"], check=True)

        print("✅ Upload para PyPI concluído!")
        print("🎉 Pacote publicado com sucesso!")
        print("💡 Instale com: pip install biorempp")
        return 0

    except subprocess.CalledProcessError as e:
        print(f"❌ Falha no upload para PyPI: {e}")
        return 1


def run_full_release(version, description=None, skip_testpypi=False):
    """Processo completo de release"""
    print("🚀 INICIANDO PROCESSO COMPLETO DE RELEASE")
    print("=" * 50)

    steps = [
        ("Criando release e tag", lambda: run_release(version, description)),
        ("Construindo distribuições", lambda: run_build()),
    ]

    if not skip_testpypi:
        steps.append(("Upload TestPyPI", run_test_pypi))
        steps.append(("Aguardando confirmação", wait_for_testpypi_confirmation))

    steps.append(("Upload PyPI oficial", run_publish))

    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")

        result = step_func()
        if result != 0:
            print(f"\n❌ FALHA na etapa: {step_name}")
            return result

    print("\n🎉 RELEASE COMPLETO CONCLUÍDO COM SUCESSO!")
    print("=" * 50)
    return 0


def wait_for_testpypi_confirmation():
    """Aguarda confirmação do teste no TestPyPI"""
    print("🔍 Aguardando confirmação do teste no TestPyPI...")
    print("💡 Teste a instalação e funcionalidade:")
    print("   pip install -i https://test.pypi.org/simple/ biorempp")
    print("   python -c 'import biorempp; print(\"OK\")'")

    response = input("\n✅ Testes no TestPyPI passaram? (y/N): ")
    if response.lower() != "y":
        print("❌ Testes falharam - abortando release")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
