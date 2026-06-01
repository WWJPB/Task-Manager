import subprocess
import sys

def run():
    backend = subprocess.Popen(['uvicorn', 'main:app', '--reload'])
    frontend = subprocess.Popen(['streamlit', 'run', 'app.py'])

    try:
        backend.wait()
        frontend.wait()
    except KeyboardInterrupt:
        backend.terminate()
        frontend.terminate()

if __name__ == '__main__':
    run()