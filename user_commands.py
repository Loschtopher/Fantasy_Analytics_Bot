"""
User-related commands for team linking
"""
from telegram import Update
from telegram.ext import ContextTypes
from user_mapping import UserMapping
from espn_api import ESPNAPI


class UserCommands:
    """Commands for linking users to teams"""
    
    def __init__(self, espn_api: ESPNAPI, user_mapping: UserMapping):
        self.espn_api = espn_api
        self.user_mapping = user_mapping
    
    async def whoami_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show user their Telegram info and linked team"""
        try:
            user = update.effective_user
            
            # Auto-detect user
            self.user_mapping.detect_user(
                user.id,
                user.username,
                user.first_name,
                user.last_name or ""
            )
            
            # Check if linked to team
            team_info = self.user_mapping.get_team_for_user(user.id)
            
            message = f"👤 **Your Info**\n\n"
            message += f"Name: {user.first_name}"
            if user.last_name:
                message += f" {user.last_name}"
            message += "\n"
            
            if user.username:
                message += f"Username: @{user.username}\n"
            message += f"User ID: `{user.id}`\n\n"
            
            if team_info:
                message += f"⭐ **Linked Team:**\n"
                message += f"{team_info['team_name']}\n\n"
                message += "Use /myteam to see your stats!"
            else:
                message += "❌ **Not linked to a team**\n\n"
                message += "Ask an admin to link you using:\n"
                message += f"`/linkuser {user.id} <team_number>`"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")
    
    async def users_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show all detected users and their team links (admin only)"""
        try:
            # Auto-detect this user too
            user = update.effective_user
            self.user_mapping.detect_user(
                user.id,
                user.username,
                user.first_name,
                user.last_name or ""
            )
            
            detected_users = self.user_mapping.get_all_detected_users()
            
            if not detected_users:
                await update.message.reply_text(
                    "No users detected yet. Users will appear here when they use any command."
                )
                return
            
            message = "👥 **Detected Users**\n\n"
            
            for user in detected_users:
                display = user.get('display_name', 'Unknown')
                user_id = user.get('user_id')
                
                if user['is_linked']:
                    message += f"✅ {display}\n"
                    message += f"   Team: {user['linked_team']}\n"
                    message += f"   ID: `{user_id}`\n\n"
                else:
                    message += f"❌ {display}\n"
                    message += f"   Not linked\n"
                    message += f"   ID: `{user_id}`\n\n"
            
            message += "\n**Link a user:**\n"
            message += "`/linkuser <user_id> <team_number>`\n\n"
            message += "**Team numbers:**\n"
            message += "Use `/teams` to see team list"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")
    
    async def teams_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show all teams with their IDs for linking"""
        try:
            teams = self.espn_api.get_teams()
            
            if not teams:
                await update.message.reply_text("Error loading teams from ESPN")
                return
            
            message = "🏈 **All Teams**\n\n"
            
            for idx, team in enumerate(teams, 1):
                team_id = team.get('id')
                team_name = team.get('name', 'Unknown Team').strip()
                
                # Check if someone is linked to this team
                linked_user = self.user_mapping.get_user_for_team(team_id)
                
                message += f"{idx}. **{team_name}**\n"
                message += f"   Team ID: `{team_id}`\n"
                
                if linked_user:
                    message += f"   👤 Linked: {linked_user['display_name']}\n"
                
                message += "\n"
            
            message += "**To link a user to a team:**\n"
            message += "`/linkuser <user_id> <team_number>`\n\n"
            message += "Get user IDs with `/users`"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")
    
    async def linkuser_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Link a user to a team (admin command)"""
        try:
            if not context.args or len(context.args) < 2:
                await update.message.reply_text(
                    "Usage: `/linkuser <user_id> <team_number>`\n\n"
                    "Example: `/linkuser 123456789 1`\n\n"
                    "Use `/users` to see user IDs\n"
                    "Use `/teams` to see team numbers",
                    parse_mode='Markdown'
                )
                return
            
            user_id = int(context.args[0])
            team_number = int(context.args[1])
            
            # Get teams
            teams = self.espn_api.get_teams()
            
            if team_number < 1 or team_number > len(teams):
                await update.message.reply_text(
                    f"Invalid team number. Choose 1-{len(teams)}\n"
                    "Use `/teams` to see the list",
                    parse_mode='Markdown'
                )
                return
            
            # Get the team
            team = teams[team_number - 1]
            team_id = team.get('id')
            team_name = team.get('name', 'Unknown Team').strip()
            
            # Link user to team
            self.user_mapping.link_user_to_team(user_id, team_id, team_name)
            
            # Get user display name
            user_info = self.user_mapping.detected_users.get(str(user_id), {})
            display_name = user_info.get('display_name', f'User {user_id}')
            
            message = f"✅ **Linked!**\n\n"
            message += f"👤 {display_name}\n"
            message += f"🏈 {team_name}\n\n"
            message += "They can now use `/myteam` to see their stats!"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except ValueError:
            await update.message.reply_text("Invalid format. Use numbers only.")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")
    
    async def myteam_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show user their team stats"""
        try:
            user_id = update.effective_user.id
            
            # Auto-detect user
            user = update.effective_user
            self.user_mapping.detect_user(
                user.id,
                user.username,
                user.first_name,
                user.last_name or ""
            )
            
            # Check if linked
            team_info = self.user_mapping.get_team_for_user(user_id)
            
            if not team_info:
                await update.message.reply_text(
                    "❌ You're not linked to a team yet!\n\n"
                    "Ask an admin to link you using `/linkuser`\n"
                    "Or use `/whoami` to see your user ID",
                    parse_mode='Markdown'
                )
                return
            
            # Get team stats from ESPN
            team_id = team_info['team_id']
            team_stats = self.espn_api.get_team_stats(team_id)
            
            if not team_stats:
                await update.message.reply_text("Error loading team data from ESPN")
                return
            
            # Build stats message
            team_name = team_stats.get('name', 'Unknown Team').strip()
            
            record = team_stats.get('record', {}).get('overall', {})
            wins = record.get('wins', 0)
            losses = record.get('losses', 0)
            ties = record.get('ties', 0)
            
            points_for = record.get('pointsFor', 0)
            points_against = record.get('pointsAgainst', 0)
            
            message = f"⭐ **YOUR TEAM** ⭐\n\n"
            message += f"🏈 **{team_name}**\n\n"
            message += f"📊 **Record:** {wins}-{losses}"
            if ties > 0:
                message += f"-{ties}"
            message += f"\n"
            
            win_pct = (wins + 0.5 * ties) / max(1, wins + losses + ties)
            message += f"📈 **Win %:** {win_pct:.1%}\n\n"
            
            message += f"⚡ **Points For:** {points_for:.1f}\n"
            message += f"🛡️ **Points Against:** {points_against:.1f}\n"
            
            if points_for > 0:
                message += f"📊 **Avg PPG:** {points_for / max(1, wins + losses + ties):.1f}\n"
            
            message += f"\n💡 Use `/power` to see where you rank!"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")
    
    async def unlink_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Unlink a user from their team (admin command)"""
        try:
            if not context.args or len(context.args) < 1:
                await update.message.reply_text(
                    "Usage: `/unlink <user_id>`\n\n"
                    "Use `/users` to see linked users",
                    parse_mode='Markdown'
                )
                return
            
            user_id = int(context.args[0])
            
            # Get user info before unlinking
            team_info = self.user_mapping.get_team_for_user(user_id)
            user_info = self.user_mapping.detected_users.get(str(user_id), {})
            display_name = user_info.get('display_name', f'User {user_id}')
            
            # Unlink
            self.user_mapping.unlink_user(user_id)
            
            if team_info:
                message = f"✅ **Unlinked!**\n\n"
                message += f"👤 {display_name}\n"
                message += f"was unlinked from {team_info['team_name']}"
            else:
                message = f"User {display_name} was not linked to any team"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except ValueError:
            await update.message.reply_text("Invalid user ID. Use numbers only.")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

