# tsp-genetic

## Development

### Setup project

* Create/copy config file:
```sh
cp config_example.json config.json
```

* Change config settings if needed

* Create venv
```sh
python3 -m venv ./venv
```

* Activate venv
```sh
. ./venv/bin/activate
```


* Install libs
```sh
pip install -r ./requirements/dev.txt
```

* Run program
```py
python3 ./src/main.py
```

### Test code

* Linter (flake8)
```sh
flake8 ./src/
```

* Unit tests (pytest)
```sh
cd ./src/
python -m pytest tests/
```

## Selected TSP Instances

|Instance|  Number of Cities | Optimal Solution  |
|---|---|---|
| berlin11_modified |  11 |  4038 |
| berlin52  | 52  | 7542  |
| kroA100  | 100  | 21282  |
| kroA150  | 150  | 26524  |
| kroA200  | 200  | 29368  |
| fl417  | 417  | 11861  |
| ali535  | 535  | 202339  |
| gr666 | 666  | 294358  |
| nrw1379 | 1379  | 56638  |
| pr2392 | 2392  | 378032  |



### Instance format example
```
NAME: ali535
TYPE: TSP
COMMENT: 535 Airports around the globe (Padberg/Rinaldi)
DIMENSION: 535
EDGE_WEIGHT_TYPE: GEO
DISPLAY_DATA_TYPE: COORD_DISPLAY
NODE_COORD_SECTION
1  36.49  7.49
2  57.06  9.51
...
534  51.33  0.14
535  24.58  91.53
EOF
```