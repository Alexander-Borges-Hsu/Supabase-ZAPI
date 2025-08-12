# WhatsApp + Supabase (Python)

Integração simples: busca contatos no Supabase e envia mensagens personalizadas via Z-API.

## Setup da tabela (Supabase)
```sql
create table if not exists contacts (
  id bigserial primary key,
  nome text not null,
  phone_e164 text unique not null
);
-- opcional: dados de exemplo
insert into contacts (nome, phone_e164) values
('Davi','5511999999999'),
('Maria','5511988888888'),
('João','5511977777777')
on conflict (phone_e164) do nothing;
