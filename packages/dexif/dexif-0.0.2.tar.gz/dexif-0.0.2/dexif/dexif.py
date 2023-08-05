def to_fixed(v):
    v = str(v)
    (si, sf) = v.split('.')
    d = int(si)
    f = float('0.' + sf)
    k = len(sf)
    mask = (10 ** k)

    r = 0
    c = 0.0
    for i in range(64):
        f *= 2
        if f > 1.0:
            c += (1 / (2 ** (i + 1)))
            r |= (1 << (63 - i))
            f -= 1.0

    r += (d << 64)
    b = r.to_bytes(16, byteorder='big')
    return int(r)


def from_fixed(v):
    if len(v) > 2:
        if v[:2] == '0x':
            v = v[2:]
    if len(v) % 2 != 0:
        v = '0' + v
    if len(v) < 16:
        raise ValueError('need at least 64 bit hex')

    b = bytes.fromhex(v)
    w = int.from_bytes(b, byteorder='big', signed=True)
    d = w & 0xffffffffffffffff

    r = 0.0
    k = 1 << 63
    for i in range(64):
        if k & d > 0:
            r += (1 / (1 << (i + 1)))
        k >>= 1

    return float("{}.{}".format((w >> 64), "{:.64f}".format(r)[2:]))
