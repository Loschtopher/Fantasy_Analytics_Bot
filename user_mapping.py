"""
User-to-Team Mapping System
Maps Telegram users to their ESPN Fantasy Football teams
"""
import json
import os
from typing import Dict, Optional, List

USER_MAPPING_FILE = "user_team_mapping.json"


class UserMapping:
    """Manages mapping between Telegram users and ESPN teams"""
    
    def __init__(self):
        self.mappings = self._load_mappings()
        self.detected_users = self._load_detected_users()
    
    def _load_mappings(self) -> Dict:
        """Load user-to-team mappings from file"""
        if os.path.exists(USER_MAPPING_FILE):
            try:
                with open(USER_MAPPING_FILE, 'r') as f:
                    data = json.load(f)
                    return data.get('mappings', {})
            except:
                return {}
        return {}
    
    def _load_detected_users(self) -> Dict:
        """Load detected users from file"""
        if os.path.exists(USER_MAPPING_FILE):
            try:
                with open(USER_MAPPING_FILE, 'r') as f:
                    data = json.load(f)
                    return data.get('detected_users', {})
            except:
                return {}
        return {}
    
    def _save(self):
        """Save mappings and detected users to file"""
        data = {
            'mappings': self.mappings,
            'detected_users': self.detected_users
        }
        with open(USER_MAPPING_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    
    def detect_user(self, user_id: int, username: str, first_name: str, last_name: str = ""):
        """Auto-detect and store user info when they interact with the bot"""
        user_key = str(user_id)
        
        self.detected_users[user_key] = {
            'user_id': user_id,
            'username': username if username else None,
            'first_name': first_name,
            'last_name': last_name,
            'display_name': self._get_display_name(username, first_name, last_name)
        }
        self._save()
    
    def _get_display_name(self, username: str, first_name: str, last_name: str) -> str:
        """Get best display name for user"""
        if username:
            return f"@{username}"
        elif first_name and last_name:
            return f"{first_name} {last_name}"
        elif first_name:
            return first_name
        else:
            return "Unknown User"
    
    def link_user_to_team(self, user_id: int, team_id: int, team_name: str):
        """Link a Telegram user to their ESPN team"""
        self.mappings[str(user_id)] = {
            'team_id': team_id,
            'team_name': team_name
        }
        self._save()
    
    def unlink_user(self, user_id: int):
        """Remove user-team mapping"""
        user_key = str(user_id)
        if user_key in self.mappings:
            del self.mappings[user_key]
            self._save()
    
    def get_team_for_user(self, user_id: int) -> Optional[Dict]:
        """Get team info for a Telegram user"""
        return self.mappings.get(str(user_id))
    
    def get_user_for_team(self, team_id: int) -> Optional[Dict]:
        """Get Telegram user for an ESPN team"""
        for user_id, mapping in self.mappings.items():
            if mapping['team_id'] == team_id:
                user_info = self.detected_users.get(user_id, {})
                return {
                    'user_id': int(user_id),
                    'display_name': user_info.get('display_name', 'Unknown'),
                    'username': user_info.get('username')
                }
        return None
    
    def get_all_detected_users(self) -> List[Dict]:
        """Get all detected users (for admin to set up mappings)"""
        users = []
        for user_id, info in self.detected_users.items():
            mapping = self.mappings.get(user_id)
            users.append({
                **info,
                'is_linked': mapping is not None,
                'linked_team': mapping.get('team_name') if mapping else None
            })
        return users
    
    def get_all_mappings(self) -> Dict:
        """Get all current user-team mappings"""
        result = {}
        for user_id, mapping in self.mappings.items():
            user_info = self.detected_users.get(user_id, {})
            result[user_id] = {
                **mapping,
                'display_name': user_info.get('display_name', 'Unknown')
            }
        return result







