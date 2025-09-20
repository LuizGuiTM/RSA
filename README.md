#  Comunicação Cliente-Servidor com RSA em Python

Este projeto demonstra uma comunicação segura entre **cliente** e **servidor** usando **RSA** (criptografia assimétrica).  
As mensagens trocadas são cifradas com a **chave pública** do destinatário e decifradas com a **chave privada** correspondente.

---

##  Estrutura do Projeto

```
.
├── servidor.py   # Código do servidor TCP com RSA
├── cliente.py    # Código do cliente TCP com RSA
└── README.md     # Documentação
```

---

## Como funciona

1. **Geração de chaves**  
   - Tanto o cliente quanto o servidor geram um par de chaves RSA `(n, e)` e `(d)`.
   - O valor `n` é o módulo, `e` o expoente público e `d` o expoente privado.

2. **Troca de chaves**  
   - O servidor envia sua chave pública ao cliente.
   - O cliente envia sua chave pública ao servidor.

3. **Envio de mensagem**  
   - O cliente digita uma mensagem.
   - A mensagem é dividida em blocos, convertida para inteiro e cifrada com a **chave pública do servidor**.
   - O servidor recebe e decifra a mensagem com sua **chave privada**.

4. **Resposta**  
   - O servidor processa a mensagem (neste exemplo, transforma em maiúsculas).
   - A resposta é cifrada com a **chave pública do cliente**.
   - O cliente recebe e decifra com sua **chave privada**.

---

##  Como executar

### 1. Inicie o servidor
No terminal:
```bash
python servidor.py
```
Saída esperada:
```
[Servidor] Chave pública: (n=..., e=...)
[Servidor] Aguardando conexão...
```

### 2. Inicie o cliente
Em outro terminal:
```bash
python cliente.py
```
Saída esperada:
```
[Cliente] Chave pública: (n=..., e=...)
[Cliente] Conectado ao servidor
```

Digite uma mensagem quando solicitado:
```
Digite a mensagem a ser enviada: ola mundo
```

### 3. Comunicação
- O servidor mostrará a mensagem recebida e a resposta em maiúsculas.  
- O cliente exibirá a resposta decifrada.

Exemplo:
```
[Cliente] Resposta do servidor: OLA MUNDO
```

---

##  Tecnologias utilizadas

- **Python 3**
- **Sockets TCP/IP**
- **RSA implementado manualmente** (geração de primos, cálculo de inverso modular, criptografia em blocos)

---

## Observações importantes

- Os tamanhos de chave no código podem ser configurados (no servidor: `4096 bits`, no cliente: `128 bits` para testes rápidos).  
- Para uso real, recomenda-se **≥2048 bits**.  
- Este projeto tem fins **educacionais** e não deve ser usado em produção sem melhorias.

---

## Referências

- William Stallings – *Cryptography and Network Security*  
- RFC 8017 – *PKCS #1: RSA Cryptography Specifications*  
- Documentação oficial do Python – [socket](https://docs.python.org/3/library/socket.html)  
