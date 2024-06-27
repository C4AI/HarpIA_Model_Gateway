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
