import sys

def decrypt(text):
    result = []
    for c in text:
        if 'A' <= c <= 'Z':
            result.append(chr(ord(c) - 1))
        elif 'a' <= c <= 'z':
            result.append(chr(ord(c) - 1))
        else:
            result.append(c) # Maybe digits too? Let's check: 3.1 -> 3.1? Wait, 1 -> 0?
    return ''.join(result)

def decrypt_file(in_path, out_path):
    with open(in_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    
    # Actually let's just shift ALL characters from ord 33 to 126 except space
    # Let's inspect the shifted text: "1%&" -> "PDE" ? P(80)->1(49)? No, 1%& -> PDE. 
    # Wait, '1' is 49, 'P' is 80. '1' -> 'P' is +31. 
    # '%' is 37, 'D' is 68. '%' -> 'D' is +31. 
    # '&' is 38, 'E' is 69. '&' -> 'E' is +31.
    # Ah! The shift is +31 for uppercase letters in that word, but 'QBSUJBM' (Q is 81) -> 'PARTIAL' (P is 80), shift is -1.
    # It seems the fonts have different encodings. This is a classic PDF font encoding issue, where different fonts map characters differently.

    pass
