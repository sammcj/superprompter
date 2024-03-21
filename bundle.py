import argparse
import os
import PyInstaller.__main__

def parse_arguments():
    parser = argparse.ArgumentParser(description='Bundle the SuperPrompter app')
    parser.add_argument('--include-models', action='store_true', help='Include models in the bundled package')
    return parser.parse_args()

def main():
    args = parse_arguments()

    pyinstaller_args = [
        'superprompter.py',
        '--name=SuperPrompter',
        '--onefile',
        '--windowed',
        '--collect-all=transformers',
        '--collect-all=torch',
        '--icon=icon.ico',
    ]

    pyinstaller_args.extend(['--exclude-module', 'tensorboard'])

    if args.include_models:
        print("Including models in the bundled package, warning: this is untested and will make the package a lot larger!")
        modelDir = os.path.expanduser("~") + "/.superprompter/model_files"
        pyinstaller_args.extend(['--add-data', f'{modelDir}:model_files'])
        pyinstaller_args.extend(['--distpath=dist/with_models'])

    PyInstaller.__main__.run(pyinstaller_args)

if __name__ == '__main__':
    main()
