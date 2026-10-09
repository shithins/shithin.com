#!/usr/bin/env python3
"""
Local dev server for shithin.com.

Why not `python3 -m http.server`: that server ignores HTTP Range requests and
always replies 200 with the whole file. Browsers need 206 Partial Content to
seek inside media, so with it `audio.seekable` is an empty range and the wave's
"start at 0:20" offset is silently dropped — the track just plays from the top.
Production hosts (Netlify, Vercel, Cloudflare, S3) all support Range, so this
only affects local testing.

Usage:
    python3 serve.py [port]      # default 8099

Note: the media files under assets/audio are gitignored, so a fresh clone needs
a track dropped in before the wave will make a sound.
"""

import http.server
import os
import re
import socketserver
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PORT = 8099


class RangeRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def _send_file(self, path, start, length, size, ctype):
        """Write a byte range, tolerating the client aborting mid-transfer.

        Browsers routinely cancel media requests once they have the bytes they
        need (every seek does this), which raises BrokenPipeError on write. It
        is expected traffic, not an error, so it must not print a traceback.
        """
        try:
            with open(path, "rb") as handle:
                handle.seek(start)
                remaining = length
                while remaining > 0:
                    chunk = handle.read(min(65536, remaining))
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    remaining -= len(chunk)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def do_GET(self):
        path = self.translate_path(self.path.split("?")[0].split("#")[0])
        if not os.path.isfile(path):
            return super().do_GET()

        size = os.path.getsize(path)
        ctype = self.guess_type(path)
        rng = self.headers.get("Range")

        if rng:
            match = re.match(r"bytes=(\d*)-(\d*)", rng)
            if match:
                start = int(match.group(1)) if match.group(1) else 0
                end = int(match.group(2)) if match.group(2) else size - 1
                end = min(end, size - 1)
                if start > end or start >= size:
                    self.send_response(416)
                    self.send_header("Content-Range", "bytes */%d" % size)
                    self.end_headers()
                    return
                length = end - start + 1
                self.send_response(206)
                self.send_header("Content-Type", ctype)
                self.send_header("Accept-Ranges", "bytes")
                self.send_header("Content-Range", "bytes %d-%d/%d" % (start, end, size))
                self.send_header("Content-Length", str(length))
                self.end_headers()
                self._send_file(path, start, length, size, ctype)
                return

        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(size))
        self.end_headers()
        self._send_file(path, 0, size, size, ctype)


class ThreadingServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
    with ThreadingServer(("127.0.0.1", port), RangeRequestHandler) as httpd:
        print("shithin.com dev server -> http://127.0.0.1:%d" % port)
        print("Range requests supported (needed for the 0:20 audio seek)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped")


if __name__ == "__main__":
    main()
