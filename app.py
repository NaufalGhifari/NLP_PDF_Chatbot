import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from PyPDF2 import PdfReader

from haystack.document_stores import InMemoryDocumentStore
from haystack.pipelines.standard_pipelines import TextIndexingPipeline
from haystack.nodes import BM25Retriever
from haystack.nodes import FARMReader
from haystack.pipelines import ExtractiveQAPipeline

# create sidebar
with st.sidebar:
    st.title("LLM PDF Chat App")
    st.markdown('''
    ### About 
    This app is a relatively simple LLM-powered chatbot capable of answering user queries based on information in a given PDF file. Primarily based on Haystack v1.25's ExtractiveQAPipeline and presented using Streamlit.
                
    ### Libraries
    - [Streamlit](https://streamlit.io/)
    - [Haystack (v1.25)](https://haystack.deepset.ai/)
    - [NLTK](https://www.nltk.org/)
    - [PyTorch](https://pytorch.org/)
                
    ### How it works:
    1. Takes a pdf
    2. Extracts text data and stores it in DocumentStore 
    3. Initialises BM25Retriever and FARMReader
    4. Connects reader & retriever with ExtractiveQAPipeline
    5. Process user query & display answer
    ''')

    add_vertical_space(5)
    st.write("Author: Muhammad Naufal Al Ghifari")

def print_answer(ans):
    """Prints out the answers data. Return: Void."""
    ans_text = ans.answer
    context = ans.context
    score = ans.score

    st.write(f"**Answer**:\n{ans_text}")
    st.write(f"**Score**:\n{round(score*100, 2)}%")
    st.write(f"**Context**:\n{context}")
    st.markdown("""---""")

def main():
    st.header("Query your PDF🗣️📄")
    pdf = st.file_uploader("Upload your PDF", type="pdf")
    
    if pdf is not None:
        # read the pdf
        pdf_reader = PdfReader(pdf)
        
        # extract the text from each page
        full_text = ""
        for page in pdf_reader.pages:
            full_text += page.extract_text()

        # save the text data
        with open(f"data.txt", "w", encoding="utf-8") as f:
            f.write(full_text)

        # initialise DocumentStore 
        document_store = InMemoryDocumentStore(use_bm25=True)

        # store corpus as haystack document object
        path = ["./data.txt"]
        indexing_pipeline = TextIndexingPipeline(document_store)
        indexing_pipeline.run_batch(file_paths=path)

        # initialise retriever and reader
        my_retriever = BM25Retriever(document_store=document_store)
        my_reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)

        # connect retriever and reader using ExctractiveQAPipeline
        pipe = ExtractiveQAPipeline(my_reader, my_retriever)

        # get user query
        user_query = st.text_input("Ask a question about your PDF here:")

        # get minimal confidence score
        min_confidence = st.slider("Minimal confidence score", 0.0, 1.0, 0.1)

        if user_query:
            # process query
            prediction = pipe.run(
                query=user_query,
                params= {"Retriever":{"top_k": 10}, "Reader":{"top_k": 5}},
                debug=True
            )

            # display the answers            
            answers = prediction['answers']

            # lists to store answers
            high_conf_answers = []
            low_conf_answers = []

            # display answers with confidence score abov min_confidence
            for i in range(len(answers)):
                ans = answers[i]
                if (ans.score >= min_confidence):
                    high_conf_answers.append(ans)
                else:
                    low_conf_answers.append(ans)

            # print answers
            st.write(f"#### {len(high_conf_answers)} answers found ():\n\n")
            for ans in high_conf_answers:
                print_answer(ans)

            st.write(f"#### {len(low_conf_answers)} less relevant answers found:\n\n")
            for ans in low_conf_answers:
                print_answer(ans)

            # delete by overwriting the user's extracted data with '''
            with open(f"data.txt", "w", encoding="utf-8") as f:
                f.write("")

if __name__ == "__main__":
    main()
