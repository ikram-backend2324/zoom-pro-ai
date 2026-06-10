# 🎥 Zoom — Room-Based Meeting Platform

A clean, modern Django web application where anyone can create a meeting room and share a code for others to join — no accounts required.

## 🚀 Quick Start

```bash
# 1. Create & activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply migrations
python manage.py migrate

# 4. (Optional) Load demo data — already done if using provided db.sqlite3
# python manage.py shell < seed.py

# 5. Run the server (ASGI — Daphne is auto-used for websockets)
python manage.py runserver
```

Visit: http://127.0.0.1:8000

> **Video calls** use native WebRTC (peer-to-peer mesh) with Django Channels
> handling signaling over websockets — no third-party iframe, and the call
> lasts as long as participants stay connected. Browsers require a secure
> context for camera/mic: `localhost` works for testing; any other host needs
> HTTPS. For production behind multiple workers, replace the in-memory channel
> layer with `channels_redis`, and add a TURN server to `ICE_CONFIG` (in
> `room_detail.html`) for users behind strict NATs.

## 📁 Structure

```
zoom_project/
├── core/               ← Main app (models, views, forms)
├── templates/          ← All HTML templates
├── static/
│   ├── css/style.css   ← Full design system
│   └── js/main.js      ← Animations & interactions
├── db.sqlite3          ← Database (with demo rooms)
└── manage.py
```

## 🔑 Demo Room Codes

| Room | Code | Password |
|------|------|----------|
| Morning Standup | See db | none |
| Design Review Q4 | See db | design24 |
| Open Study Hall | See db | none |
| Product Demo | See db | none |

Run `python manage.py shell` and `Room.objects.all()` to see codes.

## ⚙️ Admin Panel

```bash
python manage.py createsuperuser
# Visit: http://127.0.0.1:8000/admin
```

## 🌐 Pages

- `/` — Landing page
- `/create/` — Create a room
- `/join/` — Join with a code
- `/room/<code>/` — Room detail & participants
- `/about/` — About page
