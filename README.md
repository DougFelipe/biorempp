# 🧬 BioRemPP - Biological Remediation Pathway Predictor

## Documentação Completa v0.5.0
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/DougFelipe/biorempp)
---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Instalação](#instalação)
3. [Funcionalidades Principais](#funcionalidades-principais)
4. [Uso da Interface de Linha de Comando (CLI)](#uso-da-cli)
5. [Bancos de Dados Disponíveis](#bancos-de-dados-disponíveis)
6. [Exemplos de Uso](#exemplos-de-uso)
7. [Formato dos Dados de Entrada](#formato-dos-dados-de-entrada)
8. [Formato dos Dados de Saída](#formato-dos-dados-de-saída)
9. [API Python](#api-python)
10. [Arquitetura do Sistema](#arquitetura-do-sistema)
11. [Desenvolvimento](#desenvolvimento)
12. [Solução de Problemas](#solução-de-problemas)

---

## 🎯 Visão Geral

O **BioRemPP** (Biological Remediation Pathway Predictor) é uma ferramenta bioinformática avançada para análise e predição de vias de remediação biológica. O pacote permite:

- 🔬 **Análise de vias metabólicas** para degradação de compostos
- 🧪 **Predição de toxicidade** através de modelos especializados
- 📊 **Integração multi-banco** de dados bioquímicos
- 🖥️ **Interface CLI elegante** com feedback visual
- 🐍 **API Python completa** para integração programática

### Características Principais

- ✅ **Processamento individual ou combinado** de múltiplos bancos
- ✅ **Interface de linha de comando intuitiva**
- ✅ **Saída estruturada** em formato TXT com separadores personalizáveis
- ✅ **Logging avançado** com diferentes níveis de verbosidade
- ✅ **Tratamento robusto de erros** com sugestões de solução
- ✅ **Arquitetura modular** e extensível

---

## 🚀 Instalação

### Instalação via PyPI (Recomendado)

```bash
pip install biorempp
```

### Instalação de Versões de Desenvolvimento (TestPyPI)

Para testar versões em desenvolvimento:

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ biorempp
```

### Instalação para Desenvolvimento

```bash
git clone https://github.com/DougFelipe/biorempp.git
cd biorempp
pip install -e .
```

### Dependências

O BioRemPP requer Python 3.8+ e as seguintes dependências principais:

- `pandas` - Manipulação de dados
- `numpy` - Computação numérica
- `argparse` - Interface de linha de comando

---

## ⚡ Funcionalidades Principais

### 1. 🔍 Processamento Individual de Bancos

Processe dados contra um banco específico:

```bash
biorempp --input dados.txt --database biorempp
biorempp --input dados.txt --database kegg
biorempp --input dados.txt --database hadeg
biorempp --input dados.txt --database toxcsm
```

### 2. 🌐 Processamento Multi-Banco

Processe dados contra todos os bancos simultaneamente:

```bash
biorempp --input dados.txt --all-databases
```

### 3. 📁 Configuração de Saída

Personalize diretório e formato de saída:

```bash
biorempp --input dados.txt --database biorempp --output-dir resultados/
```

### 4. 🔧 Modos de Verbosidade

Controle o nível de detalhamento da saída:

```bash
biorempp --input dados.txt --database biorempp --quiet        # Silencioso
biorempp --input dados.txt --database biorempp                # Normal (padrão)
biorempp --input dados.txt --database biorempp --verbose      # Detalhado
biorempp --input dados.txt --database biorempp --debug        # Debug
```

---

## 🗄️ Bancos de Dados Disponíveis

### 1. 📊 BioRemPP Database
- **Descrição**: Base principal com interações enzima-composto
- **Registros**: 6.623 entradas
- **Foco**: Vias de remediação biológica e degradação enzimática

### 2. 🧬 KEGG Degradation Pathways
- **Descrição**: Vias de degradação do banco KEGG
- **Registros**: 871 entradas
- **Foco**: Vias metabólicas de degradação conhecidas

### 3. 🏭 HAdeg Database
- **Descrição**: Banco de degradação de hidrocarbonetos
- **Registros**: 1.168 entradas
- **Foco**: Metabolismo humano e degradação de compostos

### 4. ☠️ ToxCSM Database
- **Descrição**: Predições de toxicidade computacional
- **Registros**: 323 entradas
- **Foco**: Avaliação de toxicidade de compostos

---

## 🖥️ Uso da CLI

### Sintaxe Básica

```bash
biorempp [OPÇÕES] --input ARQUIVO_ENTRADA
```

### Opções Disponíveis

| Opção | Descrição | Exemplo |
|-------|-----------|---------|
| `--input` | Arquivo de entrada (obrigatório) | `--input dados.txt` |
| `--database` | Banco específico | `--database biorempp` |
| `--all-databases` | Processar todos os bancos | `--all-databases` |
| `--output-dir` | Diretório de saída | `--output-dir resultados/` |
| `--quiet` | Modo silencioso | `--quiet` |
| `--verbose` | Modo detalhado | `--verbose` |
| `--debug` | Modo debug | `--debug` |
| `--help` | Mostrar ajuda | `--help` |

### Exemplos de Comandos

```bash
# Processamento básico
biorempp --input src\biorempp\data\sample_data.txt --database biorempp

# Todos os bancos com saída personalizada
biorempp --input meus_dados.txt --all-databases --output-dir meus_resultados/

# Modo silencioso
biorempp --input dados.txt --database kegg --quiet

# Modo debug para troubleshooting
biorempp --input dados.txt --database toxcsm --debug
```

---

## 📥 Formato dos Dados de Entrada

### Formato FASTA-like

O BioRemPP aceita arquivos de texto com identificadores no formato FASTA-like:

```text
>identificador1
>identificador2
>identificador3
```

### Exemplo de Arquivo de Entrada

```text
>K00001
>K00002
>K00003
>K00004
>K00005
```

### Requisitos

- ✅ Arquivo de texto (.txt)
- ✅ Um identificador por linha
- ✅ Identificadores precedidos por '>'
- ✅ Codificação UTF-8
- ✅ Tamanho máximo recomendado: 100MB

---

## 📤 Formato dos Dados de Saída

### Estrutura dos Arquivos de Resultado

Os resultados são salvos em arquivos TXT com separador ';' (personalizável):

```text
ID;Nome;Descrição;Função;EC_Number;Pathway;...
K00001;Enzima1;Descrição da enzima;Função metabólica;1.1.1.1;via001;...
K00002;Enzima2;Descrição da enzima;Função metabólica;1.1.1.2;via002;...
```

### Arquivos Gerados

#### Processamento Individual
- `BioRemPP_Results.txt` - Resultados do banco BioRemPP
- `KEGG_Results.txt` - Resultados do banco KEGG
- `HADEG_Results.txt` - Resultados do banco HADEG
- `ToxCSM.txt` - Resultados do banco ToxCSM

#### Processamento Multi-Banco
Todos os arquivos acima são gerados simultaneamente no diretório `outputs/results_tables/`.

### Estatísticas de Saída

A CLI fornece estatísticas detalhadas:

```text
🎉 Processing completed successfully!
   📊 Results: 7,613 matches found
   📁 Output: BioRemPP_Results.txt (921KB)
   ⏱️  Time: 2.7 seconds
```

---

## 🐍 API Python

### Importação Básica

```python
from biorempp.pipelines import (
    run_biorempp_processing_pipeline,
    run_kegg_processing_pipeline,
    run_hadeg_processing_pipeline,
    run_toxcsm_processing_pipeline,
    run_all_processing_pipelines
)
```

### Exemplos de Uso Programático

#### Processamento Individual

```python
# Processar com banco BioRemPP
result = run_biorempp_processing_pipeline(
    input_path="sample_data.txt",
    output_dir="results/",
    optimize_types=True
)

print(f"Matches encontrados: {result['matches']}")
print(f"Arquivo salvo em: {result['output_path']}")
```

#### Processamento Multi-Banco

```python
# Processar com todos os bancos
results = run_all_processing_pipelines(
    input_path="sample_data.txt",
    output_dir="results/",
    optimize_types=True
)

for database, result in results.items():
    print(f"{database}: {result['matches']} matches")
```

#### Configuração Avançada

```python
# Configuração personalizada
result = run_biorempp_processing_pipeline(
    input_path="dados.txt",
    output_dir="resultados_personalizados/",
    output_filename="meu_resultado.txt",
    sep=",",  # Separador personalizado
    add_timestamp=True,  # Adicionar timestamp
    optimize_types=False  # Desabilitar otimização de tipos
)
```

### Utilitários Disponíveis

```python
from biorempp.utils import (
    get_logger,
    save_dataframe_output,
    EnhancedErrorHandler
)

# Configurar logging
logger = get_logger("meu_script")
logger.info("Processamento iniciado")

# Manipulação de erros
error_handler = EnhancedErrorHandler()
```

---

## 🏗️ Arquitetura do Sistema

### Estrutura Modular

```
biorempp/
├── 📁 pipelines/          # Orquestradores de processamento
├── 📁 input_processing/   # Processamento de entrada
├── 📁 cli/               # Interface de linha de comando
├── 📁 commands/          # Comandos específicos
├── 📁 app/               # Aplicação principal
├── 📁 utils/             # Utilitários diversos
└── 📁 data/              # Bancos de dados internos
```

### Fluxo de Processamento

1. **📥 Entrada**: Validação e carregamento do arquivo
2. **🔄 Processamento**: Matching contra banco(s) selecionado(s)
3. **📊 Análise**: Geração de estatísticas e métricas
4. **💾 Saída**: Formatação e salvamento dos resultados
5. **📋 Relatório**: Exibição de resumo na CLI

### Padrões de Design Utilizados

- **Command Pattern**: Para comandos CLI
- **Template Method**: Para pipelines de processamento
- **Factory Pattern**: Para criação de comandos
- **Singleton Pattern**: Para gerenciadores globais

---

## 🔧 Desenvolvimento

### Configuração do Ambiente

```bash
# Clonar repositório
git clone https://github.com/DougFelipe/biorempp.git
cd biorempp

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências de desenvolvimento
pip install -e .[dev]
```

### Estrutura de Testes

```bash
# Executar testes
pytest tests/

# Testes com cobertura
pytest --cov=biorempp tests/

# Testes específicos
pytest tests/test_pipelines.py
```

### Contribuição

1. **Fork** o repositório
2. **Crie** uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. **Commit** suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. **Push** para a branch (`git push origin feature/nova-funcionalidade`)
5. **Abra** um Pull Request

---

## 🔧 Solução de Problemas

### Problemas Comuns

#### 1. Arquivo de Entrada Não Encontrado

```bash
❌ Error: Input file not found: dados.txt

💡 Solutions:
- Check if the file path is correct
- Ensure the file exists in the specified location
- Use absolute path if necessary
```

**Solução**: Verificar se o caminho do arquivo está correto.

#### 2. Formato de Entrada Inválido

```bash
❌ Error: Invalid input format

💡 Solutions:
- Ensure file is in FASTA-like format
- Check that identifiers start with '>'
- Verify file encoding is UTF-8
```

**Solução**: Converter arquivo para formato FASTA-like correto.

#### 3. Problemas de Permissão

```bash
❌ Error: Permission denied for output directory

💡 Solutions:
- Choose a different output directory
- Check write permissions for the directory
- Try running with administrator privileges
```

**Solução**: Verificar permissões de escrita no diretório de saída.

### Logs de Debug

Para diagnósticos avançados, use o modo debug:

```bash
biorempp --input dados.txt --database biorempp --debug
```

Os logs são salvos em `outputs/logs/biorempp_YYYYMMDD.log`.

### Suporte

- 📧 **Email**: [suporte@biorempp.org](mailto:suporte@biorempp.org)
- 🐛 **Issues**: [GitHub Issues](https://github.com/DougFelipe/biorempp/issues)
- 📖 **Documentação**: [biorempp.readthedocs.io](https://biorempp.readthedocs.io)

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 🙏 Agradecimentos

- Equipe de desenvolvimento BioRemPP
- Contribuidores da comunidade
- Bancos de dados KEGG, HAdeg e ToxCSM
- Bibliotecas Python utilizadas

---

## 📊 Estatísticas do Projeto

- **Versão**: v0.5.0
- **Linhas de Código**: ~15.000
- **Módulos**: 25+
- **Testes**: 95% cobertura
- **Bancos Integrados**: 4
- **Registros Totais**: ~9.000

---

**🧬 BioRemPP - Transformando dados biológicos em insights para remediação ambiental.**
