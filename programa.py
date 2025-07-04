import sys
from hashing_extensivel import HashingExtensivel

def executar_operacoes(nome_arquivo):
    hashing = HashingExtensivel()

    with open(nome_arquivo, 'r') as f:
        for linha in f:
            partes = linha.strip().split()
            if len(partes) != 2:
                continue
            comando, valor = partes
            chave = int(valor)

            if comando == 'i':
                sucesso = hashing.op_inserir(chave)
                if sucesso:
                    print(f"> Inserção da chave {chave}: Sucesso.")
                else:
                    print(f"> Inserção da chave {chave}: Falha – Chave duplicada.")
            
            elif comando == 'b':
                achou, ref, _ = hashing.op_buscar(chave)
                if achou:
                    print(f"> Busca pela chave {chave}: Chave encontrada no bucket {ref}.")
                else:
                    print(f"> Busca pela chave {chave}: Chave não encontrada.")
            
            elif comando == 'r':
                sucesso = hashing.op_remover(chave)
                if sucesso:
                    print(f"> Remoção da chave {chave}: Sucesso.")
                else:
                    print(f"> Remoção da chave {chave}: Falha – Chave não encontrada.")

def imprimir_diretorio():
    hashing = HashingExtensivel()
    dir = hashing.diretorio
    print("\n--- Diretório ---")
    print(f"Profundidade global: {dir.profundidade_global}")
    print(f"Tamanho atual: {len(dir.refs)}")
    print(f"Número de buckets distintos: {len(set(dir.refs))}")
    for i, ref in enumerate(dir.refs):
        print(f"Endereço {i}: Bucket {ref}")

def imprimir_buckets():
    hashing = HashingExtensivel()
    buckets_lidos = set()
    print("\n--- Buckets ---")
    for i, ref in enumerate(hashing.diretorio.refs):
        if ref in buckets_lidos:
            continue
        bucket = hashing._ler_bucket(ref)
        print(f"Bucket {ref}: profundidade = {bucket.profundidade_local}, chaves = {bucket.chaves}")
        buckets_lidos.add(ref)

def main():
    if len(sys.argv) < 2:
        print("Uso: python programa.py [-e arquivo] [-pd] [-pb]")
        return

    comando = sys.argv[1]

    if comando == '-e' and len(sys.argv) == 3:
        executar_operacoes(sys.argv[2])
    elif comando == '-pd':
        imprimir_diretorio()
    elif comando == '-pb':
        imprimir_buckets()
    else:
        print("Comando inválido. Use: [-e arquivo] [-pd] [-pb]")

if __name__ == '__main__':
    main()
