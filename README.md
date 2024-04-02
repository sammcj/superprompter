# SuperPrompter

SuperPrompter is a Python-based application that utilises the SuperPrompt-v1 model to generate optimised text prompts for AI/LLM image generation (for use with Stable Diffusion etc...) from user prompts.

See [Brian Fitzgerald's Blog](https://brianfitzgerald.xyz/prompt-augmentation/) for a detailed explanation of the SuperPrompt-v1 model and its capabilities / limitations.

## Features

- Utilises the [SuperPrompt-v1](https://huggingface.co/roborovski/superprompt-v1) model for text generation
- Basic graphical user interface built with tkinter
- Customisable generation parameters (max new tokens, repetition penalty, temperature, top p, top k, seed)
- Optional logging of input parameters and generated outputs
- Bundling options to include or exclude pre-downloaded model files
- Unloads the models when the application is idle to free up memory

![screenshot](https://github.com/sammcj/superprompter/assets/862951/0da94b0d-0ae9-4043-ab45-6daac2859443)

- [SuperPrompter](#superprompter)
  - [Features](#features)
  - [Prebuilt Binaries](#prebuilt-binaries)
  - [Building](#building)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Usage](#usage)
    - [Bundling](#bundling)
  - [Windows Usage](#windows-usage)
  - [Contributing](#contributing)
  - [License](#license)
  - [Acknowledgements](#acknowledgements)

## Prebuilt Binaries

Check [releases](https://github.com/sammcj/superprompter/releases) page to see if there are any prebuilt binaries available for your platform.

## Building

### Prerequisites

- Python 3.x
- Required Python packages (listed in `requirements.txt`)
- python-tk (`brew install python-tk`)

### Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/sammcj/SuperPrompter.git
   ```

2. Navigate to the project directory:

   ```shell
   cd SuperPrompter
   ```

3. Create a virtual environment (optional but recommended):

   ```shell
   make venv
   ```

4. Install the required packages:

   ```shell
   make install
   ```

### Usage

1. Run the application:

   ```shell
   make run
   ```

2. The application window will open, displaying a splash screen while checking for the SuperPrompt-v1 model files. If the model files are not found, they will be automatically downloaded.
3. Once the model is loaded, the main application window will appear. Enter your prompt in the "Your Prompt" text area.
4. Adjust the generation parameters (max new tokens (keep this around 77 for best results), repetition penalty, temperature, top p, top k, seed) as desired.
5. Click the "Generate" button or press Enter to generate text based on the provided prompt and parameters.
6. The generated output will be displayed in the "Output" text area.
7. Optionally, enable logging by checking the "Enable Logging" checkbox. When enabled, the input parameters and generated outputs will be saved to a log file named `~/.superprompter/superprompter_log.txt` in the user's home directory.

### Bundling

SuperPrompter can be bundled into a standalone executable using PyInstaller. The bundling process is automated with a `Makefile` and a `bundle.py` script.

To bundle the application:

1. Install deps

   ```shell
   make venv
   make install
   ```

2. Check it runs

   ```shell
   make run
   ```

3. Run the bundling command

   ```shell
   make bundle
   ```

   This command will download the SuperPrompt-v1 model files and bundle the application with the model files included.
   Alternatively, if you want to bundle the application without including the model files (they will be downloaded at runtime), run:

   ```shell
   make bundleWithOutModels
   ```

4. The bundled executable will be available in the `dist` directory.

## Windows Usage

The following steps have been contributed, I am not able to test on Windows so YMMV.

```cmd
git clone https://github.com/sammcj/superprompter
cd SuperPrompter

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
pip3 install torch --index-url https://download.pytorch.org/whl/cu121

python superprompter.py
```

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- The SuperPrompt-v1 model is developed by Roborovski and can be found at [https://huggingface.co/roborovski/superprompt-v1](https://huggingface.co/roborovski/superprompt-v1).
- The application uses the Transformers library by Hugging Face for working with the SuperPrompt-v1 model.
- [Acephaliax](https://www.reddit.com/user/Acephaliax/) on Reddit for the Windows instructions.
