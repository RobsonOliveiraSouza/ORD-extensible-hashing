def gerar_endereco(chave: int, profundidade: int) -> int:
    val_hash = chave
    val_endereco = 0
    for _ in range(profundidade):
        bit = val_hash & 1
        val_endereco = (val_endereco << 1) | bit
        val_hash >>= 1
    return val_endereco

if __name__ == "__main__":
    for chave in [1, 5, 10, 13, 255]:
        for profundidade in range(1, 5):
            endereco = gerar_endereco(chave, profundidade)
            print(f"Chave: {chave}, Profundidade: {profundidade}, Endereço: {endereco} (bin: {bin(endereco)[2:].zfill(profundidade)})")
