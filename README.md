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

- If you use Ollama on localhost:

    - Define a virtual name for the host's localhost that will be accessible from the container (e.g. `ollamaserver`);
    - Use that address in your configuration file (e.g. `"ollama_address": "http://ollamaserver:11434/api"`);
    - In the remaining steps, add `--add-host=ollamaserver:host-gateway` (replacing `ollamaserver` with the chosen name).
      The commands will look like `docker run --add-host=ollamaserver:host-gateway --rm [...]`.
    - Make sure that the communication between the containers is not blocked by firewalls or system settings.

- Test an answer provider by interacting with it on a terminal
  (replace `./config/config1.py` with the path to your configuration file,
  and replace `ECHO` with the name of the desired model as specified in the
  configuration):

  ```shell
  docker run --rm -it --name harpia-gateway -v './config/config1.py':/cfg.py harpia-model-gateway:1.0 --config=/cfg.py cli --provider='ECHO'
  ```

- Start the server
  (replace `./config/config1.py` with the path to your configuration file, optionally replace all instances of `42774` with the desired port):

  ```shell
  docker run --rm -it --name harpia-gateway -v './config/config1.py':/cfg.py -p 42774:42774 harpia-model-gateway:1.0 --config=/cfg.py server --host=0.0.0.0 --port=42774 --debug
  ```
  If it works as expected, the command can be run again replacing `-it` with `-d` (to run the container in the background) and removing `--debug`.

