import discord
import random
import asyncio
from palavroes import *
from constantes import *
from permissoes_bot import *

salas_em_andamento = {}

async def pedir_sala_comnd(ctx, categoria, tipo, tempo_vida: int):
    guild = ctx.guild
    categorias = ['monitoria', 'salas']
    tipos = ['chat', 'voice']

    if categoria.lower() not in categorias:
        await ctx.send("Categoria inválida. As categorias disponíveis são 'Monitoria' e 'Salas'.")
        return

    if tipo.lower() not in tipos:
        await ctx.send("Tipo inválido. Os tipos disponíveis são 'Chat' e 'Voice'.")
        return

    categoria_obj = discord.utils.get(guild.categories, name=categoria)
    if not categoria_obj:
        await ctx.send(f"A categoria '{categoria}' não foi encontrada. Verifique as letras Maiúscula e Minúscula")
        return
    sala_nome = f'{tipo}-{ctx.author.name}-{random.randint(1000, 9999)}'
    if tipo.lower() == 'chat':
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.author: discord.PermissionOverwrite(read_messages=True)
        }

        sala = await guild.create_text_channel(name=sala_nome, category=categoria_obj, overwrites=overwrites)
    else:
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(connect=False),
            ctx.author: discord.PermissionOverwrite(connect=True)
        }

        sala = await guild.create_voice_channel(name=sala_nome, category=categoria_obj, overwrites=overwrites)

    salas_em_andamento[sala.id] = {'criador': ctx.author, 'tempo_vida': tempo_vida}
    await ctx.send(f"Sala criada: {sala.mention}. Ela será excluída após {tempo_vida} minutos.")

    await asyncio.sleep(tempo_vida * 60)

    if sala.id in salas_em_andamento:
        await sala.delete()
        del salas_em_andamento[sala.id]