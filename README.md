# Naufals_NLP
An NLP 'chatbot' able to comprehend user query and answer based on information in a given PDF file. Making good use of Haystack v1.25's ready-to-use ExtractiveQAPipeline to retrieve relevant excerpts and passing it to the reader for further comprehension. The answers are then scored and presented to the user.

This project does not make use of OpenAI's API nor any other API calls.

How it works:
- Extracts corpus (text) data from a PDF
- Using TextIndexingPipeline, convert corpus into haystack document object and store them in a DocumentStore
- Initialise BM25Retriever and FARMReader
- Connect retriever and reader using ExtractiveQAPipeline
- Run the pipeline and predict the answer to a given query


## Libraries
- [Haystack](https://haystack.deepset.ai/)
- [Streamlit](https://streamlit.io/)


## References:



## Author: Muhammad Naufal Al Ghifari
