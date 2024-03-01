# allm_urlscraper
This tool runs batch jobs to embed multiple URLs and it's subpages as document to Anything LLM.

- have docker installed
- Anything LLm up and running (tested with Ollama as LLM Backend and AnythingLLM Embedder)
- Anything LLM API Key is created
- clone repository
- change into directory
- change config.json to your needs

```
docker build . -t allm_urlscrapper
```

```
docker run -e API_KEY={{your_api_key}} allm_urlscrapper
```