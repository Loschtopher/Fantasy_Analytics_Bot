"""
Simple Interactive Team Picker
Users just click a button to link their team - no manual work!
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from user_mapping import UserMapping
from espn_api import ESPNAPI


class TeamPicker:
    """Interactive team picker with buttons"""
    
    def __init__(self, espn_api: ESPNAPI, user_mapping: UserMapping):
        self.espn_api = espn_api
        self.user_mapping = user_mapping
    
    async def pickteam_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show team picker with buttons"""
        try:
            user = update.effective_user
            
            # Auto-detect user
            self.user_mapping.detect_user(
                user.id,
                user.username,
                user.first_name,
                user.last_name or ""
            )
            
            # Check if already linked
            existing_team = self.user_mapping.get_team_for_user(user.id)
            
            # Get teams
            teams = self.espn_api.get_teams()
            
            if not teams:
                await update.message.reply_text("❌ Error loading teams from ESPN")
                return
            
            # Sort teams by name for easier finding
            teams_sorted = sorted(teams, key=lambda t: t.get('name', ''))
            
            # Create keyboard with team buttons (2 columns)
            keyboard = []
            row = []
            
            for team in teams_sorted:
                team_id = team.get('id')
                team_name = team.get('name', 'Unknown Team').strip()
                abbrev = team.get('abbrev', 'UNK')
                record = team.get('record', {}).get('overall', {})
                wins = record.get('wins', 0)
                losses = record.get('losses', 0)
                
                # Button text: Team Name (W-L)
                button_text = f"{team_name} ({wins}-{losses})"
                
                # Callback data: team_id
                callback_data = f"pickteam_{team_id}_{team_name}"
                
                row.append(InlineKeyboardButton(button_text, callback_data=callback_data[:64]))
                
                # Add row when we have 2 buttons or it's the last item
                if len(row) == 1 or team == teams_sorted[-1]:
                    keyboard.append(row)
                    row = []
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            message = "🏈 **Pick Your Team!**\n\n"
            
            if existing_team:
                message += f"You're currently: **{existing_team['team_name']}**\n\n"
                message += "Click a team below to change:\n"
            else:
                message += "Click your team below:\n"
            
            await update.message.reply_text(
                message,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def handle_team_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle team button click"""
        try:
            query = update.callback_query
            await query.answer()
            
            user = update.effective_user
            
            # Auto-detect user
            self.user_mapping.detect_user(
                user.id,
                user.username,
                user.first_name,
                user.last_name or ""
            )
            
            # Parse callback data
            parts = query.data.split('_')
            if len(parts) < 3:
                await query.edit_message_text("❌ Error processing selection")
                return
            
            team_id = int(parts[1])
            team_name = '_'.join(parts[2:])  # Rejoin in case name has underscores
            
            # Link user to team
            self.user_mapping.link_user_to_team(user.id, team_id, team_name)
            
            # Success message
            message = "✅ **Team Linked!**\n\n"
            message += f"🏈 **{team_name}**\n\n"
            message += "You're all set! Try these commands:\n"
            message += "• `/myteam` - See your stats\n"
            message += "• `/power` - See rankings (your team will be highlighted)\n"
            message += "• `/help` - See all commands"
            
            await query.edit_message_text(message, parse_mode='Markdown')
            
        except Exception as e:
            try:
                await query.edit_message_text(f"❌ Error: {str(e)}")
            except:
                pass
    
    def get_callback_handler(self):
        """Get the callback query handler for team selection"""
        return CallbackQueryHandler(self.handle_team_selection, pattern="^pickteam_")







