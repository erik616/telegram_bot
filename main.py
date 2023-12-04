import telebot

import datetime
from datetime import datetime

from pytz import timezone

import string
import random
import unidecode

from api import CHAVE

CHAVE_API = CHAVE

bot = telebot.TeleBot(CHAVE_API)

# ARQUIVO DE LIVROS
from books_data import books

gerns = {"aventura": "avnt", "ficcao": "ficc", "romance": "rmnc","terror": "terr"}

def cupom_ger(size=6, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size)) 

def Saudacao():
  data = datetime.now()
  fuso = timezone('America/Sao_Paulo')

  hora_atual = data.astimezone(fuso)
  horaStr = hora_atual.strftime('%H')
  hora = int(horaStr)

  saudacao = "Bom dia" if hora < 12 else "Boa tarde" if hora > 12 and hora < 18 else "Boa noite"

  return saudacao 


# ESCOLHER
@bot.message_handler(regexp="getbook")
def Escolher(mensagem):
  book = f"""{mensagem.text}"""
  bookid = book[14:]

  name = books[book]["name"]
  autor = books[book]["autor"]
  sinopse = books[book]["sinopse"]

  text =  f"""
Livro {name}, escrito por {autor}.

Sinopse: {sinopse}.

/Ler_{bookid} Ler Livro
/Ver_Catalogo Rever o Catalogo
"""
  bot.send_message(mensagem.chat.id, text)

# Ler
@bot.message_handler(regexp="Ler_")
def Ler(mensagem):
    idbook = f"""{mensagem.text}""".removeprefix("/Ler_")
    book = ''
    link = ''

    for keys in books:
      if keys.count(idbook) != 0:
        book = books[f"""{keys}"""]["name"]
        link = books[f"""{keys}"""]["link"]

    text = f"""{book}:  Acesse o link para ler o livro: {link}"""
    bot.send_message(mensagem.chat.id, text)

# TEM O LIVRO
@bot.message_handler(regexp="Tem")
def Tem(mensagem):
  # f"""{books[book]["name"]} {books[book]["autor"]}"""
  ignor = unidecode
  text = ''
  book = f"""{mensagem.text}""".removeprefix("Tem ").lower()

  for key in books:
    title = ignor.unidecode(books[key]["name"])
    book_ig = ignor.unidecode(book)

    if f"""{title}""".lower() == book_ig:
      text = f"""Temos o livro {books[key]["name"]} escrito por {books[key]["autor"]}.
Sinopse: {books[key]["sinopse"]}

Deseja ler?
/Ler_{key[14:]}
/Ver_Catalogo
      """   

  bot.send_message(mensagem.chat.id, text)

# GENEROS
@bot.message_handler(regexp="genero")
def Genero(mensagem):
  lista = ""
  genr = f"""{mensagem.text}""".removeprefix("/genero_")
  
  for keys in books:
    if keys.find(gerns[f"""{genr}"""]) == 9: 
        lista += f"{keys}    {books[keys]["name"]}\n"

        text = f"""{lista}"""

  bot.send_message(mensagem.chat.id, text)

# VER CATALOGO
@bot.message_handler(commands=["Ver_Catalogo"])
def Ver_Catalogo(mensagem):
  text = """
Atualmente no nosso catalogo esta divido nos seguintes generos:
/genero_aventura    Livros de Aventura   
/genero_ficcao      Livros de Ficção
/genero_romance     Livros de Romance
/genero_terror      Livros de Terror
"""
  bot.send_message(mensagem.chat.id, text)

# PROCURAR
@bot.message_handler(commands=["Procurar"])
def Procurar(mensagem):
  text = """Para procurar um Livro digite : Tem e o Nome do Livro.
Exemplo: Tem O Hobbit
  """
  bot.send_message(mensagem.chat.id, text)

#Recomende
@bot.message_handler(regexp="Recomende")
def Recomende(mensagem):

  name = ''
  id_book = ''
  get_book = ''

  if f"""{mensagem.text}""".find("aleatorio") == -1:
    rand = random.randint(0,books.__len__())
    lista = list(books.keys())
    
    name = books[lista[rand]]["name"]

    id_book = lista[rand][14:]
    get_book = lista[rand]
  else:
    book = f"""{mensagem.text}""".removeprefix("/Recomende_aleatorio_")

    genrbook = gerns[f"""{book}"""]

    lista_books = dict()

    for keys in books:
      if keys.find(genrbook) == 9: 
          lista_books[keys] = books[keys]

    rand = random.randint(0,lista_books.__len__())
    
    lista = list(lista_books.keys())
    name = lista_books[lista[rand]]["name"]
    id_book = lista[rand][14:]
    get_book = lista[rand]

  text = f"""A recomendação de hoje é {name}. 
Você pode ver um pouco sobre ele abaixo:
{get_book} {name}

E Você pode ler ele clicando abaixo.
/Ler_{id_book} Gostaria de ler {name}?

Ou
/Procurar"""

  bot.send_message(mensagem.chat.id, text)

#RECOMENDAR
@bot.message_handler(commands=["Recomendar"])
def Recomendar(mensagem):
  
  text = f"""Gostaria de um recomendação com base no seu gosto?
E so escolher pelo seu genero favorito: 
/Recomende_aleatorio_aventura Aventura
/Recomende_aleatorio_ficcao Ficção
/Recomende_aleatorio_romance Romance
/Recomende_aleatorio_terror Terror

Ou

/Recomende Recomendação Aleatoria"""

  bot.send_message(mensagem.chat.id, text)

@bot.message_handler(commands=["Suporte"])
def Suporte(mensagem):
  suport = """
    Para sanar qualquer duvida ou problema fale com a gente, nosso email é suportLivroBook@gmail.com
        """
  bot.send_message(mensagem.chat.id, suport)


### DEFAULT ###
def verificar(mensagem):
  return True

@bot.message_handler(func=verificar)
def responder(mensagem):

  saudacao = Saudacao()

  text = f""" 
  Olá,
{saudacao}, me chamo Hacoon.
Bem-Vindo a nossa livraria, abaixo esta as nossas opções (Clique e Aguarde).
  /Ver_Catalogo Ver o Catalogo
  /Procurar     Procurar um Livro
  /Recomendar   Recomende um Livro
  /Suporte      Preciso de Ajuda
  """
  bot.reply_to(mensagem, text)


bot.polling()