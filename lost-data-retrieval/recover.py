"""
JPEG recovery by file carving from a raw drive.

Run from an ADMINISTRATOR terminal on Windows (raw drive access needs it):
    python recover_jpg.py

Rules for best results:
  * Never save recovered files onto the drive you are recovering from.
  * Stop using the lost drive until recovery is finished.
"""
import os
import sys
import time

# ----------------------------- SETTINGS ------------------------------------
DRIVE = r"\\.\D:"   # source: your USB flash drive (raw access)
OUT_DIR = r"E:\saad\intenships\Arch Technologies\Lost Data Retrieval\recover"
SECTOR = 512                       # JPEGs start on sector boundaries
CHUNK = 16 * 1024 * 1024           # scan 16 MB at a time (multiple of SECTOR)
MAX_JPG = 40 * 1024 * 1024         # ignore anything bigger than 40 MB
MIN_JPG = 4 * 1024                 # ignore anything smaller than 4 KB (icons/junk)
SAVE_PARTIAL = True                # keep damaged/cut-off JPEGs with _partial suffix
# ---------------------------------------------------------------------------

SIG = b"\xff\xd8\xff"


def read_at(f, offset, length):
    """Sector-aligned read (required for raw Windows drives)."""
    length = (length + SECTOR - 1) // SECTOR * SECTOR
    f.seek(offset)
    return f.read(length)


def jpeg_end(data):
    """
    Walk the JPEG structure and return (end_index, complete).
    Skips embedded thumbnails properly (they live inside APP segments), so the
    file is not cut at the thumbnail's FFD9.
    """
    n = len(data)
    if data[:3] != SIG:
        return 0, False
    i = 2
    while i + 4 <= n:
        if data[i] != 0xFF:
            return i, False                      # lost sync -> damaged
        m = data[i + 1]
        if m == 0xFF:                            # fill byte
            i += 1
            continue
        if m == 0xD9:                            # EOI
            return i + 2, True
        if m == 0x01 or 0xD0 <= m <= 0xD7 or m == 0xD8:
            i += 2                               # markers without length
            continue
        seglen = (data[i + 2] << 8) | data[i + 3]
        if seglen < 2:
            return i, False
        i += 2 + seglen
        if m == 0xDA:                            # SOS -> entropy-coded data
            while True:
                j = data.find(b"\xff", i)
                if j < 0 or j + 1 >= n:
                    return n, False
                nxt = data[j + 1]
                if nxt == 0x00 or 0xD0 <= nxt <= 0xD7 or nxt == 0xFF:
                    i = j + 1 if nxt == 0xFF else j + 2
                    continue
                i = j                            # real marker (next scan / EOI)
                break
    return min(i, n), False


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    try:
        src = open(DRIVE, "rb")
    except PermissionError:
        sys.exit("Permission denied. Run the terminal as Administrator.")
    except OSError as e:
        sys.exit(f"Cannot open {DRIVE}: {e}")

    total = 0
    try:
        total = src.seek(0, os.SEEK_END)
        src.seek(0)
    except OSError:
        pass
    if not total and os.path.isfile(DRIVE):
        total = os.path.getsize(DRIVE)

    print(f"Scanning {DRIVE}  ->  {OUT_DIR}")
    pos = 0            # start of current chunk
    resume = 0         # never look for signatures before this offset
    count = partial = 0
    errors = 0         # consecutive read errors
    t0 = time.time()

    while True:
        if total and pos >= total:               # reached end of drive
            break
        try:
            buf = read_at(src, pos, CHUNK)
            errors = 0
        except OSError as e:                     # bad sector: skip this chunk
            errors += 1
            if errors >= 5:                      # probably past the end of drive
                print(f"\nStopping after repeated read errors at {hex(pos)}.")
                break
            print(f"\nRead error at {hex(pos)} ({e}); skipping.")
            pos += CHUNK
            continue
        if not buf:
            break

        idx = buf.find(SIG)
        while idx >= 0:
            off = pos + idx
            if idx % SECTOR == 0 and off >= resume:
                data = read_at(src, off, MAX_JPG)
                end, ok = jpeg_end(data)
                if end >= MIN_JPG and (ok or SAVE_PARTIAL):
                    name = f"{count}{'' if ok else '_partial'}.jpg"
                    with open(os.path.join(OUT_DIR, name), "wb") as out:
                        out.write(data[:end])
                    print(f"\n[{'OK' if ok else 'PARTIAL'}] {name} at {hex(off)} "
                          f"({end / 1024:.0f} KB)")
                    count += 1
                    partial += (not ok)
                    resume = off + (end + SECTOR - 1) // SECTOR * SECTOR
                else:
                    resume = off + SECTOR        # false hit, keep scanning
            idx = buf.find(SIG, idx + 1)

        # Advance, keeping a 1-sector overlap so signatures on the boundary
        # are not missed.
        if len(buf) < CHUNK:
            break
        pos += CHUNK - SECTOR

        if total:
            pct = min(pos / total * 100, 100)
            sys.stdout.write(f"\rProgress: {pct:5.1f}%  found: {count}   ")
            sys.stdout.flush()

    src.close()
    print(f"\nDone in {time.time() - t0:.0f}s. Recovered {count} files "
          f"({partial} partial). Folder: {OUT_DIR}")


if __name__ == "__main__":
    main()
