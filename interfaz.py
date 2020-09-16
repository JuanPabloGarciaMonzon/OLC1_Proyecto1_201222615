import os
import sys
import platform
import re
import Lexico_JS
import Lexico_RMT
from error_report import errorList
from css_report import stateList
from rmt_report import rmtList
from Sintactico_RMT import syn_RMT
from Lexico_CSS import lex_CSS
from Lexico_HTML import lex_HTML
#To display pdfs
import webbrowser
#Interface toolkit of python tk interface
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

#Custom text is for painting colors in a text area
from CustomText import CustomText
#For managing the Line Numbers in the text area
from TextLine import TextLineNumbers

class Interfaz(tk.Frame):
    def __init__(self, *args, **kwargs):
        self.root = root
        tk.Frame.__init__(self, *args, **kwargs)

        self.filename = None

        self.terminal = tk.Text(root, width=45, height=1, background="black",foreground="#00AA00")
        self.terminal.pack(side="right", fill="both", expand=True)

        # Special Text
        self.ter = tk.Scrollbar(orient="vertical", command=self.terminal.yview)
        self.terminal.configure(yscrollcommand=self.ter.set)
        self.ter.pack(side="right", fill="y")

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

        report_dropdown.add_command(label="Reporte de Errores Lexicos", command=self.errorReport)
        report_dropdown.add_command(label="Reporte de Grafos de JS", command=self.js_report)
        report_dropdown.add_command(label="Reporte de Estados de CSS", command=self.state_report)
        report_dropdown.add_command(label="Reporte de Errores Sintacticos de RMT", command=self.rmt_report)
        
        help_dropdown.add_command(label="Acerca de", command=self.about)
        help_dropdown.add_command(label="Manual de Usuario", command=self.m_user)
        help_dropdown.add_command(label="Manual Técnico", command=self.m_tecnic)

        menubar.add_cascade(label="Archivo", menu=file_dropdown)
        menubar.add_cascade(label="Ejecutar", menu=run_dropdown)
        menubar.add_cascade(label="Reportes", menu=report_dropdown)
        menubar.add_cascade(label="Ayuda", menu=help_dropdown)
#-------------------------------------------------------Color Tags for the Paint Method---------------------------------------------------------------------
        self.text.tag_configure("reserved", foreground="red")
        self.text.tag_configure("var", foreground="#008000")
        self.text.tag_configure("int", foreground="#0000FF")
        self.text.tag_configure("boolean", foreground="#0000FF")
        self.text.tag_configure("string", foreground="#FFFF00")
        self.text.tag_configure("comment", foreground="#808080")
        self.text.tag_configure("operator", foreground="#FFA500")
#-------------------------------------------------------Line Number Method---------------------------------------------------------------------
    def _on_change(self, event):
        self.linenumbers.redraw()
        self.text.tag_remove('resaltado', '1.0', tk.END)
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
        rmt = Lexico_RMT.lex_RMT()
        css = lex_CSS()
        html = lex_HTML()
        txt = self.text.get(1.0, tk.END)
        self.terminal.delete(1.0, tk.END)
        if(entrada == "JS"):
            sys.setrecursionlimit(100000)                                                    
            js.cadena = txt
            js.receive_input()            
            self.terminal.insert(tk.INSERT,"----------------------------------------Tokens--------------------------------\n")
            self.terminal.insert(tk.END,str(js.token_output).replace("],", "\n").replace("[[","[").replace("]]","\n").replace("[","").replace("\\n","").replace("None,","").replace("None",""))
            self.terminal.insert(tk.END,"----------------------------------------Errors--------------------------------\n")
            self.terminal.insert(tk.END,str(js.error_output).replace("],", "\n").replace("[[","[").replace("]]","\n").replace("[",""))
            self.error(js.error_list,"JS")
            self.pintar(js.token_output)
            if(str(txt).__contains__("PATHW:")):
                self.get_direction("PATHW:",js.clean)
                if(str(txt).__contains__("PATHL:")):
                    self.get_direction("PATHL:",js.clean)

        elif(entrada == "CSS"):                                              
            css.cadena = txt
            css.receive_input()            
            self.terminal.insert(tk.INSERT,"----------------------------------------Tokens--------------------------------\n")
            self.terminal.insert(tk.END,str(css.token_output).replace("],", "\n").replace("[[","[").replace("]]","\n").replace("[","").replace("\\n","").replace("None,","").replace("None",""))
            self.terminal.insert(tk.END,"----------------------------------------Errors--------------------------------\n")
            self.terminal.insert(tk.END,str(css.error_output).replace("],", "\n").replace("[[","[").replace("]]","\n").replace("[",""))       
            self.error(css.error_list,"CSS")
            self.css_state(css.state_list,"CSS")
            self.pintar(css.token_output)
            if(str(txt).__contains__("PATHW:")):
                self.get_direction("PATHW:",css.clean)
                if(str(txt).__contains__("PATHL:")):
                    self.get_direction("PATHL:",css.clean)

        elif(entrada == "HTML"):                                      
            html.cadena = txt
            html.receive_input()        
            self.terminal.insert(tk.INSERT,"----------------------------------------Tokens--------------------------------\n")
            self.terminal.insert(tk.END,str(html.token_output).replace("],", "\n").replace("[[","[").replace("]]","\n").replace("[","").replace("\\n","").replace("None,","").replace("None",""))
            self.terminal.insert(tk.END,"----------------------------------------Errors--------------------------------\n")
            self.terminal.insert(tk.END,str(html.error_output).replace("],", "\n").replace("[[","[").replace("]]","\n").replace("[",""))
            self.error(html.error_list,"HTML")
            self.pintar(html.token_output)
            if(str(txt).__contains__("PATHW:")):
                self.get_direction("PATHW:",html.clean)
                if(str(txt).__contains__("PATHL:")):
                    self.get_direction("PATHL:",html.clean)

        elif(entrada == "RMT"):                                              
            rmt.cadena = txt
            rmt.receive_input()            
            self.terminal.insert(tk.INSERT,"----------------------------------------Tokens--------------------------------\n")
            self.terminal.insert(tk.END,str(rmt.token_output).replace("],", "\n").replace("[[","[").replace("]]","\n").replace("[","").replace("\\n","").replace("None,","").replace("None",""))
            self.terminal.insert(tk.END,"----------------------------------------Errors--------------------------------\n")
            self.terminal.insert(tk.END,str(rmt.error_output).replace("],", "\n").replace("[[","[").replace("]]","\n").replace("[",""))
            self.error(rmt.error_list,"RMT")
            self.pintar(rmt.token_output)
            syn = syn_RMT(rmt.token_output)
            self.rmt_lines(syn.errorList,"RMT")
            if(str(txt).__contains__("PATHW:")):
                self.get_direction("PATHW:",html.clean)
                if(str(txt).__contains__("PATHL:")):
                    self.get_direction("PATHL:",rmt.clean)

        else:
            box_tilte ="Execution Error"
            box_msg = "Por favor revise que el archivo que haya abierto sea JS, CSS, HTML o RMT"
            messagebox.showerror(box_tilte,box_msg)            
#-------------------------------------------------------Help Menu Methods---------------------------------------------------------------------
    def about(self):
        box_tilte ="Autor"
        box_msg = "Juan Pablo García Monzón 2012-22615"
        messagebox.showinfo(box_tilte,box_msg)

    def m_user(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        direction = script_dir + "\\Manuales\\Manual de Usuario.pdf" 
        try:
            webbrowser.open_new(r'file://'+direction)
        except Exception as e:
            box_tilte ="Path Error"
            box_msg = "El archivo que trata de acceder no existe"
            messagebox.showerror(box_tilte,box_msg)
        
    def m_tecnic(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        direction = script_dir + "\\Manuales\\Manual Tecnico.pdf"
        try:
            webbrowser.open_new(r'file://'+direction)
        except Exception as e:
            box_tilte ="Path Error"
            box_msg = "El archivo que trata de acceder no existe"
            messagebox.showerror(box_tilte,box_msg)
#-------------------------------------------------------Descision Module Methods---------------------------------------------------------------------
    def verify_path(self):
        if self.filename == None:
            box_tilte ="File Extension Error"
            box_msg = "Por favor abra un archivo JS, CSS, HTML o RMT antes de analizar o escriba un archivo y guardelo con una de esas extensiones"
            messagebox.showerror(box_tilte,box_msg)
        else:
            self.path_module(self.filename)

    def path_module(self,entrada):
        if(os.path.exists(entrada)):
            var_split = os.path.splitext(entrada)[1][1:]
            self.decision_module(var_split)
        else:
            box_tilte ="Path File Error"
            box_msg = "Archivo de entrada no existe"
            messagebox.showerror(box_tilte,box_msg)
               
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
    def get_direction(self,entrada,clean):
        txt = self.text.get(1.0, tk.END)
        sistema = platform.system()
        if(entrada == "PATHW:" and sistema == "Windows"):
            path = txt.split("PATHW:")
            direction = path[1].split("\n")
            self.create_file(direction[0].replace("*/","").replace("-->","").replace("*","").replace(" ","").replace(">","").replace("?","").replace("<","").replace("|","").replace("\"",""),clean)                        
        elif(entrada == "PATHL:" and sistema == "Linux"):
            path = txt.split("PATHL:")
            direction = path[1].split("\n")
            self.create_file(direction[0].replace("*/","").replace("-->","").replace("*","").replace(" ","").replace(">","").replace(":","").replace("?","").replace("<","").replace("|","").replace("\"",""),clean)              
        else:
            box_tilte ="Operative System Error"
            box_msg = "La carpeta que esta tratando de crear no es el formato correcto en el sistema operativo en el que se encuentra actualmente"
            messagebox.showerror(box_tilte,box_msg)

    def create_file(self,direccion,clean):
        var_split = os.path.splitext(self.filename)[1][1:]
        if (os.path.exists(direccion)):
            try:
                os.chdir(direccion.replace("\\","/"))
                if(var_split=="js"):                    
                    fic = open(direccion+"file.js", "w")     
                    fic.write(clean)    
                    fic.close()
                elif(var_split=="css"):                    
                    fic = open(direccion+"file.css", "w")     
                    fic.write(clean)    
                    fic.close()
                elif(var_split=="html"):                    
                    fic = open(direccion+"file.html", "w")     
                    fic.write(clean)    
                    fic.close()
                elif(var_split=="rmt"):                    
                    fic = open(direccion+"file.rmt", "w")     
                    fic.write(clean)    
                    fic.close()
                else:
                    pass
            except Exception as e:
                box_tilte ="Path Error"
                messagebox.showerror(box_tilte,e)
        else:
            try:
                os.makedirs(direccion.replace("\\","/"))
                if(var_split=="js"):                    
                    fic = open(direccion+"file.js", "w")     
                    fic.write(clean)    
                    fic.close()
                elif(var_split=="css"):                    
                    fic = open(direccion+"file.css", "w")     
                    fic.write(clean)    
                    fic.close()
                elif(var_split=="html"):                    
                    fic = open(direccion+"file.html", "w")     
                    fic.write(clean)    
                    fic.close()
                elif(var_split=="rmt"):                    
                    fic = open(direccion+"file.rmt", "w")     
                    fic.write(clean)    
                    fic.close()
                else:
                    pass
            except Exception as e:
                box_tilte ="New Path Error"
                messagebox.showerror(box_tilte,e)
#-------------------------------------------------------Reports---------------------------------------------------------------------       
    def error(self,entrada,tipo):
        if(len(entrada)==0):
            box_tilte = "Tabla de Errores"
            box_msg = "No existe ningun error"
            messagebox.showinfo(box_tilte, box_msg)
        else:
            errorList(entrada,tipo)

    def errorReport(self):
        error_script_dir = os.path.dirname(os.path.abspath(__file__))
        print("DIR:"+error_script_dir)
        report_dir = error_script_dir + "\\Reportes\\errorList.html"
        print("DIRECCION:"+report_dir)
        if(os.path.exists(report_dir)):
            webbrowser.open_new(r'file://' + report_dir)
        else:
            print(report_dir)
            box_tilte = "Report Error"
            box_msg = "El archivo del reporte no existe"
            messagebox.showinfo(box_tilte, box_msg)       

    def css_state(self,entrada,tipo):
        if(len(entrada)==0):
            box_tilte = "Reporte de estados"
            box_msg = "No existe ningun estado"
            messagebox.showinfo(box_tilte, box_msg)
        else:
            stateList(entrada,tipo)

    def state_report(self):
        state_script_dir = os.path.dirname(os.path.abspath(__file__))
        report_dir = state_script_dir + "\\Reportes\\css_states.html"
        if(os.path.exists(report_dir)):
            webbrowser.open_new(r'file://' + report_dir)
        else:
            box_tilte = "Report Error"
            box_msg = "El archivo del reporte no existe"
            messagebox.showinfo(box_tilte, box_msg)

    def rmt_lines(self,entrada,tipo):
        if(len(entrada)==0):
            box_tilte = "Reporte de RMT"
            box_msg = "No existe ninguna linea"
            messagebox.showinfo(box_tilte, box_msg)

        else:
            rmtList(entrada,tipo)

    def rmt_report(self):
        rmt_script_dir = os.path.dirname(os.path.abspath(__file__))
        report_dir = rmt_script_dir + "\\Reportes\\rmt.html"
        if(os.path.exists(report_dir)):
            webbrowser.open_new(r'file://' + report_dir)
        else:
            box_tilte = "Report Error"
            box_msg = "El archivo del reporte no existe"
            messagebox.showinfo(box_tilte, box_msg)

    def js_report(self):
        js_script_dir = os.path.dirname(os.path.abspath(__file__))
        String = js_script_dir + "\\Grafos\\String.gv.pdf"
        Unicomentario = js_script_dir + "\\Grafos\\UniComentario.gv.pdf"
        ID = js_script_dir + "\\Grafos\\ID.gv.pdf"
        try:
            webbrowser.open_new(r'file://' + String)
            webbrowser.open_new(r'file://' + Unicomentario)
            webbrowser.open_new(r'file://' + ID)
        except Exception as e:
            box_tilte = "Report Error"
            messagebox.showinfo(box_tilte, e)           
#-------------------------------------------------------Paint Words---------------------------------------------------------------------       
    def pintar(self,token):
        for last in token:
            if(last[0]!=None):
                if(last[2]=="reservada"):
                    posicionInicial = f'{last[0]}.{last[1]-1}'
                    posicionFinal = f'{posicionInicial}+{len(str(last[3]))}c'
                    self.text.tag_add('reserved', posicionInicial, posicionFinal)

                elif(last[3].lower()=="var"):
                    posicionInicial = f'{last[0]}.{last[1]-1}'
                    posicionFinal = f'{posicionInicial}+{len(str(last[3]))}c'
                    self.text.tag_add('var', posicionInicial, posicionFinal)

                elif(last[2].lower()=="string"):
                    posicionInicial = f'{last[0]}.{last[1]-1}'
                    posicionFinal = f'{posicionInicial}+{len(str(last[3]))}c'
                    self.text.tag_add('string', posicionInicial, posicionFinal)

                elif(last[2].lower()=="TAG"):
                    posicionInicial = f'{last[0]}.{last[1]-1}'
                    posicionFinal = f'{posicionInicial}+{len(str(last[3]))}c'
                    self.text.tag_add('string', posicionInicial, posicionFinal)

                elif(last[2].lower()=="integer"):
                    posicionInicial = f'{last[0]}.{last[1]-1}'
                    posicionFinal = f'{posicionInicial}+{len(str(last[3]))}c'
                    self.text.tag_add('int', posicionInicial, posicionFinal)

                elif(last[2].lower()=="decimal"):
                    posicionInicial = f'{last[0]}.{last[1]-1}'
                    posicionFinal = f'{posicionInicial}+{len(str(last[3]))}c'
                    self.text.tag_add('int', posicionInicial, posicionFinal)

                elif(last[3].lower()=="true" or last[3].lower()=="false"):
                    posicionInicial = f'{last[0]}.{last[1]-1}'
                    posicionFinal = f'{posicionInicial}+{len(str(last[3]))}c'
                    self.text.tag_add('boolean', posicionInicial, posicionFinal)

                elif(last[2].lower()=="comentario"):
                    posicionInicial = f'{last[0]}.{last[1]-1}'
                    posicionFinal = f'{posicionInicial}+{len(str(last[3]))}c'
                    self.text.tag_add('comment', posicionInicial, posicionFinal)

                elif(last[2].lower()=="operador"):
                    posicionInicial = f'{last[0]}.{last[1]-1}'
                    posicionFinal = f'{posicionInicial}+{len(str(last[3]))}c'
                    self.text.tag_add('operator', posicionInicial, posicionFinal)

                elif(last[2].upper()=="PARA"):
                    posicionInicial = f'{last[0]}.{last[1]-1}'
                    posicionFinal = f'{posicionInicial}+{len(str(last[3]))}c'
                    self.text.tag_add('operator', posicionInicial, posicionFinal)

                elif(last[2].upper()=="PARC"):
                    posicionInicial = f'{last[0]}.{last[1]-1}'
                    posicionFinal = f'{posicionInicial}+{len(str(last[3]))}c'
                    self.text.tag_add('operator', posicionInicial, posicionFinal)

                elif(last[2].upper()=="POR"):
                    posicionInicial = f'{last[0]}.{last[1]-1}'
                    posicionFinal = f'{posicionInicial}+{len(str(last[3]))}c'
                    self.text.tag_add('operator', posicionInicial, posicionFinal)

                elif(last[2].upper()=="DIV"):
                    posicionInicial = f'{last[0]}.{last[1]-1}'
                    posicionFinal = f'{posicionInicial}+{len(str(last[3]))}c'
                    self.text.tag_add('operator', posicionInicial, posicionFinal)

                elif(last[2].upper()=="MAS"):
                    posicionInicial = f'{last[0]}.{last[1]-1}'
                    posicionFinal = f'{posicionInicial}+{len(str(last[3]))}c'
                    self.text.tag_add('operator', posicionInicial, posicionFinal)

                elif(last[2].upper()=="MENOS"):
                    posicionInicial = f'{last[0]}.{last[1]-1}'
                    posicionFinal = f'{posicionInicial}+{len(str(last[3]))}c'
                    self.text.tag_add('operator', posicionInicial, posicionFinal)

                else:
                    pass
            else:
                pass
#-------------------------------------------------------Main---------------------------------------------------------------------       
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sin titulo.txt")
    Interfaz(root).pack(side="top", fill="both", expand=True)
    root.mainloop()