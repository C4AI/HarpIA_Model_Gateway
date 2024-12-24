"""Configuration template."""

# INSTRUCTIONS:
# Create a copy of this file and edit it accordingly.
# In the variable ANSWER_PROVIDERS, keep only the models that will be used.
# Multiple instances can be used for the same class, as demonstrated in the example.
# Obtain API keys from a safe file or an environment variable.
#

_prompt = "You are a helpful assistant. Answer concisely."

ANSWER_PROVIDERS = [
    #
    # Dummy model that always return the same string:
    {
        "name": "Constant 1",
        "class": "ConstantAnswerProvider",
        "settings": {
            "message": "I will always send you this text.",
        },
    },
    #
    # Dummy model that always return the same string:
    {
        "name": "Constant 2",
        "class": "ConstantAnswerProvider",
        "settings": {
            "message": "Hi.",
        },
    },
    #
    # Dummy model that always echoes the input:
    {
        "name": "Echo",
        "class": "EchoAnswerProvider",
        "settings": {
            "to_uppercase": False,
        },
    },
    #
    # Dummy model that always echoes the input converted to uppercase:
    {
        "name": "ECHO",
        "class": "EchoAnswerProvider",
        "settings": {
            "to_uppercase": True,
        },
    },
    #
    # OpenAI's GPT model:
    {
        "name": "GPT-4o-mini",
        "class": "GPTAnswerProvider",
        "settings": {
            "default_system_prompt": _prompt,
            "api_key": "...",  # read it from an environment variable or file
            "model": "gpt-4o-mini",
            "temperature": 1.0,
            "top_p": 1.0,
        },
    },
    #
    # OpenAI's GPT model:
    {
        "name": "GPT-4o",
        "class": "GPTAnswerProvider",
        "settings": {
            "default_system_prompt": _prompt,
            "api_key": "...",  # read it from an environment variable or file
            "model": "gpt-4o",
            "temperature": 1.0,
            "top_p": 1.0,
        },
    },
    #
    # Meta's Llama model:
    {
        "name": "Llama 3.1 8B",
        "class": "OllamaAnswerProvider",
        "settings": {
            "default_system_prompt": _prompt,
            "model": "llama3.1:8b",
            "ollama_address": "http://localhost:11434/api",
            "extra_ollama_args": {},
        },
    },
    #
    # Google's Gemma model:
    {
        "name": "Gemma 2 9B",
        "class": "OllamaAnswerProvider",
        "settings": {
            "default_system_prompt": _prompt,
            "model": "gemma2:9b",
            "ollama_address": "http://localhost:11434/api",
            "extra_ollama_args": {},
        },
    },
    #
    # Mistral AI's Mistral model:
    {
        "name": "Mistral Nemo 12B",
        "class": "OllamaAnswerProvider",
        "settings": {
            "default_system_prompt": _prompt,
            "model": "mistral-nemo:12b",
            "ollama_address": "http://localhost:11434/api",
            "extra_ollama_args": {},
        },
    },
]
