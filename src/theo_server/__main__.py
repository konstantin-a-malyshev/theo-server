import os
import uvicorn

from theo_server.config import settings

def main() -> None:
    uvicorn.run(
        "theo_server.main:app",
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level,
    )

if __name__ == "__main__":
    main()
