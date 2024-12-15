# HarpIA Moodle - Answer Providers

This repository contains a Python implementation of an answer
provider backend server for the 
[HarpIA Ajax](../../../moodle-local_harpiaajax) Moodle plugin.

### Current provider classes:

- `ConstantAnswerProvider`: always generates the same answer regardless of the input.
- `EchoAnswerProvider`: always echoes the input, optionally converting it to uppercase.
- `GPTAnswerProvider`: uses OpenAI API to obtain the answers from GPT models.

### Requirements:

- Python &geq; 3.11.


### Usage instructions:

- Set the environment variables. For example, to read API keys from standard input:
```shell
read -s HARPIA_OPENAI_API_KEY; export HARPIA_OPENAI_API_KEY=$HARPIA_OPENAI_API_KEY;
```