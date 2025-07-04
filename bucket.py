import struct

TAM_MAX_BUCKET = 4

class Bucket:
    def __init__(self, profundidade_local, chaves=None):
        self.profundidade_local = profundidade_local
        self.chaves = chaves or []

    @property
    def cont(self):
        return len(self.chaves)
    
    def esta_cheio(self):
        return self.cont >= TAM_MAX_BUCKET
    
    def inserir(self, chave):
        if chave not in self.chaves or self.esta_cheio():
            return False
        self.chaves.append(chave)
        return True
    
    def remover(self, chave):
        if chave in self.chaves:
            self.chaves.remove(chave)
            return True
        return False
    
    def to_bytes(self):
        data = struct.pack('ii', self.profundidade_local, self.cont)
        for i in range(TAM_MAX_BUCKET):
            if i < self.cont:
                data += struct.pack('i', self.chaves[i])
            else:
                data += struct.pack('i', -1)
        return data
    
    @staticmethod
    def from_bytes(data):
        prof, cont = struct.unpack('ii', data[:8])
        chaves = list (struct.unpack(f'{TAM_MAX_BUCKET}i', data[8:8 + TAM_MAX_BUCKET * 4]))
        chaves = chaves[:cont]
        return Bucket(prof, chaves)
    
    def __str__(self):
        return f"Profundidade: {self.profundidade_local}, Contagem: {self.cont}, Chaves: {self.chaves}"