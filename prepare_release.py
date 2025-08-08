#!/usr/bin/env python3
"""
Script para preparar release do BioRemPP para uso no Colab
Automatiza a criação de release e fornece instruções para upload manual
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


class ReleasePreparator:
    def __init__(self):
        self.project_dir = Path.cwd()
        self.dist_dir = self.project_dir / "dist"
        self.version = "v0.5.0"

    def check_git_status(self):
        """Verificar status do git"""
        print("🔍 Verificando status do Git...")

        try:
            # Verificar se há mudanças não commitadas
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                check=True,
            )

            if result.stdout.strip():
                print("⚠️ Há mudanças não commitadas:")
                print(result.stdout)
                response = input("Continuar mesmo assim? (y/n): ")
                if response.lower() != "y":
                    return False

            # Verificar branch atual
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                check=True,
            )

            current_branch = result.stdout.strip()
            print(f"📍 Branch atual: {current_branch}")

            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao verificar Git: {e}")
            return False

    def check_build_files(self):
        """Verificar se os arquivos de build existem"""
        print("📦 Verificando arquivos de build...")

        if not self.dist_dir.exists():
            print(f"❌ Diretório dist não encontrado: {self.dist_dir}")
            return False

        whl_files = list(self.dist_dir.glob("*.whl"))
        tar_files = list(self.dist_dir.glob("*.tar.gz"))

        if not whl_files:
            print("❌ Nenhum arquivo .whl encontrado")
            return False

        if not tar_files:
            print("❌ Nenhum arquivo .tar.gz encontrado")
            return False

        print(f"✅ Encontrados:")
        for whl in whl_files:
            size_kb = whl.stat().st_size / 1024
            print(f"   📄 {whl.name} ({size_kb:.1f} KB)")

        for tar in tar_files:
            size_mb = tar.stat().st_size / (1024 * 1024)
            print(f"   📦 {tar.name} ({size_mb:.1f} MB)")

        self.whl_file = whl_files[0]
        self.tar_file = tar_files[0]
        return True

    def create_tag(self):
        """Criar tag no Git"""
        print(f"🏷️ Criando tag {self.version}...")

        try:
            # Verificar se tag já existe
            result = subprocess.run(
                ["git", "tag", "-l", self.version], capture_output=True, text=True
            )

            if result.stdout.strip():
                print(f"⚠️ Tag {self.version} já existe")
                response = input("Sobrescrever? (y/n): ")
                if response.lower() == "y":
                    subprocess.run(["git", "tag", "-d", self.version], check=True)
                    subprocess.run(
                        ["git", "push", "origin", "--delete", self.version],
                        capture_output=True,
                    )  # Não falhar se não existir no remote
                else:
                    return False

            # Criar nova tag
            tag_message = f"BioRemPP {self.version} - Build para Colab"
            subprocess.run(
                ["git", "tag", "-a", self.version, "-m", tag_message], check=True
            )

            print(f"✅ Tag {self.version} criada")
            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao criar tag: {e}")
            return False

    def push_tag(self):
        """Fazer push da tag"""
        print(f"🚀 Fazendo push da tag {self.version}...")

        try:
            subprocess.run(["git", "push", "origin", self.version], check=True)
            print(f"✅ Tag {self.version} enviada para o GitHub")
            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao fazer push da tag: {e}")
            return False

    def generate_release_notes(self):
        """Gerar notas do release"""
        notes = f"""# 🧬 BioRemPP {self.version} - Build para Google Colab

## 📋 Novidades desta versão

- ✅ **Arquivos de distribuição prontos** para instalação no Colab
- 🚀 **Instalação otimizada** via wheel (.whl)
- 🔧 **CLI completamente funcional** com todos os bancos de dados
- 📊 **Interface melhorada** com feedback visual
- 🛡️ **Tratamento robusto de erros** e validações

## 📦 Arquivos incluídos

- `{self.whl_file.name}` - Wheel para instalação rápida ({self.whl_file.stat().st_size/1024:.0f} KB)
- `{self.tar_file.name}` - Código fonte completo ({self.tar_file.stat().st_size/(1024*1024):.1f} MB)

## 🎯 Como usar no Google Colab

1. Abra o notebook: `notebooks/biorempp_colab_demo.ipynb`
2. Use o badge "Open in Colab"
3. Execute as células sequencialmente
4. O notebook baixará e instalará automaticamente estes arquivos

## 🧪 Bancos de dados incluídos

- 🧬 **BioRemPP Database** (6.623 entradas)
- 🗂️ **KEGG Degradation Pathways** (871 entradas)
- 🏭 **HAdeg Database** (1.168 entradas)
- ☠️ **ToxCSM Database** (323 entradas)

## 📚 Documentação

- 📖 [Documentação completa](https://github.com/DougFelipe/biorempp/blob/main/DOCUMENTATION.md)
- 🎮 [Notebook de demonstração](https://github.com/DougFelipe/biorempp/blob/main/notebooks/biorempp_demo.ipynb)

**Data do build:** {datetime.now().strftime('%d/%m/%Y %H:%M')}
"""
        return notes

    def show_manual_instructions(self):
        """Mostrar instruções para upload manual"""
        release_notes = self.generate_release_notes()

        print("\n" + "=" * 60)
        print("📋 INSTRUÇÕES PARA CRIAR O RELEASE")
        print("=" * 60)

        print(
            f"""
🌐 1. Acesse: https://github.com/DougFelipe/biorempp/releases/new

🏷️ 2. Configure o release:
   - Tag: {self.version}
   - Title: BioRemPP {self.version} - Build para Google Colab
   - Description: (copie as notas abaixo)

📦 3. Faça upload dos arquivos:
   - {self.whl_file.name}
   - {self.tar_file.name}

✅ 4. Publique o release

📝 NOTAS DO RELEASE (copie e cole):
{'-'*50}
{release_notes}
{'-'*50}
"""
        )

        print(f"\n📁 Arquivos para upload estão em: {self.dist_dir.absolute()}")

    def update_notebook_urls(self):
        """Gerar URLs atualizadas para o notebook"""
        base_url = (
            f"https://github.com/DougFelipe/biorempp/releases/download/{self.version}"
        )
        wheel_url = f"{base_url}/{self.whl_file.name}"
        tar_url = f"{base_url}/{self.tar_file.name}"

        print(f"\n🔗 URLs para atualizar no notebook:")
        print(f'WHEEL_URL = "{wheel_url}"')
        print(f'TARBALL_URL = "{tar_url}"')

        return wheel_url, tar_url

    def run(self):
        """Executar preparação completa"""
        print("🚀 BioRemPP Release Preparator")
        print("=" * 60)

        if not self.check_git_status():
            print("❌ Problemas com Git - cancelando")
            return False

        if not self.check_build_files():
            print(
                "❌ Arquivos de build não encontrados - execute build_package.py primeiro"
            )
            return False

        # Criar e enviar tag
        if self.create_tag() and self.push_tag():
            print("✅ Tag criada e enviada com sucesso")
        else:
            print("❌ Erro ao criar/enviar tag")
            return False

        # Mostrar instruções
        self.show_manual_instructions()

        # URLs atualizadas
        self.update_notebook_urls()

        print(f"\n🎉 Preparação concluída!")
        print(f"📋 Próximo passo: Criar release manualmente no GitHub")

        return True


if __name__ == "__main__":
    preparator = ReleasePreparator()
    success = preparator.run()
    sys.exit(0 if success else 1)
