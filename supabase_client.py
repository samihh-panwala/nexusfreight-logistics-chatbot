from supabase import create_client

SUPABASE_URL = "https://rcntxqpkaiferaclskzl.supabase.co"
SUPABASE_KEY = "sb_publishable_D_TrvkQnj3Rw88eOQ0MJgA_Omcw-3Aa"

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)