# Dockerfile: contains a set of docker instructions to build a docker image.
# To build the docker image, run 'docker build -t naufal_pdf_qa_chatbot_v1:1.0 .'

# use python base image
FROM python:3.9-slim

# set working dire
WORKDIR /

# copy the requirements.txt
COPY requirements.txt .

# install all dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy all files in the current dir
COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
