from pathlib import Path

from tqdm import tqdm

from basic import default_context
from kb.docx_loader import DocxLoader
from retriever.doc_retriever import DocRetriever


def recreate_collection():
    from qdrant_client import QdrantClient, models

    collection_name = 'word_reader_test_1024'
    qdrant_client = QdrantClient('http://192.168.100.111:6333')
    vectors_config = models.VectorParams(size=1024, distance=models.Distance.COSINE)
    if qdrant_client.collection_exists(collection_name=collection_name):
        qdrant_client.delete_collection(collection_name)
    qdrant_client.create_collection(collection_name=collection_name, vectors_config=vectors_config)


if __name__ == '__main__':
    recreate_collection()
    doc_retriever: DocRetriever = default_context['DocRetriever']
    path = Path('../data')
    for file in path.rglob('*.docx'):
        p = str(file.absolute())
        loader = DocxLoader(p)
        docs = loader.load()
        for doc in tqdm(docs, desc=loader.filename):
            doc_retriever.QdrantVectorStore.add_documents([doc])
