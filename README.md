# WATER METER Extraction with YOLOv10 and PaddleOCR & Save Data to SQL Database

## How to run:

```bash
git clone https://github.com/sunsmarterjie/yolov12.git
```

```bash
conda create -n cvproj python=3.11 -y
```

```bash
conda activate cvproj
```

```bash
pip install -r requirements.txt
```

```bash
cd yolov12
```

```bash
pip install -e .
```

```bash
cd ..
```

```bash
python sqldb.py
```

```bash
python main.py
```

## Error Fixed

```bash
pip uninstall numpy
```

```bash
pip install numpy==1.26.4
```

```bash
pip install opencv-python
```

### sqlite viewer:

https://inloop.github.io/sqlite-viewer/


