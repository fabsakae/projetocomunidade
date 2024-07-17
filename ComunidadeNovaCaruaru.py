import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('community_needs.db')
cursor = conn.cursor()

def create_tables():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Pessoa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        data_nascimento TEXT,
        sexo TEXT,
        endereco TEXT,
        contato TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Categorias_Necessidades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Necessidades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL,
        data_identificacao TEXT,
        prioridade TEXT,
        categoria_id INTEGER,
        pessoa_id INTEGER,
        FOREIGN KEY (categoria_id) REFERENCES Categorias_Necessidades(id),
        FOREIGN KEY (pessoa_id) REFERENCES Pessoa(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Sugestoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        necessidade_id INTEGER,
        descricao TEXT NOT NULL,
        data_sugestao TEXT,
        pessoa_id INTEGER,
        FOREIGN KEY (necessidade_id) REFERENCES Necessidades(id),
        FOREIGN KEY (pessoa_id) REFERENCES Pessoa(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Providencias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        necessidade_id INTEGER,
        descricao TEXT NOT NULL,
        status TEXT,
        data_inicio TEXT,
        data_conclusao TEXT,
        responsavel TEXT,
        FOREIGN KEY (necessidade_id) REFERENCES Necessidades(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Historico_Providencias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        providencia_id INTEGER,
        data_atualizacao TEXT,
        descricao TEXT,
        status_atual TEXT,
        FOREIGN KEY (providencia_id) REFERENCES Providencias(id)
    )
    ''')

    conn.commit()

create_tables()

class CommunityApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gerenciamento das Necessidades da Comunidade Nova Caruaru")
        self.geometry("800x600")

        # Create a tab control
        tab_control = ttk.Notebook(self)
        tab_control.pack(expand=1, fill='both')

        # Create tabs
        self.create_pessoa_tab(tab_control)
        self.create_necessidades_tab(tab_control)
        self.create_sugestoes_tab(tab_control)
        self.create_providencias_tab(tab_control)

    def create_pessoa_tab(self, tab_control):
        pessoa_tab = ttk.Frame(tab_control)
        tab_control.add(pessoa_tab, text='Pessoas')

        # Labels and entries for Pessoa
        labels = ['Nome', 'Data de Nascimento', 'Sexo', 'Endereço', 'Contato']
        self.pessoa_entries = {}
        for i, label in enumerate(labels):
            lbl = ttk.Label(pessoa_tab, text=label)
            lbl.grid(column=0, row=i, padx=10, pady=5)
            entry = ttk.Entry(pessoa_tab)
            entry.grid(column=1, row=i, padx=10, pady=5)
            self.pessoa_entries[label] = entry

        # Button to add Pessoa
        add_btn = ttk.Button(pessoa_tab, text='Adicionar Pessoa', command=self.add_pessoa)
        add_btn.grid(column=0, row=len(labels), columnspan=2, pady=10)

    def add_pessoa(self):
        nome = self.pessoa_entries['Nome'].get()
        data_nascimento = self.pessoa_entries['Data de Nascimento'].get()
        sexo = self.pessoa_entries['Sexo'].get()
        endereco = self.pessoa_entries['Endereço'].get()
        contato = self.pessoa_entries['Contato'].get()

        cursor.execute('''
        INSERT INTO Pessoa (nome, data_nascimento, sexo, endereco, contato)
        VALUES (?, ?, ?, ?, ?)
        ''', (nome, data_nascimento, sexo, endereco, contato))
        conn.commit()

        messagebox.showinfo('Sucesso', 'Pessoa adicionada com sucesso!')

        for entry in self.pessoa_entries.values():
            entry.delete(0, tk.END)

    def create_necessidades_tab(self, tab_control):
        necessidades_tab = ttk.Frame(tab_control)
        tab_control.add(necessidades_tab, text='Necessidades')

        # Labels and entries for Necessidades
        labels = ['Descrição', 'Data de Identificação', 'Prioridade', 'Categoria ID', 'Pessoa ID']
        self.necessidades_entries = {}
        for i, label in enumerate(labels):
            lbl = ttk.Label(necessidades_tab, text=label)
            lbl.grid(column=0, row=i, padx=10, pady=5)
            entry = ttk.Entry(necessidades_tab)
            entry.grid(column=1, row=i, padx=10, pady=5)
            self.necessidades_entries[label] = entry

        # Button to add Necessidades
        add_btn = ttk.Button(necessidades_tab, text='Adicionar Necessidade', command=self.add_necessidade)
        add_btn.grid(column=0, row=len(labels), columnspan=2, pady=10)

    def add_necessidade(self):
        descricao = self.necessidades_entries['Descrição'].get()
        data_identificacao = self.necessidades_entries['Data de Identificação'].get()
        prioridade = self.necessidades_entries['Prioridade'].get()
        categoria_id = self.necessidades_entries['Categoria ID'].get()
        pessoa_id = self.necessidades_entries['Pessoa ID'].get()

        cursor.execute('''
        INSERT INTO Necessidades (descricao, data_identificacao, prioridade, categoria_id, pessoa_id)
        VALUES (?, ?, ?, ?, ?)
        ''', (descricao, data_identificacao, prioridade, categoria_id, pessoa_id))
        conn.commit()

        messagebox.showinfo('Sucesso', 'Necessidade adicionada com sucesso!')

        for entry in self.necessidades_entries.values():
            entry.delete(0, tk.END)

    def create_sugestoes_tab(self, tab_control):
        sugestoes_tab = ttk.Frame(tab_control)
        tab_control.add(sugestoes_tab, text='Sugestões')

        # Labels and entries for Sugestoes
        labels = ['Necessidade ID', 'Descrição', 'Data de Sugestão', 'Pessoa ID']
        self.sugestoes_entries = {}
        for i, label in enumerate(labels):
            lbl = ttk.Label(sugestoes_tab, text=label)
            lbl.grid(column=0, row=i, padx=10, pady=5)
            entry = ttk.Entry(sugestoes_tab)
            entry.grid(column=1, row=i, padx=10, pady=5)
            self.sugestoes_entries[label] = entry

        # Button to add Sugestoes
        add_btn = ttk.Button(sugestoes_tab, text='Adicionar Sugestão', command=self.add_sugestao)
        add_btn.grid(column=0, row=len(labels), columnspan=2, pady=10)

    def add_sugestao(self):
        necessidade_id = self.sugestoes_entries['Necessidade ID'].get()
        descricao = self.sugestoes_entries['Descrição'].get()
        data_sugestao = self.sugestoes_entries['Data de Sugestão'].get()
        pessoa_id = self.sugestoes_entries['Pessoa ID'].get()

        cursor.execute('''
        INSERT INTO Sugestoes (necessidade_id, descricao, data_sugestao, pessoa_id)
        VALUES (?, ?, ?, ?)
        ''', (necessidade_id, descricao, data_sugestao, pessoa_id))
        conn.commit()

        messagebox.showinfo('Sucesso', 'Sugestão adicionada com sucesso!')

        for entry in self.sugestoes_entries.values():
            entry.delete(0, tk.END)

    def create_providencias_tab(self, tab_control):
        providencias_tab = ttk.Frame(tab_control)
        tab_control.add(providencias_tab, text='Providências')

        # Labels and entries for Providencias
        labels = ['Necessidade ID', 'Descrição', 'Status', 'Data de Início', 'Data de Conclusão', 'Responsável']
        self.providencias_entries = {}
        for i, label in enumerate(labels):
            lbl = ttk.Label(providencias_tab, text=label)
            lbl.grid(column=0, row=i, padx=10, pady=5)
            entry = ttk.Entry(providencias_tab)
            entry.grid(column=1, row=i, padx=10, pady=5)
            self.providencias_entries[label] = entry

        # Button to add Providencias
        add_btn = ttk.Button(providencias_tab, text='Adicionar Providência', command=self.add_providencia)
        add_btn.grid(column=0, row=len(labels), columnspan=2, pady=10)

    def add_providencia(self):
        necessidade_id = self.providencias_entries['Necessidade ID'].get()
        descricao = self.providencias_entries['Descrição'].get()
        status = self.providencias_entries['Status'].get()
        data_inicio = self.providencias_entries['Data de Início'].get()
        data_conclusao = self.providencias_entries['Data de Conclusão'].get()
        responsavel = self.providencias_entries['Responsável'].get()

        cursor.execute('''
        INSERT INTO Providencias (necessidade_id, descricao, status, data_inicio, data_conclusao, responsavel)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (necessidade_id, descricao, status, data_inicio, data_conclusao, responsavel))
        conn.commit()

        messagebox.showinfo('Sucesso', 'Providência adicionada com sucesso!')

        for entry in self.providencias_entries.values():
            entry.delete(0, tk.END)

if __name__ == "__main__":
    app = CommunityApp()
    app.mainloop()
    conn.close()
