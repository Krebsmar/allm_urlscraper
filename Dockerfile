# Verwenden Sie alpine:3.19.1 als Basisimage
FROM alpine:3.19.1

# Update the system
RUN apk update && apk upgrade

# Setzen Sie das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopieren Sie die Dateien aus Ihrem lokalen Host in das neue Arbeitsverzeichnis
COPY . /app

# Führen Sie Befehle in Ihrem neuen Image aus
# Zum Beispiel, installieren Sie einige Pakete
RUN apk add --no-cache python3 py3-pip && \
    pip3 install --no-cache-dir --break-system-packages -r requirements.txt

# Führen Sie einen Befehl aus, wenn der Container gestartet wird
CMD ["python3", "main.py"]