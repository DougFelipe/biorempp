# Sistema de Logging Centralizado BioRemPP

## Visão Geral

O BioRemPP agora possui um sistema de logging centralizado que oferece configuração consistente e flexível para todos os módulos do pacote. Este sistema permite controle fino sobre níveis de log, formatação e destinos de output.

## Características Principais

### 1. **Configuração Centralizada**
- Padrão singleton para garantir configuração única
- Configuração automática no import do pacote
- Suporte a múltiplos formatadores e handlers

### 2. **Flexibilidade de Configuração**
- Configuração via código Python
- Configuração via arquivos JSON/YAML
- Configuração via variáveis de ambiente
- Configuração via dicionários

### 3. **Múltiplos Destinos**
- Console (stdout/stderr)
- Arquivos de log
- Logs separados por nível (erro, debug, etc.)

## Como Usar

### Uso Básico

```python
from biorempp.utils.logging_config import get_logger

# Obter logger para o módulo atual
logger = get_logger("meu_modulo")

# Usar o logger
logger.info("Informação importante")
logger.warning("Aviso sobre algo")
logger.error("Erro encontrado")
logger.debug("Informação de debug")
```

### Configuração Personalizada

```python
from biorempp.utils.logging_config import setup_logging

# Configurar logging básico
setup_logging(
    level="DEBUG",
    log_file="logs/meu_app.log",
    console_output=True,
    format_style="detailed"
)
```

### Configuração via Arquivo

```python
from biorempp.utils.logging_config import BioRemPPLogger

# Configurar via arquivo JSON
logger_instance = BioRemPPLogger()
logger_instance.configure_from_file("configs/logging_config.json")

# Configurar via arquivo YAML
logger_instance.configure_from_file("configs/logging_config.yaml")
```

### Configuração via Variáveis de Ambiente

```bash
# Definir variáveis de ambiente
export BIOREMPP_LOG_LEVEL="DEBUG"
export BIOREMPP_LOG_FILE="logs/biorempp.log"
export BIOREMPP_LOG_FORMAT="json"
```

```python
from biorempp.utils.logging_config import configure_from_env

# Configurar a partir das variáveis de ambiente
configure_from_env()
```

## Padrões de Formatação

### 1. **Detailed (Padrão)**
```
2025-01-15 14:30:25 | INFO     | biorempp.input_loader    | load_data      | Processing input file
```

### 2. **Simple**
```
INFO - biorempp.input_loader - Processing input file
```

### 3. **JSON**
```json
{"timestamp": "2025-01-15 14:30:25", "level": "INFO", "logger": "biorempp.input_loader", "function": "load_data", "message": "Processing input file"}
```

## Integração nos Módulos

### Módulos Atualizados

Todos os módulos principais foram atualizados para usar o sistema centralizado:

1. **`src/biorempp/main.py`** - Ponto de entrada principal
2. **`src/biorempp/pipelines/input_processing.py`** - Pipeline de processamento
3. **`src/biorempp/input_processing/input_loader.py`** - Carregador de dados
4. **`src/biorempp/input_processing/input_validator.py`** - Validador de entrada
5. **`src/biorempp/input_processing/biorempp_merge_processing.py`** - Processador de merge
6. **`src/biorempp/utils/io_utils.py`** - Utilitários de I/O
7. **`scripts/train_model.py`** - Script de treinamento

### Padrão de Importação

```python
from biorempp.utils.logging_config import get_logger

logger = get_logger("nome_do_modulo")
```

## Configurações de Exemplo

### JSON Configuration
```json
{
    "version": 1,
    "disable_existing_loggers": false,
    "formatters": {
        "detailed": {
            "format": "%(asctime)s | %(levelname)-8s | %(name)-25s | %(funcName)-15s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "detailed",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": "logs/biorempp.log",
            "encoding": "utf-8"
        }
    },
    "loggers": {
        "biorempp": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
            "propagate": false
        }
    }
}
```

### YAML Configuration
```yaml
version: 1
disable_existing_loggers: false

formatters:
  detailed:
    format: "%(asctime)s | %(levelname)-8s | %(name)-25s | %(funcName)-15s | %(message)s"
    datefmt: "%Y-%m-%d %H:%M:%S"

handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    formatter: detailed
    stream: ext://sys.stdout

loggers:
  biorempp:
    level: DEBUG
    handlers: [console]
    propagate: false
```

## Variáveis de Ambiente

| Variável | Descrição | Valor Padrão |
|----------|-----------|--------------|
| `BIOREMPP_LOG_LEVEL` | Nível de log (DEBUG, INFO, WARNING, ERROR) | INFO |
| `BIOREMPP_LOG_FILE` | Caminho do arquivo de log | None |
| `BIOREMPP_LOG_FORMAT` | Estilo de formatação (simple, detailed, json) | detailed |

## Estrutura de Arquivos

```
biorempp/
├── src/biorempp/utils/logging_config.py    # Módulo principal
├── configs/
│   ├── logging_config.json                 # Configuração JSON
│   └── logging_config.yaml                 # Configuração YAML
├── examples/
│   └── logging_examples.py                 # Exemplos de uso
└── logs/                                   # Diretório de logs (criado automaticamente)
```

## Melhores Práticas

### 1. **Nomenclatura dos Loggers**
```python
# Use a hierarquia de módulos
logger = get_logger("input_processing.validator")
logger = get_logger("analysis.heatmaps")
logger = get_logger("utils.io_utils")
```

### 2. **Níveis de Log Apropriados**
```python
logger.debug("Informações detalhadas para debug")
logger.info("Informações gerais sobre o progresso")
logger.warning("Algo inesperado aconteceu, mas não é crítico")
logger.error("Erro sério que precisa de atenção")
logger.critical("Erro crítico que pode parar a aplicação")
```

### 3. **Tratamento de Exceções**
```python
try:
    # código que pode falhar
    process_data()
except Exception as e:
    logger.error(f"Falha no processamento: {e}", exc_info=True)
    raise
```

### 4. **Logs Estruturados**
```python
logger.info(f"Processando arquivo: {filename}")
logger.debug(f"Parâmetros: {params}")
logger.info(f"Processamento concluído em {duration:.2f}s")
```

## Benefícios da Implementação

1. **Consistência**: Formatação uniforme em todos os módulos
2. **Flexibilidade**: Múltiplas opções de configuração
3. **Manutenibilidade**: Configuração centralizada facilita mudanças
4. **Debugabilidade**: Logs detalhados facilitam diagnóstico
5. **Produção**: Configuração separada para desenvolvimento e produção

## Exemplo de Uso Completo

```python
#!/usr/bin/env python
"""
Exemplo completo de uso do sistema de logging
"""

from biorempp.utils.logging_config import setup_logging, get_logger

def main():
    # Configurar logging
    setup_logging(
        level="INFO",
        log_file="logs/exemplo.log",
        console_output=True,
        format_style="detailed"
    )

    # Obter logger
    logger = get_logger("exemplo")

    # Usar logger
    logger.info("Aplicação iniciada")

    try:
        # Processar dados
        logger.debug("Iniciando processamento")
        resultado = processar_dados()
        logger.info(f"Processamento concluído: {resultado}")

    except Exception as e:
        logger.error(f"Erro no processamento: {e}", exc_info=True)
        raise

    finally:
        logger.info("Aplicação finalizada")

if __name__ == "__main__":
    main()
```

Este sistema de logging centralizado fornece uma base sólida para monitoramento e debug de toda a aplicação BioRemPP, mantendo consistência e flexibilidade.
