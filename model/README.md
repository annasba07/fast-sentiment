# DistilBERT Fine-tuned Model

This directory should contain the fine-tuned DistilBERT model for sentiment analysis. The model files are large and not included in the repository. Follow the instructions below to download the model.

## Download the Model

To download the model, you'll need Git LFS (Large File Storage):

1. Install Git LFS if you haven't already:
```bash
# macOS (using Homebrew)
brew install git-lfs

# Ubuntu/Debian
sudo apt-get install git-lfs

# Windows (using Chocolatey)
choco install git-lfs
```

2. Initialize Git LFS:
```bash
git lfs install
```

3. Clone the model repository from Hugging Face:
```bash
git clone https://huggingface.co/winegarj/distilbert-base-uncased-finetuned-sst2 distilbert-base-uncased-finetuned-sst2
```

After downloading, your directory structure should look like:

```
model/
├── README.md
└── distilbert-base-uncased-finetuned-sst2/
    ├── config.json
    ├── model.safetensors
    ├── special_tokens_map.json
    ├── tokenizer.json
    ├── tokenizer_config.json
    └── vocab.txt
```

## Model Details

- **Architecture**: DistilBERT (a distilled version of BERT)
- **Training Data**: SST-2 (Stanford Sentiment Treebank)
- **Task**: Binary sentiment classification (positive/negative)
- **Size**: Approximately 250MB
- **Performance**: State-of-the-art results with reduced resource requirements

This model is fine-tuned for sentiment analysis and can classify text as positive or negative with corresponding confidence scores.

## Model Usage

The model is automatically loaded by the API and used for inference. You don't need to load it manually.

If you want to use the model directly, you can do so with the Hugging Face Transformers library:

```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

model_path = "./distilbert-base-uncased-finetuned-sst2"
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
classifier = pipeline(
    task="text-classification",
    model=model,
    tokenizer=tokenizer,
    top_k=None,
)

# Make predictions
result = classifier(["I love this product!", "This is terrible."])
print(result)
```