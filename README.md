# 🌐 Python HTTP Server

A custom-built Python HTTP server that serves web pages, provides JSON APIs, and stores device check-ins locally using `checkins.json`.

---

🔧 **Features**

✅ Built-in Web Server – Uses Python's built-in `http.server` module  
✅ REST API – POST `/api/checkin` to record check-ins, GET `/api/checkins` to retrieve them  
✅ HTML Dashboard – `/dashboard` route shows a live-updating table of recent check-ins  
✅ Logging – Tracks access logs by IP and timestamp in `access.log`  
✅ Persistent Storage – Saves check-ins to `checkins.json` for durability between restarts  

---

📂 **Technologies Used**

- Python 🐍 (Standard Library only)
- `http.server` (HTTP request handling)
- `json` (Data serialization)
- `datetime` (Timestamps)
- `os` & `urlparse` (Routing and file handling)

---

📡 **Endpoints**

| Method | Endpoint         | Description                        |
|--------|------------------|------------------------------------|
| GET    | `/`              | Home page                          |
| GET    | `/api/status`    | Server status in JSON              |
| GET    | `/api/checkins`  | Returns last 50 check-ins          |
| GET    | `/dashboard`     | HTML dashboard of check-ins        |
| POST   | `/api/checkin`   | Accepts JSON check-in data         |

---

📦 **Sample Check-In Payload**

```json
{
  "client_id": "device123",
  "status": "online",
  "timestamp": "2025-05-03T19:25:00"
}
```

---

🛠️ **How to Run**

```bash
python server.py
```

Then open [http://localhost:8080](http://localhost:8080) in your browser.

