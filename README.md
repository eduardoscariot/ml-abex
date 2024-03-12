## Descrição geral do projeto
https://colab.research.google.com/drive/1FYixr7V6vRzgN2Acvu4y_RTRmKKIAg18?authuser=1#scrollTo=IyXI9yCUbvQ3
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original-wordmark.svg" width="40" height="60" /><img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/streamlit/streamlit-plain-wordmark.svg" width="60" height="60" />
               
Este projeto visa realizar a **implantação de um modelo de ML** em produção, ou seja, em um servidor dedicado que poderá responder solicitações de usuários na internet por meio de um web browser. O projeto foi desenvolvido na **Pós Graduação de Big Data e Data Science da Unochapecó**.

###### Pode ser executado em qualquer plataforma.
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/linux/linux-original.svg" width="20" height="20"/><img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/apple/apple-original.svg" width="20" height="20"/><img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/windows11/windows11-original.svg" width="20" height="20"/>

### Passos para a criação e execução deste projeto

Segue o passo a passo para a criação do ambiente virtual para execução do projeto.

#### Criar um ambiente virtual
Na pasta do projeto, executar o comando abaixo que vai criar o ambiente virtual que vamos utilizar.
          
```commandline
python3 -m venv venv
```

#### Ativar o ambiente virtual
Após a criação do ambiente, precisamos ativar(entrar) no ambiente virtual. Atenção, a ativação do ambiente virtual é diferente entre os ambiente MacOS/Linux e Windows.

<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/linux/linux-original.svg" width="40" height="40"/><img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/apple/apple-original.svg" width="40" height="40"/>

```commandline
source venv/bin/activate
```

<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/windows11/windows11-original.svg" width="40" height="40"/>

```commandline
venv\Scripts\Activate.ps1
```

> Caso apresentar alguma falha ao rodar o comando em Windows, abra um Shell em modo administrador e execute o comando:
> ```commandline
> Set-ExecutionPolicy Unrestricted
> ```


### Carregar as libs dentro do ambiente virtual
Certo, agora que temos nosso projeto executando, vamos executar o comando para instalar as bibliotecas necessárias do projeto.

#### Instalar todas as libs
```commandline
pip install -r requirements.txt
```

#### Salvar as libs
Caso alguma nova biblioteca seja instalada no projeto, podemos utilizar o comando abaixo para gerar o arquivo requirements novamente, assim ele fica sempre atualizado!
```commandline
pip freeze > requirements.txt
```

#### Testar o Streamlit
Para executar o Streamlit e confirmar se está tudo certo, basta executar o comando abaixo. Vai abrir uma página padrão do Streamlit.
```commandline
python -m streamlit hello
```

#### Rodar o App
Para executarmos o arquivo que criamos no projeto, utilizamos o comando abaixo.
```commandline
streamlit run app.py
```

### Configurar AWS
Caso queira executar o projeto em uma máquina virtual do AWS, ou outro lugar de sua preferência, precisamos executar alguns comandos antes de mapear o projeto.

```commandline
sudo apt update
```

```commandline
sudo apt-get update
```

```commandline
sudo apt upgrade -y
```

```commandline
sudo apt install python3-pip
```

```commandline
sudo apt install python3.10-venv
```

Em seguida é só clonar o projeto.

### Para deixar o sistema rodando em background, usar screen (console virtual)

A documentação do **Screen** pode ser encontrada no [aqui](https://www.gnu.org/software/screen/manual/screen.html), mas os principais comandos que podem ser utilizados são:

#### Para criar um novo console virtual
```commandline
screen -S streamlit_session
```
> Nesse caso **streamlit_session** é o nome do novo console.

#### Para sair do console virtual
```commandline
ctrl+a  d
```

#### Para entrar novamente no console virtual
```commandline
screen -r streamlit_session
```
> Nesse caso **streamlit_session** é o nome do novo console.

#### Para visualizar os consoles virtuais rodando
```commandline
screen -ls
```

#### Para matar o console virtual
```commandline
screen -X -S streamlit_session quit
```
> Nesse caso **streamlit_session** é o nome do novo console.

Uma screen pode ser utilizada nesse projeto para deixar o código do Streamlit executando em um console virtual e uma outra screen para a execução da API.

#### Para iniciar a API
```commandline
uvicorn main:api --reload
```
