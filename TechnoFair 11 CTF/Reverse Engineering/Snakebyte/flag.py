from transformers import AutoTokenizer as A

enc = [
    30200989,
    44161,
    63530220,
    875004,
    74052862,
    3760874,
    30810,
    87295,
    121186,
    53404,
    127348,
    55458,
    69836,
    98592,
    53404,
    2293291,
    20540,
    529932,
    95511,
    60593,
    1802385,
    120159,
    49296,
    87295,
    93457,
    105781,
    878085,
    126321,
    88322,
    72917,
    127348,
    32864,
    1040351,
    91403,
    42107,
    119132,
    116051,
]


def D(n, k="secret-key", w="Technofair"):
    w_o = sum(ord(c) for c in w)
    k_o = [ord(c) for c in k]
    k_l = len(k_o)
    Dcd = [((x // w_o) ^ k_o[i % k_l]) for i, x in enumerate(n)]
    return Dcd


T = A.from_pretrained("Xenova/gpt-4")

Dcd = D(enc)
print("".join(T.convert_ids_to_tokens(Dcd)))
