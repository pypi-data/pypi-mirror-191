# vlogging
Easy to use logger.

## Installation
```
$ pip install vlogging
```

Install from github:
```
$ pip install git+https://github.com/yuyahnd/vlogging.git
```

To develop:
```
$ git clone https://github.com/yuyahnd/vlogging.git
$ pip install -e ./vlogging[dev]
```

## Usage

```bash
>>> import vlogging
>>> vlogging.info("Hello vlogging!")
2023-02-10 15:24:31.358 INFO     Hello vlogging!
```

```python
import vlogging
logger = vlogging.getLogger(__name__)
logger.info("Hello vlogging!")
# 2023-02-10 15:24:31.358 INFO     Hello vlogging!
```


## License
This repository is licensed under the MIT license. See LICENSE for details.

&copy; 2023 Yuya Honda
