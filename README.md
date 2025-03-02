# **FastAPI-DynCache** 🚀  
**A FastAPI-based application with dynamic caching support using Memcached.**  
This project allows **enabling/disabling caching dynamically** using environment variables, improving API performance and flexibility.  

---

## **📌 Features**  
✅ **Dynamic Caching** – Enable/Disable caching via `.env` configuration  
✅ **Memcached Integration** – Uses **Memcached** for efficient request caching  
✅ **Custom Decorator (`@cache_if_enabled`)** – Simplifies caching in endpoints  
✅ **Environment-Controlled Initialization** – Prevents unnecessary cache setup  
✅ **Manual Cache Clearing Support**  

---

## **🛠️ Installation**  

### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/your-username/FastAPI-DynCache.git
cd FastAPI-DynCache
```

### **2️⃣ Create & Activate Virtual Environment**  
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### **3️⃣ Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **4️⃣ Start Memcached**  
#### **Using Docker (Recommended)**
```bash
docker run -d --name memcached -p 11211:11211 memcached
```
#### **Without Docker (Native Installation)**
- **Ubuntu:** `sudo apt install memcached`
- **Mac (Homebrew):** `brew install memcached`
- **Windows:** Use **Memurai** or **Docker**.

---

## **⚙️ Configuration (`.env` File)**  
Create a `.env` file in the project root:  

```ini
ENABLE_CACHE=True
MEMCACHED_HOST=localhost
MEMCACHED_PORT=11211
```
- Set `ENABLE_CACHE=False` to disable caching dynamically.

---

## **🚀 Running the Application**  
```bash
uvicorn main:app --reload
```

---

## **📌 API Endpoints**  

| **Method** | **Endpoint**          | **Description**                                        |
|-----------|----------------------|--------------------------------------------------------|
| `GET`    | `/nocache`            | Returns a response without caching                    |
| `GET`    | `/cache`              | Returns a **cached response** (if enabled)            |
| `GET`    | `/custom/{item_id}`    | Caches response per `item_id`                         |
| `GET`    | `/clear-cache`         | Clears the cache manually                             |

### **🛠️ Testing API**
```bash
curl http://127.0.0.1:8000/cache
```
- First call takes **~2s** (Simulated expensive computation).
- Subsequent calls **return instantly (cached for 10s).**

```bash
curl http://127.0.0.1:8000/clear-cache
```
- Clears the cache.

---

## **🛠️ Code Overview**  

### **🔹 Project Structure**
```
FastAPI-DynCache/
│── main.py         # FastAPI app & endpoints
│── caching.py      # Cache initialization & custom decorators
│── config.py       # Environment-based configuration
│── .env            # Environment variables
│── requirements.txt # Dependencies
```

### **🔹 Caching Initialization (`caching.py`)**
```python
from fastapi_cache2 import FastAPICache
from fastapi_cache2.backends.memcached import MemcachedBackend
from pymemcache.client.base import Client as MemcacheClient
from fastapi_cache2.decorator import cache
from config import settings
import functools

def init_cache():
    """Initialize Memcached if caching is enabled."""
    if settings.ENABLE_CACHE:
        memcached_client = MemcacheClient((settings.MEMCACHED_HOST, settings.MEMCACHED_PORT))
        FastAPICache.init(MemcachedBackend(memcached_client), prefix="fastapi-cache")
    else:
        print("⚠️ Caching is DISABLED.")

def cache_if_enabled(expire: int):
    """Decorator to apply caching only when enabled."""
    def decorator(func):
        if settings.ENABLE_CACHE:
            return cache(expire=expire)(func)
        return functools.wraps(func)(func)  # Return the original function if caching is disabled
    return decorator
```

### **🔹 Usage in `main.py`**
```python
from fastapi import FastAPI
import time
from caching import init_cache, cache_if_enabled

app = FastAPI()

@app.on_event("startup")
def startup():
    init_cache()

@app.get("/cache")
@cache_if_enabled(expire=10)
async def cached_endpoint():
    time.sleep(2)
    return {"message": "Cached response", "timestamp": time.time()}
```

---

## **📌 Best Practices**
✅ Use **environment variables** for flexible caching control  
✅ **Avoid stale data** – Set cache expiration (`expire=10`)  
✅ Use **Memcached for high-speed caching**  
✅ **Manual cache clearing** for better control  

---

## **📜 License**  
This project is **open-source** under the **MIT License**.  

---

## **👨‍💻 Contributing**  
Pull requests are welcome! Feel free to contribute by:  
- Adding new features  
- Fixing bugs  
- Improving documentation  