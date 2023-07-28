import discord
from discord.ext import commands
import pandas as pd
import smtplib
import random
import asyncio
from palavroes import *
from email.mime.text import MIMEText
from constantes import *
from permissoes_bot import *

bot = commands.Bot(command_prefix='!', intents=intents)

salas_em_andamento = {}

alunos_df = pd.read_csv('alunos.csv', delimiter=',', usecols=['E-mail academico', 'Nome'])
alunos_emails = set(alunos_df['E-mail academico'].values)

professores_df = pd.read_csv('professores.csv', delimiter=',', usecols=['E-mail', 'Nome'])
professores_emails = set(professores_df['E-mail'].values)

def validar_email(email):
    return email in alunos_emails or email in professores_emails

def gerar_codigo_autenticacao():
    return str(random.randint(100000, 999999))

async def enviar_codigo_autenticacao(email, codigo):
    remetente = 'EMAIL'
    senha = 'SENHA'
    destinatario = email

    assunto = 'Código de autenticação'
    mensagem = f'O seu código de autenticação é: {codigo}'

    servidor_smtp = 'smtp.gmail.com'
    porta_smtp = 587

    msg = MIMEText(mensagem)
    msg['Subject'] = assunto
    msg['From'] = remetente
    msg['To'] = destinatario

    try:
        with smtplib.SMTP(servidor_smtp, porta_smtp) as smtp:
            smtp.starttls()
            smtp.login(remetente, senha)
            smtp.send_message(msg)
    except smtplib.SMTPException:
        print('Ocorreu um erro ao enviar o e-mail de autenticação.')

async def funcao_on_ready(bot):
    print(f'Bot conectado como {bot.user.name}')
    
    guild = bot.get_guild(GUILD_ID)

    for member in guild.members:
        if member.bot:
            continue

        if member.name in alunos_emails:
            nome_aluno = alunos_df.loc[alunos_df['E-mail academico'] == member.name, 'Nome'].iloc[0]
            await member.edit(nick=nome_aluno)  
        elif member.name in professores_emails:
            nome_professor = professores_df.loc[professores_df['E-mail'] == member.name, 'Nome'].iloc[0]
            await member.edit(nick=nome_professor) 

async def update(before, after):
    if before.nick != after.nick:
        print(f'O apelido do membro {after.name} foi atualizado de {before.nick} para {after.nick}')

async def join(member):
    guild = member.guild
    role_pretendente = discord.utils.get(guild.roles, name=CARGO_PRETENDENTE)
    await member.add_roles(role_pretendente)

    await member.send("Bem-vindo(a) ao servidor! Por favor, forneça seu email institucional para autenticação.")

    def check(message):
        return message.author == member and message.channel.type == discord.ChannelType.private

    try:
        email_message = await bot.wait_for('message', timeout=300, check=check)
    except asyncio.TimeoutError:
        await member.send("Tempo limite excedido. Você foi banido do servidor.")
        await member.ban()
        return

    email = email_message.content

    if not validar_email(email):
        await member.send("O email fornecido não é válido. Você foi banido do servidor.")
        await member.ban()
        return

    codigo = gerar_codigo_autenticacao()
    await enviar_codigo_autenticacao(email, codigo)
    await member.send("Digite o código de autenticação de 6 dígitos que foi enviado para o seu email.")

    try:
        codigo_message = await bot.wait_for('message', timeout=300, check=check)
    except asyncio.TimeoutError:
        await member.send("Tempo limite excedido. Você foi banido do servidor.")
        await member.ban()
        return

    codigo_digitado = codigo_message.content

    if codigo_digitado != codigo:
        await member.send("Código de autenticação inválido. Você tem mais 1 tentativa.")
    
    try:
        codigo_message = await bot.wait_for('message', timeout=300, check=check)
    except asyncio.TimeoutError:
        await member.send("Tempo limite excedido. Você foi banido do servidor.")
        await member.ban()
        return

    codigo_digitado_nova_tentativa = codigo_message.content

    if codigo_digitado_nova_tentativa != codigo:
        await member.send("Código de autenticação inválido. Você foi banido do servidor.")
        await member.ban()
        return


    if email in alunos_emails:
        role_aluno = discord.utils.get(guild.roles, name=CARGO_ALUNO)
        await member.add_roles(role_aluno)
        await member.remove_roles(role_pretendente)
        await member.send("Autenticação realizada com sucesso! Você agora possui o cargo de Aluno.")
        nome_aluno = alunos_df.loc[alunos_df['E-mail academico'] == email, 'Nome'].iloc[0]
        await member.edit(nick=nome_aluno)  
    elif email in professores_emails:
        role_professor = discord.utils.get(guild.roles, name=CARGO_PROFESSOR)
        await member.add_roles(role_professor)
        await member.remove_roles(role_pretendente)
        await member.send("Autenticação realizada com sucesso! Você agora possui o cargo de Professor.")
        nome_professor = professores_df.loc[professores_df['E-mail'] == email, 'Nome'].iloc[0]
        await member.edit(nick=nome_professor)  

async def on_message_p(message):
    if message.author.bot:
        return

    if any(palavra in message.content.lower() for palavra in palavroes):
        await message.delete()
        await message.channel.send(f"{message.author.mention}, mensagens com palavrões não são permitidas.")

    await bot.process_commands(message)