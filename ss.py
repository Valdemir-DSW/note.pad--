import tkinter as tk
from tkinter import filedialog, scrolledtext, simpledialog, ttk, messagebox
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import get_formatter_by_name
import os

text = None

# Funções para ações
def create_new_tab():
    global text
    tab = tk.Text(notebook)
    notebook.add(tab, text="Novo Arquivo")
    notebook.select(tab)
    text = tab  # Atribuir o widget de texto à variável text

def execute_root_file():
    if project_folder:
        current_tab = notebook.select()
        tab_text = notebook.tab(current_tab, 'text')  # Obtém o nome da aba selecionada
        file_path = os.path.join(project_folder, tab_text)  # Constrói o caminho completo do arquivo
        os.startfile(file_path)
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
            try:
                os.startfile(content)
            except Exception as e:
                print(f"Erro ao executar o arquivo: {e}")
                output_text.config(f"Erro ao executar o arquivo: {e}")
                highlight_code()
        else:
            print("O arquivo não existe.")
    else:
        print("Nenhum projeto selecionado.")


project_folder = None


def open_project():
    folder_path = filedialog.askdirectory()  # Solicita ao usuário que selecione uma pasta
    global project_folder  # Use a variável global project_folder
    folder_path = filedialog.askdirectory()  # Solicita ao usuário que selecione uma pasta
    if folder_path:
        project_folder = folder_path  
    if folder_path:
        supported_extensions = (".txt", ".py", ".java", ".c", ".cpp", ".html", ".css", ".js", ".xml", ".json", ".md", ".php", ".rb")  # Adicione as extensões suportadas aqui
        file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(supported_extensions)]
        for file_path in file_paths:
            with open(file_path, "r") as file:
                content = file.read()
            file_name = os.path.basename(file_path)
            tab = tk.Text(notebook)
            tab.insert(1.0, content)
            notebook.add(tab, text=file_name)
            add_recent_file(file_path)
            notebook.select(tab)
            



from tkinter import filedialog

def save_file():
    current_tab = notebook.select()
    text_widget = notebook.nametowidget(current_tab)
    
    filetypes = [
        ("Text Files", "*.txt"),
        ("All Files", "*.*"),
        ("Python Files", "*.py"),
        ("Java Files", "*.java"),
        ("C Files", "*.c"),
        ("C++ Files", "*.cpp"),
        ("HTML Files", "*.html"),
        ("CSS Files", "*.css"),
        ("JavaScript Files", "*.js"),
        ("XML Files", "*.xml"),
        ("JSON Files", "*.json"),
        ("Markdown Files", "*.md"),
        ("PHP Files", "*.php"),
        ("Ruby Files", "*.rb")
    ]
    
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=filetypes, initialfile="Novo Arquivo")
    
    if file_path:
        with open(file_path, "w") as file:
            content = text_widget.get(1.0, tk.END)
            file.write(content)
        notebook.tab(current_tab, text=file_path)  # Atualiza o nome da aba


def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            content = file.read()
        tab = tk.Text(notebook)
        tab.insert(1.0, content)
        notebook.add(tab, text=file_path)
        add_recent_file(file_path)
        notebook.select(tab)

def highlight_code():
    current_tab = notebook.select()
    text_widget = notebook.nametowidget(current_tab)
    content = text_widget.get(1.0, tk.END)
    lexer = get_lexer_by_name("python", stripall=True)
    formatter = get_formatter_by_name("html")
    highlighted_code = highlight(content, lexer, formatter)
    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.insert(1.0, highlighted_code)
    output_text.config(state=tk.DISABLED)

def run_code():
    current_tab = notebook.select()
    text_widget = notebook.nametowidget(current_tab)
    code = text_widget.get(1.0, tk.END)
    try:
        exec(code)
    except Exception as e:
        output_text.config(state=tk.NORMAL)
        output_text.delete(1.0, tk.END)
        output_text.insert(1.0, f"Erro: {str(e)}", "error")
        output_text.config(state=tk.DISABLED)


def open_recent_file(file_path):
    if file_path:
        with open(file_path, "r") as file:
            content = file.read()
        tab = tk.Text(notebook)
        tab.insert(1.0, content)
        notebook.add(tab, text=file_path)
        notebook.select(tab)

def add_recent_file(file_path):
    recent_files.insert(0, file_path)
    if len(recent_files) > 5:
        recent_files.pop()

def open_recently():
    if recent_files:
        choice = simpledialog.askstring("Abrir Recentemente", "Escolha um arquivo recente (1-5):")
        try:
            choice = int(choice)
            if 1 <= choice <= len(recent_files):
                file_path = recent_files[choice - 1]
                open_recent_file(file_path)
            else:
                messagebox.showerror("Erro", "Escolha inválida.")
        except (ValueError, TypeError):
            messagebox.showerror("Erro", "Escolha inválida.")

# Funções para temas
def set_theme(theme):
    if theme == "light":
        # Tema claro
        bg_color = "white"
        fg_color = "black"
        text_bg_color = "white"
        output_bg_color = "white"
        header_fg_color = "black"  # Cor do texto do cabeçalho
    else:
        # Tema escuro (padrão)
        bg_color = "#1e1e1e"
        fg_color = "white"
        text_bg_color = "black"
        output_bg_color = "#333333"
        header_fg_color = "white"  # Cor do texto do cabeçalho

    app.configure(bg=bg_color)
    text.configure(bg=text_bg_color, fg=fg_color)
    output_text.configure(bg=output_bg_color, fg=fg_color)
    menu.configure(bg=bg_color, fg=fg_color)
    file_menu.configure(bg=bg_color, fg=fg_color)
    code_menu.configure(bg=bg_color, fg=fg_color)
    


    app.option_add("*TButton*highlightBackground", bg_color)
    app.option_add("*TButton*highlightColor", bg_color)
    current_theme_var.set(theme)


def switch_theme():
    if current_theme_var.get() == "light":
        set_theme("dark")
    else:
        set_theme("light")

# Inicialização
app = tk.Tk()
app.title(f"Note Pad -- ")
app.iconbitmap(os.path.abspath("ico.ico"))

# Defina o tema inicial e a interface do aplicativo
current_theme_var = tk.StringVar(value="dark")

# Abas
notebook = ttk.Notebook(app)
notebook.pack(fill="both", expand=True)

# Widgets de texto e saída
create_new_tab()  # Cria a primeira aba

output_text = scrolledtext.ScrolledText(app, wrap=tk.WORD, state="disabled")
output_text.pack(fill="both", expand=True)

# Menu
menu = tk.Menu(app)
app.config(menu=menu)

file_menu = tk.Menu(menu)
menu.add_cascade(label="Arquivo", menu=file_menu)
file_menu.add_command(label="Abrir", command=open_file)
file_menu.add_command(label="Salvar", command=save_file)
file_menu.add_command(label="Abrir projeto", command=open_project)
file_menu.add_separator()
file_menu.add_command(label="Abrir Recentemente", command=open_recently)
file_menu.add_separator()
file_menu.add_command(label="Sair", command=app.quit)
file_menu.add_separator()
file_menu.add_command(label="Alternar Tema da tela", command=switch_theme)


code_menu = tk.Menu(menu)
menu.add_cascade(label="Código", menu=code_menu)
code_menu.add_command(label="Realçar Sintaxe", command=highlight_code)
code_menu.add_separator()
code_menu.add_separator()
code_menu.add_command(label="Executar Código", command=run_code)
code_menu.add_command(label="Executar raiz", command=execute_root_file)

# Defina o tema após a criação do widget de texto
set_theme(current_theme_var.get())

# Botão para alternar o tema
file_menu.insert_separator(4)  # Insira uma separação antes do botão

# Lista de arquivos recentes
recent_files = []

app.mainloop()