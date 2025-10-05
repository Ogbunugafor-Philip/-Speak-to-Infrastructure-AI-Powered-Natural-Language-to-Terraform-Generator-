from transformers import pipeline

# Load a simple NLP pipeline for testing
nlp = pipeline("fill-mask", model="distilbert-base-uncased")

# Run a quick test
result = nlp("Terraform is a very [MASK] tool.")
print(result)
