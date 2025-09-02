# Frontend (Vite + React + TS)

## Dev setup

```bash
cd frontend
npm install
npm run dev
```

Create `frontend/.env.development` if needed:

```
VITE_API_BASE=http://127.0.0.1:8000
```

Backend must run at the same URL or adjust `VITE_API_BASE`.

Pages:
- Products (public)
- Login/Register
- Checkout (quick buy by product id)
- Admin Products (requires admin token)
