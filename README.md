# zipind
Zipind - From a folder, make a splitted ZIP with INDependent parts

Source: https://github.com/apenasrr/zipind

Compresses a folder into independent parts.

Works in hybrid mode with features:

- Compact folder dividing into independent parts, grouping your files in
 alphanumeric order.
- Respects the ordering of folders and files.
- Respects the internal structure of folders.
- If any file is larger than the defined maximum size, the specific file is partitioned in dependent mode.
- Set file types to be ignored in compression (config/ignore_extensions.txt)

Requirement:

- To compress to Zip format, It is necessary to have [7Zip](https://www.7-zip.org/download.html) app installed and added in system variables
- To compress to Rar format, It is necessary to have [Winrar](https://www.win-rar.com/download.html) app installed and added in system variables

Support:

- Compression to .zip or .rar
  - Set on `config.ini`. flag mode: zip or rar

## Usage

### From interactive terminal

- Execute `zipind.bat`
- Follow the terminal instructions

### From CLI interface

- Open a terminal in the same folder as this repository
- Enter: `python zipind_cli.py --help` for more instructions

#### Examples

To pack the a folder with 'rar' extension, each part having up to 1000 MB and ignoring mp4 files\
`python zipind_cli.py c:\input_folder -s 1000 -m rar -i mp4 c:\output_folder`

To pack the a folder with 'zip' extension, each part having up to 2000 MB\
`python zipind_cli.py c:\input_folder -s 2000 -m zip c:\output_folder`

---
Do you wish to buy a coffee to say thanks?
LBC (from LBRY) digital Wallet
> bFmGgebff4kRfo5pXUTZrhAL3zW2GXwJSX

### We recommend:
[mises.org](https://mises.org/) - Educate yourself about economic and political freedom\
[lbry.tv](http://lbry.tv/) - Store files and videos on blockchain ensuring free speech\
[A Cypherpunk's Manifesto](https://www.activism.net/cypherpunk/manifesto.html) - How encryption is essential to Free Speech and Privacy