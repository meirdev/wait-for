# Wait For

Wait until the resource is available. Inspired by https://www.npmjs.com/package/wait-on.

## Example

```python
from wait_for import wait_for

# HTTP/HTTPS
wait_for("http://www.google.com")

# TCP/UDP
wait_for("tcp://127.0.0.1:8080", timeout=10)

# File
wait_for("file:///home/user/file.txt")
```
