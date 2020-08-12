import os

#To display pdfs
import webbrowser

#Interface toolkit of python tk interface
import tkinter as tk
from tkinter import filedialog, simpledialog
from tkinter import messagebox

#Handmade classes
#Custom text is for painting colors in a text area
from CustomText import CustomText
#For managing the Line Numbers in the text area
from TextLine import TextLineNumbers

class Interfaz(tk.Frame):
    ejecutar = None
    def __init__(self, *args, **kwargs):
        self.root = root
        tk.Frame.__init__(self, *args, **kwargs)

        self.tipoAnalizador = True

        self.filename = None

        self.terminal = tk.Text(root, width=45, height=1, background="black",foreground="#00AA00")
        self.terminal.pack(side="right", fill="both", expand=True)


        # Special Text
        self.text = CustomText(self)
        self.vsb = tk.Scrollbar(orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)



        # Text line number
        self.linenumbers = TextLineNumbers(self, width=30)
        self.linenumbers.attach(self.text)
        self.vsb.pack(side="right", fill="y")
        self.linenumbers.pack(side="left", fill="y")
        self.text.pack(side="right", fill="both", expand=True)
        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Configure>", self._on_change)
        
        #Menu bar
        menubar = tk.Menu(self)
        root.config(menu=menubar)
        file_dropdown = tk.Menu(menubar, tearoff=0)
        run_dropdown = tk.Menu(menubar, tearoff=0)
        help_dropdown = tk.Menu(menubar, tearoff=0)
        tool_dropdown = tk.Menu(menubar, tearoff=0)
        option_dropdown = tk.Menu(menubar, tearoff=0)

        option_dropdown.add_command(label="Tema 1", command=self.whiteTheme)
        option_dropdown.add_command(label="Tema 2", command=self.blackTheme)

        file_dropdown.add_command(label="Nuevo", command=self.new_file)
        file_dropdown.add_command(label="Abrir", command=self.open_file)
        file_dropdown.add_command(label="Guardar", command=self.save)
        file_dropdown.add_command(label="Guardar Como", command=self.save_as)
        file_dropdown.add_command(label="Cerrar", command=self.root.destroy)
        file_dropdown.add_separator()
        file_dropdown.add_command(label="Salir", command=self.root.destroy)

        tool_dropdown.add_command(label="Copiar Ctrl + C", command=self.copiar)
        tool_dropdown.add_command(label="Pegar Ctrl + V", command=self.pegar)
        tool_dropdown.add_command(label="Cortar Ctrl + X", command=self.cortar)
        tool_dropdown.add_command(label="Buscar Ctrl + F", command=self.find)
        tool_dropdown.add_command(label="Reemplazar Ctrl + R", command=self.replace)


        help_dropdown.add_command(label="Acerca de", command=self.about)
        help_dropdown.add_command(label="Ayuda", command=self.ayuda)



        menubar.add_cascade(label="Archivo", menu=file_dropdown)
        menubar.add_cascade(label="Editar", menu=tool_dropdown)
        menubar.add_cascade(label="Ejecutar", menu=run_dropdown)
        menubar.add_cascade(label="Opciones", menu=option_dropdown)
        menubar.add_cascade(label="Ayuda", menu=help_dropdown)


        self.text.tag_configure("reservadas", foreground="#580382")
        self.text.tag_configure("registros", foreground="#4B7A90")
        self.text.tag_configure("etiquetas", foreground="#C09003")
        self.text.tag_configure("valores", foreground="#0935E5")
        self.text.tag_configure("especial", foreground="#878686")
        self.text.tag_configure("resaltado", background="#A9D0F5")
        self.text.tag_configure("debug", background="#A9D0F5")
        self.text.tag_configure("dark", background="#A9D0F5")

        self.bind_all('<Control-c>', self.copiar)
        self.bind_all('<Control-v>', self.pegar)
        self.bind_all('<Control-x>', self.cortar)
        self.bind_all('<Control-f>', self.find)
        self.bind_all('<Control-r>', self.replace)


    def blackTheme(self):
        self.text.config(background="black",foreground="#00AA00")
        self.terminal.config(background="white",foreground="black")

    def whiteTheme(self):
        self.text.config(background="white",foreground="black")
        self.terminal.config(background="black",foreground="#00AA00")


    def copiar(self, *args):
        self.text.clipboard_clear()
        self.text.clipboard_append(self.text.selection_get())

    def pegar(self, *args):
        self.text.insert('insert', self.selection_get(selection='CLIPBOARD'))

    def cortar(self, *args):
        self.copiar()
        self.text.delete('sel.first', 'sel.last')

    def find(self,*args):
        searchValue = simpledialog.askstring(title="Buscar", prompt="")
        self.text.tag_remove('resaltado', '1.0', tk.END)
        if searchValue:
            posicionIndex = self.text.index(tk.INSERT)
            posicionInicial = self.text.search(searchValue, posicionIndex, nocase=1, stopindex=tk.END)
            posicionFinal = f'{posicionInicial}+{len(searchValue)}c'
            self.posicionIndex = posicionFinal
            for tag in self.text.tag_names():
                self.text.tag_remove(tag, posicionInicial, posicionFinal)
            self.text.tag_add('resaltado', posicionInicial, posicionFinal)

    def replace(self,*args):
        searchValue = simpledialog.askstring(title="Buscar", prompt="")
        replace = simpledialog.askstring(title="Reemplazar", prompt="")
        self.text.tag_remove('resaltado', '1.0', tk.END)
        if searchValue:
            posicionIndex = self.text.index(tk.INSERT)
            posicionInicial = self.text.search(searchValue, posicionIndex, nocase=1, stopindex=tk.END)
            posicionFinal = f'{posicionInicial}+{len(searchValue)}c'
            self.text.delete(posicionInicial, posicionFinal)
            self.text.insert(posicionInicial, replace)
            posicionFinal = f'{posicionInicial}+{len(replace)}c'
            self.posicionIndex = posicionFinal
    #File Methods
    def set_window_title(self, name=None):
        if name:
            self.root.title(name +" - AugusIDE")
        else:
            self.root.title("Sin titulo.txt - AugusIDE")


    def new_file(self):
        self.text.delete(1.0, tk.END)
        self.filename = None
        self.set_window_title()

    def open_file(self):
        self.filename = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("All Files","*.*"),("Text Files",".txt")])
        if self.filename:
            self.text.delete(1.0, tk.END)
            with open(self.filename, "r") as f:
               self.text.insert(1.0, f.read())
            self.set_window_title(self.filename)

    def save(self):
        if self.filename:
            try:
                textarea_content = self.text.get(1.0, tk.END)
                with open(self.filename, "w") as f:
                    f.write(textarea_content)
            except Exception as e:
                print(e)
        else:
            self.save_as()

    def save_as(self):
        try:
            new_file = filedialog.asksaveasfilename(initialfile="Sin titulo.txt", defaultextension=".txt", filetypes=[("All Files","*.*"),("Text Files",".txt")])
            textarea_content = self.text.get(1.0, tk.END)
            with open(new_file,"w") as f:
                f.write(textarea_content)
            self.filename = new_file
            self.set_window_title(self.filename)
        except Exception as e:
            print(e)

        #Line number method
    def _on_change(self, event):
        self.linenumbers.redraw()
        self.text.tag_remove('resaltado', '1.0', tk.END)
        #lex = compiler.make_lexer()
        #lex.input(self.text.get('1.0', tk.END))
        #self.pintar(lex)    

    def about(self):
        box_tilte ="Autor"
        box_msg = "Juan Pablo García Monzón 2012-22615"
        messagebox.showinfo(box_tilte,box_msg)

    def ayuda(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))

        webbrowser.open_new(r'file://'+script_dir+'/WS.pdf')
        webbrowser.open_new(r'file://' + script_dir + '/WS.pdf')
        


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sin titulo.txt - AugusIDE")
    Interfaz(root).pack(side="top", fill="both", expand=True)
    root.mainloop()