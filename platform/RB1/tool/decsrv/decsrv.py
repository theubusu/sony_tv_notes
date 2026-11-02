import socket
import struct

HOST = "192.168.1.71"
PORT = 5151

def decrypt_data(data, key, iv):
    key_type=2
    mac=None
    compress=0
    
    print(f"    [decrypt_data] decrypting {len(data)}...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        req = struct.pack('<I', key_type)
        req += key.ljust(16, b'\x00')[:16]
        req += struct.pack('B', 1 if iv else 0) + (iv.ljust(16, b'\x00')[:16] if iv else b'\x00' * 16)
        req += struct.pack('B', 1 if mac else 0) + (mac.ljust(16, b'\x00')[:16] if mac else b'\x00' * 16)
        req += struct.pack('<II', compress, len(data))
        req += data

        s.sendall(req)

        def recv_exact(n):
            buf = b''
            while len(buf) < n:
                chunk = s.recv(n - len(buf))
                if not chunk:
                    raise ConnectionError("short read")
                buf += chunk
            return buf

        result = struct.unpack('<i', recv_exact(4))[0]
        if result != 0:
            print(f"    [decrypt_data] DECRYPTION FAILED: result={result}")
            return None
        
        size = struct.unpack('<I', recv_exact(4))[0]
        out = recv_exact(size)
        return out


if __name__ == '__main__':
    key = open('releasekey.bin', 'rb').read()
    iv = open('iv.bin', 'rb').read()
    data = open('data.bin', 'rb').read()

    out = decrypt_data(data, key, iv)
    open('out.bin', 'wb').write(out)