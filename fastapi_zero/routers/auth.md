# Autenticação

Aqui você vai aprender a autenticar usuários em sua aplicação FastAPI.
Quero, documentar a autenticação de usuários em minha aplicação FastAPI.

```mermaid
sequenceDiagram

Client ->> Servidor: Envia credenciais (e-email e senha) via formulário OAuth2

Servidor ->> Servidor: Valida as credenciais

Servidor ->> Client: Retorna um token de acesso JWT
```

Se o envio das credenciais for bem-sucedido, o servidor retornará um token de acesso JWT (JSON Web Token) que o cliente usará para acessar recursos protegidos.

Caso, contrário, o servidor retornará um erro.

## Endpoint de autenticação `/token`

Para autenticar um usuário, você precisará criar um endpoint `/token` que aceite credenciais e retorne um token de acesso JWT.

O FastAPI fornece uma maneira facil de implementar autenticação OAuth2 com JWT. Com o FastAPI, você pode usar o pacote `fastapi.security` para implementar autenticação OAuth2.

O `OAuth2PasswordRequestForm` é uma classe do FastAPI que você pode usar para validar as credenciais do usuário.

O retorno do endpoint `/token` será um token de acesso JWT que o cliente usará para acessar recursos protegidos.

### O que é um token de acesso JWT?

Um token de acesso JWT é um token que contém informações sobre o usuário autenticado. O token é assinado com uma chave secreta e pode ser decodificado para obter informações sobre o usuário.

O token de acesso JWT é usado para autenticar o usuário em cada solicitação subsequente.

O token de acesso JWT é composto por três partes: o cabeçalho, o payload e a assinatura.

#### Cabeçalho

> [!NOTE]
> Algorítimo + Tipo de token

O cabeçalho contém informações sobre o tipo de token e o algoritmo de assinatura usado.

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

#### Payload

> [!NOTE]
> Dados que serão usados para assinatura

O payload contém as informações do usuário autenticado.

```json
{
  "sub": "ant@ant.v",
  "exp": 163
}
```

- **Claims:**

Claims são informações sobre o usuário autenticado que são codificadas no token de acesso JWT. As reivindicações são usadas para transmitir informações sobre o usuário autenticado.

As reivindicações mais comuns são:

- `sub`: O identificador exclusivo do usuário
- `exp`: O tempo de expiração do token (em segundos)

#### Assinatura

> [!NOTE]
> Aplicação do algoritmo + chave secreta

A assinatura é usada para verificar a integridade do token. A assinatura é gerada a partir do cabeçalho, do payload e de uma chave secreta.

#### Testando a biblioteca jwt

```python
>>> import jwt
>>> jwt.encode({'sub': 'ant@ant.v'}, '123')
'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbnRAYW50LnYifQ.cNA2qaEHAPxv4YnJhSInpXoDpUOlaTytRqg0qJXxk0Y'
```

O token gerado é retornado para o cliente, que o usará para acessar recursos protegidos. Pertinentes ao usuário em 'sub'.

![alt text](image.png)
