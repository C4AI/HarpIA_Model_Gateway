# HarpIA Model Gateway

HarpIA Model Gateway is a simple implementation of a
language model gateway for HarpIA, required by
[HarpIA Ajax](../../../moodle-local_harpiaajax) Moodle plugin.


We refer to language models as "answer providers".
A configuration file defines the list of answer providers
and their parameters. Currently, the following provider
classes are implemented:


- `GPTAnswerProvider`: uses OpenAI API to obtain the answers from GPT models;
- `OllamaAnswerProvider`: uses Ollama API to obtain the answers from
    [many local models](https://ollama.com/library), such as
    Llama, Mistral, Gemma, Qwen and DeepSeek;
- `ConstantAnswerProvider`: always generates the same answer regardless of the input
    (for testing purposes);
- `EchoAnswerProvider`: always echoes the input, optionally converting it to uppercase
    (for testing purposes).




[Installation instructions](../../wiki/Installation-instructions)

[Usage instructions](../../wiki/Usage-instructions)



