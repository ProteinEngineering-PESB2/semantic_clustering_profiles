#recibe la fecha y el nombre del directorio
def get_fecha_format(fecha, name_dir):
    fecha_format = ''#variable incializada
    if 'FI' in name_dir:#si dentro del nombre del directorio encuentra a FI hara el formato de yeard con dos digitos
        fecha_format = '%y%m%d'
    else:#no lo encontro, hara el formato de 4 digitos
        fecha_format = '%Y%m%d'
    
    date_time_object = datetime.strptime(fecha, '%Y-%m-%d')#instancia un objeto de datetime con la fecha en el formato de entrada
    fecha_object = dataset_processed.strftime(fecha_format)#obtiene el string que corresponde segun el formato preprocesado
    return fecha_object#retorna el string

#como llamarla
respuesta1 = get_fecha_format('2021-03-01', 'FI') #devolveria 210301
respuesta2 = get_fecha_format('2021-03-01', 'NORM')#devolveria 20210301

dict_data = {
    'REND':{
        'FII':{
            'id_nodo_origen' : 1,
            'filename' : 'Nombre de archivo'
        },
        'FIII':{
            'id_nodo_origen' : 1,
            'filename' : 'Nombre de archivo'
        }
    },
    'NORM':{
        'id_nodo_origen' : 1,
        'filename' : 'Nombre de archivo'
    }
    'MPJ':{
        'id_nodo_origen' : 1,
        'filename' : 'Nombre de archivo'
    }
}