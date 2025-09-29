import sys
import subprocess
import signal

def run_uvicorn():
    try:
        process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "main:app"],
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
