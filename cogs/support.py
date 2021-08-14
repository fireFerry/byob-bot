from discord.ext import commands
import discord


class support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def support(self, ctx):
        embed = discord.Embed(title="Support",
                              description="**1.** Ask your question, don't ask to ask.\n**2.** Be patient for support. Don't mention staff, this will result in a punishment.\n**3.** Don't repeat your questions, and don't put them in multiple channels.",
                              color=0x5cffb0)
        await ctx.message.delete()
        await ctx.send(embed=embed)


    # port forwarding command


    @commands.command(aliases=['portforward', 'pfw', ''])
    async def portforwarding(self, ctx):
        embed = discord.Embed(title="Port forwarding",
                              description="Port forwarding is done on your router, and may be called port mapping, or virtual servers too. Port triggering is not the same as port forwarding. \nTo use the web-gui version of byob you need to forward ports 1337-1339 to your machine that you're hosting byob on.",
                              color=0x5cffb0)
        await ctx.message.delete()
        await ctx.send(embed=embed)


    # requirements command


    @commands.command(aliases=['req'])
    async def requirements(self, ctx):
        embed = discord.Embed(title="Requirements", description="requirements for byob:", color=0x5cffb0)
        embed.add_field(name="OS", value="A Linux distribution", inline=False)
        embed.add_field(name="Software", value="**1.** Python 3 & pip\n**2.** Docker", inline=False)
        await ctx.message.delete()
        await ctx.send(embed=embed)


    # wsl command


    @commands.command()
    async def wsl(self, ctx):
        embed = discord.Embed(title="Windows Subsystem for Linux",
                              description="Using wsl for byob isn't supported. This means that you will receive no support if you try to use byob with wsl. Wsl is if you run a linux terminal on Windows, also known as the Ubuntu/Kali from the Microsoft store.",
                              color=0x5cffb0)
        await ctx.message.delete()
        await ctx.send(embed=embed)


    # vps command


    @commands.command()
    async def vps(self, ctx):
        embed = discord.Embed(title="Virtual Private Server",
                              description="Byob is not recommended on a vps. If you are using a vps for byob you may need to do some extra configuration with your vps provider. You also need to be able to open ports if you want to use byob, staff will not help with this.",
                              color=0x5cffb0)
        await ctx.message.delete()
        await ctx.send(embed=embed)


    # executable command


    @commands.command(aliases=['exe'])
    async def executable(self, ctx):
        embed = discord.Embed(title="Executable generation",
                              description="If your executable doesn't generate correctly, here are some things you should check:\n**1.** Make sure you are using the latest version of byob and rebooted at least once.\n**2.** Run this command: sudo usermod -aG docker $USER && sudo chmod 666 /var/run/docker.sock, and reboot your system.\n**3.** If this still doesn't work, uninstall docker, and run startup.sh again, and reboot your system.\n**4.** If you tried all of this and it didn't help, you can try using pyinstaller to compile the python payload manually.",
                              color=0x5cffb0)
        await ctx.message.delete()
        await ctx.send(embed=embed)


    # wiki command


    @commands.command()
    async def wiki(self, ctx):
        embed = discord.Embed(title="Wiki",
                              description="web-gui wiki: https://byob.dev/guide\ncli wiki: https://github.com/malwaredllc/byob/wiki\nGitHub: https://github.com/malwaredllc/byob/",
                              color=0x5cffb0)
        await ctx.message.delete()
        await ctx.send(embed=embed)






def setup(bot):
    bot.add_cog(support(bot))