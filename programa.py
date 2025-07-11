import sys
import os

from hashing_extensivel import HashingExtensivel

# Rafael Monteiro Zancanaro
# Robson Oliveira de Souza
# Vitor Fernando Regis

def executar_operacoes(nome_arquivo):
    hashing = HashingExtensivel()

    with open(nome_arquivo, 'r') as f:
        print("\n---- Operações ----\n")
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
            
        print(f"\nAs operações do arquivo {nome_arquivo} foram concluídas com sucesso!\n")

def imprimir_diretorio():
    hashing = HashingExtensivel()
    dir = hashing.diretorio
    print("\n---- Diretório ----\n")
    for i, ref in enumerate(dir.refs):
        print(f"dir[{i}] = bucket[{ref}]")
    print(f"\nProfundidade: {dir.profundidade_global}")
    print(f"Tamanho atual: {len(dir.refs)}")
    print(f"Número total de buckets: {len(set(dir.refs))}\n")

def imprimir_buckets():
    hashing = HashingExtensivel()
    bucket_usados = set(hashing.diretorio.refs)
    print("\n---- Buckets ----\n")
    try:
        with open(hashing.arq_buckets, 'rb') as f:
            f.seek(0, os.SEEK_END)
            total_buckets = f.tell() // hashing.tamanho_bucket

        for rrn in range(total_buckets):
            bucket = hashing._ler_bucket(rrn)
            if rrn in bucket_usados:
                chaves_formatadas = bucket.chaves + [-1] * (hashing.TAM_MAX_BUCKET - len(bucket.chaves))
                print(f"Bucket {rrn} (Prof = {bucket.profundidade_local}):")
                print(f"ContaChaves = {bucket.cont}")
                print(f"Chaves = {chaves_formatadas}\n")
            else:
                print(f"Bucket {rrn} --> Removido \n")
    except FileNotFoundError:
        print("Arquivo de buckets não encontrado.")

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
        print("\nComando inválido. Use: [-e arquivo] [-pd] [-pb]\n")

if __name__ == '__main__':
    main()