import discord
import random, os, requests, asyncio
from discord.ext import commands
from model.model import classify_food
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)
@bot.command()
async def hitungKal(ctx):
    await ctx.send("Hitung kalori makananmu! Kirimkan nama makan")
    
@bot.command()
async def checkAI(ctx):
    if ctx.message.attachments:
        try: 
            for file in ctx.message.attachments:
                namaFile = file.filename
                urlFile = file.url
                if not os.path.exists('images'):
                    os.makedirs('images')
                file_path = f'images/{namaFile}'
                await file.save(file_path)
                await ctx.send(f'Berhasil menyimpan gambar dengan nama {namaFile}')
                hasil  = classify_food(file_path, 'D:\coding\Bot Ai 1323\model\module\keras_model.h5', 'D:\coding\Bot Ai 1323\model\module\labels.txt')
                if hasil[0] == "Makanan cepat saji" and hasil[1] >= 0.7:
                    await ctx.send("ini adalah makanan cepat saji")
                    await ctx.send(f'skor klasifikasinya adalah {int(hasil[1]*100)}%')
                    await ctx.send("makanan cepat saji tidak baik jika dimakan terlalu sering,\n karena mengandung lemak jenuh")
                elif hasil[0] == "Masakan rumahan" and hasil[1] >= 0.7:
                    await ctx.send("ini adalah Masakan rumahan")
                    await ctx.send(f'skor klasifikasinya adalah {int(hasil[1]*100)}%')
                    await ctx.send("makanan rumahan adalah, makanan yang bertujuan untuk menimbulkan rasa hangat dan nyaman, yang menimbulkan nostalgia atau nilai tersendiri bagi seseorang.")
                else:
                    await ctx.send("bukan termasuk makanan rumahan atau makanan cepat saji")

                try:
                    await ctx.send("Apakah jawaban tersebut benar?")
                    response = await bot.wait_for('message', timeout=30)  # Menunggu respons dari pengguna selama 30 detik
                    if response.content.lower() == 'ya':
                        await ctx.send("Terima kasih!")
                    elif response.content.lower() == 'tidak':
                        await ctx.send("Baik, saya akan mencoba lebih baik lain kali.")
                    else:
                        await ctx.send("maaf pesan tersebut tidak dapat saya mengerti")
                except asyncio.TimeoutError:
                    await ctx.send("Waktu habis, silakan coba lagi.")

        except Exception as e:
            await ctx.send(f"terjadi error{e}")
    else:
        await ctx.send("Tidak ada gambar")



bot.run("Token")