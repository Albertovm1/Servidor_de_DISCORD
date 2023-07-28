# Servidor de DISCORD
Esse é meu primeiro projeto na linguagem python, feito no primeiro periodo de curso.

# Objetivos
Criar um servidor no discord para o curso de engenharia de computação com mecanismo de autenticação de usuários.

# funções do bot
![about](https://img.shields.io/badge/-Autenticação:-blue
)

 <p align = "justify">O servidor deve ser capaz de autenticar automaticamente os usuários entrantes para que só possa ser admitido no servidor aquela pessoa (aluno ou professor) que faz parte da instituição. Dois arquivos CSV serão usados: um para alunos e outro para os professores.

<p align = "center"> O processo de autenticação deve funcionar da seguinte forma:
<p>
⚙️Quando um usuário entrar no servidor, o bot de autenticação deve atribuir o cargo de pretendente a esse usuário.
<p>
<p>
⚙️Em seguida, o bot deve solicitar ao usuário qual o seu email institucional. O bot enviará um código único de 6 dígitos para o email do usuário. Este deve digitar esse código de 6 dígitos no canal de autenticação em até 5 minutos. Caso isso não aconteça, o usuário é banido do servidor. Caso o usuário forneça o código correto, é atribuído a ele o cargo correspondente ao seu perfil (aluno, professor, etc.) e ele poderá acessar os canais correspondentes ao seu cargo. Caso o usuário forneça um e-mail que não está na base de dados ele também será banido do servidor.
<p>
<p>
⚙️Será feita uma verificação para saber se o email institucional consta na lista de alunos matriculados no curso ou na lista de professores do IFPB.
<p>
<p>
⚙️Após a autenticação do usuário, deve ser atribuído a ele o cargo de professor ou aluno de acordo com a base de dados em que se encontra seu email.
<p>
<p>
⚙️Apenas alunos e professores serão autenticados automaticamente. Os alunos egressos serão incluídos manualmente no servidor uma vez que não possuem mais email institucional.

![about](https://img.shields.io/badge/-Criação%20de%20sala:-blue
)

<p>
⚙️Quando um usuário digita o comando !pedir_sala "categoria da sala" "tempo da sala" "senha da sala"
ele vai criar uma sala na categoria que existe com um tempo X que apos inspiração a sala sera deleta automaticamente e com uma senha de acesso.
<p>
<p>
⚙️Caso o usuario faça algo diferente, recebera um aviso para o erro ser corrigido.
<p>

![about](https://img.shields.io/badge/-Sem%20Palavrões:-blue
)

<p>
⚙️ Quando usuario escreve algum palavrão da lista de palavrões do codigo, a mensagem enviada será apagada automaticamente e recebera um aviso.
<p>
