from typing import List, Dict, Any
from pathlib import Path
import json
import pandas as pd

class APIIntegrations:
    def __init__(self):
        """Initialize API integrations with data paths"""
        self.data_path = Path(__file__).parent.parent / "data"
        
    def fetch_job_listings(self, filters: dict = None) -> List[Dict[str, Any]]:
        """Fetch job listings from data file"""
        try:
            jobs_path = self.data_path / "job_listing_data.csv"
            if not jobs_path.exists():
                print(f"Warning: Job listings file not found at {jobs_path}")
                return []
            
            df = pd.read_csv(jobs_path)
            data = df.to_dict('records')
            return self._apply_filters(data, filters) if filters else data
        except Exception as e:
            print(f"Error loading job listings: {e}")
            return []

    def fetch_events(self) -> List[Dict[str, Any]]:
        """Fetch events from data file"""
        try:
            events_path = self.data_path / "session_details.json"
            if not events_path.exists():
                print(f"Warning: Events file not found at {events_path}")
                return []
                
            with open(events_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading events: {e}")
            return []

    def fetch_mentorship_programs(self, filters: dict = None) -> List[Dict[str, Any]]:
        """Fetch mentorship programs from data file"""
        try:
            mentorship_path = self.data_path / "mentorship_programs.json"
            if not mentorship_path.exists():
                print(f"Warning: Mentorship programs file not found at {mentorship_path}")
                return []
                
            with open(mentorship_path, 'r') as f:
                data = json.load(f)
            return self._apply_filters(data, filters) if filters else data
        except Exception as e:
            print(f"Error loading mentorship programs: {e}")
            return []

    def _apply_filters(self, data: List[Dict[str, Any]], filters: dict) -> List[Dict[str, Any]]:
        """Apply filters to the data"""
        if not filters:
            return data
            
        filtered_data = data.copy()
        for key, value in filters.items():
            filtered_data = [
                item for item in filtered_data 
                if str(item.get(key, '')).lower() == str(value).lower()
            ]
        return filtered_data