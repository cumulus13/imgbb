# ImgBB CLI (`imgbb-cli`)

A lightweight, production-ready Command Line Interface (CLI) tool and Python library for uploading images directly to [ImgBB](https://imgbb.com/) with beautiful terminal formatting via [Rich](https://github.com/Textualize/rich).

<p align="center">
  <img src="https://simgbb.com/images/logo.png" width="100%" alt="ImgBB Logo">
</p>

## Features

- **Environment Variable Support**: Automatically reads `IMGBB_API_KEY`.
- **Rich Terminal UI**: Includes upload progress bars, emojis, and cleanly sectioned outputs.
- **Flexible Output Formats**: Choose between sectionized rich view (`--format pretty`) or raw JSON (`--format json`) for scripting.
- **Advanced Options**: Custom naming and auto-expiration timers.

---

## Installation

Clone this repository or install it locally in editable mode:

```bash
pip install imgbb-cli
```

```bash
pip install . or pip install -e . # dev mode

```

---

## Configuration

Set your API key as an environment variable:

### Windows (PowerShell / CMD)

```cmd
setx IMGBB_API_KEY "your_api_key_here"

```

### Linux / macOS (Bash / Zsh)

```bash
export IMGBB_API_KEY="your_api_key_here"

```

---

## Usage

```bash
Usage: imgbb [-h] [-k API_KEY] [-e EXPIRATION] [-n NAME]
             [-f {pretty,json,url,display_url,delete_url,thumb_url,medium_url}]
             [IMAGES ...]

A production-ready CLI tool to upload images to ImgBB with wildcard support and flexible outputs.

Positional Arguments:
  IMAGES                Path or wildcard pattern to the image file(s) to upload (e.g., *.jpg,
                        image?.png, *).

Options:
  -h, --help            show this help message and exit
  -k, --key API_KEY     ImgBB API key. Can also be set via IMGBB_API_KEY environment variable.
  -e, --expiration EXPIRATION
                        Enable auto-deletion after given seconds (60-15552000).
  -n, --name NAME       Custom name for the uploaded image file (applicable if uploading a single
                        file).
  -f, --format {pretty,json,url,display_url,delete_url,thumb_url,medium_url}
                        Output format style or specific JSON field to extract: - pretty : Rich
                        formatted panel view (default) - json : Full raw JSON response - url :
                        Direct image URL only - display_url : Viewer / display page URL only -
                        delete_url : Deletion URL only - thumb_url : Thumbnail URL only -
                        medium_url : Medium image URL only
```

### 1. Standard Rich Output (Default)

Uploads the image with an interactive progress bar and structured, colorized sections:

```bash
imgbb-cli photo.png

```

### 2. Raw JSON Output (For Automation / Scripting)

If you want to parse the output in scripts, use `--format json`:

```bash
imgbb-cli photo.png --format json

```

### 3. Available Options

* `-k`, `--key`: Provide ImgBB API key explicitly.
* `-e`, `--expiration`: Set auto-deletion time in seconds (e.g., `86400` for 1 day).
* `-n`, `--name`: Specify a custom name for the uploaded file.
* `-f`, `--format`: Output format style (`pretty` or `json`). Default is `pretty`.
* `-h`, `--help`: Show help message.

**Example with options:**

```bash
imgbb-cli banner.png -e 3600 -n my_banner -f pretty

```

---

## License

[MIT](LICENSE)


## 👤 Author
        
[Hadi Cahyadi](mailto:cumulus13@gmail.com)
    

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/cumulus13)

[![Donate via Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/cumulus13)
 
[Support me on Patreon](https://www.patreon.com/cumulus13)
