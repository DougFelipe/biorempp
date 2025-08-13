#!/usr/bin/env python3
"""
PyPI Upload Manager - Script Maestro

Este script coordena todo o processo de configuração e upload para PyPI/TestPyPI.
Oferece um menu interativo para executar as tarefas mais comuns.

Usage:
    python scripts/pypi_manager.py
    python scripts/pypi_manager.py --setup
    python scripts/pypi_manager.py --test-upload
"""

import sys
import subprocess
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(title):
    """Print a formatted header."""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{title:^60}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}")


def print_success(message):
    """Print a success message."""
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")


def print_error(message):
    """Print an error message."""
    print(f"{Colors.RED}❌ {message}{Colors.END}")


def print_info(message):
    """Print an info message."""
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")


def run_script(script_name, args=None):
    """Run a Python script with optional arguments."""
    script_path = Path(__file__).parent / script_name
    cmd = [sys.executable, str(script_path)]
    
    if args:
        cmd.extend(args)
    
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        print_error(f"Script not found: {script_name}")
        return False


def check_pypirc_status():
    """Check the status of .pypirc configuration."""
    try:
        subprocess.run(
            [sys.executable, "scripts/create_pypirc.py", "--show-path"],
            capture_output=True,
            text=True
        )
        
        pypirc_path = Path.home() / ".pypirc"
        
        if pypirc_path.exists():
            try:
                with open(pypirc_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                has_testpypi = '[testpypi]' in content
                has_pypi = '[pypi]' in content
                has_placeholder = 'YOUR_' in content
                
                status = "🟢 Configurado"
                if has_placeholder:
                    status = "🟡 Parcial (tokens pendentes)"
                
                return {
                    'exists': True,
                    'has_testpypi': has_testpypi,
                    'has_pypi': has_pypi,
                    'has_placeholder': has_placeholder,
                    'status': status,
                    'path': pypirc_path
                }
            except Exception:
                return {
                    'exists': True,
                    'status': "🔴 Erro na leitura",
                    'path': pypirc_path
                }
        else:
            return {
                'exists': False,
                'status': "🔴 Não configurado",
                'path': pypirc_path
            }
            
    except Exception:
        return {
            'exists': False,
            'status': "🔴 Erro ao verificar",
            'path': "Desconhecido"
        }


def show_status():
    """Show current configuration status."""
    print_header("STATUS DA CONFIGURAÇÃO PYPI")
    
    # Check .pypirc
    pypirc_status = check_pypirc_status()
    print("\n📄 Arquivo .pypirc:")
    print(f"   Status: {pypirc_status['status']}")
    print(f"   Localização: {pypirc_status['path']}")
    
    if pypirc_status['exists']:
        if pypirc_status.get('has_testpypi'):
            print("   ✅ TestPyPI configurado")
        if pypirc_status.get('has_pypi'):
            print("   ✅ PyPI configurado")
        if pypirc_status.get('has_placeholder'):
            print("   ⚠️  Tokens pendentes de configuração")
    
    # Check project structure
    print("\n📁 Estrutura do Projeto:")
    pyproject_exists = Path("pyproject.toml").exists()
    src_exists = Path("src").exists()
    
    print(f"   pyproject.toml: {'✅' if pyproject_exists else '❌'}")
    print(f"   src/ directory: {'✅' if src_exists else '❌'}")
    
    # Check tools
    print("\n🛠️  Ferramentas:")
    try:
        subprocess.run([sys.executable, "-m", "build", "--help"],
                       capture_output=True, check=True)
        print("   build: ✅")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("   build: ❌ (pip install build)")
    
    try:
        subprocess.run(["twine", "--help"], capture_output=True, check=True)
        print("   twine: ✅")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("   twine: ❌ (pip install twine)")


def show_menu():
    """Show the main menu."""
    print_header("GERENCIADOR DE UPLOAD PYPI")
    
    print(f"\n{Colors.BOLD}Opções Disponíveis:{Colors.END}")
    print("1. 📊 Ver status da configuração")
    print("2. 🔧 Configurar .pypirc (criar/editar tokens)")
    print("3. 🧪 Upload para TestPyPI")
    print("4. 🚀 Upload para PyPI oficial")
    print("5. 📚 Ver documentação")
    print("6. 🛠️  Instalar ferramentas necessárias")
    print("0. ❌ Sair")
    
    return input(f"\n{Colors.YELLOW}Escolha uma opção (0-6): {Colors.END}")


def setup_pypirc():
    """Configure .pypirc file."""
    print_header("CONFIGURAÇÃO DO .PYPIRC")
    print("\nEste processo criará/atualizará seu arquivo .pypirc")
    print("Você precisará dos tokens do PyPI e TestPyPI")
    
    choice = input("\nDeseja usar modo interativo? [Y/n]: ")
    if choice.lower() in ['', 'y', 'yes', 's', 'sim']:
        success = run_script("create_pypirc.py", ["--interactive"])
    else:
        success = run_script("create_pypirc.py", ["--help"])
    
    if success:
        print_success("Configuração concluída!")
    else:
        print_error("Erro na configuração")


def test_upload():
    """Upload to TestPyPI."""
    print_header("UPLOAD PARA TESTPYPI")
    
    pypirc_status = check_pypirc_status()
    if not pypirc_status['exists']:
        print_error("Arquivo .pypirc não encontrado!")
        print("Execute a opção 2 primeiro para configurar")
        return
    
    print("Iniciando upload para TestPyPI...")
    success = run_script("upload_to_testpypi.py")
    
    if success:
        print_success("Upload para TestPyPI concluído!")
    else:
        print_error("Erro no upload para TestPyPI")


def production_upload():
    """Upload to PyPI."""
    print_header("UPLOAD PARA PYPI OFICIAL")
    
    print(f"{Colors.YELLOW}⚠️  ATENÇÃO: Upload para PyPI OFICIAL{Colors.END}")
    print("Certifique-se de que:")
    print("✅ Testou no TestPyPI primeiro")
    print("✅ Versão está correta")
    print("✅ Não é possível sobrescrever versões")
    
    confirm = input(f"\n{Colors.RED}Confirma upload para PyPI oficial? [y/N]: {Colors.END}")
    
    if confirm.lower() in ['y', 'yes', 's', 'sim']:
        try:
            subprocess.run(["twine", "upload", "--repository", "pypi", "dist/*"], check=True)
            print_success("Upload para PyPI oficial concluído!")
        except subprocess.CalledProcessError:
            print_error("Erro no upload para PyPI oficial")
        except FileNotFoundError:
            print_error("twine não encontrado. Instale com: pip install twine")
    else:
        print("Upload cancelado")


def show_documentation():
    """Show available documentation."""
    print_header("DOCUMENTAÇÃO DISPONÍVEL")
    
    docs = {
        "1": ("DOCUMENTACAO_SCRIPTS_PYPI.md", "Documentação completa dos scripts"),
        "2": ("PYPI_SETUP_GUIDE.md", "Guia de configuração (inglês)"),
        "3": (".pypirc_template", "Template do arquivo .pypirc"),
        "4": ("README_PYPI_SETUP.md", "README de configuração"),
    }
    
    print(f"\n{Colors.BOLD}Documentos disponíveis:{Colors.END}")
    for key, (filename, description) in docs.items():
        exists = "✅" if Path(f"scripts/{filename}").exists() else "❌"
        print(f"{key}. {exists} {filename} - {description}")
    
    choice = input(f"\n{Colors.YELLOW}Ver documento (1-4) ou Enter para voltar: {Colors.END}")
    
    if choice in docs:
        filename = docs[choice][0]
        filepath = Path(f"scripts/{filename}")
        
        if filepath.exists():
            print(f"\n{Colors.BOLD}📄 Conteúdo de {filename}:{Colors.END}")
            print("-" * 60)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                print(content[:2000])  # Show first 2000 chars
                if len(content) > 2000:
                    print(f"\n... (mostrando primeiros 2000 caracteres de {len(content)})")
            except Exception as e:
                print_error(f"Erro ao ler arquivo: {e}")
        else:
            print_error(f"Arquivo não encontrado: {filename}")


def install_tools():
    """Install required tools."""
    print_header("INSTALAÇÃO DE FERRAMENTAS")
    
    tools = ["build", "twine"]
    
    print("Instalando ferramentas necessárias...")
    for tool in tools:
        print(f"\n📦 Instalando {tool}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", tool], check=True)
            print_success(f"{tool} instalado com sucesso")
        except subprocess.CalledProcessError:
            print_error(f"Erro ao instalar {tool}")


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="PyPI Upload Manager")
    parser.add_argument("--setup", action="store_true", help="Configure .pypirc")
    parser.add_argument("--test-upload", action="store_true", help="Upload to TestPyPI")
    parser.add_argument("--status", action="store_true", help="Show status")
    
    args = parser.parse_args()
    
    if args.setup:
        setup_pypirc()
        return
    
    if args.test_upload:
        test_upload()
        return
    
    if args.status:
        show_status()
        return
    
    # Interactive menu
    while True:
        choice = show_menu()
        
        if choice == "0":
            print("\n👋 Até logo!")
            break
        elif choice == "1":
            show_status()
        elif choice == "2":
            setup_pypirc()
        elif choice == "3":
            test_upload()
        elif choice == "4":
            production_upload()
        elif choice == "5":
            show_documentation()
        elif choice == "6":
            install_tools()
        else:
            print_error("Opção inválida. Escolha 0-6.")
        
        input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.END}")


if __name__ == "__main__":
    main()
