import uvicorn

from src.apps.base.bootstrap import build_app

app = build_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
