import struct

class Diretorio:
    def __init__(self, profundidade_global):
        self.profundidade_global = profundidade_global
        self.refs = [0] * (2 ** profundidade_global)

    def duplicar(self):
        self.refs += self.refs
        self.profundidade_global += 1

    def atualizar_referencia(self, endereco, rrn):
        self.refs[endereco] = rrn

    def obter_referencia(self, endereco):
        return self.refs[endereco]

    def salvar_em_arquivo(self, nome_arquivo):
        with open(nome_arquivo, 'wb') as f:
            f.write(struct.pack('<i', self.profundidade_global))
            for ref in self.refs:
                f.write(struct.pack('<i', ref))

    @staticmethod
    def carregar_de_arquivo(nome_arquivo):
        with open(nome_arquivo, 'rb') as f:
            profundidade_global = struct.unpack('<i', f.read(4))[0]
            tamanho = 2 ** profundidade_global
            refs = [struct.unpack('<i', f.read(4))[0] for _ in range(tamanho)]
        d = Diretorio(profundidade_global)
        d.refs = refs
        return d

    def __str__(self):
        info = f"Profundidade Global: {self.profundidade_global}\n"
        for i, ref in enumerate(self.refs):
            info += f"dir[{i}] -> bucket({ref})\n"
        return info
