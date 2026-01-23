# SEI Pilot — AutoAtribuidor

Automação de rotina processual no **SEI (Sistema Eletrônico de Informações)** usando **Python + Selenium + Firefox**, com foco em tarefas repetitivas de **pesquisa**, **consulta** e **exportação de dados de processos**.

> Licença: **MIT**  
> Linguagem: **Python 3.x**

---

## 📌 Visão geral

O **SEI Pilot (AutoAtribuidor)** é uma automação em Python que utiliza **Selenium + Firefox** para executar rotinas operacionais no SEI (ambiente DF), facilitando atividades repetitivas relacionadas à **pesquisa e consulta de processos**.

O sistema oferece um **menu interativo (CLI)** para executar tarefas como:

- ✅ Consultar andamentos de processos em lote a partir de um CSV  
- ✅ Listar processos recebidos na unidade e salvar em CSV  
- ✅ Pesquisar processos de uma unidade específica e salvar em CSV  

---

## ⚙️ Funcionalidades

### 1) Consultar andamentos (em lote)
Lê um arquivo CSV com números de processo e, para cada um:

1. abre o processo no SEI  
2. acessa o menu lateral (“árvore”) via `ifrArvore`  
3. clica no botão **Consultar Andamento** (`divConsultarAndamento`)  

📌 Há um *throttling randômico* entre requisições (1 a 2 segundos) para reduzir comportamento robótico.

---

### 2) Ler "Processos Recebidos" e gerar CSV
Varre a tabela `tblProcessosRecebidos`, extraindo:

- Número do processo  
- Descrição do processo  
- Anotação (quando existir)  
- Tag/marcador (quando existir)  

E salva os dados em um CSV na pasta `csv/`.

---

### 3) Pesquisar processos de uma unidade
Executa uma pesquisa no SEI com base no código da unidade, coletando:

- Título completo da linha encontrada  
- Número do processo extraído do texto  

E exporta o resultado para CSV.

---

## 🧱 Estrutura do projeto

```
AutoAtribuidor/
├─ main.py
├─ requirements.txt
├─ LICENSE
├─ csv/
│  ├─ processos.csv
│  ├─ processos_recebidos.csv
│  └─ processos_save.csv
└─ gestorsei/
   ├─ cli.py
   ├─ config.py
   ├─ sei_client.py
   ├─ webdriver_factory.py
   ├─ handlers/
   │  ├─ processos.py
   │  └─ pesquisa.py
   └─ utils/
      ├─ env.py
      ├─ io_csv.py
      ├─ strings.py
      └─ paths.py
```

---

## ✅ Requisitos

- Python **3.x**
- Mozilla Firefox instalado
- Selenium + GeckoDriver  
  - Instalado automaticamente via `webdriver-manager` (dependência do projeto)

Dependências principais (definidas em `requirements.txt`):

- `selenium`
- `webdriver-manager`
- `beautifulsoup4`
- `python-dotenv`

---

## 🚀 Instalação

### 1) Baixe/clone o repositório
```bash
git clone https://github.com/munizigor/AutoAtribuidor.git
cd AutoAtribuidor
```

> Se você baixou como `.zip`, apenas extraia e entre na pasta do projeto.

---

### 2) Crie um ambiente virtual (recomendado)

#### Windows (PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

#### Linux/Mac
```bash
python -m venv .venv
source .venv/bin/activate
```

---

### 3) Instale as dependências
```bash
pip install -r requirements.txt
```

---

## 🔐 Configuração de credenciais (recomendado)

O sistema pode solicitar usuário/senha no terminal, mas você também pode salvar no `.env` para facilitar.

Na **raiz do projeto**, crie um arquivo chamado:

📄 `.env`

Com o conteúdo:

```env
SEI_USUARIO=seu_usuario
SEI_SENHA=sua_senha
SEI_ORGAO_VALUE=cod_orgao

SEI_URL = Endereço raiz do seu SEI. Ex.: "https://sei.df.gov.br/"
FIREFOX_BINARY = Endereço raiz do Firefox. Ex.: "C:/Program Files/Mozilla Firefox/firefox.exe" (Se o seu Firefox estiver em outro local, ajuste essa variável.)
```

✅ O programa detecta automaticamente e tenta usar as credenciais salvas.

> O campo `SEI_ORGAO_VALUE` corresponde ao valor selecionado no `<select id="selOrgao">` da tela de login do SEI.  


---

## ▶️ Como executar

Execute:

```bash
python main.py
```

Isso chama o CLI:

```python
from gestorsei.cli import main
```

Você verá um menu parecido com:

```
1. Consultar andamentos (via CSV)
2. Ler processos recebidos e salvar em CSV
3. Salvar processos de uma unidade em CSV
```

---

## 📄 Arquivos gerados (CSV)

Todos os arquivos são salvos automaticamente na pasta:

📁 `csv/`

---

### Opção 1 — consultar andamentos

Você deve fornecer um CSV contendo processos.

Exemplo de arquivo `csv/processos.csv`:

```csv
0700000-00.2026.8.07.0000
0700000-00.2026.8.07.0001
```

✅ A automação vai abrir cada processo e clicar em **Consultar Andamento**.

---

### Opção 2 — processos recebidos

Gera automaticamente:

📄 `csv/processos_recebidos.csv`

Formato:

```csv
Processo,Descricao,Anotacoes,Tag
0700000-00.2026.8.07.0000,Descrição...,Anotação...,Tag...
```

---

### Opção 3 — processos de uma unidade

Você informa o código da unidade, e ele gera:

📄 `csv/processos_save.csv`

Formato:

```csv
Título,Processo
Texto completo do item,0700000-00.2026.8.07.0000
```

---

## 🧠 Observações importantes

### ✅ Uso de iframes no SEI
Algumas páginas do SEI carregam conteúdo em iframes como:

- `ifrArvore`
- `ifrConteudoVisualizacao`
- `ifrVisualizacao`

Por isso o código alterna entre:

- `driver.switch_to.default_content()`  
- `frame_to_be_available_and_switch_to_it(...)`

---

### ✅ Robustez e possíveis ajustes
Como o SEI pode variar por órgão/unidade e pode sofrer mudanças de layout, pode ser necessário ajustar seletores.

Exemplo: no handler de pesquisa há um XPath fixo:

```python
driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/ul/li[4]/a").click()
```

Se o menu mudar, esse trecho deve ser atualizado para um seletor mais estável.

---

## 🧪 Troubleshooting

### Erro: Firefox não encontrado
✔ Ajuste `FIREFOX_BINARY` em:

`gestorsei/config.py`

---

### Erro: GeckoDriver ou Selenium não inicia
O projeto usa `webdriver-manager`, mas você pode configurar manualmente via variável de ambiente:

```bash
set GECKODRIVER_PATH=C:\caminho\para\geckodriver.exe
```

---

### SEI abre mas não faz login
Verifique:

- Usuário/senha corretos  
- `SEI_ORGAO_VALUE` compatível com seu órgão no `<select>`  
- Se o SEI exige captcha/MFA (pode impedir automação)  

---

## 🔒 Segurança

Recomendações:

- ❌ Nunca comitar `.env` no Git
- ✅ Usar `.gitignore` para evitar vazamento de credenciais
- ✅ Executar a automação apenas com autorização institucional, conforme políticas internas

---

## 📌 Roadmap sugerido (melhorias futuras)

- [ ] Adicionar modo `--headless`
- [ ] Implementar modo `--dry-run` (simulação)
- [ ] Exportar logs estruturados (JSON/NDJSON)
- [ ] Trocar XPaths frágeis por seletores mais estáveis
- [ ] Transformar em pacote instalável (`pip install -e .`)
- [ ] Criar `.env.example` e CSVs de exemplo

---

## 👤 Autor

**Igor Muniz da Silva**  
2026

---

## 📜 Licença

Este projeto é distribuído sob licença **MIT**. Consulte o arquivo [LICENSE](LICENSE).
