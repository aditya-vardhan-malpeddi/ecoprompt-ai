"""
EcoPrompt AI - Application Launcher
Runs the FastAPI web server and provides direct console links to the web dashboard and API docs.
"""

import sys
import socket
import uvicorn


def is_port_available(port: int, host: str = "127.0.0.1") -> bool:
    """Check if the target port is free to bind."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) != 0


def find_free_port(start_port: int = 8000, max_attempts: int = 10) -> int:
    """Find the first available port starting from start_port."""
    for p in range(start_port, start_port + max_attempts):
        if is_port_available(p):
            return p
    return start_port


if __name__ == "__main__":
    host = "127.0.0.1"
    port = find_free_port(8000)

    print("=" * 64)
    print("🌿  EcoPrompt AI — Green AI & Sustainability Suite")
    print("=" * 64)
    print(f" Web Dashboard:    http://{host}:{port}")
    print(f" Swagger API Docs:  http://{host}:{port}/docs")
    print(f" Health Check:     http://{host}:{port}/api/health")
    print("=" * 64)
    print("Press CTRL+C to stop the server.\n")

    uvicorn.run("app.main:app", host=host, port=port, reload=False)
