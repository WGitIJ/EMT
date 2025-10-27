import os
from typing import List

class DatabaseService:
    def __init__(self):
        supabase_url = os.getenv('VITE_SUPABASE_URL')
        supabase_key = os.getenv('VITE_SUPABASE_ANON_KEY')

        if not supabase_url or not supabase_key:
            raise ValueError("Supabase credentials not found in environment variables")


    def save_recent_stop(self, stop_number: int):
        try:
            existing = self.client.table('recent_stops').select('id').eq('stop_number', stop_number).maybeSingle().execute()

            if existing.data:
                self.client.table('recent_stops').update({
                    'last_accessed': 'now()'
                }).eq('stop_number', stop_number).execute()
            else:
                self.client.table('recent_stops').insert({
                    'stop_number': stop_number
                }).execute()
        except Exception as e:
            print(f"Error saving recent stop: {e}")

    def get_recent_stops(self, limit: int = 10) -> List[int]:
        try:
            response = self.client.table('recent_stops').select('stop_number').order('last_accessed', desc=True).limit(limit).execute()

            return [item['stop_number'] for item in response.data]
        except Exception as e:
            print(f"Error fetching recent stops: {e}")
            return []
