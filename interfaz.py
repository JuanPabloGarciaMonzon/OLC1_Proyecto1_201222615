import os
import platform
import re
#To display pdfs
import webbrowser
import RegExp
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
    categoriasTokens = {
    "comentarios": r"\/\*(\*(?!\/)|[^*])*\*\/",
    "numeros": r"0b[0-1]+|0[0-7]+|0x([0-9]|[a-f]|[A-F])+|(?!0)\d{1,}|0",
    "palabrasReservadas": r"_if|_while|_main"
    }
    categoriasNumeros ={
    "decimal": r"(?!0)\d{1,}|0(\s|$)",
    "binario": r"0b[0-1]+",
    "octal": r"0[0-7]+",
    "hexadecimal": r"0x([0-9]|[a-f]|[A-F])+"
    }
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
        self.linenumbers = TextLineNumbers(self, width=70)
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


        file_dropdown.add_command(label="Nuevo", command=self.new_file)
        file_dropdown.add_command(label="Abrir", command=self.open_file)
        file_dropdown.add_command(label="Guardar", command=self.save)
        file_dropdown.add_command(label="Guardar Como", command=self.save_as)
        file_dropdown.add_separator()
        file_dropdown.add_command(label="Salir", command=self.end)

        run_dropdown.add_command(label="Ejecutar Analisis JS", command=self.analyze)
        run_dropdown.add_command(label="Ejecutar Analisis CSS", command=self.analyze)
        run_dropdown.add_command(label="Ejecutar Analisis HTML", command=self.analyze)

        help_dropdown.add_command(label="Acerca de", command=self.about)
        help_dropdown.add_command(label="Manual de Usuario", command=self.m_user)
        help_dropdown.add_command(label="Manual Técnico", command=self.m_tecnic)



        menubar.add_cascade(label="Archivo", menu=file_dropdown)
        menubar.add_cascade(label="Ejecutar", menu=run_dropdown)
        menubar.add_cascade(label="Ayuda", menu=help_dropdown)


        self.text.tag_configure("reservadas", foreground="#580382")
        self.text.tag_configure("registros", foreground="#4B7A90")
        self.text.tag_configure("etiquetas", foreground="#C09003")
        self.text.tag_configure("valores", foreground="#0935E5")
        self.text.tag_configure("especial", foreground="#878686")
        self.text.tag_configure("resaltado", background="#A9D0F5")
        self.text.tag_configure("debug", background="#A9D0F5")
        self.text.tag_configure("dark", background="#A9D0F5")

#-------------------------------------------------------Line Number Method---------------------------------------------------------------------
    def _on_change(self, event):
        self.linenumbers.redraw()
        self.text.tag_remove('resaltado', '1.0', tk.END)
        #lex = compiler.make_lexer()
        #lex.input(self.text.get('1.0', tk.END))
        #self.pintar(lex)   


#-------------------------------------------------------File Menu Methods---------------------------------------------------------------------
    def set_window_title(self, name=None):
        if name:
            self.root.title(name)
        else:
            self.root.title("Sin titulo.txt")


    def new_file(self):
        self.text.delete(1.0, tk.END)
        self.filename = None
        self.set_window_title()

    def open_file(self):
        self.filename = filedialog.askopenfilename(defaultextension="*.*", 
        filetypes=[("All Files","*.*"),("JS Files",".js"),("CSS Files",".css"),("HTML Files",".html")])
        if self.filename:
            self.text.delete(1.0, tk.END)
            with open(self.filename, "r") as f:
               self.text.insert(1.0, f.read())
            self.set_window_title(self.filename)
            self.path_module(self.filename)

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
            new_file = filedialog.asksaveasfilename(initialfile="Sin titulo.txt", defaultextension="*.*", 
            filetypes=[("All Files","*.*"),("JS Files",".js"),("CSS Files",".css"),("HTML Files",".html")])
            textarea_content = self.text.get(1.0, tk.END)
            with open(new_file,"w") as f:
                f.write(textarea_content)
            self.filename = new_file
            self.set_window_title(self.filename)
        except Exception as e:
            print(e)
    
    def end(self):
        value = messagebox.askokcancel("Salir", "Está seguro que desea salir?")
        if value :
            root.destroy()


#-------------------------------------------------------Execution Menu Methods---------------------------------------------------------------------       
    def analyze(self):
        self.terminal.delete(1.0, tk.END)
        textarea_content = self.text.get(1.0, tk.END)
        self.result(textarea_content)


#-------------------------------------------------------Help Menu Methods---------------------------------------------------------------------
    def about(self):
        box_tilte ="Autor"
        box_msg = "Juan Pablo García Monzón 2012-22615"
        messagebox.showinfo(box_tilte,box_msg)

    def m_user(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))

        webbrowser.open_new(r'file://'+script_dir+'/WS.pdf')

        
    def m_tecnic(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))

        webbrowser.open_new(r'file://'+script_dir+'/WS.pdf')


#-------------------------------------------------------Descision Module Methods---------------------------------------------------------------------
    def path_module(self,entrada):
        replaceS = entrada.replace("\\", "/")
        x = replaceS.split(":",1)
        if(x[0].isupper()):
            var_split = os.path.splitext(replaceS)[1][1:]
            self.decision_module(var_split)
        else:
            var_split = os.path.splitext(replaceS)[1][1:]
            self.decision_module(var_split)
    
    def decision_module(self,entrada):
        if(entrada == "html"):
            print("h")
        elif(entrada == "css"):
            print("c")
        elif(entrada == "js"):
            print("j")
        else:
            print("Ingrese un archivo html, css o js para hacer el analisis lexico")   

#-------------------------------------------------------Analisis Lexico---------------------------------------------------------------------       
    def clasificarTokens(self,tokensEncontrados):
        Tokens = []
        for token in tokensEncontrados:

            cadena = token.group()
            if (self.esComentario(cadena)):
                Tokens.append( ("comentario", cadena))
            else:
                Tokens.append(("simbolo", cadena))
        return Tokens

    def esComentario (self,cadena):
        return re.match(self.categoriasTokens["comentarios"],cadena)
    
    def result(self,entrada):    
        regexTokens = r"\/\*(\*(?!\/)|[^*])*\*\/|0b[0-1]+|0[0-7]+|0x([0-9]|[a-f]|[A-F])+|(?!0)\d{1,}|0|_if|_while|_main|[A-z]{1}(\d|\w)*"

        tokensEncontrados = re.finditer(regexTokens,entrada)
        Tokens = self.clasificarTokens(tokensEncontrados)

        Tabla = """\
    +---------------------------------------------+
    | Tipo                 |                 Valor|
    |---------------------------------------------|
    {}
    +---------------------------------------------+\
    """
        Tabla = (Tabla.format('\n'.join("| {:<20} | {:>20} |".format(*fila)
         for fila in Tokens)))
        print(Tabla)
        self.terminal.insert(tk.INSERT,Tabla)

        
#-------------------------------------------------------Main---------------------------------------------------------------------       
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sin titulo.txt")
    Interfaz(root).pack(side="top", fill="both", expand=True)
    root.mainloop()