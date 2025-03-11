# HarpIA Model Gateway

This repository contains a Python implementation of an answer
provider backend server for the
[HarpIA Ajax](../../../moodle-local_harpiaajax) Moodle plugin.

[Installation instructions](../../wiki/Installation-instructions)

### Current provider classes:

- `ConstantAnswerProvider`: always generates the same answer regardless of the input.
- `EchoAnswerProvider`: always echoes the input, optionally converting it to uppercase.
- `GPTAnswerProvider`: uses OpenAI API to obtain the answers from GPT models.
- `OllamaAnswerProvider`: uses Ollama API to obtain the answers from several local
  models.

