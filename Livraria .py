from tkinter import *
import os
import cx_Oracle

os.chdir("C:")
os.chdir("C:\\instantclient_19_11")

#-=--Autor
def cadastreAutor():
    cursor = conexao.cursor()
    autor = str(nome.get())
    try:
        cursor.execute("INSERT INTO Autores (id_autor,Nome) VALUES (seq_Autores.nextval,'"+autor+"')")
        conexao.commit()
    except cx_Oracle.DatabaseError:
      lblMensagem["text"] = 'O campo Nome deve ser preenchido.'
    else:
        lblMensagem["text"] = 'Cadastro realizado com sucesso!'

def removaAutor ():
    cursor = conexao.cursor()
    autor = str(nome.get())

    cursor.execute("SELECT id_autor FROM Autores WHERE Nome='"+autor+"'")
    conexao.commit ()

    linha = cursor.fetchone()
    if not linha:
        lblMensagem["text"] = 'Autor inexistente.'
    else:
        cursor.execute("DELETE FROM Autores WHERE Nome='"+autor+"'")
        conexao.commit ()
        lblMensagem ["text"] = 'Autor removido com sucesso!'

def listarAutor(): ##
    cursor=conexao.cursor()
    cursor.execute("SELECT Autores.nome FROM autores")
   
    linha = cursor.fetchone()
    if not linha:
        lblMensagem ["text"] = 'Esse autor não foi cadastrado!'
        return
    lista = " "
    while linha:
        lista = linha[0]+"\n"+lista
        linha = cursor.fetchone()    
    lblMensagem ["text"] = lista 
    
#---Livros

def cadastreLivro ():
    cursor    = conexao.cursor()
    TituloLivro = str(titulo.get())
    
    try:
        precoLivro = str(PrecoLivro.get())
    except ValueError:
        lblMensagem ["text"] = 'Preco inválido.'
    else:   
        autor = str(nome.get())

        cursor.execute("SELECT Id_autor FROM Autores WHERE Nome='"+autor+"'")
        linha = cursor.fetchone()
        if not linha:
            lblMensagem ["text"] = 'Autor ainda não cadastrado.'
        else:
            idAutor = linha[0]

            try:
              cursor.execute("INSERT INTO Livros (Codigo,Titulo,Preco,Autores) VALUES (seq_Livros.nextval,'"+TituloLivro+"','"+precoLivro+"','"+autor+"')")
              conexao.commit ()
              lblMensagem ["text"] = 'Livro cadastrado com sucesso!'
            except cx_Oracle.DatabaseError:
              lblMensagem ["text"] = 'Livro já foi cadastrado!'

def removeLivro ():
    cursor = conexao.cursor()
    Titulo = str(titulo.get())

    cursor.execute("SELECT Titulo FROM Livros WHERE Titulo='"+Titulo+"'")
    conexao.commit ()

    linha = cursor.fetchone()
    if not linha:
        lblMensagem ["text"] = 'Livro não cadastrado.'
    else:
        cursor.execute("DELETE FROM Livros WHERE Titulo='"+Titulo+"'")
        conexao.commit ()
        lblMensagem ["text"] = 'Livro removido com suceesso!'

def listeLivros (): 
    cursor=conexao.cursor()
    cursor.execute("SELECT Livros.Titulo FROM livros ")

    linha = cursor.fetchone()
    if not linha:
        lblMensagem ["text"] = 'Nao ha nenhum Livro'
        return
    lista = " "
    while linha:
        lista = linha[0]+"\n"+lista
        linha = cursor.fetchone()    
    lblMensagem ["text"] = lista         

def listeLivrosAtePreco (): ##
    cursor=conexao.cursor()
    precoAte = float(Preco.get())
    cursor.execute("SELECT Livros.Titulo,Livros.Preco FROM Livros WHERE Livros.Preco <= "+str(precoAte))
    linha = cursor.fetchone()
    

    if not linha:
        lblMensagem ["text"] = 'Nao há nenhum livro dentro dessa faixa de preço.'
        return
        
    lista = " "
    while linha:
        lista = linha[0]+"\n"+lista
        linha = cursor.fetchone()    
    lblMensagem ["text"] = lista    

def listeLivrosFaixadePreco (): ##
    cursor=conexao.cursor()
    PrecoA = float(PrecoMinimo.get())
    PrecoB = float(PrecoMaximo.get())
    cursor.execute("SELECT Livros.Titulo, Livros.Preco FROM Livros WHERE Livros.preco >= "+str(PrecoA)+"  AND Livros.preco <= "+str(PrecoB)+" ")

    linha = cursor.fetchone()
    if not linha:
        lblMensagem ["text"] = 'Nao há nenhum livro dentro dessa faixa de preço.'
        return
        
    lista = " "
    while linha:
        lista = linha[0]+"\n"+lista
        linha = cursor.fetchone()    
    lblMensagem ["text"] = lista    

def listeLivrosAcimaPreco (): ##
    cursor=conexao.cursor()
    precoAcima = float(Preco.get())
    cursor.execute("SELECT Livros.Titulo, Livros.Preco FROM Livros WHERE Livros.Preco >= " + str(precoAcima))

    linha = cursor.fetchone()
    if not linha:
        lblMensagem ["text"] = 'Nao há nenhum livro acima dessa faixa de preço.'
        return
        
    lista = " "
    while linha:
        lista = linha[0]+"\n"+lista
        linha = cursor.fetchone()    
    lblMensagem ["text"] = lista  

#---

print ("PROGRAMA PARA PARA CADASTRAR LIVROS E SEUS AUTORES")

servidor = 'localhost/xe'
usuario  = 'system'
senha    = 'python'

try:
    conexao = cx_Oracle.connect(dsn=servidor,user=usuario,password=senha)
    cursor  = conexao.cursor()
except cx_Oracle.DatabaseError:
    print ("Erro de conexão com o BD\n")

try:
    conexao = cx_Oracle.connect(dsn=servidor,user=usuario,password=senha)
    cursor  = conexao.cursor()
except cx_Oracle.DatabaseError:
    print ("Erro de conexão com o BD\n")

try:
    cursor.execute("CREATE SEQUENCE seq_Autores START WITH 1 INCREMENT BY 1 MINVALUE 1 MAXVALUE 999 NOCACHE CYCLE;")
    conexao.commit()
except cx_Oracle.DatabaseError:
    pass # ignora, pois a sequência já existe

try:
    cursor.execute("CREATE TABLE Autores (id_autor NUMBER(3) PRIMARY KEY, Nome NVARCHAR2(50) UNIQUE NOT NULL)")
    conexao.commit()
except cx_Oracle.DatabaseError:
    pass # ignora, pois a tabela já existe

try:
    cursor.execute("CREATE SEQUENCE seq_Livros START WITH 1 INCREMENT BY 1 MAXVALUE 999 NOCACHE CYCLE")
    conexao.commit()
except cx_Oracle.DatabaseError:
    pass 

try:
    cursor.execute("CREATE TABLE Livros (Codigo NUMBER(10) PRIMARY KEY, Titulo NVARCHAR2(25) UNIQUE NOT NULL, Autores VARCHAR2(30), Preco NUMBER(5,2) NOT NULL")
    conexao.commit()
except cx_Oracle.DatabaseError:
    pass 


    #--- Parte gráfica

    janela = Tk()
    janela.geometry('600x700')
    janela.title('Livraria Vitual')

    #---

    fonte = ("Calibri", "11")

    #---

    painelDeOrientacao = Frame(janela)
    painelDeOrientacao["pady"] = 10
    painelDeOrientacao.pack()

    titulo = Label(painelDeOrientacao, text="Preencha os campos:")
    titulo["font"] = ("Calibri", "12", "bold")
    titulo.pack ()


    #---Nome


    painelDeNome = Frame(janela)
    painelDeNome["padx"] = 20
    painelDeNome["pady"] = 5
    painelDeNome.pack()

    lblnome = Label(painelDeNome, text="Autor:", font=fonte, width=12)
    lblnome.pack(side=LEFT)

    nome = Entry(painelDeNome)
    nome["width"] = 25
    nome["font"] = fonte
    nome.pack(side=LEFT)

    #---Titulo

    painelDeTitulo = Frame(janela)
    painelDeTitulo["padx"] = 20
    painelDeTitulo["pady"] = 5
    painelDeTitulo.pack()

    lblTitulo = Label(painelDeTitulo, text="Titulo:", font=fonte, width=12)
    lblTitulo.pack(side=LEFT)

    titulo = Entry(painelDeTitulo)
    titulo["width"] = 25
    titulo["font"] = fonte
    titulo.pack(side=LEFT)


    #---Preço

    painelDePreco = Frame(janela)
    painelDePreco["padx"] = 20
    painelDePreco["pady"] = 5
    painelDePreco.pack()
 
    lblPrecoLivro = Label(painelDePreco, text="Preço:", font=fonte, width=12)
    lblPrecoLivro.pack(side=LEFT)
 
    PrecoLivro = Entry(painelDePreco)
    PrecoLivro["width"] = 25
    PrecoLivro["font"] = fonte
    PrecoLivro.pack(side=LEFT)

    #---Botões

    painelDeBotoes = Frame(janela)
    painelDeBotoes["padx"] = 20
    painelDeBotoes["pady"] = 10
    painelDeBotoes.pack()

    bntInsert = Button(painelDeBotoes, text="Cadastrar Autor", font=fonte, width=13)
    bntInsert["command"] = cadastreAutor
    bntInsert.pack (side=LEFT)

    bntDelete = Button(painelDeBotoes, text="Excluir Autor", font=fonte, width=13)
    bntDelete["command"] = removaAutor
    bntDelete.pack(side=LEFT)

    bntListarAu = Button(painelDeBotoes, text="Listar Autores", font=fonte, width=13)
    bntListarAu["command"] = listarAutor
    bntListarAu.pack(side=LEFT)

    bntInsert = Button(painelDeBotoes, text="Cadastrar Livro", font=fonte, width=13)
    bntInsert["command"] = cadastreLivro
    bntInsert.pack(side=LEFT)

    bntDelete = Button(painelDeBotoes, text="Remover Livro", font=fonte, width=13)
    bntDelete["command"] = removeLivro
    bntDelete.pack(side=LEFT)

    #---Listar
    painelListar = Frame(janela)
    painelListar["padx"] = 20
    painelListar["pady"] = 10
    painelListar.pack()

    lblPreco = Label(painelListar, text="Listar livros por:", width=15)
    lblPreco["font"] = ("Calibri", "12", "bold")
    lblPreco.pack(side=LEFT)

    painelDePreco = Frame(janela)
    painelDePreco["padx"] = 20
    painelDePreco["pady"] = 5
    painelDePreco.pack()

    lblPreco = Label(painelDePreco, text="Preço:", font=fonte, width=15)
    lblPreco.pack(side=LEFT)

    Preco = Entry(painelDePreco)
    Preco["width"] = 25
    Preco["font"] = fonte
    Preco.pack(side=LEFT)   

    painelPrecoMinimo = Frame(janela)
    painelPrecoMinimo["padx"] = 20
    painelPrecoMinimo["pady"] = 5
    painelPrecoMinimo.pack()

    lblPrecoMin = Label(painelPrecoMinimo, text="Preço Mínimo:", font=fonte, width=15)
    lblPrecoMin.pack(side=LEFT)

    PrecoMinimo = Entry(painelPrecoMinimo)
    PrecoMinimo["width"] = 25
    PrecoMinimo["font"] = fonte
    PrecoMinimo.pack(side=LEFT)

    painelPrecoMaximo = Frame(janela)
    painelPrecoMaximo["padx"] = 20
    painelPrecoMaximo["pady"] = 5
    painelPrecoMaximo.pack()

    lblPrecoMax = Label(painelPrecoMaximo, text="Preço Máximo:", font=fonte, width=15)
    lblPrecoMax.pack(side=LEFT)

    PrecoMaximo = Entry(painelPrecoMaximo)
    PrecoMaximo["width"] = 25
    PrecoMaximo["font"] = fonte
    PrecoMaximo.pack(side=LEFT)
    

    #---Botões listar livros pelo preço

    painelDeListar = Frame(janela)
    painelDeListar["padx"] = 20
    painelDeListar["pady"] = 10
    painelDeListar.pack()

    btnListar = Button(painelDeListar, text="Todos os livros", font=fonte, width=13)
    btnListar["command"] = listeLivros
    btnListar.pack(side=RIGHT)

    btnListarAte = Button(painelDeListar, text="Até o preço", font=fonte, width=13)
    btnListarAte["command"] = listeLivrosAtePreco
    btnListarAte.pack(side=RIGHT)

    btnListarFaixa = Button(painelDeListar, text="Faixa de preço", font=fonte, width=13)
    btnListarFaixa["command"] = listeLivrosFaixadePreco
    btnListarFaixa.pack(side=RIGHT)

    btnListarAcima = Button(painelDeListar, text="Acima do preço", font=fonte, width=13)
    btnListarAcima["command"] = listeLivrosAcimaPreco
    btnListarAcima.pack(side=RIGHT)


    #---Painel de mensagem
    painelDeMensagens = Frame(janela)
    painelDeMensagens["pady"] = 15
    painelDeMensagens.pack()

    lblTituloMensagem = Label(painelDeMensagens, text="Mensagem: ")
    lblTituloMensagem["font"] = ("Calibri", "12", "italic", "bold")
    lblTituloMensagem.pack()

    lblMensagem = Label(painelDeMensagens)
    lblMensagem["font"] = ("Calibri", "12", "italic", "bold")
    lblMensagem.pack()

    #---

    janela.mainloop()

