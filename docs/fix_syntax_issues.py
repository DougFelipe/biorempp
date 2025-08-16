#!/usr/bin/env python3
"""
Script para corrigir problemas específicos de sintaxe após as correções de docstring.
"""

import re
from pathlib import Path


def fix_triple_quotes(content: str) -> str:
    """Corrige problemas com triple quotes malformadas."""
    # Corrige sequências de aspas malformadas
    content = re.sub(r'""""{2,}', '"""', content)
    content = re.sub(r"''''{2,}", "'''", content)

    # Remove linhas com apenas aspas
    lines = content.split("\n")
    fixed_lines = []

    for i, line in enumerate(lines):
        stripped = line.strip()
        # Se a linha tem apenas aspas repetidas, pula
        if re.match(r'^["\'\s]*$', stripped) and len(stripped) > 10:
            continue
        # Se a linha anterior terminou um docstring, não adiciona mais aspas
        if stripped in ['"""', "'''"]:
            if i > 0 and lines[i - 1].strip().endswith(('"""', "'''")):
                continue
        fixed_lines.append(line)

    return "\n".join(fixed_lines)


def fix_indentation(content: str) -> str:
    """Corrige problemas de indentação."""
    lines = content.split("\n")
    fixed_lines = []

    for i, line in enumerate(lines):
        # Se a linha está mal indentada depois de um docstring
        if line.strip() and not line.startswith(" ") and i > 0:
            prev_line = lines[i - 1].strip()
            if prev_line.endswith('"""') or prev_line.endswith("'''"):
                # Adiciona indentação apropriada
                if not line.startswith(("def ", "class ", "import ", "from ")):
                    line = "    " + line.lstrip()

        fixed_lines.append(line)

    return "\n".join(fixed_lines)


def fix_file(file_path: Path) -> bool:
    """Corrige um arquivo específico."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content

        # Aplica correções
        content = fix_triple_quotes(content)
        content = fix_indentation(content)

        # Se houve mudanças, salva o arquivo
        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✓ Fixed syntax issues in: {file_path}")
            return True

        return False

    except Exception as e:
        print(f"✗ Error processing {file_path}: {e}")
        return False


def main():
    """Função principal."""
    src_dir = Path("../src/biorempp")
    files_fixed = 0

    # Processa todos os arquivos Python
    for file_path in src_dir.rglob("*.py"):
        if fix_file(file_path):
            files_fixed += 1

    print(f"\nFixed syntax issues in {files_fixed} files")


if __name__ == "__main__":
    main()
