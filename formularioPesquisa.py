import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('pesquisa_online.db')
cursor = conn.cursor()

def create_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Respostas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER,
        cidade TEXT,
        experiencia TEXT,
        sugestao TEXT
    )
    ''')
    conn.commit()

create_table()

class FormularioPesquisa(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Formulário de Pesquisa Online")
        self.geometry("600x400")

        # Labels and Entries
        labels = ['Nome:', 'Idade:', 'Cidade:', 'Experiência:', 'Sugestões:']
        self.entries = {}
        for i, label_text in enumerate(labels):
            label = ttk.Label(self, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=10, sticky=tk.W)
            entry = ttk.Entry(self, width=50)
            entry.grid(row=i, column=1, padx=10, pady=10)
            self.entries[label_text] = entry

        # Botão para enviar o formulário
        submit_btn = ttk.Button(self, text="Enviar", command=self.submit_form)
        submit_btn.grid(row=len(labels), columnspan=2, pady=20)

    def submit_form(self):
        nome = self.entries['Nome:'].get()
        idade = self.entries['Idade:'].get()
        cidade = self.entries['Cidade:'].get()
        experiencia = self.entries['Experiência:'].get()
        sugestao = self.entries['Sugestões:'].get()

        # Validar se todos os campos estão preenchidos
        if nome.strip() == '' or idade.strip() == '' or cidade.strip() == '' or experiencia.strip() == '':
            messagebox.showwarning('Campos Incompletos', 'Por favor, preencha todos os campos obrigatórios.')
            return

        # Inserir dados no banco de dados
        cursor.execute('''
        INSERT INTO Respostas (nome, idade, cidade, experiencia, sugestao)
        VALUES (?, ?, ?, ?, ?)
        ''', (nome, idade, cidade, experiencia, sugestao))
        conn.commit()

        messagebox.showinfo('Sucesso', 'Formulário enviado com sucesso!')

        # Limpar campos após envio
        for entry in self.entries.values():
            entry.delete(0, tk.END)

if __name__ == "__main__":
    app = FormularioPesquisa()
    app.mainloop()

    # Fechar conexão com o banco de dados ao fechar a aplicação
    conn.close()
