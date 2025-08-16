#!/usr/bin/env python3
"""
Script avançado para corrigir warnings críticos de formatação RST.

Corrige problemas específicos:
- Missing matching underline for section title overline
- Invalid section title or transition marker
- Title underline too short
- Unexpected indentation
"""

import re
from pathlib import Path


def fix_rst_sections(content: str) -> str:
    """Corrige seções RST malformadas."""
    lines = content.split("\n")
    fixed_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Detecta overlines malformados (linhas com apenas hífens/iguais)
        if re.match(r'^[-=~`#"^*+<>]{3,}$', line.strip()):
            # Se é um overline, precisa ter título e underline
            if i + 1 < len(lines) and lines[i + 1].strip():
                title = lines[i + 1]

                # Se há um underline na próxima linha
                next_line_pattern = r'^[-=~`#"^*+<>]{3,}$'
                if i + 2 < len(lines) and re.match(
                    next_line_pattern, lines[i + 2].strip()
                ):
                    # Corrige os tamanhos para serem iguais ao título
                    char = line.strip()[0] if line.strip() else "-"
                    correct_length = len(title.strip())

                    fixed_lines.append(char * correct_length)  # overline
                    fixed_lines.append(title)  # título
                    fixed_lines.append(char * correct_length)  # underline
                    i += 3
                    continue
                else:
                    # Remove overline órfão e mantém o título simples
                    fixed_lines.append(title)
                    i += 2
                    continue
            else:
                # Remove linha de hífens órfã
                i += 1
                continue

        # Detecta underlines muito curtos
        if i > 0 and re.match(r'^[-=~`#"^*+<>]{3,}$', line.strip()):
            prev_line = lines[i - 1]
            if prev_line.strip() and len(line.strip()) < len(prev_line.strip()):
                # Corrige o underline para ter o mesmo tamanho do título
                char = line.strip()[0] if line.strip() else "-"
                fixed_lines[-1] = prev_line  # Mantém o título
                fixed_lines.append(char * len(prev_line.strip()))
                i += 1
                continue

        fixed_lines.append(line)
        i += 1

    return "\n".join(fixed_lines)


def fix_code_indentation(content: str) -> str:
    """Corrige problemas de indentação em blocos de código."""
    lines = content.split("\n")
    fixed_lines = []
    in_docstring = False

    for i, line in enumerate(lines):
        # Detecta docstrings
        if '"""' in line or "'''" in line:
            if line.count('"""') == 1 or line.count("'''") == 1:
                in_docstring = not in_docstring

        if in_docstring:
            # Adiciona linha em branco antes de exemplos de código
            example_pattern = r"^\s*(Example|Examples?|Usage):"
            if (
                re.match(example_pattern, line.strip(), re.IGNORECASE)
                or "Example Usage" in line
            ):
                if i > 0 and fixed_lines and fixed_lines[-1].strip():
                    fixed_lines.append("")

            # Corrige indentação de blocos de código
            if re.match(r"^\s*```", line.strip()) and i > 0:
                if fixed_lines and fixed_lines[-1].strip():
                    fixed_lines.append("")

            # Adiciona linha em branco após blocos de código
            if re.match(r"^\s*```\s*$", line.strip()):
                fixed_lines.append(line)
                if i + 1 < len(lines) and lines[i + 1].strip():
                    fixed_lines.append("")
                continue

        fixed_lines.append(line)

    return "\n".join(fixed_lines)


def fix_definition_lists(content: str) -> str:
    """Corrige listas de definição sem linhas em branco."""
    lines = content.split("\n")
    fixed_lines = []

    for i, line in enumerate(lines):
        # Detecta fim de lista de definição
        if (
            re.match(r"^\s*\w+:.*", line)
            and i > 0
            and lines[i - 1].strip()
            and not re.match(r"^\s*\w+:.*", lines[i - 1])
            and not lines[i - 1].strip().endswith(":")
        ):

            if fixed_lines and fixed_lines[-1].strip():
                fixed_lines.append("")

        fixed_lines.append(line)

    return "\n".join(fixed_lines)


def fix_transitions(content: str) -> str:
    """Corrige marcadores de transição inválidos."""
    lines = content.split("\n")
    fixed_lines = []

    for i, line in enumerate(lines):
        # Remove linhas com apenas hífens que causam problemas
        if re.match(r"^[-]{3,}$", line.strip()) and i > 0 and not lines[i - 1].strip():
            # Pula esta linha de transição problemática
            continue

        # Remove sequências duplas de hífens
        if (
            re.match(r"^[-=]{10,}$", line.strip())
            and i + 1 < len(lines)
            and re.match(r"^[-=]{10,}$", lines[i + 1].strip())
        ):
            # Mantém apenas uma linha
            fixed_lines.append(line)
            # Pula a próxima linha duplicada
            if i + 1 < len(lines):
                i += 1
            continue

        fixed_lines.append(line)

    return "\n".join(fixed_lines)


def fix_documentation_report(content: str) -> str:
    """Corrige problemas específicos do DOCUMENTATION_BUILD_REPORT.md."""
    # Remove transição no início do documento
    lines = content.split("\n")
    if len(lines) > 5 and re.match(r"^[-]{3,}$", lines[4].strip()):
        lines.pop(4)  # Remove a linha de transição

    return "\n".join(lines)


def fix_file(file_path: Path) -> bool:
    """Corrige um arquivo específico."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content

        # Aplica correções baseadas no tipo de arquivo
        if file_path.suffix == ".py":
            content = fix_rst_sections(content)
            content = fix_code_indentation(content)
            content = fix_definition_lists(content)
            content = fix_transitions(content)
        elif file_path.name == "DOCUMENTATION_BUILD_REPORT.md":
            content = fix_documentation_report(content)

        # Se houve mudanças, salva o arquivo
        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✓ Fixed RST issues in: {file_path}")
            return True

        return False

    except Exception as e:
        print(f"✗ Error processing {file_path}: {e}")
        return False


def main():
    """Função principal."""
    # Corrige arquivos Python
    src_dir = Path("../src/biorempp")
    files_fixed = 0

    for file_path in src_dir.rglob("*.py"):
        if fix_file(file_path):
            files_fixed += 1

    # Corrige arquivos específicos da documentação
    docs_files = [
        Path("DOCUMENTATION_BUILD_REPORT.md"),
    ]

    for file_path in docs_files:
        if file_path.exists() and fix_file(file_path):
            files_fixed += 1

    print(f"\nFixed RST formatting issues in {files_fixed} files")


if __name__ == "__main__":
    main()
