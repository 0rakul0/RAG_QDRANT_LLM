# README.md

## Projeto de ETL para RAG utilizando Qdrant e LLM

### Descrição do Projeto

Este projeto tem como objetivo realizar um processo de ETL (Extração, Transformação e Carga) utilizando um conjunto de dados de vinhos, disponível no Kaggle. O processo envolve a extração e limpeza dos dados, o envio dos dados para o banco de vetores no Qdrant, e a utilização de uma Language Model (LLM) para realizar consultas sobre esses dados.

### Estrutura do Projeto

1. **Extração dos Dados**:
   - Os dados são extraídos de um arquivo CSV contendo informações sobre vinhos, incluindo descrições, país de origem, preço, e pontuação.

2. **Transformação**:
   - O dataset é limpo e colunas irrelevantes são removidas.
   - As colunas com informações essenciais sobre os vinhos (como país, preço, variedade, etc.) são mantidas.
   - Tipos de dados incorretos são ajustados, e valores ausentes são tratados.

3. **Carga (Upload para o Qdrant)**:
   - Os dados são convertidos para embeddings utilizando o modelo `all-MiniLM-L6-v2`.
   - Esses embeddings, junto com os metadados, são enviados para uma coleção no Qdrant, criando um banco de vetores para consultas semânticas.

4. **Consulta utilizando LLM**:
   - Uma LLM (Large Language Model) é utilizada para fazer consultas aos dados armazenados no Qdrant.
   - As consultas permitem encontrar vinhos com base em parâmetros como preço, país de origem e pontuação, retornando resultados relevantes.

### Fluxo do Código

1. **Importação de Bibliotecas**:
   O script utiliza as bibliotecas `pandas`, `qdrant_client`, `sentence_transformers`, `langchain`, entre outras, para manipulação dos dados, criação de embeddings e conexão com o Qdrant.

2. **Carregamento dos Dados**:
   Os dados são carregados a partir do CSV disponível no Kaggle:
   - Dataset: [Wine Reviews](https://www.kaggle.com/datasets/zynicide/wine-reviews)

3. **Processamento e Limpeza dos Dados**:
   - Colunas desnecessárias são removidas, e as colunas de `price` e `points` têm seus tipos ajustados.

4. **Envio dos Dados ao Qdrant**:
   - Uma coleção chamada `vinhos_analise_rag` é criada no Qdrant, e os documentos são convertidos em embeddings utilizando o modelo `all-MiniLM-L6-v2` da biblioteca `sentence-transformers`.
   - Cada documento contém informações como país de origem, variedade de uvas, preço, e descrição do vinho.

5. **Consultando com LLM**:
   - A LLM utilizada é a `Ollama`, que se conecta ao Qdrant para realizar consultas semânticas com base nos dados armazenados.
   - Um exemplo de consulta é buscar vinhos dos Estados Unidos com preço entre 15 e 30 dólares e pontuação acima de 90.

### Como Executar o Projeto

1. **Instalação das Dependências**:
   - Certifique-se de ter as seguintes dependências instaladas:
     ```bash
     pip install pandas qdrant-client sentence-transformers langchain langchain_community nest_asyncio
     ```

2. **Execução do Script**:
   - Para rodar o script, certifique-se de que o Qdrant está rodando no Docker na porta `6333`.
   - Execute o script para realizar o processamento dos dados e subir para o Qdrant:
     ```bash
     python ETL.py
     ```

3. **Consultas com LLM**:
   - Após os dados serem carregados no Qdrant, você pode realizar consultas semânticas utilizando a LLM conforme o exemplo no script.

### Requisitos

- Python 3.x
- Qdrant rodando no Docker
- Kaggle Dataset: [Wine Reviews](https://www.kaggle.com/datasets/zynicide/wine-reviews)

### Contribuição

Sinta-se à vontade para abrir issues e pull requests para melhorias e correções.

### Licença

Este projeto está sob a licença MIT.