# CIDA - Consulting Insights With Deep Analysis

## IAs utilizadas

- Phi-3.5 - Instruct Mini

- Gemini 1.5 - Flash

## Detalhamento da arquitetura de IA

A arquitetura de IA do CIDA é baseada em um pipeline de dois estágios, utilizando dois modelos de linguagem diferentes para otimizar o processo de análise de documentos e geração de insights:

1. **Resumo de documentos: Phi-3.5 Instruct Mini**
   - O Phi-3.5 Instruct Mini é utilizado para resumir os documentos de entrada.
   - Este modelo foi escolhido devido à sua eficiência em tarefas de resumo e sua capacidade de processar grandes volumes de texto rapidamente.
   - A implementação envolve o uso da API Azure AI, onde o modelo Phi-3.5 é acessado através do `ChatCompletionsClient`.

2. **Geração de insights: Gemini 1.5 Flash**
   - O Gemini 1.5 Flash é utilizado para analisar o resumo gerado e produzir insights de consultoria.
   - Este modelo foi selecionado por sua capacidade avançada de compreensão contextual e geração de conteúdo detalhado e relevante.
   - A implementação é feita através da biblioteca `google.generativeai`, que permite acessar o modelo Gemini diretamente.

### Razões para esta arquitetura:

1. **Eficiência de processamento**: O uso do Phi-3.5 para resumir documentos permite processar grandes quantidades de texto de forma rápida e eficiente, reduzindo a carga de trabalho para o modelo subsequente.

2. **Qualidade dos insights**: O Gemini 1.5 Flash, sendo um modelo mais avançado, é capaz de gerar insights mais profundos e relevantes a partir do resumo conciso.

3. **Flexibilidade**: Esta arquitetura em dois estágios permite ajustar cada etapa independentemente, otimizando o desempenho geral do sistema.

4. **Custo-efetividade**: Utilizando um modelo mais leve para o resumo inicial e um modelo mais potente apenas para a geração final de insights, consegue-se um equilíbrio entre desempenho e custo computacional.

### Implementação:

- O processo é implementado na função `analyze` no arquivo `main.py`.
- Primeiro, os documentos são processados e resumidos usando o Phi-3.5 através da Azure AI API.
- Em seguida, o resumo é passado para o Gemini 1.5 Flash com um prompt específico para geração de insights de consultoria.
- O resultado final é retornado como uma resposta HTTP contendo os insights gerados.

Esta arquitetura permite que o CIDA processe eficientemente grandes volumes de dados corporativos e produza análises e recomendações de alta qualidade, tornando-o uma ferramenta valiosa para consultoria empresarial baseada em IA.


## Funcionalidades da API

A API do CIDA oferece um conjunto robusto de funcionalidades para processamento e análise de documentos empresariais. Abaixo estão detalhadas as principais funcionalidades implementadas:

### 1. Análise de Documentos (`/analyze`)

- **Método**: POST
- **Descrição**: Esta é a funcionalidade principal da API, que processa e analisa documentos para gerar insights de consultoria.
- **Parâmetros de entrada**:
  - `container`: Nome do contêiner no Azure Blob Storage onde os documentos estão armazenados.
  - `file_names`: Lista de nomes de arquivos a serem analisados.
- **Processo**:
  1. Recupera os arquivos especificados do Azure Blob Storage.
  2. Extrai o texto dos documentos, suportando vários formatos (PDF, DOCX, XLSX, CSV, TXT).
  3. Utiliza o Phi-3.5 Instruct Mini para resumir o conteúdo dos documentos.
  4. Passa o resumo para o Gemini 1.5 Flash para gerar insights de consultoria.
- **Resposta**: Retorna um objeto JSON contendo os insights gerados.

### 2. Processamento de Diferentes Tipos de Arquivo

- **Descrição**: A API possui capacidade de extrair texto de diversos formatos de arquivo:
- PDF: Utiliza PyPDF2 para extrair texto de arquivos PDF.
- DOCX: Usa docx2txt para processar documentos do Word.
- XLSX: Emprega openpyxl para extrair dados de planilhas Excel.
- CSV: Processa arquivos CSV nativamente.
- TXT: Lê arquivos de texto simples.

### 3. Integração com Azure Blob Storage

- **Descrição**: A API se integra diretamente com o Azure Blob Storage para acessar e processar documentos.
- **Funcionalidades**:
- Recuperação de blobs individuais.
- Listagem de todos os blobs em um contêiner.
- Suporte para operações de leitura em diferentes tipos de arquivo armazenados no Blob Storage.

### 4. Listagem de Blobs (`/get-all-blobs/{container}`)

- **Método**: GET
- **Descrição**: Recupera uma lista de todos os blobs (arquivos) em um contêiner específico do Azure Blob Storage.
- **Parâmetros de entrada**:
  - `container`: Nome do contêiner no Azure Blob Storage.
- **Resposta**: Retorna um dicionário onde as chaves são os nomes dos blobs e os valores são as URLs correspondentes.

### 5. Documentação Automática da API (`/`)

- **Método**: GET
- **Descrição**: A rota raiz ("/") agora redireciona automaticamente para "/docs", onde é apresentada a documentação interativa da API.
- **Funcionalidade**:
  - Fornece uma interface Swagger UI para visualizar e interagir com todos os endpoints da API.
  - Permite aos desenvolvedores testar as rotas diretamente no navegador.
  - Oferece descrições detalhadas de cada endpoint, incluindo parâmetros de entrada e formatos de resposta.
  - Facilita a compreensão e o uso da API para novos usuários e desenvolvedores.

Esta mudança melhora significativamente a acessibilidade e usabilidade da API, fornecendo documentação clara e interativa diretamente através da interface web.

### 6. Configuração Flexível

- **Descrição**: A API utiliza variáveis de ambiente para configuração, permitindo fácil adaptação a diferentes ambientes e chaves de API.
- **Configurações**:
  - Chave de API e endpoint para Azure AI.
  - Chave de API para Gemini.
  - URL da conta do Azure Blob Storage.

### 7. Suporte CORS

- **Descrição**: A API implementa middleware CORS (Cross-Origin Resource Sharing), permitindo que ela seja acessada de diferentes origens, facilitando a integração com aplicações frontend.

## Passos para rodar o servidor

1. Crie um arquivo `.env` com o seguinte conteúdo:

```
AZURE_AI_API_KEY=YOUR_API_KEY
AZURE_AI_ENDPOINT=YOUR_ENDPOINT
GEMINI_API_KEY=YOUR_API_KEY
```
(Ou baixe o arquivo que eu enviei na entrega e renomeie para `.env`)

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

