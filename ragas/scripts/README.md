# Ragas Scripts

This directory contains utility scripts for working with Ragas test datasets and evaluations.

**⚠️ Ragas v0.2 Required:** These scripts are designed for Ragas v0.2+. If you're using v0.1, please update to v0.2 or see the migration guide: https://docs.ragas.io/en/stable/howtos/migrations/migrate_from_v01_to_v02/

## Installation

Install dependencies:

```bash
cd scripts
pip install -r requirements.txt
```

Set your API key:

```bash
export OPENAI_API_KEY="your-api-key"
```

## Scripts Overview

### 🎯 Test Data Generation (Priority)

#### 1. `generate_testset.py`
Generate synthetic test datasets from documents.

```bash
# Generate 50 questions from markdown files
python generate_testset.py docs/ --size 50 --output testset.json

# Custom question type distribution
python generate_testset.py docs/ --size 100 --simple 0.5 --reasoning 0.3 --multi-context 0.2

# From single file
python generate_testset.py document.pdf --size 20
```

**Options:**
- `--size N`: Number of questions to generate (default: 50)
- `--model MODEL`: LLM for generation (default: gpt-4o)
- `--simple/--reasoning/--multi-context`: Question type proportions
- `--chunk-size N`: Document chunk size (default: 1000)
- `--format json|csv`: Output format

#### 2. `augment_dataset.py`
Add missing fields to existing datasets (ground truth, contexts, responses).

```bash
# Add ground truth answers
python augment_dataset.py questions.json --add-reference

# Add retrieved contexts
python augment_dataset.py questions.json --add-contexts --num-contexts 3

# Add contexts from knowledge base
python augment_dataset.py questions.json --add-contexts --knowledge-base docs.txt

# Add everything
python augment_dataset.py questions.json --add-all --output complete.json
```

**Options:**
- `--add-reference`: Generate ground truth answers
- `--add-contexts`: Generate mock retrieved contexts
- `--add-response`: Generate RAG responses
- `--add-all`: Add all missing fields
- `--model MODEL`: LLM to use (default: gpt-4o)
- `--knowledge-base FILE`: Use knowledge base for context generation

#### 3. `analyze_testset.py`
Analyze test dataset quality and characteristics.

```bash
# Analyze dataset
python analyze_testset.py testset.json

# Save detailed report
python analyze_testset.py testset.json --report analysis.json

# Adjust duplicate threshold
python analyze_testset.py testset.json --similarity-threshold 0.85
```

**Features:**
- Basic statistics (sample counts, field coverage, lengths)
- Diversity analysis (lexical diversity, question types, keywords)
- Duplicate detection (exact and near-duplicates)
- Topic coverage analysis
- Quality scoring

#### 4. `convert_production_to_test.py`
Convert production traces/logs to test datasets.

```bash
# Convert LangSmith traces
python convert_production_to_test.py langsmith_export.json --output testset.json

# Remove PII
python convert_production_to_test.py traces.json --remove-pii

# Sample 100 diverse examples
python convert_production_to_test.py traces.json --sample-size 100 --sample-strategy diverse

# Force specific format
python convert_production_to_test.py data.json --format langfuse
```

**Supported formats:**
- LangSmith
- Langfuse
- Phoenix
- Generic RAG format (auto-detected)

### ✅ Dataset Validation

#### 5. `validate_dataset.py`
Validate dataset structure and metric compatibility.

```bash
# Validate structure
python validate_dataset.py testset.json

# Check metric compatibility
python validate_dataset.py testset.json --metrics Faithfulness AnswerRelevancy

# Get metric suggestions
python validate_dataset.py testset.json --suggest

# Generate report
python validate_dataset.py testset.json --report validation.json
```

**Checks:**
- Dataset structure (required fields, data types)
- Metric compatibility (field requirements)
- Suggests compatible metrics
- Identifies data quality issues

### 📊 Evaluation

#### 6. `evaluate_rag.py`
Run Ragas evaluations with CLI.

```bash
# Basic evaluation
python evaluate_rag.py testset.json --metrics Faithfulness AnswerRelevancy

# Custom model
python evaluate_rag.py testset.json --metrics Faithfulness --model gpt-4o-mini

# Multiple metrics with output
python evaluate_rag.py testset.json \\
    --metrics Faithfulness AnswerRelevancy ContextPrecision \\
    --output results.json

# Markdown report
python evaluate_rag.py testset.json --metrics Faithfulness --format markdown
```

**Available metrics:**
- Faithfulness
- AnswerRelevancy
- ContextPrecision
- ContextRecall
- AnswerCorrectness
- AnswerSimilarity
- ContextRelevancy

### 🔧 Dataset Utilities

#### 7. `merge_datasets.py`
Combine multiple test datasets.

```bash
# Merge datasets (with deduplication)
python merge_datasets.py dataset1.json dataset2.json --output merged.json

# Keep duplicates
python merge_datasets.py *.json --output all.json --no-deduplicate
```

#### 8. `split_dataset.py`
Split datasets into train/validation/test sets.

```bash
# 80/10/10 split
python split_dataset.py dataset.json --ratios 0.8 0.1 0.1

# Custom output directory
python split_dataset.py dataset.json --ratios 0.7 0.15 0.15 \\
    --output-dir splits/ --prefix my_data

# Reproducible split
python split_dataset.py dataset.json --ratios 0.8 0.1 0.1 --seed 42
```

## Common Workflows

### Workflow 1: Generate and Validate Test Data

```bash
# 1. Generate synthetic testset
python generate_testset.py docs/ --size 50 --output testset.json

# 2. Analyze quality
python analyze_testset.py testset.json --report analysis.json

# 3. Validate structure
python validate_dataset.py testset.json --suggest

# 4. Run evaluation
python evaluate_rag.py testset.json --metrics Faithfulness AnswerRelevancy
```

### Workflow 2: Convert Production Data

```bash
# 1. Convert production traces
python convert_production_to_test.py langsmith_export.json \\
    --remove-pii --sample-size 100 --output testset.json

# 2. Augment with missing fields
python augment_dataset.py testset.json --add-reference --output augmented.json

# 3. Validate before evaluation
python validate_dataset.py augmented.json --metrics Faithfulness ContextRecall

# 4. Run evaluation
python evaluate_rag.py augmented.json --metrics Faithfulness ContextRecall
```

### Workflow 3: Build Comprehensive Test Suite

```bash
# 1. Generate from multiple sources
python generate_testset.py docs/section1/ --size 30 --output test1.json
python generate_testset.py docs/section2/ --size 30 --output test2.json
python convert_production_to_test.py prod_logs.json --sample-size 40 --output test3.json

# 2. Merge datasets
python merge_datasets.py test1.json test2.json test3.json --output full_testset.json

# 3. Analyze merged dataset
python analyze_testset.py full_testset.json

# 4. Split for different purposes
python split_dataset.py full_testset.json --ratios 0.7 0.15 0.15 --output-dir splits/

# 5. Evaluate
python evaluate_rag.py splits/split_test.json --metrics Faithfulness AnswerRelevancy
```

## Tips

### Performance
- Use `gpt-4o-mini` for faster/cheaper generation when quality permits
- Generate smaller test sets first to validate your approach
- Use `--sample-size` to limit large production exports

### Quality
- Always run `analyze_testset.py` to check diversity
- Use `validate_dataset.py` before expensive evaluation runs
- Remove PII from production data with `--remove-pii`

### Cost Management
- Synthetic generation and augmentation use API calls
- Typical costs:
  - Generate 50 questions: ~$0.50-$1.00
  - Augment 50 samples (all fields): ~$1.00-$2.00
  - Evaluate 50 samples (3 metrics): ~$2.00-$4.00

## Troubleshooting

### Import Errors
```bash
pip install -r requirements.txt
```

### API Key Issues
```bash
export OPENAI_API_KEY="your-key"
# Or add to .env file
```

### Document Loading Errors
For PDFs:
```bash
pip install pdfminer.six
```

For Office documents:
```bash
pip install python-docx python-pptx
```

## Advanced Usage

### Custom LLM Providers

Azure OpenAI:
```python
# In your code, before running scripts:
export AZURE_OPENAI_ENDPOINT="https://your-endpoint.openai.azure.com/"
export AZURE_OPENAI_API_KEY="your-key"
```

Use with `--model azure/gpt-4o`

### Batch Processing

Process multiple directories:
```bash
for dir in docs/*/; do
    python generate_testset.py "$dir" --size 20 --output "testsets/$(basename $dir).json"
done
```

## Support

For issues or questions:
- Check the main SKILL.md for Ragas documentation
- See references/ folder for detailed guides
- Consult Ragas documentation: https://docs.ragas.io
