import os
class errorList:
    def __init__(self, list,tipo):

        if len(list) > 0:

            script_dir = os.path.dirname(os.path.abspath(__file__))
            direction = script_dir + "/Reportes/errorList.html"
            try:
                try:
                    os.remove(direction)
                except Exception as e:
                    print("Error borrando archivo de reportes de errores,ya que no existe")
                
                file = open(direction, 'w')
                if file:
                    file.write('<center><table border="4">')
                    file.write(
                        '<h1>' + 'Errores Lexicos de'+" "+tipo +'</h1>'
                        '<tr>'
                                  
                       '<td>' + 'No.' +    '</td>'
                       '<td>' + 'Linea' + '</td>'
                       '<td>' + 'Columna' +    '</td>'
                       '<td>' + 'Descripcion' + '</td>'
                                                                                      
                    '</tr>')
                    for error in list:
                        file.write(
                            '<tr>'
                            
                            '<td>' + str(list[error]['count']) + '</td>'
                            '<td>' + str(list[error]['line']) + '</td>'
                            '<td>' + str(list[error]['column']) + '</td>'
                            '<td>' + str(list[error]['Descripcion']) + '</td>'
                            
                            '</tr>')
                    file.write('</table></center>')
                file.close()
                print('Tabla de errores generada')
            except Exception as e:
                print("Error al abrir el archivo de reporte de errores lexicos")
