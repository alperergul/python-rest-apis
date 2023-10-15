FROM python:3

WORKDIR C:/Users/alper/AlperProjects/RestApi-Python/text-similarity/web
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python -m spacy download en_core_web_sm
CMD [ "python", "app.py" ]