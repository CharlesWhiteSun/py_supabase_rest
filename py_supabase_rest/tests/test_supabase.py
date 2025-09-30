from py_supabase_rest.app.config import supabase

def test_connection():
    try:
        data = supabase.table("plc_device").select("*").limit(3).execute()
        print("✅ Supabase 連線成功，資料：", data)
    except Exception as e:
        print("❌ Supabase 連線失敗：", e)

if __name__ == "__main__":
    test_connection()
