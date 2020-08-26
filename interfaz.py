import os
import os.path
import platform
import re
import Lexico_JS
from error_report import errorList
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
        report_dropdown = tk.Menu(menubar, tearoff=0)
        help_dropdown = tk.Menu(menubar, tearoff=0)


        file_dropdown.add_command(label="Nuevo", command=self.new_file)
        file_dropdown.add_command(label="Abrir", command=self.open_file)
        file_dropdown.add_command(label="Guardar", command=self.save)
        file_dropdown.add_command(label="Guardar Como", command=self.save_as)
        file_dropdown.add_separator()
        file_dropdown.add_command(label="Salir", command=self.end)

        run_dropdown.add_command(label="Ejecutar", command=self.verify_path)

        report_dropdown.add_command(label="Errores Lexicos", command=self.errorReport)
        

        help_dropdown.add_command(label="Acerca de", command=self.about)
        help_dropdown.add_command(label="Manual de Usuario", command=self.m_user)
        help_dropdown.add_command(label="Manual Técnico", command=self.m_tecnic)



        menubar.add_cascade(label="Archivo", menu=file_dropdown)
        menubar.add_cascade(label="Ejecutar", menu=run_dropdown)
        menubar.add_cascade(label="Reportes", menu=report_dropdown)
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
        
        #self.pintar(txt)   


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
    def analyze(self,entrada):
        js = Lexico_JS.lex_JS() 
        self.terminal.delete(1.0, tk.END)
        txt = self.text.get(1.0, tk.END)

        if(entrada == "JS"):                                              
            js.cadena = txt
            js.receive_input()            
            self.terminal.insert(tk.INSERT,"----------------------------------------Tokens--------------------------------\n")
            self.terminal.insert(tk.END,str(js.token_output).replace("],", "\n").replace("[[","[").replace("]]","\n").replace("[","").replace("\\n","").replace("None,","").replace("None",""))
            self.terminal.insert(tk.END,"----------------------------------------Errors--------------------------------\n")
            self.terminal.insert(tk.END,str(js.error_output).replace("],", "\n").replace("[[","[").replace("]]","\n").replace("[",""))


        else:
            box_tilte ="Execution Error"
            box_msg = "Por favor revise que el archivo que haya abierto sea JS, CSS, HTML o RMT"
            messagebox.showerror(box_tilte,box_msg)
        
        self.error(js.error_list)
        self.pintar(js.token_output)
        if(str(txt).__contains__("PATHW:")): 
            self.get_direction("PATHW:",js.clean)
            if(str(txt).__contains__("PATHL:")):
                self.get_direction("PATHL:",js.clean)
        
        
                
             
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
    def verify_path(self):
        if self.filename == None:
            box_tilte ="Path Error"
            box_msg = "Por favor abra un archivo JS, CSS, HTML o RMT antes de analizar o escriba un archivo y guardelo con una de esas extensiones"
            messagebox.showerror(box_tilte,box_msg)
        else:
            self.path_module(self.filename)
  
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
        decision_flag = ""
        if(entrada == "html"):
            decision_flag = "HTML"
            self.analyze(decision_flag)
        elif(entrada == "css"):
            decision_flag = "CSS"
            self.analyze(decision_flag)
        elif(entrada == "js"):
            decision_flag = "JS"
            self.analyze(decision_flag)
        elif(entrada == "rmt"):
            decision_flag = "RMT"
            self.analyze(decision_flag)
        else:
            decision_flag = "NONE"
            self.analyze(decision_flag)
#-------------------------------------------------------File Management---------------------------------------------------------------------       
    def create_file(self,path,clean):
        fic = open(path+"file.js", "w")
        
        fic.write(clean)    
        fic.close()

    def get_direction(self,entrada,clean):
        txt = self.text.get(1.0, tk.END)
        sistema = platform.system()
        if(entrada == "PATHW:" and sistema == "Windows"):            
            path = txt.split(entrada)
            direction = path[1].split("\n")
            self.create_directory(direction[0],clean)
        elif(entrada == "PATHL:" and sistema == "Linux"):
            path = txt.split(entrada)
            direction = path[1].split("\n")
            self.create_directory(direction[0],clean)
        else:
            print("")
            box_tilte ="Operative System Error"
            box_msg = "La carpeta que esta tratando de crear no es el formato correcto en el sistema operativo en el que se encuentra actualmente"
            messagebox.showerror(box_tilte,box_msg)

 
    def create_directory(self,ruta,clean):
        try:
            os.makedirs(ruta)
            self.create_file(ruta,clean)
        except OSError:
            pass
  # si no podemos crear la ruta dejamos que pase
  # si la operación resulto con éxito nos cambiamos al directorio 
        os.chdir(ruta)
        self.create_file(ruta,clean)
#-------------------------------------------------------Reports---------------------------------------------------------------------       
    def error(self,entrada):
        if(len(entrada)==0):
            box_tilte = "Tabla de Errores"
            box_msg = "No existe ningun error"
            messagebox.showinfo(box_tilte, box_msg)
        else:
            errorList(entrada)

    def errorReport(self):
        webbrowser.open_new('errorList.html')

#-------------------------------------------------------Paint Words---------------------------------------------------------------------       
    def pintar(self,token):
        for last in token:
            if(last[2]=="reservada"):
                posicionInicial = f'{last[0]}.{last[1]-1}'
                print(posicionInicial)
                posicionFinal = f'{posicionInicial}+{len(str(last[3]))}c'
                print(posicionFinal)
                self.text.tag_add('registros', posicionInicial, posicionFinal)
            elif(last[3]=="Entrada"):
                posicionInicial = f'{last[0]}.{last[1]-1}'
                print(posicionInicial)
                posicionFinal = f'{posicionInicial}+{len(str(last[3]))}c'
                print(posicionFinal)
                self.text.tag_add('registros', posicionInicial, posicionFinal)
            else:
                pass
#-------------------------------------------------------Main---------------------------------------------------------------------       
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sin titulo.txt")
    Interfaz(root).pack(side="top", fill="both", expand=True)
    root.mainloop()