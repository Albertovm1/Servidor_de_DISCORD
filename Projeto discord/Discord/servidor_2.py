from constantes import *
from palavroes import *
from funcoes_bot import *
from permissoes_bot import *
from comandos import *

async def autenticacao():
    email = "example@example.com"
    if validar_email(email):
        codigo = gerar_codigo_autenticacao()
        await enviar_codigo_autenticacao(email, codigo)
    
@bot.event
async def on_ready():
    await funcao_on_ready(bot)

@bot.event
async def on_member_update(before, after):
    await update(before, after)

@bot.event
async def on_member_join(member):
    await join(member)

@bot.event
async def on_message(message):
    await on_message_p(message)

@bot.command()
async def pedir_sala(ctx, categoria, tipo, tempo_vida: int):
    await pedir_sala_comnd(ctx, categoria, tipo, tempo_vida)

bot.run("TOKEN")