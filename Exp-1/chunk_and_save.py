import json
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from embedding_generator import EmbeddingGenerator

def process_pdfs_and_embed():
    """
    Loads PDFs, chunks them, generates embeddings, and saves to a JSON file.
    """
    pdf_files = [
        "On the theoretical limitations of embedding based retrival.pdf",
        "Revisiting Neural Retrieval on Accelerators.pdf"
    ]
    
    all_chunks_data = []
    
    print("Loading embedding model...")
    embed_generator = EmbeddingGenerator()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=350,
        length_function=len,
    )
    
    for pdf_file in pdf_files:
        print(f"Processing {pdf_file}...")
        loader = PyPDFLoader(pdf_file)
        documents = loader.load()
        
        chunks = text_splitter.split_documents(documents)
        
        for i, chunk in enumerate(chunks):
            print(f"  - Generating embedding for chunk {i+1}/{len(chunks)}")

            embedding = embed_generator.get_embedding(chunk.page_content)
            
            chunk_data = {
                "pdf_name": pdf_file,
                "chunk_no": i + 1,
                "chunk_text": chunk.page_content,
                "embedding": embedding
            }
            all_chunks_data.append(chunk_data)

    output_filename = "chunks_with_embeddings.json"
    print(f"Saving all chunks and embeddings to {output_filename}...")
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(all_chunks_data, f, ensure_ascii=False, indent=4)
        
    print("Processing complete.")

if __name__ == '__main__':
    process_pdfs_and_embed()