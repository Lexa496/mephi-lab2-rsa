import math

P = 241
Q = 307
MESSAGE = "RSA"


def is_prime(x: int) -> bool:
    if x < 2:
        return False
    if x % 2 == 0:
        return x == 2
    d = 3
    while d * d <= x:
        if x % d == 0:
            return False
        d += 2
    return True


def egcd(a: int, b: int):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1


def mod_inverse(a: int, m: int) -> int:
    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError("Обратный элемент не существует")
    return x % m


def choose_e(phi: int) -> int:
    e = 2
    while math.gcd(e, phi) != 1:
        e += 1
    return e


def block_size(n: int) -> int:
    k = 1
    while 256 ** (k + 1) < n:
        k += 1
    return k


def encrypt(text: str, e: int, n: int):
    data = text.encode("utf-8")
    k = block_size(n)
    cipher = []
    for i in range(0, len(data), k):
        chunk = data[i:i + k]
        padded = chunk + b"\x00" * (k - len(chunk))
        m = int.from_bytes(padded, "big")
        c = pow(m, e, n)
        cipher.append(c)
    return cipher, len(data), k


def decrypt(cipher, d: int, n: int, length: int, k: int) -> str:
    out = bytearray()
    for c in cipher:
        m = pow(c, d, n)
        out += m.to_bytes(k, "big")
    return bytes(out[:length]).decode("utf-8")


def main():
    assert is_prime(P) and is_prime(Q)

    n = P * Q
    phi = (P - 1) * (Q - 1)
    e = choose_e(phi)
    d = mod_inverse(e, phi)

    print(f"p = {P}, q = {Q}")
    print(f"n = {n}")
    print(f"phi(n) = {phi}")
    print(f"e = {e}, gcd(e, phi) = {math.gcd(e, phi)}")
    print(f"d = {d}")
    print(f"Открытый ключ: (e, n) = ({e}, {n})")
    print(f"Секретный ключ: (d, n) = ({d}, {n})")
    print(f"Проверка: (e*d) mod phi = {(e * d) % phi}")

    cipher, length, k = encrypt(MESSAGE, e, n)
    restored = decrypt(cipher, d, n, length, k)

    print(f"Сообщение: {MESSAGE!r}")
    print(f"Размер блока: {k} байт")
    print(f"Длина UTF-8: {length} байт")
    print(f"Шифртекст: {cipher}")
    print(f"Расшифровка: {restored!r}")
    print(f"Совпадение: {restored == MESSAGE}")


if __name__ == "__main__":
    main()