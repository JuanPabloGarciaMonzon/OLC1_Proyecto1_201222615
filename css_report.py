import os
class stateList:
    def __init__(self, list,tipo):

        if len(list) > 0:

            script_dir = os.path.dirname(os.path.abspath(__file__))
            direction = script_dir + "\\Reportes\\css_states.html"
            try:
                try:
                    os.remove(direction)
                except Exception as e:
                    print("Error borrando archivo de reportes de estados,ya que no existe")
                
                file = open(direction, 'w')
                if file:
                    file.write('<center><table border="4">')
                    file.write(
                        '<h1>' + 'Reporte de estados de' + " "+tipo +'</h1>'
                        '<tr>'
                                  
                       '<td>' + 'No.' +    '</td>'
                       '<td>' + 'Estado' + '</td>'
                       '<td>' + 'Token' +    '</td>'
                                                                                      
                    '</tr>')
                    for state in list:
                        file.write(
                            '<tr>'
                            
                            '<td>' + str(list[state]['count']) + '</td>'
                            '<td>' + str(list[state]['estado']) + '</td>'
                            '<td>' + str(list[state]['token']) + '</td>'
                            
                            '</tr>')
                    file.write('</table></center>')
                file.close()
                print('Tabla de errores generada')
            except Exception as e:
                print("Error al abrir el archivo de reporte de errores lexicos")
