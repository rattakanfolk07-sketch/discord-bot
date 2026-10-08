import os
import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

class RoleButton(discord.ui.View):
    def __init__(self, role: discord.Role, button_text: str):
        super().__init__(timeout=None)
        self.role = role
        
        button = discord.ui.Button(
            label=button_text,
            style=discord.ButtonStyle.primary,
            custom_id=f"button_role_{role.id}"
        )
        button.callback = self.button_callback
        self.add_item(button)

    async def button_callback(self, interaction: discord.Interaction):
        user = interaction.user
        if self.role in user.roles:
            await user.remove_roles(self.role)
            await interaction.response.send_message(f"ถอดยศ {self.role.mention} เรียบร้อยแล้วครับ!", ephemeral=True)
        else:
            await user.add_roles(self.role)
            await interaction.response.send_message(f"รับยศ {self.role.mention} เรียบร้อยแล้วครับ!", ephemeral=True)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Error syncing commands: {e}")

@bot.tree.command(name="setup_role", description="สร้าง Embed พร้อมปุ่มกดรับยศ")
@app_commands.describe(
    role="ยศที่ต้องการแจก",
    title="หัวข้อของ Embed",
    description="รายละเอียดข้อความ",
    button_text="ข้อความบนปุ่มกด",
    gif_url="ลิงก์รูป GIF หรือรูปภาพ (ใส่หรือไม่ใส่ก็ได้)"
)
async def setup_role(
    interaction: discord.Interaction,
    role: discord.Role,
    title: str,
    description: str,
    button_text: str,
    gif_url: str = None
):
    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Color.blue()
    )
    if gif_url:
        embed.set_image(url=gif_url)

    view = RoleButton(role=role, button_text=button_text)
    await interaction.channel.send(embed=embed, view=view)
    await interaction.response.send_message("สร้างระบบรับยศเรียบร้อยแล้วครับ!", ephemeral=True)

TOKEN = os.environ.get('DISCORD_TOKEN')

if __name__ == "__main__":
    bot.run(TOKEN)