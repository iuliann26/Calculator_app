FROM python:3.10-slim
WORKDIR /app
copy . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD [ "python","app.py" ]