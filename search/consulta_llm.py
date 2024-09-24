import warnings
import nest_asyncio
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.tracers import ConsoleCallbackHandler
from langchain_community.vectorstores import Qdrant
from langchain_community.llms import Ollama
from qdrant_client import QdrantClient

nest_asyncio.apply()

warnings.filterwarnings("ignore")

handler = ConsoleCallbackHandler()

# chama o llm
llm = Ollama(
    model="llama3",
    base_url="http://localhost:11434"
)

# chama o encoder
embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')

# chama o banco
cliente = QdrantClient(url="http://localhost:6333")
vectorstore = Qdrant(client=cliente, collection_name="vinhos_analise_rag", embeddings=embeddings)

# descrição das colunas
metadata_field_info = [
    AttributeInfo(
        name="title",
        description="descrição do vinho",
        type="string"
    ),
    AttributeInfo(
        name="country",
        description="O país de onde o vinho é proveniente",
        type="string",
    ),
    AttributeInfo(
        name="points",
        description="O número de pontos que a WineEnthusiast classificou o vinho em uma escala de 1 a 100",
        type="integer",
    ),
    AttributeInfo(
        name="price",
        description="O preço de uma garrafa de vinho",
        type="float",
    ),
    AttributeInfo(
        name="variety",
        description="As uvas utilizadas para fazer o vinho",
        type="string",
    ),
]

document_content_description = "Breve descrição do vinho"

# passando as informações para o llm consultar no banco
retriever = SelfQueryRetriever.from_llm(
    llm,
    vectorstore,
    document_content_description,
    metadata_field_info
)

# dá para substituir pelo input e deixar dinamico ou até mesmo usar o Streamlit para gerar uma página de pesquisa
response = retriever.invoke("Quais vinhos dos US têm preço entre 15 e 30 e pontos acima de 90")

if response != None:
    for res in response:
        print(res.page_content,
              '\n',res.metadata['title'],
              '\n price: ', res.metadata['price'],
              '\n points: ', res.metadata['points'],
              '\n\n')
else:
    print("Nada encontrado")
