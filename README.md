# WhatsApp + Supabase (Python)

Integração simples que:
1. Busca contatos no banco de dados **Supabase**.
2. Personaliza a mensagem usando `{{nome_contato}}`.
3. Envia via **Z-API** para até 3 contatos.

---

## 📌 Requisitos
- Python **3.11+**
- Conta no [Supabase](https://supabase.com)
- Conta e instância no [Z-API](https://z-api.io) (plano gratuito)
- Ambiente virtual Python configurado

---

## Orientação

Na ***pasta do projeto*** copie o .env.example para .env substituindo as variáveis com seus dados.

O projeto foi testado em ambiente virtual, segue o passo a passo:

**Criar** o ambiente virtual: python -m venv .venv

**Windows (PowerShell)**

Ativar amviente virtual no Windows: .venv\Scripts\Activate.ps1

**Linux/Mac**

Ativar ambiente virtual Linux/Mac: source .venv/bin/activate

Dentro da pasta whatsapp-supabase instale as dependências:

pip install -r requirements.txt

Execute o código:
python src/main.py

**Dúvidas ou Dicas** alexanderborgeshsu@gmail.com

## Fluxo

Busca até 3 contatos da tabela contacts no Supabase.
Substitui {{nome_contato}} na mensagem pelo nome salvo no banco.
Envia a mensagem via Z-API.
Mostra no terminal o status de cada envio.

#Observações

Necessário que a instância Z-API esteja Online/Conectada (QR code lido recentemente).
Mensagens só serão entregues se o número existir no WhatsApp.
Projeto desenvolvido com boas práticas:
.env para variáveis sensíveis
Logs de execução
Retries com tenacity para chamadas externas

## 🗄️ Configuração da Tabela no Supabase

No **SQL Editor** do Supabase, execute:

```sql
create table if not exists contacts (
  id bigserial primary key,
  nome text not null,
  phone_e164 text unique not null
);

-- Inserir alguns contatos (substitua pelos seus números no formato E.164)
insert into contacts (nome, phone_e164) values
('Gustavo', '5511999999999'),
('Eduardo', '5511988888888'),
('Henrique', '5511977777777')
on conflict (phone_e164) do nothing;

---

