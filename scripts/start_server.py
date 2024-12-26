import os
import subprocess
import socket
import sys

# Add the root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import run_server

if __name__ == '__main__':
    try:
        # Run the server directly
        run_server()
    except Exception as e:
        print(f"Error starting server: {e}")
        exit(1)