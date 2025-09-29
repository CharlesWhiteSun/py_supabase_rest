import sys
import subprocess
import signal
import os
from dotenv import load_dotenv

def run_uvicorn():
    try:
        load_dotenv()

        host = os.getenv("HOST", "127.0.0.1")
        port = os.getenv("PORT", "8000")

        process = subprocess.Popen(
            [
                sys.executable, "-m", "uvicorn", "py_supabase_rest.main:app",
                "--host", host,
                "--port", port,
            ],
            stdout=sys.stdout,
            stderr=sys.stderr
        )

        def signal_handler(sig, frame):
            print("\n🛑 Gracefully shutting down...")
            process.terminate()
            process.wait()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        process.wait()

    except Exception as e:
        print(f"啟動失敗: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_uvicorn()
