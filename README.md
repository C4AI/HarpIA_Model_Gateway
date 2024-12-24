# HarpIA Model Gateway

This repository contains a Python implementation of an answer
provider backend server for the
[HarpIA Ajax](../../../moodle-local_harpiaajax) Moodle plugin.

### Current provider classes:

- `ConstantAnswerProvider`: always generates the same answer regardless of the input.
- `EchoAnswerProvider`: always echoes the input, optionally converting it to uppercase.
- `GPTAnswerProvider`: uses OpenAI API to obtain the answers from GPT models.
- `OllamaAnswerProvider`: uses Ollama API to obtain the answers from several local
  models.

### Requirements:

- Python &geq; 3.11;
- Docker (recommended).

### Usage instructions:

- Create a configuration file. Create a copy of the
  [config_TEMPLATE.py](config/config_TEMPLATE.py) file and edit it
  to choose the models that will be provided. Follow the instructions in the file.

- Build the Docker image:

  ```shell
  docker build -t harpia-model-gateway:1.0 -f containers/prod/Dockerfile .
  ```

- Test an answer provider by interacting with it on a terminal
  (replace `./config/config1.py` with the path to your configuration file,
  and replace `ECHO` with the name of the desired model as specified in the
  configuration):

  ```shell
  docker run --rm -it --name harpia-gateway -v './config/config1.py':/cfg.py harpia-model-gateway:1.0 --config=/cfg.py cli --provider='ECHO'
  ```
