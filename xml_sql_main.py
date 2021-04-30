'''
    1º Necesita una carpeta de la cual sacar los archivos .xml
    2º Necesita una carpeta a la cual exportar el archivo .csv
    Sintaxis:
        from xml_sql_main import xml_sql    =   Importa el modulo
        xml_sql.xml_csv()        =   Uso de las funciones
        xml_sql.borrar_tabla()
        xml_sql.crear_tabla()
        datos = xml_sql.upload()
        xml_sql.subir(datos)
        consulta()
'''
class xml_sql():

    def xml_csv(ruta='entrada', ruta2='salida'):
        # Importa los datos de un xml y los exporta a un csv.
        def org_xml(ruta):
            from xml.dom import minidom
            import os
            # Coge el nombre de los archivos del directorio.
            archivos = os.listdir(ruta)
            # Definir listas para luego usarlas.
            common_list = []
            botanical_list = []
            zone_list = []
            light_list = []
            price_list = []
            avai_list = []
            dic = {}
            # Bucle que separa por nombre los archivos para ejecutar las acciones.
            for archivo in archivos:
                # Lee los archivos y guarda los valores en las variables.
                xml = minidom.parse(ruta+'/'+archivo)
                docs = xml.getElementsByTagName('PLANT')
                # Guarda el valor de cada etiqueta en una lista diferente.
                for doc in docs:
                    common = doc.getElementsByTagName('COMMON')[0]
                    common_list.append(common.firstChild.data)
                    botanical = doc.getElementsByTagName('BOTANICAL')[0]
                    botanical_list.append(botanical.firstChild.data)
                    zone = doc.getElementsByTagName('ZONE')[0]
                    zone_list.append(zone.firstChild.data)
                    light = doc.getElementsByTagName('LIGHT')[0]
                    light_list.append(light.firstChild.data)
                    price = doc.getElementsByTagName('PRICE')[0]
                    price_list.append(price.firstChild.data)
                    avai = doc.getElementsByTagName('AVAILABILITY')[0]
                    avai_list.append(avai.firstChild.data)
                # Añade al diccionario cada lista.
                dic['COMMON']=(common_list)
                dic['BOTANICAL']=(botanical_list)
                dic['ZONE']=(zone_list)
                dic['LIGHT']=(light_list)
                dic['PRICE']=(price_list)
                dic['AVAILABILITY']=(avai_list)
            # Devuelve la variable dic.
            return dic
        dic = org_xml('entrada')
        def exp_csv(ruta2,datos):
            import pandas as pd
            # Exporta el diccionario dic a un archivo .csv
            df = pd.DataFrame(datos)
            df.reset_index().to_csv('salida/export.csv', header=False, index=False)
        exp_csv(ruta2,dic)

    def crear_tabla():
        import mysql.connector
        connect = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            db='init'
        )
        cursor = connect.cursor()
        try:
            # Crea una nueva tabla vacia.
            Tabla_de_plantas =  'CREATE TABLE tabla_de_plantas(id INT AUTO_INCREMENT PRIMARY KEY, COMMON TEXT, BOTANICAL TEXT, ZONE TEXT, LIGHT TEXT, PRICE TEXT, AVAILABILITY TEXT)'
            cursor.execute(Tabla_de_plantas)
            connect.close() 
        except:
            print('Ya está creada la tabla')
            connect.close() 
    
    def borrar_tabla():
        import mysql.connector
        connect = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            db='init'
        )
        cursor = connect.cursor()
        # Borra la tabla, por si tiene algun dato.
        BorrarTabla = "DROP TABLE IF EXISTS tabla_de_plantas;"
        cursor.execute(BorrarTabla)
        connect.close() 

    def upload():
        import pandas as pd
        # Importa los datos del csv exportado anteriormente.
        # Y crea una variable nueva con los datos ordenados.
        datos = [pd.read_csv('./salida/export.csv', header=0)]
        datos = str(datos)
        datos = datos.split('\n')
        lista_data=[] 
        for data in datos:
            data = data.split(' ')
            list_data=[]
            for datas in data:
                if datas != '':
                    list_data.append(datas)
            lista_data.append(list_data[2:10])
        # Devuelve la variable nueva con los valores ordenados.
        return lista_data
        
    def subir(datos):
        import mysql.connector
        connect = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            db='init'
        )
        cursor = connect.cursor()
        sql = 'insert into tabla_de_plantas(COMMON, BOTANICAL, ZONE, LIGHT, PRICE, AVAILABILITY) values(%s,%s,%s,%s,%s,%s)'
        for data in datos:
            print(data)
            cursor.execute(sql, data)
        connect.commit()
        connect.close()  

def consulta():
    import mysql.connector
    connect = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            db='init'
        )
    cursor = connect.cursor()
    try:
        cursor.execute('SELECT * FROM tabla_de_plantas')
        plantas = cursor.fetchall()
        for planta in plantas:
            print(planta)
        connect.close()
    except:
        print('Ha habido algún error.')
        connect.close() 
        input()