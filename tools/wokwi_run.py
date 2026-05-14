#!/usr/bin/env python3
"""Run a MicroPython script on a Wokwi RFC2217 serial port with proper timing."""
import sys
import time
import serial

HOST = "localhost"
PORT = 4000
DELAY = 0.15  # seconds between control sequences — tunable

def read_until(ser, token: bytes, timeout: float = 10.0) -> bytes:
    buf = b""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        chunk = ser.read(ser.inWaiting() or 1)
        if chunk:
            buf += chunk
            if token in buf:
                return buf
    return buf

def enter_raw_repl(ser):
    ser.write(b"\r\x03\r\x03")     # Ctrl+C twice — interrupt running code
    # Wait for ">>> " to confirm REPL is ready before sending Ctrl+A.
    # Over RFC2217/TCP the banner may still be in-flight when we connect,
    # so a fixed sleep is not reliable.
    data = read_until(ser, b">>> ")
    if b">>> " not in data:
        raise RuntimeError(f"REPL prompt not found; got: {data!r}")
    # flush any extra prompts produced by double Ctrl+C
    time.sleep(0.05)
    ser.flushInput()
    ser.write(b"\r\x01")            # Ctrl+A — enter raw REPL
    data = read_until(ser, b"raw REPL; CTRL-B to exit\r\n>")
    if b"raw REPL; CTRL-B to exit\r\n>" not in data:
        raise RuntimeError(f"could not enter raw REPL; got: {data!r}")

def soft_reset(ser):
    ser.write(b"\x04")              # Ctrl+D — soft reset
    data = read_until(ser, b"raw REPL; CTRL-B to exit\r\n")
    if b"raw REPL; CTRL-B to exit\r\n" not in data:
        raise RuntimeError(f"soft reset failed; got: {data!r}")

def exec_raw(ser, code: bytes):
    # Write code followed by Ctrl+D to execute
    ser.write(code)
    ser.write(b"\x04")
    out = read_until(ser, b"\x04", timeout=30)
    # Raw REPL response: b'\x04' + output + b'\x04' + error
    if out.startswith(b"\x04"):
        out = out[1:]
    parts = out.split(b"\x04", 1)
    stdout = parts[0]
    stderr = parts[1] if len(parts) > 1 else b""
    return stdout, stderr

def exit_raw_repl(ser):
    ser.write(b"\r\x02")            # Ctrl+B — back to friendly REPL

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Run a MicroPython script via Wokwi RFC2217")
    parser.add_argument("script", help="MicroPython script to run")
    parser.add_argument("--port", type=int, default=PORT, help=f"RFC2217 TCP port (default: {PORT})")
    parser.add_argument("--host", default=HOST, help=f"RFC2217 host (default: {HOST})")
    args = parser.parse_args()

    script_path = args.script
    with open(script_path, "rb") as f:
        code = f.read()

    url = f"rfc2217://{args.host}:{args.port}"
    print(f"Connecting to {url} ...")
    ser = serial.serial_for_url(url, baudrate=115200, timeout=1)

    time.sleep(0.3)                 # let RFC2217 negotiate

    try:
        print("Entering raw REPL ...")
        enter_raw_repl(ser)
        print("Soft resetting ...")
        soft_reset(ser)
        print(f"Running {script_path} ...")
        stdout, stderr = exec_raw(ser, code)
        if stdout:
            sys.stdout.buffer.write(stdout)
            sys.stdout.buffer.flush()
        if stderr:
            sys.stderr.buffer.write(stderr)
            sys.stderr.buffer.flush()
    finally:
        exit_raw_repl(ser)
        ser.close()

if __name__ == "__main__":
    main()
