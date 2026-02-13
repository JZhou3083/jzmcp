import subprocess
import json
import sys
import time

def send(proc, obj):
    proc.stdin.write(json.dumps(obj) + "\n")
    proc.stdin.flush()

def recv(proc):
    line = proc.stdout.readline()
    if not line:
        return None
    return json.loads(line)

def main():
    print("Starting MCP server...\n")

    proc = subprocess.Popen(
        [sys.executable, "server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    time.sleep(0.2)

    # 1. initialize (correct MCP format)
    init_req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "0.1"
            }
        }
    }
    print(">>> Sending initialize")
    send(proc, init_req)
    print(recv(proc), "\n")

    # 2. client sends "initialized" notification
    initialized = {
        "jsonrpc": "2.0",
        "method": "initialized",
        "params": {}
    }
    print(">>> Sending initialized")
    send(proc, initialized)

    # 3. list tools (correct MCP format)
    list_req = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {
            "cursor": None
        }
    }
    print(">>> Sending tools/list")
    send(proc, list_req)
    print(recv(proc), "\n")

    # 4. call echo tool
    call_req = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "echo",
            "arguments": {"text": "Hello MCP!"}
        }
    }
    print(">>> Sending tools/call")
    send(proc, call_req)
    print(recv(proc), "\n")

    print("Done.")
    proc.terminate()

if __name__ == "__main__":
    main()
