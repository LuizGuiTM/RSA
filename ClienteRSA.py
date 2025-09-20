import socket
import random
from math import gcd

def witness(a, d, s, n):
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return True
    for _ in range(s - 1):
        x = pow(x, 2, n)
        if x == n - 1:
            return True
    return False

def is_probable_prime(n: int) -> bool:
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    if n in small:
        return True
    for p in small:
        if n % p == 0:
            return False

    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for a in (2, 3, 5, 7, 11):
        if not witness(a, d, s, n):
            return False
    return True



def gerarNumeroPrimo(bits=128):
    while True:
        N = random.getrandbits(bits)
        N |= (1 << (bits - 1))
        if is_probable_prime(N):
            return N

def egcd(a, b):
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)

def modinv(a, m):
    g, x, _ = egcd(a, m)
    if g != 1:
        raise Exception("Inverso modular não existe")
    return x % m

def gerar_par_chaves(bits=128):
    p = gerarNumeroPrimo(bits)
    q = gerarNumeroPrimo(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 3
    while gcd(e, phi) > 1:
        e += 2
    d = modinv(e, phi)
    return (n, e, d)

def rsa_encrypt_blocks(msg, e, n, block_size=32):
    msg_bytes = msg.encode("utf-8")
    blocks = []
    for i in range(0, len(msg_bytes), block_size):
        bloco = msg_bytes[i:i+block_size]
        bloco_int = int.from_bytes(bloco, "big")
        blocks.append(pow(bloco_int, e, n))
    return blocks

def rsa_decrypt_blocks(cipher_blocks, d, n):
    msg_bytes = b""
    for c in cipher_blocks:
        bloco_int = pow(c, d, n)
        bloco_bytes = bloco_int.to_bytes((bloco_int.bit_length() + 7) // 8, "big")
        msg_bytes += bloco_bytes
    return msg_bytes.decode("utf-8")

# -----------------------
# --- Cliente TCP ---
# -----------------------
HOST = "127.0.0.1"
PORT = 5000

nC, eC, dC = gerar_par_chaves()
print(f"[Cliente] Chave pública: (n={nC}, e={eC})")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("[Cliente] Conectado ao servidor")

    # 1) Recebe chave pública do servidor
    pubS = s.recv(65536).decode()
    nS, eS = map(int, pubS.split(","))
    print(f"[Cliente] Chave pública do servidor: n={nS}, e={eS}")

    # 2) Envia chave pública do cliente
    s.sendall(f"{nC},{eC}".encode())

    # 3) Envia mensagem cifrada com a chave pública do servidor
    msg = input("Digite a mensagem a ser enviada: ")
    cipher_blocks = rsa_encrypt_blocks(msg, eS, nS)
    s.sendall(",".join(map(str, cipher_blocks)).encode())
    print(f"[Cliente] Mensagem enviada: {msg}")

    # 4) Recebe resposta cifrada
    data = s.recv(65536).decode()
    resposta_blocks = [int(x) for x in data.split(",") if x.strip()]
    resposta = rsa_decrypt_blocks(resposta_blocks, dC, nC)
    print(f"[Cliente] Resposta do servidor: {resposta}")
