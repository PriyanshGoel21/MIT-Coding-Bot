import discord


async def handle_role(interaction: discord.Interaction, role_id: int):
    role: discord.Role = interaction.guild.get_role(role_id)
    if role in interaction.user.roles:
        await interaction.user.remove_roles(role)
        await interaction.response.send_message(
            f"{role.mention} role removed.", ephemeral=True
        )
    else:
        await interaction.user.add_roles(role)
        await interaction.response.send_message(
            f"{role.mention} role added.", ephemeral=True
        )


class CompetitiveCoding(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Competitive Coding",
        style=discord.ButtonStyle.grey,
        custom_id="competitive_coding",
        emoji=discord.PartialEmoji.from_str("<:thinkcpp:1009845268168052869>"),
    )
    async def cp(self, interaction: discord.Interaction, button: discord.ui.Button):
        await handle_role(interaction, 1020327962865844385)


class LanguageRoles(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Python",
        style=discord.ButtonStyle.grey,
        custom_id="python",
        emoji=discord.PartialEmoji.from_str("<:py:1009845257162203146>"),
    )
    async def python(self, interaction: discord.Interaction, button: discord.ui.Button):
        await handle_role(interaction, 1020330177965862932)

    @discord.ui.button(
        label="Java",
        style=discord.ButtonStyle.grey,
        custom_id="java",
        emoji=discord.PartialEmoji.from_str("<:java:1009845262350565426>"),
    )
    async def java(self, interaction: discord.Interaction, button: discord.ui.Button):
        await handle_role(interaction, 1020330526311202926)

    @discord.ui.button(
        label="JavaScript",
        style=discord.ButtonStyle.grey,
        custom_id="javascript",
        emoji=discord.PartialEmoji.from_str("<:js:1009845270697230426>"),
    )
    async def javascript(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await handle_role(interaction, 1020330326976888942)

    @discord.ui.button(
        label="C",
        style=discord.ButtonStyle.grey,
        custom_id="clang",
        emoji=discord.PartialEmoji.from_str("<:c_:1019264465767760023>"),
    )
    async def clang(self, interaction: discord.Interaction, button: discord.ui.Button):
        await handle_role(interaction, 1020330285096767578)

    @discord.ui.button(
        label="C++",
        style=discord.ButtonStyle.grey,
        custom_id="cpp",
        emoji=discord.PartialEmoji.from_str("<:cpp:1019264346406264952>"),
    )
    async def cpp(self, interaction: discord.Interaction, button: discord.ui.Button):
        await handle_role(interaction, 1020330226632376360)

    @discord.ui.button(
        label="Functional Languages",
        style=discord.ButtonStyle.grey,
        custom_id="fp_langs",
    )
    async def cpp(self, interaction: discord.Interaction, button: discord.ui.Button):
        await handle_role(interaction, 1020330397395066931)

    @discord.ui.button(
        label="Other Languages",
        style=discord.ButtonStyle.grey,
        custom_id="other",
    )
    async def cpp(self, interaction: discord.Interaction, button: discord.ui.Button):
        await handle_role(interaction, 1020330440386674699)
