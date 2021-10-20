def cycle_shift(v, pos):
    bin_str = []
    for i in range(32):
        bin_str.append(v % 2)
        v >>= 1
    bin_str.reverse()
    for i in range(pos):
        bit = bin_str[0]
        for j in range(1, 32):
            bin_str[j-1] = bin_str[j]
        bin_str[31] = bit
    number = 0
    for i in range(32):
        number += bin_str[i] * (2 ** (31 - i))
    return number


def function_choose(j):
    functions = [lambda x, y, z: (x ^ y ^ z),
                 lambda x, y, z: ((x & y) | ((~x) & z)),
                 lambda x, y, z: ((x | (~y)) ^ z),
                 lambda x, y, z: ((x & z) | (y & (~z))),
                 lambda x, y, z: (x ^ (y | (~z)))]
    if j < 16:
        return functions[0]
    if 16 <= j < 32:
        return functions[1]
    if 32 <= j < 48:
        return functions[2]
    if 48 <= j < 64:
        return functions[3]
    if 64 <= j:
        return functions[4]


def RIPEMD160(byte):
    # дополнение
    byte_message = byte
    len_message = len(byte_message) * 8
    byte_message.append(0x80)
    while (len(byte_message) * 8) % 512 != 448:
        byte_message.append(0x00)
    if len_message >= 2**64:
        len_message &= 0xFFFFFFFFFFFFFFFF
    first_part = len_message & 0xFFFFFFFF
    first_part = first_part.to_bytes(4, byteorder="little")
    second_part = len_message >> 32
    second_part = second_part.to_bytes(4, byteorder="little")
    byte_message += first_part
    byte_message += second_part
    # инициализация
    
    constant_adding = [0x00000000, 0x5A827999, 0x6ED9EBA1, 0x8F1BBCDC, 0xA953FD4E]
    constant_adding_hatch = [0x50A28BE6, 0x5C4DD124, 0x6D703EF3, 0x7A6D76E9, 0x00000000]
    r = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
         7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8,
         3, 10, 14, 4, 9, 15, 8, 1, 2, 7, 0, 6, 13, 11, 5, 12,
         1, 9, 11, 10, 0, 8, 12, 4, 13, 3, 7, 15, 14, 5, 6, 2,
         4, 0, 5, 9, 7, 12, 2, 10, 14, 1, 3, 8, 11, 6, 15, 13]
    r_hatch = [5, 14, 7, 0, 9, 2, 11, 4, 13, 6, 15, 8, 1, 10, 3, 12,
               6, 11, 3, 7, 0, 13, 5, 10, 14, 15, 8, 12, 4, 9, 1, 2,
               15, 5, 1, 3, 7, 14, 6, 9, 11, 8, 12, 2, 10, 0, 4, 13,
               8, 6, 4, 1, 3, 11, 15, 0, 5, 12, 2, 13, 9, 7, 10, 14,
               12, 15, 10, 4, 1, 5, 8, 7, 6, 2, 13, 14, 0, 3, 9, 11]
    s = [11, 14, 15, 12, 5, 8, 7, 9, 11, 13, 14, 15, 6, 7, 9, 8,
         7, 6, 8, 13, 11, 9, 7, 15, 7, 12, 15, 9, 11, 7, 13, 12,
         11, 13, 6, 7, 14, 9, 13, 15, 14, 8, 13, 6, 5, 12, 7, 5,
         11, 12, 14, 15, 14, 15, 9, 8, 9, 14, 5, 6, 8, 6, 5, 12,
         9, 15, 5, 11, 6, 8, 13, 12, 5, 12, 13, 14, 11, 8, 5, 6]
    s_hatch = [8, 9, 9, 11, 13, 15, 15, 5, 7, 7, 8, 11, 14, 14, 12, 6,
               9, 13, 15, 7, 12, 8, 9, 11, 7, 7, 12, 7, 6, 15, 13, 11,
               9, 7, 15, 11, 8, 6, 6, 14, 12, 13, 5, 14, 13, 13, 7, 5,
               15, 5, 8, 11, 14, 14, 6, 14, 6, 9, 12, 9, 12, 5, 15, 8,
               8, 5, 12, 9, 12, 5, 14, 6, 8, 13, 6, 5, 15, 13, 11, 11]
    h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]
    # разделение сообщения на слова
    length = len(byte_message) * 8
    separated_message = []
    for i in range((length//512)):
        part = byte_message[64 * i:64*(i + 1)]
        separated_message.append([])
        for j in range(16):
            word = part[4 * j:4*(j + 1)]
            separated_message[i].append(int.from_bytes(word, byteorder="little", signed=False))
    # Алгоритм
    for i in range(len(separated_message)):
        part = separated_message[i]
        A = h[0]
        B = h[1]
        C = h[2]
        D = h[3]
        E = h[4]
        A_hatch = h[0]
        B_hatch = h[1]
        C_hatch = h[2]
        D_hatch = h[3]
        E_hatch = h[4]
        for j in range(80):
            f = function_choose(j)
            f_hatch = function_choose(79 - j)
            if j < 16:
                k = constant_adding[0]
                k_hatch = constant_adding_hatch[0]
            if 16 <= j < 32:
                k = constant_adding[1]
                k_hatch = constant_adding_hatch[1]
            if 32 <= j < 48:
                k = constant_adding[2]
                k_hatch = constant_adding_hatch[2]
            if 48 <= j < 64:
                k = constant_adding[3]
                k_hatch = constant_adding_hatch[3]
            if 64 <= j < 80:
                k = constant_adding[4]
                k_hatch = constant_adding_hatch[4]
            x = part[r[j]]
            x_hatch = part[r_hatch[j]]
            T = (A + f(B, C, D) + x + k) % (2**32)
            T = cycle_shift(T, s[j])
            T = (T + E) % (2**32)
            A = E
            E = D
            D = cycle_shift(C, 10)
            C = B
            B = T
            T = (A_hatch + f_hatch(B_hatch, C_hatch, D_hatch) + x_hatch + k_hatch) % (2 ** 32)
            T = cycle_shift(T, s_hatch[j])
            T = (T + E_hatch) % (2 ** 32)
            A_hatch= E_hatch
            E_hatch = D_hatch
            D_hatch = cycle_shift(C_hatch, 10)
            C_hatch = B_hatch
            B_hatch = T
        T = (h[1] + C + D_hatch) % (2 ** 32)
        h[1] = (h[2] + D + E_hatch) % (2 ** 32)
        h[2] = (h[3] + E + A_hatch) % (2 ** 32)
        h[3] = (h[4] + A + B_hatch) % (2 ** 32)
        h[4] = (h[0] + B + C_hatch) % (2 ** 32)
        h[0] = T
    else:
        word = h[0].to_bytes(4, byteorder="little")
        word = int.from_bytes(word, byteorder="big")
        hashed = word
        hashed <<= 32
        word = h[1].to_bytes(4, byteorder="little")
        word = int.from_bytes(word, byteorder="big")
        hashed |= word
        hashed <<= 32
        word = h[2].to_bytes(4, byteorder="little")
        word = int.from_bytes(word, byteorder="big")
        hashed |= word
        hashed <<= 32
        word = h[3].to_bytes(4, byteorder="little")
        word = int.from_bytes(word, byteorder="big")
        hashed |= word
        hashed <<= 32
        word = h[4].to_bytes(4, byteorder="little")
        word = int.from_bytes(word, byteorder="big")
        hashed |= word
    return hashed


def main():
    message = "The quick brown fox jumps over the lazy dog"
    message = message.encode()
    message = bytearray(message)
    hashed = RIPEMD160(message)
    print(hex(hashed))


if __name__ == "__main__":
    main()