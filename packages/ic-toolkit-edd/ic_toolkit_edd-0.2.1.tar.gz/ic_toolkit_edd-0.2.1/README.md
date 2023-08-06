# IC-ToolKit-EDD

<img src="https://user-images.githubusercontent.com/71731452/177205395-ffe34180-5a7d-41f5-aba2-31ccc5b31031.gif" alt="exemplo imagem">

> Esse projeto tem como objetivo facilitar a resolução de problemas da equipe de transformação.

### Ajustes e melhorias

É possivel implementar qualquer tipo de script nesse projeto

## 💻 Pré-requisitos

Antes de começar, verifique se você atendeu aos seguintes requisitos:
<!---Estes são apenas requisitos de exemplo. Adicionar, duplicar ou remover conforme necessário--->
* Você instalou uma versão do Python superior a 3.7
* Você tem uma máquina `<Windows / Linux>`.

## 🚀 Instalando IC-ToolKit-EDD

Para instalar o IC-ToolKit-EDD, siga estas etapas:

Linux:
```
pip3 install ic-toolkit-edd
```

Windows:
```
pip install ic-toolkit-edd
```

Windows / Linux:

Use o comando abaixo para informar as credencias do seu banco MySQL.
```
ic config
```
> Obs: Isso vai gerar um arquivo .credentials em uma pasta .intuitivecare

<img src="https://user-images.githubusercontent.com/71731452/177249673-6373a5e5-8d13-4c70-8d2b-fefab60002db.svg" width=500>

## ☕ Comandos IC-ToolKit-EDD

Use o comando abaixo para calcular as hashs dos arquivos do diretório atual e gerar uma query para acompanhá-los na pipeline

```
ic gethash
```

>Opções:
>- `--sha256`: calcula os hashes usando o algoritmo SHA-256 ao invés do MD5 (Obs.: ao usar essa opção, não é gerada uma query)  

> Obs: Apos a execução do comando, a query gerada será copiada para a área de transferência


<img src="https://user-images.githubusercontent.com/71731452/177250804-c6833e17-9ec4-45a1-a166-6e07397f08d7.png" width=600>

---
Use o comando abaixo para baixar um ou mais arquivos da Amazon S3

```
ic downorig <>
```

>Opções:
> - `--tipo-id ou -t`: define o tipo dos IDs informados, podendo assumir um dentre os valores `original|parseado|padronizado|arquivo`
> - `--output-path ou -o`: define o caminho do diretório para o qual os arquivos devem ser baixados 
>   - Valor padrão: diretório atual (`"."`)

> Obs: Tambem é possivel baixar parseados e padronizados da mesma forma, utilizando os comandos downpars ou downpadr

<img src="https://user-images.githubusercontent.com/71731452/177250567-1464f5fa-292b-4b60-963c-f0892867780d.svg" width=600>

---
Use o comando abaixo para fazer upload de um ou mais arquivos para o seu diretorio correto na Amazon S3

```
ic upload
```
> Obs: Esse comando faz o upload de todos os arquivos do diretorio atual que contenham uma extenção compativel com nossas transformações.

<img src="https://user-images.githubusercontent.com/94455042/178642229-3c392b88-430a-40fc-8c3d-c4c4b846660f.svg" width=600>

---
Use o comando abaixo para gerar um filtro para vizualizar um arquivo na plataforma.

```
ic filtro
```
> Obs: Esse comando gera um filtro para a plataforma IC com base em um id_arquivo.

<img src="https://user-images.githubusercontent.com/94455042/203675246-ac481c56-2d26-43b7-80a9-11c0c663dbde.svg" width=600>

O comando abaixo pode ser utilizado para converter um ou mais documentos PDF em TXT usando a API da IC

````commandline
ic cvtpdf <>
````

>Opções:
> - `--input-path ou -i`: define o caminho para o PDF (ou diretório contendo arquivos PDF) a ser convertido para TXT
>   - Valor padrão: diretório atual (`"."`)
> - `--stripper ou -s`: define o *stripper* a ser utilizado para gerar o TXT, podendo assumir um dentre os valores `raw|layout|ordered_raw|ordered_layout`
>   - Valor padrão: `raw`
> - `--output-path ou -o`: define o caminho do diretório para o qual os arquivos devem ser baixados 
>   - Valor padrão: diretório atual (`"."`)

Use o comando abaixo para gerar o código de equivalências (Python) a partir da planilha de equivalências

```commandline
ic equiv
```

Basta entrar o nome do *Dataframe* de destino e copiar as três primeiras colunas da planilha de equivalência, pressionando enter logo em seguida.
O código de equivalências será gerado e copiado para sua área de transferência.

>Opções:
> - `--destino ou -d`: define o nome do *Dataframe* de destino (também pode ser informado via prompt)
> - `--origem ou -o`: define o nome do *Dataframe* de origem (opcional)
>   - Valor padrão: `df`

Use o comando abaixo para obter o *version_id* de um arquivo na S3:

```commandline
ic verids3
```

Basta informar o *Bucket*, Prefixo e Nome do arquivo na S3 e o *version_id* será exibido na tela e copiado para sua área de transferência.

Use o comando abaixo para baixar um arquivo qualquer na S3:

```commandline
ic downs3
```

Basta informar o *Bucket*, Prefixo e Nome do arquivo na S3 e o arquivo será baixado no diretório de destino (por padrão, o diretório atual).

>Opções:
>  - `--output-path ou -o`: define o caminho do diretório para o qual os arquivos devem ser baixados 
>   - Valor padrão: diretório atual (`"."`)

Use o comando abaixo para fazer o upload de um arquivo qualquer para a S3:

```commandline
ic uploads3
```

Basta informar o *Bucket*, prefixo e, opcionalmente, o nome do objeto (definido, por padrão, como o mesmo nome do arquivo) a ser gerado na S3 para o arquivo. 

>Opções:
>  - `--input-path ou -i`: define o caminho do arquivo a ser enviado para a s3 (também pode ser informado via prompt)

Use o comando abaixo para executar o script de reexecução do @AndreMartinsIC para uma lista de arquivos:

```commandline
ic reexec
```

Basta executar o comando e informar o passo do *pipeline* a ser reexecutado, o intervalo entre o disparo das requisições de reexecução e a lista de IDs dos arquivos a serem reprocessados.
Os IDs podem estar separados por vírgulas ou espaços (verticais ou horizontais). Após entrar os IDs, basta pressionar enter duas vezes para disparar a reexecução.

>Opções:
>  - `--passo-pipeline ou -p`: define o passo da pipeline a ser reexecutado e pula esse prompt 
>  - `--tempo-intervalo ou -t`: define o tempo de espera após disparar cada requisição (em segundos) e pula esse prompt
>    - Valor padrão: 30 segundos
>  - `--mostrar-ids ou -i`: se essa flag for utilizada, os IDs de cada arquivo reprocessado são exibidos na tela


## 🤝 Contribuindo

### Adicionando novas funções

Para adicionar novas funcionalidades acesse a documentação.

https://typer.tiangolo.com/


## 💡 Lembranças do grande idealizador do projeto: Marcelo Assis
<p align="center">
  <img src="https://github.com/IntuitiveCare/IC-ToolKit-EDD/blob/main/images/marcelo_o_criador.jpeg" width="350" title="Criador Toolkit">
</p>
