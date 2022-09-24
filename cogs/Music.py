import discord
from discord import app_commands
from discord.ext import commands
from discord import FFmpegAudio
import asyncio
import os
import random

def align_en_ch(str_in,str_en_width):
    lst = []
    for i in range(33,127):
        lst.append(chr(i))
    no_chr_count = 0

    str_test = str_in
    for i in str_test:
        if i not in lst:
            no_chr_count += 1

    return ('{0:<{width}}'.format(str_test,width = str_en_width-no_chr_count))

class Music(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot
        self.all_music_list = []
        self.play_music_list = []

    @commands.Cog.listener()
    async def on_ready(self): 
        print('Music cog loaded.')

    @commands.command()
    async def sync(self,ctx) -> None:
        fmt = await ctx.bot.tree.sync(guild = ctx.guild)
        await ctx.send(f'synced {len(fmt)} commands.')

    # @app_commands.command(name='questions',description='questions form')
    # async def questions(self,interaction:discord.Interaction,question:str):
    #     await interaction.channel.send('answered')

    @app_commands.command(name='join',description='加入你所在的voice_channel')
    async def join(self,interaction:discord.Interaction):
        if interaction.user.voice.channel:
            await interaction.user.voice.channel.connect()
            await interaction.channel.send('我已加入你所在的voice_channel')
        else:
            await interaction.channel.send('你必須先進入voice_channel,否則我無法加入')
    
    @app_commands.command(name='leave',description='離開你所在的voice_channel')
    async def leave(self,interaction:discord.Interaction):
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.disconnect()
            await interaction.channel.send('我已離開voice_channel')
        else:
            await interaction.channel.send('我根本沒加入任何voice_channel')
    
    @app_commands.command(name='show_all_music_list',description='陳列 所有曲目')
    async def show_all_music_list(self,interaction:discord.Interaction):
        files = os.listdir(path="./download")
        self.all_music_list = [str(x) for x in files if "mp3" in x]
        str_list = ""
        for i in range(len(self.all_music_list)):
            if i%2 == 1:
                str_list += (align_en_ch(str(i+1) +"."+self.all_music_list[i],50)+"\n")
            else :
                str_list += align_en_ch(str(i+1) +"."+self.all_music_list[i],50)
        str_show = f"```{str_list}```"
        await interaction.channel.send(str_show)
    
    @app_commands.command(name='set_play_music_list_as_all',description='設定 播放清單 如同 所有的曲目')
    async def set_play_music_list_as_all(self,interaction:discord.Interaction):
        files = os.listdir(path="./download")
        self.play_music_list = [str(x) for x in files if "mp3" in x]
        str_list = ""
        for i in range(len(self.play_music_list)):
            if i%2 == 1:
                str_list += (align_en_ch(str(i+1) +"."+self.play_music_list[i],50)+"\n")
            else :
                str_list += align_en_ch(str(i+1) +"."+self.play_music_list[i],50)
        str_show = f"```{str_list}```"
        await interaction.channel.send(f'set_play_music_list_as_all complete \n{str_show}\n共{len(self.play_music_list)}首')

    @app_commands.command(name='show_play_music_list',description='陳列 播放清單')
    async def show_play_music_list(self,interaction:discord.Interaction):
        str_list = ""
        for i in range(len(self.play_music_list)):
            if i%2 == 1:
                str_list += (align_en_ch(str(i+1) +"."+self.play_music_list[i],50)+"\n")
            else :
                str_list += align_en_ch(str(i+1) +"."+self.play_music_list[i],50)
        str_show = f"```{str_list}```"
        await interaction.channel.send(f'show_play_music_list \n{str_show}\n共{len(self.play_music_list)}首')
    
    @app_commands.command(name='set_play_music_list',description='設定 播放清單(用,分格曲目 不加任何引號及空格)')
    async def set_play_music_list(self,interaction:discord.Interaction,play_list:str):
        self.play_music_list = list(play_list.split(","))
        str_list = ""
        for i in range(len(self.play_music_list)):
            if i%2 == 1:
                str_list += (align_en_ch(str(i+1) +"."+self.play_music_list[i],50)+"\n")
            else :
                str_list += align_en_ch(str(i+1) +"."+self.play_music_list[i],50)
        str_show = f"```{str_list}```"
        await interaction.channel.send(f'set_play_music_list complete \n{str_show}\n共{len(self.play_music_list)}首')
    
    @app_commands.command(name='random_play_music_list',description='亂序 播放清單')
    async def random_play_music_list(self,interaction:discord.Interaction):
        random.shuffle(self.play_music_list)
        str_list = ""
        for i in range(len(self.play_music_list)):
            if i%2 == 1:
                str_list += (align_en_ch(str(i+1) +"."+self.play_music_list[i],50)+"\n")
            else :
                str_list += align_en_ch(str(i+1) +"."+self.play_music_list[i],50)
        str_show = f"```{str_list}```"
        await interaction.channel.send(f'random_play_music_list complete \n{str_show}\n共{len(self.play_music_list)}首')
    
    @app_commands.command(name='play_music',description='播放音樂(必須先下 join 指令使 bot 加入你所在的 voice_channel)')
    async def play_music(self,interaction:discord.Interaction):
        if interaction.user.voice.channel != None:
            for i in range(len(self.play_music_list)):
                interaction.guild.voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=f"./download/{self.play_music_list[i]}"))
                await interaction.channel.send(f"playing {i+1}.{self.play_music_list[i]}")
                while 1 :
                    if interaction.guild.voice_client.is_playing():
                        await asyncio.sleep(1)
                        continue
                    elif interaction.guild.voice_client.is_paused() == True:
                        await asyncio.sleep(1)
                        continue
                    else :
                        break
            await interaction.channel.send("我放完了啦")
        else:
            await interaction.channel.send('我不在語音頻道啦!')
    
    @app_commands.command(name='pause_music',description='暫停 音樂')
    async def pause_music(self,interaction:discord.Interaction):
        if interaction.guild.voice_client.is_paused() != True:
            interaction.guild.voice_client.pause()
            await interaction.channel.send("> **The video player is now paused**")
        else:
            if interaction.guild.voice_client.is_playing() == True:
                await interaction.channel.send("> **The video player is already paused.**")
            else:
                await interaction.channel.send("> **There is no song currently playing.**")

    @app_commands.command(name='resume_music',description='恢復 音樂')
    async def resume_music(self,interaction:discord.Interaction):
        if interaction.guild.voice_client.is_paused() == True:
            interaction.guild.voice_client.resume()
            await interaction.channel.send('> **Now resuming:**')
        else:
            await interaction.channel.send('> **The video player is not paused**')

    @app_commands.command(name='next_music',description='快進到下一首曲目')
    async def next_music(self,interaction:discord.Interaction):
        if interaction.guild.voice_client.is_playing:
            interaction.guild.voice_client.stop()
            await interaction.channel.send('> **Next**')
        else:
            pass
    
    @app_commands.command(name='all_in_one',description='亂序所有曲目->加入->播放')
    async def all_in_one(self,interaction:discord.Interaction):
        files = os.listdir(path="./download")
        self.play_music_list = [str(x) for x in files if "mp3" in x]
        random.shuffle(self.play_music_list)
        str_list = ""   
        for i in range(len(self.play_music_list)):
            if i%2 == 1:
                str_list += (align_en_ch(str(i+1) +"."+self.play_music_list[i],50)+"\n")
            else :
                str_list += align_en_ch(str(i+1) +"."+self.play_music_list[i],50)
        str_show = f"```{str_list}```"
        await interaction.channel.send(f'set_play_music_list complete \n {str_show} \n共{len(self.play_music_list)}首')
        if interaction.user.voice.channel:
            await interaction.user.voice.channel.connect()
            for i in range(len(self.play_music_list)):
                interaction.guild.voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=f"./download/{self.play_music_list[i]}"))
                await interaction.channel.send(f"playing {i+1}.{self.play_music_list[i]}")
                while 1 :
                    if interaction.guild.voice_client.is_playing():
                        await asyncio.sleep(1)
                        continue
                    elif interaction.guild.voice_client.is_paused() == True:
                        await asyncio.sleep(1)
                        continue
                    else :
                        break
            await interaction.channel.send("我放完了啦")
        else:
            await interaction.channel.send('你必須先進入voice_channel,否則我無法加入')
    # @app_commands.command(name='count',description='count')
    # async def count(self,interaction:discord.Interaction):
    #     await interaction.channel.send(str(len(self.play_music_list)))


async def setup(bot):
    await bot.add_cog(Music(bot),guilds = [discord.Object(id=977465748467351574),discord.Object(id=968697961741705246),discord.Object(id=707562413901348984)])
    