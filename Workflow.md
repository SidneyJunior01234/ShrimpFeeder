## ✅ Pipeline: From Raw WAVs to Final Comparison Plots

### 🔧 **CORE UTILITY MODULE (used by batch scripts)**

**1.** `src/detection/click_detection_utils.py`

* **Functions**:

  * `detect_clicks(file_path, config)`
  * `save_detection_results(df, output_path, wav_path)`
* **Purpose**: Implements the core DSP-based click detection logic and CSV saving.
* 💡 This module is **imported** by `click_detection_batch.py` and **should not be run directly**.

---

### 🏃‍♂️ **EXECUTION SCRIPTS (Run these in sequence)**

**2.** `src/detection/click_detection_batch.py`

* Detects click events for all `.wav` files under `data/raw/`
* Saves output as: `data/metadata/model_detections/**/{filename}_events.csv`

```bash
python src/detection/click_detection_batch.py
```

---

**3.** `src/aggregation/aggregate_detections_batch.py`

* Aggregates click events using sliding time windows (e.g., 60s).
* Input: `*_events.csv`
* Output: `*_aggregated.csv`

```bash
python src/aggregation/aggregate_detections_batch.py model_detections
python src/aggregation/aggregate_detections_batch.py reference_detections
```

---

**4.** `src/aggregation/joint_aggregate_detections.py`

* Concatenates all `*_aggregated.csv` files in a folder, preserving time continuity.
* Output: `*_joint.csv` for each trial folder.

```bash
python src/aggregation/joint_aggregate_detections.py model_detections
python src/aggregation/joint_aggregate_detections.py reference_detections
```

---

**5.** `src/visualization/plot_detection_comparison.py`

* Plots side-by-side comparison between model and reference detections.
* Input: `*_joint.csv` from both folders.
* Output: `data/figures/comparison/{trial_name}_comparison.png`

```bash
python src/visualization/plot_detection_comparison.py
```

---

### 🧪 Optional

**notebooks/exploratory/detection\_analysis.ipynb**

* Interactive exploration of detection, parameter tuning, and feature visualization.

---

## 🧭 Summary of Core and Scripts

| Type            | Script/Module                   | Purpose                                 |
| --------------- | ------------------------------- | --------------------------------------- |
| 🔧 Core Utility | `click_detection_utils.py`      | Implements detection + CSV saving       |
| ▶️ Script       | `click_detection_batch.py`      | Run detection for all `.wav` files      |
| ▶️ Script       | `aggregate_detections_batch.py` | Aggregate detection events              |
| ▶️ Script       | `joint_aggregate_detections.py` | Combine aggregated results across files |
| ▶️ Script       | `plot_detection_comparison.py`  | Generate comparison plots               |
| 📓 Notebook     | `detection_analysis.ipynb`      | Interactive analysis of detection logic |