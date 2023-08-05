### miclon 个人代码工具包

### APIS

- [Dict](kit/dict/addict.py)

```python
from kit.dict import Dict

d = Dict({'a': {'d': {'e': 100}}, 'b': 2, 'c': 3})
print(d.a.d.e)  # 100
print(d.a.c)  # {}
```