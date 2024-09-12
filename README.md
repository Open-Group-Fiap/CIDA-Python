# Passos para rodar o servidor

1. Crie um arquivo `.env` com o seguinte conteúdo:

```
AZURE_AI_API_KEY=YOUR_API_KEY
AZURE_AI_ENDPOINT=YOUR_ENDPOINT
GEMINI_API_KEY=YOUR_API_KEY
```
(Ou baixe o arquivo que eu mandei no teams e renomeie para `.env`)

2. Instale as dependências:

```
pip install -r requirements.txt
```

3. Execute o servidor:

```
python -m uvicorn main:app --reload
```

4. Acesse o servidor em `http://localhost:8000/docs`

5. Envie um POST para o servidor no endereço `http://localhost:8000/analyze` com o seguinte corpo:

```
{
    "container": "container-name",
    "file_names": ["CIDA-2023-01-01.pdf", "CIDA-2023-02-01.pdf"]
}
```

6. O servidor retornará um objeto JSON com o resultado do processamento do relatório.

