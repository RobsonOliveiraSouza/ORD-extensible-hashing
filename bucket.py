import struct

class Bucket:
    def __init__(self, profundidade_local, chaves=None):
        self.profundidade_local = profundidade_local
        self.chaves = chaves or []
        
    @property
    def cont(self):
        return len(self.chaves)

    def esta_cheio(self, tam_max):
        return self.cont >= tam_max

    def inserir(self, chave, tam_max):
        if chave in self.chaves or self.esta_cheio(tam_max):
            return False
        self.chaves.append(chave)
        return True

    def remover(self, chave):
        if chave in self.chaves:
            self.chaves.remove(chave)
            return True
        return False

    def to_bytes(self, tam_max):
        data = struct.pack('<ii', self.profundidade_local, self.cont)
        for i in range(tam_max):
            if i < self.cont:
                data += struct.pack('<i', self.chaves[i])
            else:
                data += struct.pack('<i', -1)
        return data

    @staticmethod
    def from_bytes(data, tam_max):
        prof, cont = struct.unpack('<ii', data[:8])
        chaves = list(struct.unpack(f'<{tam_max}i', data[8:8 + 4 * tam_max]))
        chaves = chaves[:cont]
        return Bucket(prof, chaves)

    def __str__(self):
        return f"Bucket(Prof: {self.profundidade_local}, Cont: {self.cont}, Chaves: {self.chaves})"
