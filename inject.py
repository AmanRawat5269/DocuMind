from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
# from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
import os

#Loading the Documents

all_docs =[]

for filename in os.listdir("./data"):  #os.listdir karke dynamically ek folder se sare lists utha sakte hai. os module import karra hai jo ki python library hai
    if filename.endswith(".pdf"):
        path_file = "./data/"+filename #yee path bana dia jo PyPDFLoader mai dal sake
        loader = PyPDFLoader(path_file)
        docs = loader.load()
        all_docs.extend(docs) #sab all_docs mai save kar dia
        print(f"Loaded: {filename} ({len(docs)} pages)")

        

print(f"Total no. of documents in all_docs : {len(all_docs)} ") #f indicates f-string means using f you can able to write the variables inside the string using {}. Ager ye nahi hoga to we have to write like this "Total no. of doc : "+ str(len(all_docs))



#Text splitting the Documents

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 50
)

splitted_result = splitter.split_documents(all_docs)

print(f"Total chunks are : {len(splitted_result)}")



#Embedding and vecctor storing 

embedding_vector = OllamaEmbeddings(model="nomic-embed-text")
vector_store=Chroma.from_documents(
    embedding= embedding_vector,
    documents = splitted_result,
    persist_directory = 'my_chroma_db', #name of the database
    collection_name = 'research_paper'# name of the table
)


print("Database created successfully!")


#retrieving from the database