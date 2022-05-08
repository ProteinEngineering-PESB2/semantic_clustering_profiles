
from Bio.KEGG import REST

#Se utiliza el módulo REST para hacer peticiones.
#Algunos ejemplos:
#Se listan las vias metabólicas del organismo homo sapiens (hsa).
human_pathways = REST.kegg_list("pathway", "hsa").read()
print(human_pathways)
#Se muestra el detalle de la ruta hsa00010 (glucólisis)
path = REST.kegg_get("path:hsa00010").read()
print(path)
#Se selecciona la primera enzima de la ruta, una hexokinasa y se muestran sus detalles
enzime = REST.kegg_get("ec:2.7.1.1").read()
print(enzime)
#Se selecciona un gen de esta hexokinasa y se muestra su secuencia de aminoácidos. 
sequence = REST.kegg_get("oga:100947200", option="aaseq").read()
print(sequence)
#Se selecciona un gen de esta hexokinasa y se muestra su secuencia de nucleótidos. 
sequence = REST.kegg_get("oga:100947200", option="ntseq").read()
print(sequence)
#Se muestra en qué rutas se encuentra este gen en particular. 
paths = REST.kegg_link("pathway","oga:100947200").read()
print(paths)