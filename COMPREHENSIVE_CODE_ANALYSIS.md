# VARTAPRAVAH Project - Comprehensive Code Analysis Report
**Date:** April 26, 2026  
**Total Issues Found:** 32  
**Critical:** 12 | **High:** 10 | **Medium:** 7 | **Low:** 3

---

## Table of Contents
1. [Critical Issues (12)](#critical-issues)
2. [High Severity Issues (10)](#high-severity-issues)
3. [Medium Severity Issues (7)](#medium-severity-issues)
4. [Low Severity Issues (3)](#low-severity-issues)
5. [Dependency Analysis](#dependency-analysis)
6. [Docker Build Issues](#docker-build-issues)
7. [Environment Variables](#environment-variables)
8. [Summary & Recommendations](#summary--recommendations)

---

# CRITICAL ISSUES

## 1. Stream Engine Invalid Import
**File:** `app/services/stream_engine.py`  
**Line:** 1  
**Severity:** 🔴 CRITICAL  
**Error Type:** Import Error

### Issue
```python
from app import config  # ❌ WRONG
```

### Problem
This import is **invalid** because `stream_engine.py` is inside the `app` package. The statement tries to import `app` from within `app`, causing a circular import or ModuleNotFoundError.

### Suggested Fix
```python
import config  # ✅ CORRECT - relative import to parent package
# OR
from . import config  # ✅ ALTERNATIVE - explicit relative import
```

---

## 2. App Dockerfile - Wrong CMD Module Path
**File:** `app/Dockerfile`  
**Line:** 35  
**Severity:** 🔴 CRITICAL  
**Error Type:** Docker Build/Runtime Error

### Issue
```dockerfile
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Problem
The module `main.py` is located at `/app/app/main.py`, but the CMD tries to run `main:app`. This will fail with `ModuleNotFoundError: No module named 'main'`.

### Current Structure
```
/app/
  ├── app/
  │   └── main.py          ← actual location
  └── Dockerfile
```

### Suggested Fix
```dockerfile
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 3. Main.py - Unsafe Docker Control Endpoints
**File:** `app/main.py`  
**Lines:** 52, 56  
**Severity:** 🔴 CRITICAL  
**Error Type:** Runtime/Security Error

### Issue
```python
@app.get("/start")
def start_stream():
    os.system("docker start vartapravah_streamer")  # ❌ UNSAFE
    return {"status": "started"}

@app.get("/stop")
def stop_stream():
    os.system("docker stop vartapravah_streamer")   # ❌ UNSAFE
    return {"status": "stopped"}
```

### Problems
1. **Container Isolation:** When running inside Docker, the container doesn't have Docker socket by default
2. **Process Safety:** `os.system()` is unsafe and doesn't properly handle errors
3. **Security:** Direct system commands are a security risk

### Suggested Fix
Remove these endpoints or add Docker socket mounting:

```python
# In docker-compose.yml:
volumes:
  - /var/run/docker.sock:/var/run/docker.sock

# OR completely remove these endpoints if not needed
```

---

## 4. Main.py - Relative Paths in Static File Mounting
**File:** `app/main.py`  
**Lines:** 15, 17  
**Severity:** 🔴 CRITICAL  
**Error Type:** Runtime Error

### Issue
```python
app.mount("/static", StaticFiles(directory="app/static"), name="static")  # ❌ Relative path
# ...
app.mount("/videos", StaticFiles(directory="output"), name="videos")     # ❌ Relative path
```

### Problem
When running in Docker, the working directory is `/app`, so:
- `"app/static"` resolves to `/app/app/static` ❌
- `"output"` resolves to `/app/output` ✅ (only this one might work)

### Suggested Fix
```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
STATIC_DIR = BASE_DIR / "static"
OUTPUT_DIR = BASE_DIR / "output"

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.mount("/videos", StaticFiles(directory=str(OUTPUT_DIR)), name="videos")
```

Or use config:
```python
app.mount("/static", StaticFiles(directory=os.path.join(config.ASSETS_DIR, "..", "static")), name="static")
app.mount("/videos", StaticFiles(directory=config.OUTPUT_DIR), name="videos")
```

---

## 5. Redis Service Missing from Docker Compose
**Files:** `docker-compose.yml`, `docker-compose-hetzner.yml`, `docker-compose-oracle.yml`  
**Severity:** 🔴 CRITICAL  
**Error Type:** Service Configuration Error

### Issue
The code extensively uses Redis:
- `app/config.py`: Configures Redis connection
- `app/main.py` (line 13): Creates Redis client
- `app/workers/sadtalker_worker.py`: Uses Redis for queue
- `app/scheduler/scheduler.py`: Pushes tasks to Redis queue

But **NO Redis service** is defined in any docker-compose file!

### Problem
- Application will fail with `ConnectionRefusedError` on startup
- Queue operations will hang or fail

### Suggested Fix - Add to docker-compose.yml:
```yaml
services:
  redis:
    image: redis:7-alpine
    container_name: vartapravah_redis
    restart: always
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
```

---

## 6. Requirements.txt - No Version Pinning
**File:** `requirements.txt`  
**Severity:** 🔴 CRITICAL  
**Error Type:** Dependency Conflict

### Issue
```
fastapi              # ❌ No version
uvicorn              # ❌ No version
python-dotenv        # ❌ No version
groq                 # ❌ No version
redis                # ❌ No version
celery               # ❌ No version
requests             # ❌ No version
pydantic             # ❌ No version
moviepy              # ❌ No version
ffmpeg-python        # ❌ No version
TTS                  # ❌ No version
psycopg2-binary      # ❌ No version
```

### Problem
- Different installations will have different package versions
- Breaking changes in newer versions will cause failures
- Impossible to reproduce issues

### Suggested Fix
Pin all versions:
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-dotenv==1.0.0
groq==0.4.2
redis==5.0.0
celery==5.3.4
requests==2.31.0
pydantic==2.5.0
moviepy==1.0.3
ffmpeg-python==0.2.1
TTS==0.22.0
psycopg2-binary==2.9.9
```

---

## 7. App Requirements - Outdated NumPy
**File:** `app/requirements.txt`  
**Line:** 15  
**Severity:** 🔴 CRITICAL  
**Error Type:** Dependency Incompatibility

### Issue
```
numpy==1.22.0  # ❌ VERY OLD (Released May 2022)
```

### Problems
1. **Incompatible with Python 3.10+**: NumPy 1.22.0 has known issues with Python 3.10+
2. **Incompatible with modern packages**: TorchVision 0.16.0+ requires NumPy ≥ 1.21.0 but prefers ≥ 1.23.0
3. **Security issues**: Very old version has unpatched vulnerabilities
4. **Missing wheels**: Binary wheels for 1.22.0 may not be available for all platforms

### Suggested Fix
```
numpy==1.24.3  # Compatible with Python 3.10+ and modern packages
```

Or:
```
numpy>=1.24.0,<2.0.0  # More flexible versioning
```

---

## 8. Docker Compose Oracle - Incomplete
**File:** `docker-compose-oracle.yml`  
**Severity:** 🔴 CRITICAL  
**Error Type:** Service Configuration Error

### Issue
The oracle compose file is missing:
1. ❌ Database service (postgres)
2. ❌ Redis service
3. ❌ Only has streamer and dashboard services
4. ❌ Dashboard service has wrong port mapping (8888:80)

### Problem
- Main application cannot start (no database, no Redis)
- Configuration suggests Oracle deployment but lacks required services

### Suggested Fix
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: vartapravah
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD:-password}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    restart: always

  dashboard:
    build: ./app
    container_name: vartapravah_dashboard
    command: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
    ports:
      - "8000:8000"
    env_file: .env
    depends_on:
      - postgres
      - redis

  streamer:
    build: ./streamer
    container_name: vartapravah_stream
    restart: always
    env_file: .env

volumes:
  postgres_data:
```

---

## 9. SadTalker Dockerfile - Problematic Sed Patch
**File:** `sadtalker/Dockerfile`  
**Line:** 43  
**Severity:** 🔴 CRITICAL  
**Error Type:** Build Configuration Error

### Issue
```dockerfile
# 6. Patch basicsr (Compatibility Fix)
RUN sed -i "s/from torchvision.transforms.functional_tensor import rgb_to_grayscale/from torchvision.transforms.functional import rgb_to_grayscale/g" $(python -c 'import basicsr; print(basicsr.__path__[0])')/data/degradations.py || true
```

### Problems
1. **Ordering Issue**: Tries to import `basicsr` in the sed command but it's installed in next command
2. **Error Silenced**: `|| true` hides the actual error, making it hard to debug
3. **Path Fragility**: Assumes specific package structure
4. **Race Condition**: May execute before basicsr is fully installed

### Suggested Fix
Move to after basicsr installation:
```dockerfile
# Install base dependencies
RUN pip install numpy==1.26.4 Cython

# Install PyTorch
RUN pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cpu

# Install basic dependencies
RUN pip install tqdm yacs pyyaml librosa

# Install ML packages
RUN pip install face-alignment facexlib gfpgan imageio imageio-ffmpeg kornia ninja resampy dlib-bin

# NOW patch basicsr after it's installed
RUN pip install basicsr && \
    python -c "import basicsr; \
    basicsr_path = basicsr.__path__[0]; \
    deg_file = f'{basicsr_path}/data/degradations.py'; \
    import subprocess; \
    subprocess.run(['sed', '-i', 's/from torchvision.transforms.functional_tensor import rgb_to_grayscale/from torchvision.transforms.functional import rgb_to_grayscale/g', deg_file], check=False)"
```

---

## 10. Config.py - Path Resolution Issues
**File:** `app/config.py`  
**Lines:** 23-36  
**Severity:** 🔴 CRITICAL  
**Error Type:** Runtime Configuration Error

### Issue
```python
def get_assets_dir():
    # 1. Try absolute path (Standard Docker)
    if os.path.exists("/app/assets/promo.mp4"):
        return "/app/assets"
    
    # 2. Try nested path (Coolify specific)
    if os.path.exists("/app/app/assets/promo.mp4"):
        return "/app/app/assets"
    
    # 3. Local fallback
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "assets")
```

### Problems
1. **Unreliable during build**: Files don't exist during `docker build`, only after `COPY`
2. **Multiple fallbacks**: Creates ambiguity about actual location
3. **Hard to debug**: Multiple paths makes troubleshooting difficult
4. **Coolify inconsistency**: Suggests build context confusion

### Suggested Fix
Use explicit environment variables:
```python
import os
from dotenv import load_dotenv

load_dotenv()

ASSETS_DIR = os.getenv("ASSETS_DIR", "/app/assets")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/app/output")

# Validate on startup
if not os.path.exists(ASSETS_DIR):
    os.makedirs(ASSETS_DIR, exist_ok=True)
    print(f"⚠️ Created ASSETS_DIR: {ASSETS_DIR}")

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"⚠️ Created OUTPUT_DIR: {OUTPUT_DIR}")
```

---

## 11. Docker Compose Hetzner - Build Context Issue
**File:** `docker-compose-hetzner.yml`  
**Lines:** 6-16  
**Severity:** 🔴 CRITICAL  
**Error Type:** Service Configuration Error

### Issue
```yaml
app:
  build: ./app
  command: python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Problems
1. Build context is `./app`, so COPY operations look in `./app/` directory
2. But `main.py` is in the build context root (./app/main.py)
3. Command tries to run `main:app` which becomes `./app/main:app` ❌
4. This is inconsistent with docker-compose.yml which uses `.` context

### Suggested Fix
```yaml
app:
  build:
    context: .
    dockerfile: ./app/Dockerfile
  command: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Or use root Dockerfile:
```yaml
app:
  build: .
  command: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 12. Requirements - Missing Cython Dependency
**File:** `requirements.txt`  
**Severity:** 🔴 CRITICAL  
**Error Type:** Missing Dependency

### Issue
TTS package installation will fail because it requires Cython to compile:
- `TTS` depends on `librosa`
- `librosa` may need to compile extensions
- Cython is not listed as a dependency

### Problem
During `pip install -r requirements.txt`, you'll see:
```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed.
...
error: Microsoft Visual C++ 14.0 or greater is required.
```

### Suggested Fix
Add to requirements.txt:
```
Cython==0.29.36
numpy==1.24.3
# ... rest of packages
```

And update Dockerfile:
```dockerfile
RUN pip install --upgrade pip setuptools wheel Cython
RUN pip install -r requirements.txt
```

---

# HIGH SEVERITY ISSUES

## 1. App Dockerfile - Conflicting NumPy Installations
**File:** `app/Dockerfile`  
**Lines:** 24-25  
**Severity:** 🟠 HIGH  
**Error Type:** Build Configuration

### Issue
```dockerfile
RUN pip install numpy==1.22.0 Cython pyworld==0.3.4
RUN pip install -r requirements.txt  # also has numpy==1.22.0
```

### Problem
- NumPy installed twice (wasteful)
- No dependency coordination
- If requirements.txt changes, version inconsistency could occur

### Suggested Fix
```dockerfile
# Install base dependencies first
RUN pip install --upgrade pip setuptools wheel

# Install dependencies from requirements.txt (which should have numpy pinned)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install additional build-time dependencies if needed
RUN pip install Cython pyworld==0.3.4
```

---

## 2. Main.py - Missing Redis Error Handling
**File:** `app/main.py`  
**Line:** 13  
**Severity:** 🟠 HIGH  
**Error Type:** Error Handling

### Issue
```python
r = redis.Redis(host=config.REDIS_HOST, port=int(config.REDIS_PORT))
```

### Problem
- No try-except block
- If Redis is down on startup, FastAPI app still starts but will crash when trying to use Redis
- No graceful degradation

### Suggested Fix
```python
import redis
from redis.exceptions import ConnectionError

def get_redis_client():
    try:
        r = redis.Redis(
            host=config.REDIS_HOST,
            port=int(config.REDIS_PORT),
            socket_connect_timeout=5,
            decode_responses=True
        )
        r.ping()  # Test connection
        print("✅ Redis connection successful")
        return r
    except ConnectionError:
        print("⚠️ Redis connection failed - using fallback")
        return None

r = get_redis_client()

@app.get("/api/analytics")
def get_analytics():
    try:
        if r is None:
            return {"status": "OFFLINE", "error": "Redis unavailable"}
        # ... rest of logic
    except Exception as e:
        return {"status": "OFFLINE", "error": str(e)}
```

---

## 3. SadTalker Dockerfile - No Git Clone Error Handling
**File:** `sadtalker/Dockerfile`  
**Line:** 20  
**Severity:** 🟠 HIGH  
**Error Type:** Build Error

### Issue
```dockerfile
RUN git clone https://github.com/OpenTalker/SadTalker.git && \
    cd SadTalker && \
    git config core.compression 9
```

### Problem
- If git clone fails (network issue, repo moved), error is silently passed
- Subsequent commands will fail with confusing errors
- No indication clone failed until much later

### Suggested Fix
```dockerfile
RUN git clone https://github.com/OpenTalker/SadTalker.git || \
    (echo "Failed to clone SadTalker repository" && exit 1) && \
    cd SadTalker && \
    git config core.compression 9
```

---

## 4. Fact Checker - Incomplete Implementation
**File:** `app/services/fact_checker.py`  
**Line:** 56  
**Severity:** 🟠 HIGH  
**Error Type:** Logic Error

### Issue
The `is_verified()` function ends abruptly:
```python
count = sum(news_title.lower()[:50] in str(d).lower() for d in data)

if count >= 2:
    print("✅ [FACT-CHECK] Verification SUCCESS. Sources match.")
    return True
else:
    print("❌ [FACT-CHECK] Verification FAILED. Source mismatch or missing.")
    return False
# ← Missing implementation - comment ends but logic is incomplete
```

### Problem
- Logic is shallow (only checks if title in response)
- NLP comment suggests better implementation planned but not done
- May return incorrect verification results

### Suggested Fix
Complete the implementation:
```python
def is_verified(news_title):
    """
    Validates news authenticity by comparing multiple sources.
    Returns True if the headline is found in at least 2 sources.
    """
    if not news_title:
        return False

    print(f"🔍 [FACT-CHECK] Verifying authenticity of: {news_title[:60]}...")
    
    data = fetch_sources(news_title)

    if len(data) < 2:
        print("⚠️ [FACT-CHECK] Insufficient sources. Single source, assuming valid.")
        return len(data) > 0  # True if at least 1 source found

    # Better matching: check if title keywords appear in multiple sources
    title_keywords = set(news_title.lower().split())
    matching_sources = 0
    
    for source_data in data:
        source_text = str(source_data).lower()
        matching_keywords = sum(1 for kw in title_keywords if kw in source_text)
        # If >50% of keywords match, consider this source a match
        if matching_keywords >= len(title_keywords) * 0.5:
            matching_sources += 1
    
    is_verified = matching_sources >= 2
    
    if is_verified:
        print("✅ [FACT-CHECK] Verification SUCCESS. Found in multiple sources.")
    else:
        print("❌ [FACT-CHECK] Verification FAILED. Source mismatch or insufficient matches.")
    
    return is_verified
```

---

## 5. Docker Compose - Missing .env File
**File:** `docker-compose.yml`  
**Severity:** 🟠 HIGH  
**Error Type:** Configuration Error

### Issue
```yaml
services:
  app:
    env_file: .env
```

### Problem
- `.env` file is not provided in repository
- `docker-compose up` will fail with: `FileNotFoundError: .env`
- No template or example .env provided

### Suggested Fix
1. Create `.env.example`:
```
# API Keys
GROQ_API_KEY=your_groq_api_key
NEWS_API_KEY=your_newsapi_key
YOUTUBE_STREAM_KEY=your_youtube_rtmp_key
WORLD_NEWS_API_KEY=optional_world_news_api_key

# Database
DB_HOST=postgres
DB_NAME=vartapravah
DB_USER=postgres
DB_PASS=password

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Paths
ASSETS_DIR=/app/assets
OUTPUT_DIR=/app/output

# GPU (Optional)
USE_GPU=False
```

2. Update docker-compose.yml to handle missing file:
```yaml
env_file:
  - .env
  - .env.local  # optional local overrides

# OR make it optional
env_file:
  - .env.default
```

---

## 6. Main.py - Output Directory Creation Issues
**File:** `app/main.py`  
**Lines:** 17-18  
**Severity:** 🟠 HIGH  
**Error Type:** Runtime Error

### Issue
```python
if not os.path.exists("output"):
    os.makedirs("output")
app.mount("/videos", StaticFiles(directory="output"), name="videos")
```

### Problems
1. Relative path "output" is unpredictable in Docker
2. Directory creation happens at runtime, may fail if no permissions
3. Mount happens even if directory creation fails

### Suggested Fix
```python
import os
from pathlib import Path

# Use config
OUTPUT_DIR = config.OUTPUT_DIR  # Should be "/app/output"

# Create with proper error handling
try:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
except PermissionError:
    print(f"❌ Failed to create {OUTPUT_DIR}: Permission denied")

# Mount with verification
if os.path.isdir(OUTPUT_DIR):
    app.mount("/videos", StaticFiles(directory=OUTPUT_DIR), name="videos")
else:
    print(f"⚠️ Warning: {OUTPUT_DIR} not accessible")
```

---

## 7. App Dockerfile - Module Path in CMD
**File:** `app/Dockerfile`  
**Line:** 35  
**Severity:** 🟠 HIGH  
**Error Type:** Runtime Error

### Issue
The working directory is `/app` and the code is in `/app/app/main.py`:
```dockerfile
WORKDIR /app
COPY . .
CMD ["python", "-m", "uvicorn", "main:app", ...]  # ❌ main not found
```

### Problem
- Python looks for module `main` in `/app` but it's in `/app/app`
- Will fail with: `ModuleNotFoundError: No module named 'main'`

### Suggested Fix
Either change CMD:
```dockerfile
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Or change WORKDIR:
```dockerfile
WORKDIR /app/app
COPY app .
```

---

## 8. Scheduler Import Path
**File:** `app/scheduler/scheduler.py`  
**Line:** 1  
**Severity:** 🟠 HIGH  
**Error Type:** Import Error

### Issue
```python
from services.news_fetcher import fetch_news
from services.script_generator import generate_script
from services.fact_checker import is_verified
```

### Problem
- `scheduler.py` is in `app/scheduler/` subdirectory
- `services/` is at `app/services/`
- Relative import won't work from subdirectory

### Suggested Fix
Use absolute imports:
```python
from app.services.news_fetcher import fetch_news
from app.services.script_generator import generate_script
from app.services.fact_checker import is_verified
```

Or relative imports:
```python
from ..services.news_fetcher import fetch_news
from ..services.script_generator import generate_script
from ..services.fact_checker import is_verified
```

---

## 9. Workers Import Paths
**File:** `app/workers/sadtalker_worker.py`, `app/workers/queue_worker.py`  
**Lines:** 6-8  
**Severity:** 🟠 HIGH  
**Error Type:** Import Error

### Issue
```python
from services.tts_engine import init_tts, generate_audio
from services.sadtalker_engine import generate_ai_video
from services.video_engine import VideoEngine
```

### Problem
- Workers are in `app/workers/`
- Services are in `app/services/`
- Relative path imports won't resolve

### Suggested Fix
```python
from app.services.tts_engine import init_tts, generate_audio
from app.services.sadtalker_engine import generate_ai_video
from app.services.video_engine import VideoEngine
```

---

## 10. Dockerfile - Missing LibSndFile
**File:** `Dockerfile`  
**Severity:** 🟠 HIGH  
**Error Type:** Missing Dependency

### Issue
Root Dockerfile installs packages but misses `libsndfile1`:

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    espeak-ng \
    curl \
    fonts-noto \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*
```

### Problem
- `librosa` (used in TTS) requires `libsndfile1` system library
- Without it, audio processing will fail
- Error: `OSError: cannot load library 'libsndfile.so.1'`

### Suggested Fix
```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    espeak-ng \
    curl \
    fonts-noto \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*
```

---

# MEDIUM SEVERITY ISSUES

## 1. Docker Compose - Hardcoded Postgres Credentials
**File:** `docker-compose.yml`  
**Lines:** 45-50  
**Severity:** 🟡 MEDIUM  
**Error Type:** Configuration Mismatch

### Issue
```yaml
postgres:
  environment:
    POSTGRES_DB: vartapravah
    POSTGRES_USER: postgres
    POSTGRES_PASSWORD: password  # ❌ Hardcoded
```

### Problem
- Credentials hardcoded in compose file
- Doesn't match values in `app/database.py` environment variables
- Security risk if file is committed

### Suggested Fix
```yaml
postgres:
  image: postgres:15
  environment:
    POSTGRES_DB: ${DB_NAME:-vartapravah}
    POSTGRES_USER: ${DB_USER:-postgres}
    POSTGRES_PASSWORD: ${DB_PASS:-password}
```

And update `.env.example`:
```
DB_NAME=vartapravah
DB_USER=postgres
DB_PASS=your_secure_password_here
```

---

## 2. Root Dockerfile - Missing Cython
**File:** `Dockerfile`  
**Severity:** 🟡 MEDIUM  
**Error Type:** Build Dependency

### Issue
No explicit Cython installation before pip install:

```dockerfile
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt  # TTS needs Cython
```

### Problem
- TTS package requires Cython to build some extensions
- May fail or be very slow without precompiled wheels
- Error: `error: command 'gcc' failed with exit status 1`

### Suggested Fix
```dockerfile
RUN pip install --upgrade pip setuptools wheel Cython
RUN pip install -r requirements.txt
```

---

## 3. SadTalker Dockerfile - CPU/GPU Mismatch
**File:** `sadtalker/Dockerfile`  
**Line:** 51  
**Severity:** 🟡 MEDIUM  
**Error Type:** Configuration Mismatch

### Issue
```dockerfile
CMD ["python", "inference.py", "--cpu"]
```

But in `docker-compose.yml` there was:
```yaml
sadtalker:
  # GPU RESERVATION REMOVED FOR CPU TEST RUN (comment suggests GPU was used before)
```

### Problem
- Docker image configured for CPU but environment comments suggest GPU expected
- Confusion about whether GPU support is active
- Performance will be very poor on CPU

### Suggested Fix
1. If using CPU, be explicit:
```dockerfile
ENV TORCH_DEVICE=cpu
CMD ["python", "inference.py", "--cpu"]
```

2. If supporting both, use environment variable:
```dockerfile
ENV TORCH_DEVICE=${TORCH_DEVICE:-cpu}
CMD ["python", "-c", "import os; device = os.getenv('TORCH_DEVICE', 'cpu'); exec(open('inference.py').read().replace('torch.device(\"cuda\")', f'torch.device(\"{device}\")'))"]
```

---

## 4. Lip Sync - Hardcoded Wav2Lip Path
**File:** `app/services/lip_sync.py`  
**Line:** 15  
**Severity:** 🟡 MEDIUM  
**Error Type:** Path Error

### Issue
```python
cmd = f"""
python /app/Wav2Lip/inference.py \
...
"""
```

### Problem
- Hardcoded path assumes Wav2Lip is at `/app/Wav2Lip`
- Current project structure shows Wav2Lip not in repository
- Path will fail at runtime

### Suggested Fix
```python
import os
import config

WAV2LIP_PATH = os.getenv("WAV2LIP_PATH", "/app/Wav2Lip")

if not os.path.exists(WAV2LIP_PATH):
    raise FileNotFoundError(f"Wav2Lip not found at {WAV2LIP_PATH}")

cmd = f"""
python {WAV2LIP_PATH}/inference.py \
...
"""
```

---

## 5. Video Engine - Hardcoded Font Path
**File:** `app/services/video_engine.py`  
**Lines:** 12-14  
**Severity:** 🟡 MEDIUM  
**Error Type:** Dependency Error

### Issue
```python
font_path = "/usr/share/fonts/truetype/noto/NotoSansMarathi-Regular.ttf"

if not os.path.exists(font_path):
    font_path = "DejaVu Sans"
```

### Problem
- Hardcoded path may not exist in all environments
- Fallback to "DejaVu Sans" may not support Marathi characters
- No validation that font actually works

### Suggested Fix
```python
import os
from pathlib import Path

def find_marathi_font():
    """Find a Marathi-compatible font on the system."""
    candidates = [
        "/usr/share/fonts/truetype/noto/NotoSansMarathi-Regular.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    
    for font_path in candidates:
        if os.path.exists(font_path):
            return font_path
    
    # If no font found, might need to install:
    # apt-get install fonts-noto fonts-noto-devanagari
    return "DejaVu Sans"  # Last resort, may not render Marathi properly

font_path = find_marathi_font()
```

---

## 6. Docker Compose Inconsistency
**Files:** `docker-compose.yml`, `docker-compose-hetzner.yml`, `docker-compose-oracle.yml`  
**Severity:** 🟡 MEDIUM  
**Error Type:** Configuration Consistency

### Issue
Three different compose files with different:
- Build contexts
- Service configurations
- Commands
- Volume mounts

### Problem
- Difficult to maintain three versions
- Easy to miss updates across all three
- Deployment context confusion

### Suggested Fix
Create one base compose file with environment overrides:

**docker-compose.yml** (base):
```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    command: python -m uvicorn app.main:app --host 0.0.0.0 --port ${APP_PORT:-8000}
    environment:
      DEPLOYMENT_ENV: ${DEPLOYMENT_ENV:-local}
    depends_on:
      - postgres
      - redis
```

**docker-compose.override.yml** (local development):
```yaml
services:
  app:
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app/app
```

**docker-compose.hetzner.yml** (production):
```yaml
services:
  app:
    command: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
```

Then deploy with: `docker-compose -f docker-compose.yml -f docker-compose.hetzner.yml up`

---

## 7. Main.py - Scheduler Thread Management
**File:** `app/main.py`  
**Lines:** 84-86  
**Severity:** 🟡 MEDIUM  
**Error Type:** Process Management

### Issue
```python
@app.on_event("startup")
async def startup_event():
    # ...
    thread = threading.Thread(target=run_scheduler, daemon=True)
    thread.start()
```

### Problem
1. Daemon thread may be killed abruptly on container shutdown
2. No graceful shutdown mechanism
3. Scheduler may lose state mid-task
4. No signal handling for SIGTERM

### Suggested Fix
```python
import signal
import atexit

scheduler_thread = None

def shutdown_handler(signum, frame):
    print("🛑 Shutdown signal received, cleaning up...")
    # Add cleanup logic here
    if scheduler_thread:
        scheduler_thread.join(timeout=5)
    sys.exit(0)

@app.on_event("startup")
async def startup_event():
    global scheduler_thread
    
    def run_scheduler_with_signals():
        signal.signal(signal.SIGTERM, shutdown_handler)
        scheduler_main()
    
    scheduler_thread = threading.Thread(target=run_scheduler_with_signals, daemon=False)
    scheduler_thread.start()
    print("🏢 [MAIN] Enterprise Dashboard & Scheduler started.")

atexit.register(lambda: scheduler_thread.join(timeout=5) if scheduler_thread else None)
```

---

# LOW SEVERITY ISSUES

## 1. Requirements-Light.txt - Unused/Redundant
**File:** `requirements-light.txt`  
**Severity:** 🟢 LOW  
**Error Type:** Documentation Clarity

### Issue
A "light" requirements file exists but:
- Not referenced in docker-compose files
- Not documented in README
- Creates confusion about which to use

### Suggested Fix
Either:
1. Document when to use:
   - Add comment in README: "Use requirements-light.txt for basic API server without ML models"
2. Or remove it if unused:
   - Delete file if it's truly unused

---

## 2. Dockerfile.sadtalker - Duplicate/Unused
**File:** `Dockerfile.sadtalker`  
**Severity:** 🟢 LOW  
**Error Type:** Maintenance Confusion

### Issue
- Separate `Dockerfile.sadtalker` exists in root
- But `sadtalker/Dockerfile` is used by docker-compose
- Creates confusion about which file is active

### Suggested Fix
Delete `Dockerfile.sadtalker` or consolidate logic:
```bash
rm Dockerfile.sadtalker
```

Or if different, rename and document:
```bash
mv Dockerfile.sadtalker Dockerfile.sadtalker.archive  # Mark as deprecated
```

---

## 3. Health Check - Not Integrated
**File:** `app/health_check.py`  
**Severity:** 🟢 LOW  
**Error Type:** Integration Issue

### Issue
`health_check.py` exists and implements health checks, but:
- Never called from startup
- `/health` endpoint added manually to main.py (lines 24-26)
- Script runs standalone, not integrated into app

### Suggested Fix
Integrate into main.py properly:
```python
# Option 1: Call health check function
from health_check import check_stream

@app.get("/health", tags=["System"])
async def health_endpoint():
    if check_stream():
        return {"status": "healthy"}
    else:
        return {"status": "unhealthy"}, 503

# Option 2: Run as background task
@app.on_event("startup")
async def health_monitoring():
    async def monitor():
        while True:
            if not check_stream():
                print("⚠️ Health check failed!")
            await asyncio.sleep(30)
    
    asyncio.create_task(monitor())
```

---

# DEPENDENCY ANALYSIS

## Current Dependency Issues

| Package | Version | Python | Issue | Recommended |
|---------|---------|--------|-------|-------------|
| numpy | 1.22.0 | 3.10+ | ❌ Outdated, incompatible | 1.24.3+ |
| moviepy | unpinned | any | ⚠️ Unpinned, unstable | 1.0.3 |
| TTS | unpinned | 3.10+ | ⚠️ Unpinned, may break | 0.22.0 |
| torch | 2.1.0 | 3.10+ | ✅ OK | 2.1.0+ |
| librosa | unpinned | 3.10+ | ⚠️ Unpinned | 0.10.0+ |
| Cython | missing | any | ❌ Required for builds | 0.29.36 |
| libsndfile1 | missing | system | ❌ Required for librosa | Install |

## Recommended Requirements File

**requirements.txt** (pinned versions):
```
# FastAPI & Web
fastapi==0.104.1
uvicorn[standard]==0.24.0
httpx==0.25.0

# Configuration
python-dotenv==1.0.0
pydantic==2.5.0

# APIs & Clients
requests==2.31.0
groq==0.4.2
redis==5.0.0

# Audio & Video (ML)
TTS==0.22.0
librosa==0.10.1
moviepy==1.0.3
ffmpeg-python==0.2.1

# Database
psycopg2-binary==2.9.9
sqlalchemy==2.0.23

# Data Processing
numpy==1.24.3
Cython==0.29.36

# System
celery==5.3.4
python-multipart==0.0.6
pillow==10.0.1
```

---

# DOCKER BUILD ISSUES

## Issues Summary

| Issue | Severity | Impact |
|-------|----------|--------|
| Module paths incorrect in CMD | CRITICAL | Build/runtime failure |
| NumPy version incompatible | CRITICAL | Installation failure |
| Redis service missing | CRITICAL | Runtime failure |
| Relative paths in code | CRITICAL | Runtime failure |
| Build context confusion | HIGH | Build failure |
| Missing system libraries | HIGH | Runtime failure |
| No version pinning | CRITICAL | Non-reproducible builds |

## Build Order Recommendations

For optimal builds:
```dockerfile
# Step 1: System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential python3-dev gcc g++ cmake ...

# Step 2: Python build tools
RUN pip install --upgrade pip setuptools wheel Cython

# Step 3: Dependencies from requirements
RUN pip install -r requirements.txt

# Step 4: Additional configuration
RUN python setup_verify.py

# Step 5: Copy application (last to invalidate cache less)
COPY . .
```

---

# ENVIRONMENT VARIABLES

## Required Environment Variables (not in .env)

```bash
# API Keys (CRITICAL)
GROQ_API_KEY=             # Groq API key for LLM
NEWS_API_KEY=             # NewsAPI key for news fetching
YOUTUBE_STREAM_KEY=       # YouTube RTMP stream key
WORLD_NEWS_API_KEY=       # World News API key (optional)

# Database
DB_HOST=postgres          # Default: postgres
DB_NAME=vartapravah       # Default: vartapravah
DB_USER=postgres          # Default: postgres
DB_PASS=password          # Default: password ⚠️ CHANGE IN PRODUCTION

# Redis
REDIS_HOST=redis          # Default: redis
REDIS_PORT=6379           # Default: 6379

# Paths
ASSETS_DIR=/app/assets    # Asset files location
OUTPUT_DIR=/app/output    # Video output location
WAV2LIP_PATH=/app/Wav2Lip # Wav2Lip library path (optional)

# GPU
USE_GPU=False             # Enable GPU acceleration

# Deployment
DEPLOYMENT_ENV=local      # local|hetzner|oracle
APP_PORT=8000             # Application port
```

## Template .env File

See `.env.example` provided in CRITICAL issue #5 of HIGH SEVERITY section.

---

# SUMMARY & RECOMMENDATIONS

## Critical Actions Required

1. **Fix Python Module Paths** (Issues #1, #2, #8, #9)
   - Update imports to use absolute paths
   - Fix Dockerfile CMD entries
   - Ensure proper PYTHONPATH configuration

2. **Add Missing Services** (Issue #5)
   - Add Redis to all docker-compose files
   - Ensure database service configuration
   - Test service startup order

3. **Version All Dependencies** (Issues #6, #7, #12)
   - Pin all package versions
   - Add Cython to requirements
   - Update NumPy to 1.24.3+

4. **Fix Docker Paths** (Issues #4, #10, #11)
   - Use absolute paths in code
   - Update docker-compose build contexts
   - Create proper .env configuration

5. **Add Error Handling** (Issues #2, #3)
   - Add try-except for Redis connection
   - Handle missing static files gracefully
   - Add service health checks

## Testing Checklist

- [ ] All Python files parse without syntax errors
- [ ] All imports resolve correctly
- [ ] Docker build completes successfully
- [ ] All docker-compose services start
- [ ] FastAPI application responds to /health
- [ ] Redis connection works
- [ ] Database connection works
- [ ] Scheduler starts without errors
- [ ] Workers connect to Redis queue
- [ ] All API endpoints are accessible

## Deployment Priority

1. **IMMEDIATE** - Prevent deployment:
   - Issue #1: stream_engine.py import
   - Issue #2: app/Dockerfile CMD
   - Issue #5: Missing Redis service
   - Issue #6: Unpinned requirements
   - Issue #7: Outdated NumPy

2. **BEFORE PRODUCTION** - Resolve within 1 sprint:
   - All CRITICAL issues
   - Error handling (all HIGH issues)
   - Configuration (all docker-compose issues)

3. **BEFORE NEXT RELEASE** - Resolve within 2 sprints:
   - All MEDIUM severity issues
   - Dependency cleanup
   - Documentation

---

**Report Generated:** April 26, 2026  
**Analysis Time:** Comprehensive examination of all Python files, Dockerfiles, requirements, and docker-compose files  
**Status:** 32 issues identified, fixes provided for all
