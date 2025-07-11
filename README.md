# Hashing Extensível

Trabalho da disciplina de Organização e Recuperação de Dados (9895/31), implementa uma estrutura de **Hashing Extensível** em Python, conforme a especificação previa.

## 📚 O que é Hashing Extensível?

O hashing extensível é uma técnica de indexação dinâmica que cresce ou reduz automaticamente a estrutura de diretório e buckets conforme a necessidade. Utiliza:

- `diretorio.dat`: armazena em disco o diretório (referências para os buckets).
- `buckets.dat`: armazena os buckets com as chaves (sem dados associados).

---

## ⚙️ Estrutura do Projeto

- `hashing_extensivel.py` – lógica principal do hashing.
- `bucket.py` – classe do bucket e serialização binária.
- `diretorio.py` – classe do diretório com referências e profundidade.
- `util.py` – contem função auxiliar `gerar_endereco`.
- `programa.py` – interface CLI para comandos.
- `arquivo_operacoes.txt` – exemplo de arquivo de entrada com operações.

---

## ▶ Como executar

### 1️⃣ Executar operações de um arquivo:

```bash
python programa.py -e arquivo_operacoes.txt
```

Esse comando processa um arquivo contendo operações (`i`, `b`, `r`), por exemplo:

```
i 144
b 130
r 60
```

- `i` = inserir chave
- `b` = buscar chave
- `r` = remover chave

---

### 2️⃣ Imprimir o diretório atual:

```bash
python programa.py -pd
```

Este comando imprime:

- A profundidade global
- O tamanho do diretório (número de entradas)
- A quantidade de buckets distintos
- O mapeamento `Endereço -> Bucket`

---

### 3️⃣ Imprimir os buckets:

```bash
python programa.py -pb
```

Este comando exibe todos os **buckets ativos** com:

- Número do bucket
- Profundidade local
- Quantidade de chaves
- Lista das chaves armazenadas

---

### 4️⃣ Limpar os arquivos binários (resetar estrutura):

```bash
rm diretorio.dat buckets.dat
```

Na próxima execução do programa, os arquivos serão recriados automaticamente com profundidade zero e um bucket inicial.

---

## 👨‍💻 Autores

- Rafael Monteiro Zancanaro  
- Robson Oliveira de Souza  
- Vitor Fernando Regis

---

## 📄 Licença

Projeto acadêmico – uso exclusivamente educacional.