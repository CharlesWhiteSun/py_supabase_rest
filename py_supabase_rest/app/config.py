import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()  # 載入 .env

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL 或 SUPABASE_KEY 未設定，請檢查 .env 檔案")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
