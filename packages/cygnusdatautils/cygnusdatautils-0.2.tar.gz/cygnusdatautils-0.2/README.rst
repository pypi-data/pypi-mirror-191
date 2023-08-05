# cygnusdatautils

## Installing:

```
pip install cygnusdatautils
```

## Usage:

```python
from cygnusdatautils import Cysharefile

sf = Cysharefile(hostname, client_id, client_secret, username, password)

token = sf.authenticate()

print(sf.get_dir_list_wrapper())



```