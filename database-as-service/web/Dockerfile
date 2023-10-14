FROM python:3
WORKDIR C:/Users/alper/AlperProjects/RestApi-Python/database-as-service/web
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python", "app.py" ]