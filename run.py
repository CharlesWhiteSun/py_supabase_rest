import sys
import subprocess
import signal

def run_uvicorn():
    try:
        process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "main:app", "--reload"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        def signal_handler(sig, frame):
            print("\n🛑 Gracefully shutting down...")
            process.terminate()  # 停止 uvicorn
            process.wait()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)   # CTRL+C
        signal.signal(signal.SIGTERM, signal_handler)  # 終止信號

        stdout, stderr = process.communicate()

    except Exception as e:
        print(f"啟動失敗: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_uvicorn()
