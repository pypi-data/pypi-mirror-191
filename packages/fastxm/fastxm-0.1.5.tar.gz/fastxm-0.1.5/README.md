# fastxm

For cross-matching astronomical catalogs. Like `np.intersect1d` but faster. 

### Installation

From `PyPI`:

```bash
pip install fastxm
```

From source (requires [maturin](https://github.com/PyO3/maturin/)):

```bash
git clone https://github.com/al-jshen/fastxm
cd fastxm
maturin build --release
pip install target/release/<path to wheel>
```

### Example usage

```python
from fastxm import intersect_1d

catalog_1 = ...
catalog_2 = ...

match_ix_1, match_ix_2 = intersect_1d(catalog_1['common_id'], catalog_2['common_id'], parallel=True)
```

### Tests/Benchmarks

This requires `pytest` and `pytest-benchmark`.

```bash
git clone https://github.com/al-jshen/fastxm
cd fastxm
maturin develop
pytest
```
