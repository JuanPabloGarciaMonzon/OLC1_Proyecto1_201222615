class errorList:
    def __init__(self, list):
        if len(list) > 0:
            try:
                file = open('errorList.html', 'w')
                if file:
                    file.write('<center><table border="4">')
                    file.write('<tr>'
                               '<td>' + 'Posicion' + '</td>'
                                                             '<td>' + 'Descripcion' + '</td>'
                                                                                      '<td>')
                    for error in list:
                        file.write('<tr>'
                                   '<td>' + str(list[error]['pos']) + '</td>'
                                                                                                           '<td>' + str(
                            list[error]['Descripcion']) + '</td>'
                                                                                                    '</tr>')
                    file.write('</table></center>')
                file.close()
                print('Tabla de errores generada')
            except Exception as e:
                file.close()
                print(e)
