from typing import List, TypedDict
from supabase import create_client, Client
import os

class Contact(TypedDict):
    id: int
    nome: str
    phone_e164: str

def get_supabase_client() -> Client:
    url = os.environ["SUPABASE_URL"]
    key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]  
    return create_client(url, key)

def fetch_contacts(limit: int = 3) -> List[Contact]:
    supa = get_supabase_client()
    res = supa.table("contacts").select("id,nome,phone_e164").limit(limit).execute()
    return res.data or []
