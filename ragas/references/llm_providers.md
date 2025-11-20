# LLM Provider Configuration

## Overview

Ragas supports multiple LLM providers through wrappers. This guide covers configuration for major providers and best practices for selecting evaluator LLMs.

## Quick Configuration with llm_factory

The simplest way to use different providers:

```python
from ragas.llms import llm_factory

# OpenAI (default)
llm = llm_factory("gpt-4o")

# Anthropic Claude
llm = llm_factory("claude-3-5-sonnet-20241022", provider="anthropic")

# Google Gemini
llm = llm_factory("gemini-1.5-pro", provider="google")

# Local with Ollama
llm = llm_factory("mistral", provider="ollama", base_url="http://localhost:11434")
```

## OpenAI

### Basic Configuration

```python
from langchain_openai import ChatOpenAI
from ragas.llms import LangchainLLMWrapper

llm = LangchainLLMWrapper(ChatOpenAI(
    model="gpt-4o",
    temperature=0.0,
    api_key="your-api-key"  # Or set OPENAI_API_KEY env var
))
```

### With Embeddings

```python
from langchain_openai import OpenAIEmbeddings
from ragas.embeddings import LangchainEmbeddingsWrapper

embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings(
    model="text-embedding-3-large",
    api_key="your-api-key"
))
```

### Cost Optimization

```python
# Use GPT-3.5 for development
dev_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-3.5-turbo"))

# Use GPT-4 for production evaluation
prod_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o"))

# Use smaller embedding model
embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings(
    model="text-embedding-3-small"  # Cheaper alternative
))
```

**Model recommendations:**
- **Development/Testing:** gpt-3.5-turbo (~$0.002/1K tokens)
- **Production Evaluation:** gpt-4o (~$0.005-0.015/1K tokens)
- **High-Quality Evaluation:** gpt-4-turbo or gpt-4o-mini

## Azure OpenAI

### Configuration

```python
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

# Configure LLM
azure_llm = LangchainLLMWrapper(AzureChatOpenAI(
    openai_api_version="2023-05-15",
    azure_endpoint="https://your-endpoint.openai.azure.com/",
    azure_deployment="your-deployment-name",
    model="gpt-4o",
    temperature=0.0,
    api_key="your-azure-api-key",  # Or set AZURE_OPENAI_API_KEY
    validate_base_url=False
))

# Configure embeddings
azure_embeddings = LangchainEmbeddingsWrapper(AzureOpenAIEmbeddings(
    openai_api_version="2023-05-15",
    azure_endpoint="https://your-endpoint.openai.azure.com/",
    azure_deployment="your-embedding-deployment",
    model="text-embedding-3-large",
    api_key="your-azure-api-key"
))
```

### Environment Variables

```bash
export AZURE_OPENAI_API_KEY="your-key"
export AZURE_OPENAI_ENDPOINT="https://your-endpoint.openai.azure.com/"
export AZURE_OPENAI_API_VERSION="2023-05-15"
```

```python
# Use without explicit credentials
azure_llm = LangchainLLMWrapper(AzureChatOpenAI(
    azure_deployment="your-deployment-name",
    model="gpt-4o"
))
```

## Anthropic Claude

### Configuration

```python
from langchain_anthropic import ChatAnthropic
from ragas.llms import LangchainLLMWrapper

claude_llm = LangchainLLMWrapper(ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0.0,
    api_key="your-anthropic-api-key",  # Or set ANTHROPIC_API_KEY
    max_tokens=4096
))
```

**Model recommendations:**
- **High-Quality Evaluation:** claude-3-5-sonnet-20241022
- **Cost-Effective:** claude-3-haiku-20240307
- **Maximum Capability:** claude-3-opus-20240229

**Note:** Claude doesn't provide native embeddings. Use OpenAI or other providers for embedding models.

```python
# Claude for LLM, OpenAI for embeddings
claude_llm = LangchainLLMWrapper(ChatAnthropic(model="claude-3-5-sonnet-20241022"))
openai_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings())
```

## AWS Bedrock

### Configuration

```python
from langchain_aws import ChatBedrockConverse, BedrockEmbeddings
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

config = {
    "credentials_profile_name": "default",
    "region_name": "us-east-1",
    "llm": "anthropic.claude-3-5-sonnet-20241022-v2:0",
    "embeddings": "amazon.titan-embed-text-v2:0",
    "temperature": 0.4
}

# Configure LLM
bedrock_llm = LangchainLLMWrapper(ChatBedrockConverse(
    credentials_profile_name=config["credentials_profile_name"],
    region_name=config["region_name"],
    model=config["llm"],
    temperature=config["temperature"]
))

# Configure embeddings
bedrock_embeddings = LangchainEmbeddingsWrapper(BedrockEmbeddings(
    credentials_profile_name=config["credentials_profile_name"],
    region_name=config["region_name"],
    model_id=config["embeddings"]
))
```

**Available models on Bedrock:**
- Claude 3.5 Sonnet: `anthropic.claude-3-5-sonnet-20241022-v2:0`
- Claude 3 Opus: `anthropic.claude-3-opus-20240229-v1:0`
- Claude 3 Haiku: `anthropic.claude-3-haiku-20240307-v1:0`
- Titan Embeddings: `amazon.titan-embed-text-v2:0`

### IAM Permissions Required

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": [
        "arn:aws:bedrock:*::foundation-model/*"
      ]
    }
  ]
}
```

## Google Gemini

### Configuration

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from ragas.llms import LangchainLLMWrapper

gemini_llm = LangchainLLMWrapper(ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0.0,
    google_api_key="your-google-api-key"  # Or set GOOGLE_API_KEY
))
```

**Model recommendations:**
- **High-Quality:** gemini-1.5-pro
- **Fast & Cost-Effective:** gemini-1.5-flash

## Local Models (Ollama)

### Setup Ollama

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull mistral
ollama pull llama2
```

### Configuration

```python
from langchain_ollama import ChatOllama
from ragas.llms import LangchainLLMWrapper

ollama_llm = LangchainLLMWrapper(ChatOllama(
    model="mistral",
    base_url="http://localhost:11434",
    temperature=0.0
))
```

**Model recommendations (7B+ parameters):**
- mistral (7B) - Good balance
- llama2:13b - Better quality
- mixtral:8x7b - High quality
- neural-chat - Fast and accurate

**Important:** Use models with 7B+ parameters for reliable evaluation quality.

### Running Ollama Server

```bash
# Start Ollama server
ollama serve

# In another terminal, pull and run model
ollama run mistral
```

## Custom/Other Providers

For providers not directly supported:

```python
from ragas.llms import llm_factory

custom_llm = llm_factory(
    "model-name",
    api_key="your-api-key",
    base_url="https://your-api-endpoint"
)
```

Or use LangChain's generic interfaces:

```python
from langchain.chat_models import ChatOpenAI  # Works with OpenAI-compatible APIs
from ragas.llms import LangchainLLMWrapper

custom_llm = LangchainLLMWrapper(ChatOpenAI(
    model="model-name",
    openai_api_base="https://your-endpoint/v1",
    openai_api_key="your-key"
))
```

## LlamaIndex Integration

For LlamaIndex users:

```python
from llama_index.llms.openai import OpenAI
from ragas.llms import LlamaIndexLLMWrapper

llm = LlamaIndexLLMWrapper(OpenAI(
    model="gpt-4o",
    temperature=0.0
))
```

**Supported LlamaIndex LLMs:**
- OpenAI
- Anthropic
- Azure OpenAI
- Google Gemini
- Ollama
- HuggingFace

## Evaluation LLM Selection Guide

### Quality Tiers

**Tier 1 (Highest Quality):**
- GPT-4o, GPT-4-turbo
- Claude 3.5 Sonnet, Claude 3 Opus
- Gemini 1.5 Pro
- Best for production evaluation, critical assessments

**Tier 2 (Good Quality):**
- GPT-4o-mini
- Claude 3 Haiku
- Gemini 1.5 Flash
- Good for development, cost-sensitive production

**Tier 3 (Acceptable Quality):**
- GPT-3.5-turbo
- Mistral 7B (local)
- Suitable for development, quick iterations

**Not Recommended:**
- Models under 7B parameters
- Non-instruction-tuned models
- Very old models (GPT-3, etc.)

### Use Case Recommendations

**Development & Iteration:**
- LLM: GPT-3.5-turbo or GPT-4o-mini
- Embeddings: text-embedding-3-small
- Cost: ~$0.002-0.005 per sample

**Production Monitoring:**
- LLM: GPT-4o or Claude 3.5 Sonnet
- Embeddings: text-embedding-3-large
- Cost: ~$0.015-0.03 per sample

**High-Stakes Evaluation:**
- LLM: GPT-4-turbo or Claude 3 Opus
- Embeddings: text-embedding-3-large
- Cost: ~$0.03-0.06 per sample

**Budget-Conscious:**
- LLM: GPT-3.5-turbo for faithfulness/relevancy
- LLM: GPT-4o-mini for correctness/similarity
- Embeddings: text-embedding-3-small
- Mixed approach: ~$0.003-0.008 per sample

## Configuration Best Practices

1. **Use environment variables** for API keys (never hardcode)
2. **Set temperature to 0** for consistent evaluation
3. **Configure timeouts** for reliability
4. **Use retries** for production systems
5. **Monitor costs** with usage tracking
6. **Validate setup** before large-scale evaluation

### Production Configuration Example

```python
import os
from langchain_openai import ChatOpenAI
from ragas.llms import LangchainLLMWrapper

def get_evaluator_llm():
    """Production-ready LLM configuration."""
    return LangchainLLMWrapper(ChatOpenAI(
        model="gpt-4o",
        temperature=0.0,
        api_key=os.getenv("OPENAI_API_KEY"),
        max_retries=3,
        request_timeout=60,
        max_tokens=2000
    ))

def get_embeddings():
    """Production-ready embeddings configuration."""
    from langchain_openai import OpenAIEmbeddings
    from ragas.embeddings import LangchainEmbeddingsWrapper
    
    return LangchainEmbeddingsWrapper(OpenAIEmbeddings(
        model="text-embedding-3-large",
        api_key=os.getenv("OPENAI_API_KEY"),
        chunk_size=1000
    ))
```

## Troubleshooting

**Rate Limits:**
```python
from langchain_openai import ChatOpenAI

llm = LangchainLLMWrapper(ChatOpenAI(
    model="gpt-4o",
    max_retries=5,
    request_timeout=120
))
```

**API Errors:**
- Check API key validity
- Verify model name/availability
- Confirm endpoint URLs
- Review quota/rate limits

**Cost Management:**
```python
# Use cheaper models for less critical metrics
fast_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-3.5-turbo"))
quality_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o"))

# Assign appropriately
from ragas.metrics import Faithfulness, AnswerCorrectness

faithfulness = Faithfulness(llm=fast_llm)  # Less critical
correctness = AnswerCorrectness(llm=quality_llm)  # More critical
```
