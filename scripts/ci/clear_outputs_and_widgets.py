import argparse
import json
import sys

def main():
    parser = argparse.ArgumentParser(description='Check if a Jupyter notebook has cleared output and widget states.')
    parser.add_argument('file', metavar='FILE', help='path to the Jupyter notebook file')
    args = parser.parse_args()

    with open(args.file, 'r') as f:
        notebook = json.load(f)

    has_output_or_widgets = False
    for cell in notebook['cells']:
        if 'outputs' in cell and cell['outputs']:
            has_output_or_widgets = True
            print(f"Notebook '{args.file}' has uncleared output")
            break

        if 'metadata' in cell and 'widgets' in cell['metadata']:
            has_output_or_widgets = True
            print(f"Notebook '{args.file}' has uncleared widget states")
            break
        
    if has_output_or_widgets:
        sys.exit(1)
    else:
        print(f"Notebook '{args.file} is clear")
        sys.exit(0)

if __name__ == '__main__':
    main()
