FROM python:3.10
WORKDIR /app
COPY src/ ./
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 10000
CMD ["python", "app.py"] 