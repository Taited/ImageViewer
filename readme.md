# FastAPI Setup

## Requirements

- Python 3.x
- `uvicorn` (`pip install uvicorn`)
- SSL key and certificate files (`select.key`, `select.crt`)

## How to Run

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Start the app:

   ```bash
   python app.py
   ```

   - Runs on `https://0.0.0.0:5001`
   - To change the port or disable SSL, edit `app.py`:

   ```python
   uvicorn.run('app:app', port=YOUR_PORT, ssl_keyfile=None, ssl_certfile=None)
   ```

3. API can only access image files in `IMAGE_DIR` (default: `./`). To change the directory, edit `IMAGE_DIR` in `app.py`.

4. Place a unique JSON file in `jsons/` (follow `jsons/demo.json` for format).

## Example

Access the API at:

```
https://localhost:5001/image/
```

Replace `{item_name}` with the image filename in `IMAGE_DIR`.
