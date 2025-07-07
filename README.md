# Caching Proxy Server

# Caching Proxy Server
A CLI-powered HTTP caching proxy server built with FastAPI and httpx.
It forwards client requests to an origin server, caches the responses, and serves cached content on repeated requests — improving performance and reducing load on the origin.

📌 Inspired by caching and proxy design patterns.
📌 [Project Roadmap Source](https://roadmap.sh/projects/caching-server)

---

## 🚀 Features
- ✅ CLI to start the proxy server with custom port and origin URL
- ✅ Forwards requests to the origin server and caches responses
- ✅ Returns cached responses for identical repeated requests
- ✅ Adds X-Cache: HIT or X-Cache: MISS to indicate cache status
- ✅ Manual cache clearing via CLI command
- 🔁 Handles redirects and rewrites Location headers
- ⏳ Cache TTL (Time-to-Live) support (default: 5 minutes)
- 🧪 Built-in logging and debug support
---

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **HTTP Client**: httpx(async)
- **CLI TOOL**: Typer
- **RunTime**: Uvicorn


---

## 📦 Installation

1. Clone the repository

```bash
git clone https://github.com/eniolaomotee/Caching_Proxy_Server.git
cd caching-proxy-server
```

2. Create and activate a Virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 🚀 Usage

1. Start the Proxy Server
```bash
python main.py run --port 3001 --origin https://dummyjson.com

```
This starts the proxy on http://localhost:3001 and forwards requests to https://dummyjson.com.



2. Make requests via proxy
Sends a request to:
```bash
http://localhost:3001/products
```
It will be forwarded to:

```bash
https://dummyjson.com/products
```

You’ll get an X-Cache: MISS on the first request and X-Cache: HIT on repeated identical requests.

3. Clear the cache
```bash
python main.py clear-cache-cmd

```


### This project is licensed under the MIT License.
