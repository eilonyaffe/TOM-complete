# TOM

**TOM (The OSINT MATRIX)** is an information preservation system based on Input-Output inquiries. While it is designed for OSINT (Open Source Intelligence) applications, it can be adapted for other purposes.

## Features

- Structured data input and output handling
- Web interface for data interaction
- CSV-based data storage
- Modular design for extensibility

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/eilonyaffe/TOM-complete.git
   cd TOM-complete
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To start the application:

```bash
python server.py
```

Then, navigate to `http://localhost:5000` in your web browser to access the interface.

## Project Structure

- `server.py`: Main application script
- `templates/`: HTML templates for the web interface
- `static/`: Static files (CSS, JavaScript)
- `data1.csv`, `tools1.csv`: Sample data files
- `requirements.txt`: Python dependencies
- `install.txt`: Installation notes

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for enhancements or bug fixes.

## License

This project is open-source and available under the [MIT License](LICENSE).
