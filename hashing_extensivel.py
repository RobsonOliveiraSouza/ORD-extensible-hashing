import os
import struct
from diretorio import Diretorio
from bucket import Bucket
from util import gerar_endereco

# Rafael Monteiro Zancanaro
# Robson Oliveira de Souza
# Vitor Fernando Regis

class HashingExtensivel:
    def __init__(self, tam_max_buck=3, arq_diretorio='diretorio.dat', arq_buckets='buckets.dat'):
        self.TAM_MAX_BUCKET = tam_max_buck
        self.arq_diretorio = arq_diretorio
        self.arq_buckets = arq_buckets
        self.tamanho_bucket = 5 * 4

        if os.path.exists(self.arq_diretorio):
            self.diretorio = Diretorio.carregar_de_arquivo(self.arq_diretorio)
        else:
            with open(self.arq_buckets, 'wb') as f:
                pass
            self.diretorio = Diretorio(0)
            bucket0 = Bucket(profundidade_local=0)
            self._escrever_bucket(bucket0, 0)
            self.diretorio.refs = [0]
        self._salvar_diretorio()

    def _salvar_diretorio(self):
        self.diretorio.salvar_em_arquivo(self.arq_diretorio)

    def _ler_bucket(self, rrn):
        with open(self.arq_buckets, 'rb') as f:
            f.seek(rrn * self.tamanho_bucket)
            data = f.read(self.tamanho_bucket)
        return Bucket.from_bytes(data, self.TAM_MAX_BUCKET)  # <- corrigido

    def _escrever_bucket(self, bucket, rrn):
        with open(self.arq_buckets, 'r+b') as f:
            f.seek(rrn * self.tamanho_bucket)
            f.write(bucket.to_bytes(self.TAM_MAX_BUCKET))  # <- corrigido


    def op_buscar(self, chave):
        endereco = gerar_endereco(chave, self.diretorio.profundidade_global)
        ref_bucket = self.diretorio.obter_referencia(endereco)
        bucket = self._ler_bucket(ref_bucket)
        if chave in bucket.chaves:
            return True, ref_bucket, bucket
        return False, ref_bucket, bucket

    def op_inserir(self, chave):
        achou, ref_bucket, bucket = self.op_buscar(chave)
        if achou:
            return False
        self.inserir_chave_bucket(chave, ref_bucket, bucket)
        return True

    def inserir_chave_bucket(self, chave, ref_bucket, bucket):
        print(f"Tentando inserir chave {chave} no bucket {ref_bucket} (cont = {bucket.cont})")
        if bucket.cont < self.TAM_MAX_BUCKET:
            print(f"Inserindo no bucket {ref_bucket} diretamente.")
            bucket.inserir(chave, self.TAM_MAX_BUCKET)
            self._escrever_bucket(bucket, ref_bucket)
        else:
            print(f"Bucket {ref_bucket} cheio (cont = {bucket.cont}). Chamando _dividir_bucket.")
            self._dividir_bucket(ref_bucket, bucket)
            self.op_inserir(chave)  # Reinsere a chave após divisão

    def _dividir_bucket(self, ref_bucket, bucket):
        print(f"\n===> Iniciando divisão do bucket {ref_bucket}")
        print(f"Bucket antes da divisão: {bucket}")

        if bucket.profundidade_local == self.diretorio.profundidade_global:
            print("Profundidade local == global, dobrando diretório.")
            self.dobrar_diretorio()

        nova_profundidade = bucket.profundidade_local + 1
        novo_bucket = Bucket(profundidade_local=nova_profundidade)
        bucket.profundidade_local = nova_profundidade

        rrn_novo_bucket = len(set(self.diretorio.refs))  # novo RRN único

        for i in range(len(self.diretorio.refs)):
            endereco = i >> (self.diretorio.profundidade_global - nova_profundidade)
            if endereco & 1:
                if self.diretorio.refs[i] == ref_bucket:
                    self.diretorio.refs[i] = rrn_novo_bucket

        print(f"RRN novo bucket: {rrn_novo_bucket}")
        print(f"Redistribuindo chaves entre bucket {ref_bucket} e {rrn_novo_bucket}")

        chaves_antigas = bucket.chaves[:]
        bucket.chaves.clear()
        novo_bucket.chaves.clear()

        for chave in chaves_antigas:
            endereco = gerar_endereco(chave, nova_profundidade)
            if endereco & 1:
                print(f"Movendo chave {chave} para novo bucket")
                novo_bucket.inserir(chave, self.TAM_MAX_BUCKET)
            else:
                print(f"Retendo chave {chave} no bucket original")
                bucket.inserir(chave, self.TAM_MAX_BUCKET)

        self._escrever_bucket(bucket, ref_bucket)
        self._escrever_bucket(novo_bucket, rrn_novo_bucket)
        self._salvar_diretorio()

        print(f"Bucket {ref_bucket} após divisão: {bucket}")
        print(f"Bucket {rrn_novo_bucket} criado: {novo_bucket}\n")

    def _buscar_proximo_rrn(self):
        with open(self.arq_buckets, 'rb') as f:
            f.seek(0, os.SEEK_END)
            tamanho_atual = f.tell()
        return tamanho_atual // self.tamanho_bucket

    def dobrar_diretorio(self):
        print(f"Dobrando diretório. Profundidade global atual: {self.diretorio.profundidade_global}")
        self.diretorio.refs += self.diretorio.refs
        self.diretorio.profundidade_global += 1
        print(f"Nova profundidade global: {self.diretorio.profundidade_global}")
        print(f"Referências do diretório: {self.diretorio.refs}")
        self._salvar_diretorio()


    def op_remover(self, chave):
        achou, ref_bucket, bucket = self.op_buscar(chave)
        if not achou:
            return False
        return self.remover_chave_bucket(chave, ref_bucket, bucket)

    def remover_chave_bucket(self, chave, ref_bucket, bucket):
        if chave not in bucket.chaves:
            return False
        bucket.remover(chave)
        self._escrever_bucket(bucket, ref_bucket)
        self.tentar_combinar_bucket(chave, ref_bucket, bucket)
        return True

    def tentar_combinar_bucket(self, chave_removida, ref_bucket, bucket):
        tem_amigo, endereco_amigo = self.encontrar_bucket_amigo(chave_removida, bucket)
        if not tem_amigo:
            return
        ref_amigo = self.diretorio.obter_referencia(endereco_amigo)
        bk_amigo = self._ler_bucket(ref_amigo)
        if bk_amigo.cont + bucket.cont <= self.TAM_MAX_BUCKET:
            bucket = self.combinar_buckets(ref_bucket, bucket, ref_amigo, bk_amigo)
            for i in range(len(self.diretorio.refs)):
                if self.diretorio.refs[i] == ref_amigo:
                    self.diretorio.refs[i] = ref_bucket
            if self.tentar_diminuir_diretorio():
                self.tentar_combinar_bucket(chave_removida, ref_bucket, bucket)
            self._salvar_diretorio()

    def encontrar_bucket_amigo(self, chave_removida, bucket):
        if self.diretorio.profundidade_global == 0:
            return False, None
        if bucket.profundidade_local < self.diretorio.profundidade_global:
            return False, None
        end_comum = gerar_endereco(chave_removida, bucket.profundidade_local)
        end_amigo = end_comum ^ 1
        return True, end_amigo

    def combinar_buckets(self, ref_bucket, bucket, ref_amigo, bucket_amigo):
        for chave in bucket_amigo.chaves:
            bucket.inserir(chave, self.TAM_MAX_BUCKET)
        bucket.profundidade_local -= 1
        self._escrever_bucket(bucket, ref_bucket)
        bucket_vazio = Bucket(profundidade_local=0)
        self._escrever_bucket(bucket_vazio, ref_amigo)
        return bucket

    def tentar_diminuir_diretorio(self):
        if self.diretorio.profundidade_global == 0:
            return False
        tamanho = 2 ** self.diretorio.profundidade_global
        diminuir = True
        for i in range(0, tamanho, 2):
            if self.diretorio.refs[i] != self.diretorio.refs[i + 1]:
                diminuir = False
                break
        if diminuir:
            self.diretorio.refs = self.diretorio.refs[::2]
            self.diretorio.profundidade_global -= 1
        return diminuir