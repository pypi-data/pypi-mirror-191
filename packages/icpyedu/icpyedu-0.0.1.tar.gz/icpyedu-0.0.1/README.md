# ICPyEdu
O **ICPyEdu** é uma ferramenta para Assinaturas Digitais utilizando Certificado ICPEdu. Esse _package_ foi desenvolvido como um artefato complementar ao trabalho de conclusão de curso do aluno **Kemuel dos Santos Rocha** para obtenção do grau de Bacharelado em Engenharia da Computação.

O **ICPyEdu** é uma biblioteca para fins educativos e possibilita a assinatura de documentos em formato _.pdf_, assim como também a verificação da assinatura digital.

## Como instalar a biblioteca

Para fazer a instalação da biblioteca, basta executar o comando abaixo:
```python
pip install icpyedu
```
## Como importar as classes e métodos da biblioteca

Para utilizar as funcionalidades da o _package_, importe com o seguinte código:
```python
from icpyedu import signer 
```

Para instanciar a classe responsável pelos métodos de assinatura digital, basta declarar uma variável recebendo _Sign_ da seguinte forma:
```python
var = signer.Sign()
```

Para instanciar a classe responsável pelos métodos de verificação de assinaturas digitais, basta declarar uma variável recebendo _Verifier_ da seguinte forma:
```python
var = signer.Verify()
```

Finalmente para utilizar para assinar um pdf, basta chamar a função _signFile_ passando os parametros solicitados como por exemplo:
```python
var.signFile("email", "password", "filePath", "certificatePath")
```

De modo semelhante, para verificar um pdf, basta chamar a função _verifySignature_ passando os parametros solicitados como por exemplo:
```python
var.verifySignature("pdf","certifying authority_1", "certifying authority_2")
```
Os certificados de autoridades certificadoras são arquivos que vem juntos ao certificado pessoal exportado pelo ICPEdu