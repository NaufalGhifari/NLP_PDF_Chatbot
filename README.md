# PDF question-answering chatbot 🗣️📄
A relatively simple NLP 'chatbot' able to comprehend user query and answer based on information in a given PDF file. Making good use of Haystack v1.25's ready-to-use ExtractiveQAPipeline to retrieve relevant excerpts and passing it to the reader for further comprehension. The answers are then scored and presented to the user.

This project **does not** make use of OpenAI's API nor any other API calls.

How it works:
- Extracts corpus (text) data from a PDF
- Using TextIndexingPipeline, convert corpus into haystack document object and store them in a DocumentStore
- Initialise BM25Retriever and FARMReader
- Connect retriever and reader using ExtractiveQAPipeline
- Run the pipeline and predict the answer to a given query

## Option 1: Clone repo and run
- Clone this repo and ```cd``` to the cloned dir
- run ```streamlit run app.py``` in the cli
- Access the web app at http://localhost:8501
- You are using the application

## Option 2: Use the Docker file
- Make sure you have [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Build the image on your end using ```docker build -t naufal_pdf_qa_chatbot_v1:1.0 .```

## Libraries 📚
- [Haystack](https://haystack.deepset.ai/)
- [Streamlit](https://streamlit.io/)

## References:
- Haystack v1.25 ExtractiveQAPipeline documentation: https://haystack.deepset.ai/tutorials/01_basic_qa_pipeline

## Author: Muhammad Naufal Al Ghifari
