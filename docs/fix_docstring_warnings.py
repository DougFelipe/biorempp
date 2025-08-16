#!/usr/bin/env python3
"""
Script para corrigir warnings de formatação nos docstrings do Sphinx.

Este script corrige sistematicamente os problemas de formatação RST identificados
pelo Sphinx, incluindo:
- Title underlines too short
- Unexpected indentation
- Block quotes without blank lines
- Definition lists without blank lines

Uso:
    python fix_docstring_warnings.py [--dry-run] [--file path]
"""

import argparse
import re
import sys
from pathlib import Path


class DocstringFixer:
    """Corrige problemas comuns de formatação em docstrings."""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.fixes_applied = 0
        self.files_processed = 0

    def fix_title_underlines(self, content: str) -> str:
        """Corrige underlines de títulos que são muito curtos."""
        lines = content.split("\n")
        fixed_lines = []

        for i in range(len(lines)):
            line = lines[i]
            fixed_lines.append(line)

            # Se a próxima linha é um underline, verifica se precisa corrigir
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                # Padrões de underline RST
                if re.match(r'^[-=~`#"^*+<>]{2,}$', next_line):
                    # Se o underline é mais curto que o título, estende
                    if len(next_line) < len(line):
                        underline_char = next_line[0] if next_line else "-"
                        fixed_lines.append(underline_char * len(line))
                        # Pula a próxima linha original
                        if i + 1 < len(lines):
                            i += 1  # Esta linha será processada no próximo ciclo
                            continue

        return "\n".join(fixed_lines)

    def fix_code_blocks(self, content: str) -> str:
        """Corrige problemas de indentação em blocos de código."""
        lines = content.split("\n")
        fixed_lines = []
        in_docstring = False

        for i, line in enumerate(lines):
            # Detecta início/fim de docstring
            if '"""' in line or "'''" in line:
                in_docstring = not in_docstring

            if in_docstring:
                # Corrige blocos de código sem linha em branco antes
                code_pattern1 = re.match(r"^\s*```\w*", line.strip())
                code_pattern2 = re.match(r"^\s*::", line.strip())
                if code_pattern1 or code_pattern2:
                    if i > 0 and fixed_lines and fixed_lines[-1].strip():
                        fixed_lines.append("")  # Adiciona linha em branco

                # Corrige final de blocos de código sem linha em branco depois
                if re.match(r"^\s*```\s*$", line.strip()):
                    fixed_lines.append(line)
                    if i + 1 < len(lines) and lines[i + 1].strip():
                        fixed_lines.append("")  # Adiciona linha em branco depois
                    continue

                # Corrige listas de definição sem linha em branco
                if re.match(r"^\s*\w+:", line) and i > 0:
                    prev_line = lines[i - 1].strip()
                    if prev_line and not prev_line.endswith(":"):
                        if fixed_lines and fixed_lines[-1].strip():
                            fixed_lines.append("")

            fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def fix_cross_references(self, content: str) -> str:
        """Corrige referências cruzadas inválidas."""
        # Remove referências py:class inválidas comuns
        patterns_to_fix = [
            # Referências de status de execução inválidas
            (
                r":py:class:`(Successful execution|General errors|validation|"
                r"unexpected exceptions|File not found errors|"
                r"Permission errors|User interruption|Ctrl\+C)`",
                r"`\1`",
            ),
            # Referências de tipos inválidas
            (
                r':py:class:`(default=None|default="INFO"|default True|'
                r'default "detailed"|optional|callable|pd\.DataFrame)`',
                r"`\1`",
            ),
            # Remove referências py:exc inválidas
            (r"`([^`]+)`", r"`\1`"),
        ]

        for pattern, replacement in patterns_to_fix:
            content = re.sub(pattern, replacement, content)

        return content

    def fix_myst_references(self, content: str) -> str:
        """Corrige referências MyST inválidas em arquivos Markdown."""
        # Remove referências cruzadas que não existem
        invalid_refs = [
            r"\{ref\}`[^`]+`",  # Remove referências {ref} inválidas
            # Converte links .md para .html se necessário
            r"\[([^\]]+)\]\([^)]+\.md\)",
        ]

        for pattern in invalid_refs:

            def replace_func(match):
                return match.group(1) if "(" in match.group(0) else match.group(0)

            content = re.sub(pattern, replace_func, content)

        return content

    def fix_file(self, file_path: Path) -> bool:
        """Corrige um arquivo específico."""

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                original_content = f.read()

            content = original_content

            # Aplica correções baseadas na extensão do arquivo
            if file_path.suffix == ".py":
                content = self.fix_title_underlines(content)
                content = self.fix_code_blocks(content)
                content = self.fix_cross_references(content)
            elif file_path.suffix == ".md":
                content = self.fix_myst_references(content)

            # Se houve mudanças e não é dry-run, salva o arquivo
            if content != original_content:
                if not self.dry_run:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    print(f"✓ Fixed: {file_path}")

                else:
                    print(f"Would fix: {file_path}")

                self.fixes_applied += 1
                return True

            return False

        except Exception as e:
            print(f"✗ Error processing {file_path}: {e}")
            return False

    def process_directory(self, directory: Path) -> None:
        """Processa todos os arquivos Python e Markdown em um diretório."""
        patterns = ["**/*.py", "**/*.md"]

        for pattern in patterns:
            for file_path in directory.rglob(pattern):
                if self.should_process_file(file_path):
                    self.fix_file(file_path)
                    self.files_processed += 1

    def should_process_file(self, file_path: Path) -> bool:
        """Determina se um arquivo deve ser processado."""
        # Ignora arquivos em diretórios específicos
        ignore_dirs = {
            ".git",
            "__pycache__",
            ".pytest_cache",
            "build",
            "dist",
            "_build",
        }

        for part in file_path.parts:
            if part in ignore_dirs:
                return False

        return True

    def print_summary(self) -> None:
        """Imprime um resumo das correções aplicadas."""
        mode = "DRY RUN" if self.dry_run else "APPLIED"
        print(f"\n{mode} Summary:")
        print(f"Files processed: {self.files_processed}")
        fix_word = "identified" if self.dry_run else "applied"
        print(f"Fixes {fix_word}: {self.fixes_applied}")


def main():
    """Função principal."""
    description = "Fix Sphinx docstring formatting warnings"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be fixed without making changes",
    )
    parser.add_argument(
        "--file", type=str, help="Fix a specific file instead of the entire project"
    )
    parser.add_argument(
        "--directory",
        type=str,
        default="../src",
        help="Directory to process (default: ../src)",
    )

    args = parser.parse_args()

    fixer = DocstringFixer(dry_run=args.dry_run)

    if args.file:
        # Processa um arquivo específico
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File {file_path} does not exist")
            sys.exit(1)

        fixer.fix_file(file_path)
        fixer.files_processed = 1

    else:
        # Processa diretório
        directory = Path(args.directory)
        if not directory.exists():
            print(f"Error: Directory {directory} does not exist")
            sys.exit(1)

        print(f"Processing directory: {directory.absolute()}")
        fixer.process_directory(directory)

    fixer.print_summary()


if __name__ == "__main__":
    main()
