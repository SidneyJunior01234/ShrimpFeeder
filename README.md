# Shrimp Click Detection using Passive Acoustic Monitoring

This repository implements a modular pipeline for detecting shrimp clicks using passive acoustic monitoring based on Digital Signal Processing (DSP) techniques. The objective is to develop a reproducible, scalable, and modular framework for quantifying shrimp feeding activity by analyzing acoustic data.

The project is structured to maintain a clear separation of processing stages: data processing, feature extraction, event detection, and aggregation. All parameter configurations are consolidated into a single `config.yaml` file for clarity and consistency.

---

## ✅ Project Structure

```

onset-shrimp-detection/
├── README.md                  # Project overview and documentation
├── requirements.txt           # Python dependencies
├── .gitignore                 # Files and directories to be excluded from version control
├── setup.py                   # Installation script for the package
├── setup_structure.py         # Script to automatically generate project structure and placeholder files
├── config/                    # Configuration files for parameter management
│   ├── __init__.py            # Marks the config directory as a package
│   └── config.yaml            # Single consolidated configuration file
├── data/                      # Data directory for organizing datasets
│   ├── __init__.py            # Marks the data directory as a package
│   ├── raw/                   # Unprocessed audio data
│   ├── processed/             # Processed datasets (e.g., segmented audio)
│   ├── interim/               # Temporary datasets during processing
│   └── metadata/              # Detection results and event annotations
├── models/                    # Directory for extracted features and potential ML models
│   ├── __init__.py
│   └── extracted_features/    # Feature vectors (e.g., SF, HFC, WPD, CD)
├── notebooks/                 # Jupyter notebooks for data exploration and experimentation
│   ├── __init__.py
│   └── exploratory/           # Exploratory Data Analysis (EDA)
├── src/                       # Source code for data processing, feature extraction, detection, and aggregation
│   ├── __init__.py
│   ├── config/                # Configuration management module
│   │   ├── __init__.py
│   │   └── config_loader.py   # Load configuration parameters
│   ├── data/                  # Data processing module
│   │   └── preprocess.py      # Audio loading and segmentation functions
│   ├── features/              # Feature extraction module
│   │   └── extract_features.py # DSP-based feature extraction (SF, HFC, WPD, CD)
│   ├── detection/             # Event detection module
│   │   ├── __init__.py
│   │   ├── detect_clicks.py       # Core detection logic for a single `.wav` file
│   │   └── process_directory.py   # Orchestrates multi-file processing and directory scanning
│   ├── visualization/                # Visualization tools for EDA, spectrograms, and result inspection
│   │   ├── __init__.py
│   │   ├── plot_setup.py       # Configures plot aesthetics
│   │   └── plot_spectrogram.py   # Plot spectrograms
│   └── aggregation/           # Aggregation module (future use)
│       └── aggregate_detections.py # Aggregate detection results over time
├── tests/                     # Unit and integration tests for DSP functions
│   ├── __init__.py
│   ├── test_data.py
│   ├── test_features.py
│   └── test_detection.py
└── logs/                      # Logs generated during data processing and detection

```

### 📂 Main Directories:
- **src/**: Core modules for data processing, feature extraction, detection, and (future) aggregation.
- **config/**: Single consolidated configuration file (`config.yaml`) for all processing parameters.
- **data/**: Data storage, including raw audio data, processed data, and detection outputs.
- **models/**: Placeholder for extracted features and potential ML model storage.
- **notebooks/**: Jupyter notebooks for exploratory data analysis and verification.
- **tests/**: Unit tests for core processing modules.
- **logs/**: Logs for monitoring data processing and detection workflows.

---

## ✅ Installation

1. Clone the repository:

```bash
git clone https://github.com/igendriz/onset-shrimp-detection.git
cd onset-shrimp-detection
```

2. Create a virtual environment and activate it:

```bash
python -m venv .venv
source .venv/bin/activate  # Unix/Mac
.venv\Scripts\activate  # Windows
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Verify the structure by running the setup script:

```bash
python setup_structure.py
```

---

## 🚀 Usage

1. **Data Processing:**

- Extract audio segments and preprocess data:

```bash
python src/data/preprocess.py
```

2. **Feature Extraction:**

- Compute SF, HFC, WPD, and CD for each audio segment:

```bash
python src/features/extract_features.py
```

3. **Onset Detection:**

- Detect click events and generate detection files:

```bash
python src/detection/event_detection.py
```

4. **Data Aggregation (Future Implementation):**

- Aggregate detection files over defined time windows (1-second windows, for example).

---

## ✅ Configuration

All parameters (e.g., window sizes, thresholds, frequency bands) are consolidated into a single configuration file located at `config/config.yaml`.

Example structure of `config/config.yaml`:

```yaml
audio:
  default_fs: 44100

processing:
  short_term_duration: 0.001
  mid_term_duration: 1.0

  detection:
    threshold: 0.2
    frequency_band:
      low: 1000
      high: 5000

aggregation:
  window_size: 1.0
```

---

## 🌱 Future Work

- Develop data aggregation and quantification for feeding activity analysis.
- Implement visualization tools for detection and aggregation results.
- Explore ML-based approaches for post-processing and event classification.

---

## 📄 License

This project is licensed under the MIT License.
