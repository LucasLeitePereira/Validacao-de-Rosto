**Projeto de Reconhecimento Facial com Python e MongoDB**

## 📖 Resumo do Projeto

Este projeto nasce da necessidade de controlar o acesso de usuários em uma academia de forma automática e segura, utilizando reconhecimento facial. Nele, desenvolvemos dois scripts em Python:

1. **Cadastro de Rosto**: Captura a imagem do rosto via webcam e armazena os dados faciais em um banco de dados NoSQL (MongoDB).
2. **Validação de Acesso**: Captura uma nova imagem pela webcam, busca a face cadastrada no banco de dados e valida se pertence ao usuário correto antes de liberar a catraca.

O sistema grava informações sobre cada conta (nome, sexo, idade) e armazena o vetor de codificação facial diretamente no documento do usuário no MongoDB para maior eficiência e flexibilidade.

---

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado em sua máquina:

* **Python 3.7** ou superior
* **MongoDB** (versão 4.0 ou superior)
* **Git** (para clonar este repositório)

Além disso, vamos utilizar as seguintes bibliotecas Python:

```txt
face_recognition
opencv-python
pymongo
numpy
```

---

## ⚙️ Instalação e Configuração

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/LucasLeitePereira/Validacao-de-Rosto
   ```

2. **Crie e ative um ambiente virtual** (opcional, mas recomendado):

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate    # Windows
   ```

3. **Instale as dependências**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o MongoDB**:

   * Certifique-se de que o serviço do MongoDB está em execução.
   * O sistema criará automaticamente o banco de dados `face_access_db` e a coleção `users` ao ser executado pela primeira vez.

5. **Atualize o arquivo de configuração** (`config.py`) com sua URI do MongoDB, se necessário.

---

## ▶️ Uso

### 1. Cadastro de Rosto

Este script solicita que o usuário forneça seus dados e posicione o rosto à frente da webcam para salvar a codificação facial no banco:

```bash
python cadastrarConta.py
```

#### Fluxo:

1. Solicita Nome, Idade e Sexo.
2. Abre a câmera e detecta o rosto.
3. Converte a imagem para vetores faciais (encodings).
4. Insere o documento contendo os dados do usuário e o vetor facial no MongoDB.

### 2. Validação de Acesso

Este script abre a webcam, captura a face e compara com a cadastrada para o usuário informado:

```bash
python validarRosto.py
```

#### Fluxo:

1. Solicita o nome para validação.
2. Abre a câmera e detecta o rosto ao vivo.
3. Gera o vetor facial da captura.
4. Busca o vetor do usuário no MongoDB e realiza a comparação.
5. Se houver correspondência, exibe "Access Granted"; caso contrário, "Access Denied".

---

## 🤝 Contribuição

Sinta-se à vontade para abrir issues e pull requests! Para sugestões ou melhorias no código, siga as normas de estilo Python (PEP8).

---

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
