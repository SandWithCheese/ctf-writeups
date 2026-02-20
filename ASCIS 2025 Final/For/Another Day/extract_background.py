#!/usr/bin/env python3
import sys
import os
import struct
import string

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
DATA_LENGTH = 1536  # the `num` in ChangeImage()


def get_system_configuration_bytes():
    # Mirrors C# GetSystemConfiguration():
    #   text  = Environment.GetEnvironmentVariable("PROCESSOR_ARCHITECTURE") ?? "AMD64";
    #   text2 = Environment.GetEnvironmentVariable("PROCESSOR_REVISION") ?? "0000";
    #   string s = text + text2;
    #   return Encoding.UTF8.GetBytes(s);
    arch = "AMD64"
    rev = "b701"
    s = arch + rev
    return s.encode("utf-8")


def validate_png(data: bytes) -> None:
    if not data.startswith(PNG_MAGIC):
        raise ValueError("Not a PNG file (bad magic)")


def find_idat_offset(data: bytes) -> int:
    # C# FindImageChunk: looks for chunk whose type is 'IDAT'
    # PNG layout: [len:4][type:4][data:len][crc:4]
    # They scan starting at offset 8
    for i in range(8, len(data) - 12):
        if data[i + 4 : i + 8] == b"IDAT":
            return i
    return -1


def get_chunk_length(data: bytes, pos: int) -> int:
    # same as GetChunkLength: big-endian u32
    return struct.unpack(">I", data[pos : pos + 4])[0]


def extract_cipher_from_png(path: str, data_len: int) -> bytes:
    with open(path, "rb") as f:
        data = f.read()

    validate_png(data)
    pos = find_idat_offset(data)
    if pos == -1:
        raise RuntimeError("IDAT chunk not found")

    chunk_length = get_chunk_length(data, pos)
    # In C#:
    #   int num2 = num + 8 + (chunkLength - dataLength);
    #   Array.Copy(array, num2, array2, 0, dataLength);
    start = pos + 8 + (chunk_length - data_len)
    end = start + data_len

    if start < 0 or end > len(data):
        raise RuntimeError("Computed cipher slice is out of bounds")

    cipher = data[start:end]
    return cipher


def xor_decrypt(cipher: bytes, key: bytes) -> bytes:
    out = bytearray(len(cipher))
    klen = len(key)
    for i, c in enumerate(cipher):
        out[i] = c ^ key[i % klen]
    return bytes(out)


def printable_strings(buf: bytes, min_len: int = 4):
    """
    Simple strings(1)-like extractor: sequences of printable ASCII.
    """
    printable = set(bytes(string.printable, "ascii"))
    current = bytearray()
    for b in buf:
        if b in printable and b not in b"\r\n":
            current.append(b)
        else:
            if len(current) >= min_len:
                yield current.decode("ascii", errors="replace")
            current = bytearray()
    if len(current) >= min_len:
        yield current.decode("ascii", errors="replace")


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} background.png")
        sys.exit(1)

    png_path = sys.argv[1]

    print(f"[+] Reading PNG: {png_path}")
    cipher = extract_cipher_from_png(png_path, DATA_LENGTH)
    print(f"[+] Extracted cipher bytes from last {DATA_LENGTH} bytes of IDAT")

    key = get_system_configuration_bytes()
    print(f"[+] Key (PROCESSOR_ARCHITECTURE+REVISION) = {key!r}")

    theme_data = xor_decrypt(cipher, key)
    print(f"[+] Decrypted themeData length = {len(theme_data)} bytes")

    # Save to file for ndisasm / other tools
    out_path = "theme_dec.bin"
    with open(out_path, "wb") as f:
        f.write(theme_data)
    print(f"[+] Written decrypted shellcode to {out_path}")

    # Small hex preview
    print("\n=== Hex preview (first 128 bytes) ===")
    print(theme_data[:128].hex())

    # Extract printable strings
    print("\n=== Printable ASCII strings (len >= 4) ===")
    found_any = False
    for s in printable_strings(theme_data, min_len=4):
        found_any = True
        print(s)
    if not found_any:
        print("(no long printable strings found)")


if __name__ == "__main__":
    main()
