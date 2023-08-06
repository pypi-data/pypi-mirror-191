# ML4Data Python SDK

Homepage: [https://ml4data.com](https://ml4data.com)

## Installation

### From setup

```bash
python3 setup.py install
```

## Usage

### NLP

```python
from ml4data import NLPClient
client = NLPClient('YOUR API KEY HERE!')
client.analyze_sentiment("Este cine no esta bueno porque era muy sucio")
```

### Vision 

```python
from ml4data import VisionClient
client = VisionClient('YOUR API KEY HERE!')
client.detect_objects('examples/restaurant.png')
```

