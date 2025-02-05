# 📷 Screen Gif Recorder

Screen Gif Recorder is a Python-based tool that allows you to record a selected area of your screen and save it as an animated GIF. Using a fullscreen, semi-transparent window for region selection and the [Pillow](https://python-pillow.org/) library for image processing, the script continuously captures screenshots until you stop the recording with **CTRL+C** !!!

## Requirements

- Python 3.x
- [Pillow](https://python-pillow.org/) (Install via `pip install pillow`)
- `tkinter` (Usually included with Python)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/maxverwiebe/ScreenGifRecorder.git
   cd screen-gif-recorder
   ```

2. **Install the required dependencies:**

   ```bash
   pip install pillow
   ```

## Usage

Run the script with the desired parameters using Python:

```bash
python3 script.py [--quality QUALITY] [--output OUTPUT] [--delay DELAY]
```

### Command-Line Arguments

- `--quality` or `-q`:  
  Set the number of colors for the GIF (must be between 2 and 256).  
  _Default: 256_

- `--output` or `-o`:  
  Specify the output file name for the GIF.  
  _Default: output.gif_

- `--delay` or `-d`:  
  Define the delay between frames in seconds.  
  _Default: 0.1_

### Examples

- **Run with default settings:**

  ```bash
  python3 script.py
  ```

- **Custom quality and output file:**

  ```bash
  python3 script.py --quality 128 --output my_animation.gif
  ```

- **Custom delay between frames:**

  ```bash
  python3 script.py --delay 0.2
  ```

## How It Works

1. A fullscreen, semi-transparent window opens upon running the script. Click and drag your mouse to select the recording area, then release to confirm.

2. After the selection, the script starts capturing screenshots of the specified region at intervals defined by the delay parameter. Press **CTRL+C** in the terminal to stop recording.

3. Once recording stops, the captured frames are processed (converted to a palette mode with the specified quality) and saved as an animated GIF.

## Contributing
Contributions, issues, and feature requests are welcome!

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Disclaimer
This tool is provided "as is" without any warranty. Use it at your own risk.
```

---

Feel free to modify the content as needed for your project. Replace `your-username` with your actual GitHub username and adjust any other details specific to your project.
