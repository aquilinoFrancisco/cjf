def dfs(graph, start, end, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []

    visited.add(start)
    path.append(start)

    if start == end:
        return path

    if start in graph:
        for neighbor in graph[start]:
            if neighbor not in visited:
                new_path = dfs(graph, neighbor, end, visited, path)
                if new_path:
                    return new_path

    path.pop()
    visited.remove(start)
    return None

# Constructing the list and relations
entidades=["Principio de Contradicción","Sentencia 338/2018","Juez de Amparo","Tribunal Colegiado","Auto de Vinculación a Proceso","Juez de Control",
"Organo Jurisdiccional","Juzgado de Control","Juzgado de Distrito","Norma Convencional que contempla justa indemnizacion","Sentencia 423/2019","Autoridad Jurisdiccional","Suprema Corte de Justicia de la Nación","Artículo 63.1 Convención Americana sobre Derechos Humanos","Norma Convencional","Prisión Preventiva Oficiosa"]
nodos=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

relaciones = {nodos:entidades for (nodos,entidades) in zip(nodos,entidades)}
relaciones2 = {entidades:nodos for (entidades,nodos) in zip(entidades,nodos)}

# Constructing the graph from the list of connections
connections = [(1, 2), (3, 4), (5, 6), (7, 6), (8, 2), (9, 2), (10, 11),
               (12, 13), (7, 3), (10, 14), (3, 9), (4, 2), (10, 15),
               (16, 7), (12, 7)]

graph = {}
for item1, item2 in connections:
    if item1 not in graph:
        graph[item1] = []
    if item2 not in graph:
        graph[item2] = []
    graph[item1].append(item2)
    graph[item2].append(item1)

# Example usage
start_element = relaciones2["Principio de Contradicción"]
end_element = relaciones2["Auto de Vinculación a Proceso"]
path = dfs(graph, start_element, end_element)

relaciones3=[]
if path!=None:
    for i in path:
        relaciones3.append(relaciones[i])
else:
  relaciones3="**** NO EXISTE CONEXION ENTRE LOS ELEMENTOS INGRESADOS ****"

print(f"Lista de elementos que integran la ruta de conexión entre el {relaciones[start_element]} y el {relaciones[end_element]}: {relaciones3}")