"""
esse é um projeto de ETL para fazer RAG usando o QDRANT

O objetivo é extrair um csv vindo do kaggle, estruturalo e subir os dados no qdrant,
e usar uma LLM para fazer a consulta desses dados.
"""

import pandas as pd
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
import pandas as pd
import warnings
import logging
from tqdm import tqdm

warnings.filterwarnings("ignore")

# modelo de embedding
embedd = SentenceTransformer('all-MiniLM-L6-v2')

# acesso ao qdrant no docker
client = QdrantClient(url="http://localhost:6333")

"""link dos vinhos https://www.kaggle.com/datasets/zynicide/wine-reviews"""

# abre o dataframe
df = pd.read_csv('./LAKE/winemag-data-130k-v2.csv')

# faz uma copia de segurança
vinhos = df.copy()

# elimina as colunas que não vamos usar
vinhos = vinhos.drop(['Unnamed: 0','designation','province','region_1','region_2','taster_name','taster_twitter_handle','winery'], axis=1)

# elimina linhas vazias
vinhos = vinhos.dropna(subset=['country', 'price', 'variety'])

# concerta o tipo da coluna
vinhos['price'] = pd.to_numeric(vinhos['price'], errors='coerce')
vinhos['points'] = pd.to_numeric(vinhos['points'], downcast='integer', errors='coerce')

print(f'tamanho do dataframe {vinhos.shape} \n suas colunas: {vinhos.columns.tolist()}')

### criando a coleção
if "vinhos_analise_rag" not in [col.name for col in client.get_collections().collections]:
    client.create_collection(
        collection_name="vinhos_analise_rag",
        vectors_config=models.VectorParams(
            size=embedd.get_sentence_embedding_dimension(),
            distance=models.Distance.COSINE,
        ),
    )

### gerando o documento para o banco
class Document:
    """
    Classe para representar um documento a ser inserido no banco de vetores.
    page_content é o texto semantico do documento
    metadata é caracteristicas do documento
    """
    def __init__(self, page_content, metadata):
        self.page_content = page_content
        self.metadata = metadata

def df_to_document(vinhos):
    """
    Converte um DataFrame em uma lista de objetos Document.

    """
    documents = []
    # gera um metadado do texto de acordo com os marcadores
    for _, row in vinhos.iterrows():
        metadata = {
            'country': row['country'],
            'points': row['points'],
            'price': row['price'],
            'variety': row['variety'],
            'title': row['title']
        }
        document = Document(page_content=row['description'], metadata=metadata)
        documents.append(document)
    return documents

def gera_banco():
    """
    Gera o banco de dados de vetores no Qdrant a partir do DataFrame de vinhos.
    """
    try:
        docs = df_to_document(vinhos)
        points = [
            models.PointStruct(
                id=idx,
                vector=embedd.encode(doc.page_content).tolist(),
                payload={'metadata': doc.metadata, 'page_content': doc.page_content}
            ) for idx, doc in tqdm(enumerate(docs))
        ]
        ## joga a informação no banco
        client.upload_points(
            collection_name="vinhos_analise_rag",
            points=points
        )

        logging.info("Dados enviados com sucesso para o Qdrant.")
    except Exception as e:
        logging.error(f"Erro ao processar dados: {e}")

gera_banco()