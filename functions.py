def getinfo(supermercado, key , max_range=481):
#supermercado = Nombre del supermercado
#key = clave de ScraperApi
#max_range = número máximo de páginas a scrapear (481 = Mercadona)

    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    import time

    scraperapi_key = key

    productos = []
    porcion = []
    kcal = []
    grasa = []
    saturadas = []
    carbs = []
    azucares = []
    sal = []
    prote = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    for page in range(451, max_range):
        url1 = f'https://www.fatsecret.es/calor%C3%ADas-nutrici%C3%B3n/search?q={supermercado}&pg={page}'
        url_ = f'http://api.scraperapi.com?api_key={scraperapi_key}&url={url1}'

        try:
            response = requests.get(url_, headers=headers)
            print(f'Searching in {url_}, {response}')
            if response.status_code != 200:
                print(f"Failed to retrieve page {page}")
                continue
            #Si response no es 200, que no se pare, que continue.

            soup = BeautifulSoup(response.content, 'html.parser')

            # Get productos
            name = soup.find_all(class_="prominent")
            for i in range(len(name)):
                producto = name[i].get_text()
                productos.append(producto)

            # Get links para cada uno de los productos
            links = ['https://www.fatsecret.es' + name[i].get('href') for i in range(len(name))]

            for linkaso in links:
                try:
                    url_product = f'http://api.scraperapi.com?api_key={scraperapi_key}&url={linkaso}'
                    response_macro = requests.get(url_product, headers=headers)
                    print(f'Searching in {url_product}, {response_macro}')
                    if response_macro.status_code != 200:
                        print(f"Failed to retrieve {linkaso}")
                        continue

                    soup_macro = BeautifulSoup(response_macro.content, 'html.parser')

                    # Get porciones Porque no todas son 100g
                    porcion_get = soup_macro.find(class_="serving_size black serving_size_value").get_text()
                    porcion.append(porcion_get)
                    tabla = soup_macro.find(class_="nutrition_facts eu")

                    # Get Kcal porque no está en negrita como los demás macronutrientes
                    kcal_get = tabla.find_all(class_='nutrient left tRight w2')[0].get_text()  # Siempre son Kcal
                    kcal.append(kcal_get)

                    # Get Macros
                    macros = tabla.find_all(class_='nutrient black left tRight w2')
                    grasa.append(macros[1].get_text())
                    saturadas.append(macros[2].get_text())
                    carbs.append(macros[3].get_text())
                    azucares.append(macros[4].get_text())
                    prote.append(macros[5].get_text())
                    sal.append(macros[6].get_text())

                except Exception as e:
                    print(f"Error retrieving macro data for {linkaso}: {e}")
                    #Si nos falla, como el producto está buscado en otro link, que nos apendeé un nulo. 
                    #Si no, el código falla porque las listas tienen tamaños diferentes
                    porcion.append(None)
                    kcal.append(None)
                    grasa.append(None)
                    saturadas.append(None)
                    carbs.append(None)
                    azucares.append(None)
                    prote.append(None)
                    sal.append(None)
                time.sleep(2)  #Para que no nos detecte como bot
        except Exception as e:
            print(f"Error retrieving page {page}: {e}")
        time.sleep(4)  #Para que no nos detecte como bot
     # Asegurarse de que todas las listas tienen la misma longitud
    max_len = max(len(productos), len(porcion), len(kcal), len(grasa), len(saturadas), len(carbs), len(azucares), len(prote), len(sal))
    

    #Por si acaso, no debería pasar, pero por si acaso. 
    #Esto nos asegura que todas tengan la misma lenght añadiendo nulos si no tienen el mismo tamaño las listas. 
    #Si esto pasa hay que rehacer la scrapeada. porque se pueden desordenar pero nos podemos quedar con parte del Dataframe
    def pad_list(lst, max_len):
        return lst + [None] * (max_len - len(lst))

    productos = pad_list(productos, max_len)
    porcion = pad_list(porcion, max_len)
    kcal = pad_list(kcal, max_len)
    grasa = pad_list(grasa, max_len)
    saturadas = pad_list(saturadas, max_len)
    carbs = pad_list(carbs, max_len)
    azucares = pad_list(azucares, max_len)
    prote = pad_list(prote, max_len)
    sal = pad_list(sal, max_len)

    data = pd.DataFrame({
        'Producto': productos,
        'Porcion': porcion,
        'Kcal': kcal,
        'Grasa': grasa,
        'Grasas saturadas': saturadas,
        'Carbohidratos': carbs,
        'Azucares': azucares,
        'Proteina': prote,
        'Sal': sal
    })

    data.to_csv(f'Dataset/Scrap_{supermercado}.csv', index=False)


def prediction(data):
    import pandas as pd
    from sklearn.metrics import pairwise_distances

    #Preguntamos al usuario qué producto quiere seleccionar
    producto = input('Dime un producto: ')
    masca = data['Producto'] == producto

    #Si el producto está duplicado en el Dataframe por estar en varios supermercados:
    macarrones = data[masca]
    if len(macarrones)>1:
        print(macarrones['Supermercado'].unique())
        
        supermercado = input('Selecciona el supermercado del producto comentado:')
         
        mascarilla = (data['Producto'] == producto) & (data['Supermercado'] == supermercado)
    
    #No encontramos producto
    elif len(macarrones) == 0:
        return 'no producto found'
    #Si el producto no tiene dupplicados
    else:
        mascarilla = (data['Producto'] == producto)
    
    fila = data[mascarilla]
    cluster_producto = fila['Cluster_Kmeans'].values[0]

    #Filtramos para quitar el producto del que usuario (también quitamos el mismo producto de otro super, ya de paso seleccionamos el mismo cluster)
    filtrado = data[(data['Cluster_Kmeans'] == cluster_producto) & (data['Producto'] != producto)]

    #elminamos las columnas no numércias.
    filtrado_values = filtrado.drop(columns=['Producto', 'Supermercado', 'Cluster_Kmeans']).values
    fila_values = fila.drop(columns=['Producto', 'Supermercado', 'Cluster_Kmeans']).values

    #Distancias:
    distances = pairwise_distances(fila_values, filtrado_values).flatten()
    ranking = filtrado.copy()
    ranking['Distancia'] = distances

    ranking10 = ranking.sort_values(by='Distancia').head(10)
    print('Productos más similares:')
    return ranking10

def KNN(data):

    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.cluster import KMeans
    from sklearn.metrics import pairwise_distances_argmin_min
    from sklearn.metrics import pairwise_distances
    from sklearn.preprocessing import StandardScaler


    x=data[list(data.drop(columns=['Producto', 'Supermercado']).columns)]
    scaler=StandardScaler()
    x_prep=scaler.fit_transform(x)

    K=range(2, 20)
    inertia=[]
    for k in K:
        kmeans=KMeans(n_clusters=k, random_state=42)
        kmeans.fit(x_prep)
        inertia.append(kmeans.inertia_)

    plt.figure(figsize=(16,8))
    plt.plot(K, inertia, "bx-")
    plt.xlabel("k")
    plt.ylabel("inertia")
    plt.xticks(np.arange(min(K), max(K)+1, 1.0))
    plt.show()

    clst = input('Número clústers:')
    kmeans = KMeans(n_clusters=int(clst), random_state=123)
    kmeans.fit(x_prep)
    cluster = kmeans.predict(x_prep)
    data['Cluster_Kmeans'] = cluster

    return data['Cluster_Kmeans'].value_counts()


def encontrar_productos_similares(producto, dataframe, n=6, cutoff=60):
    from fuzzywuzzy import process
    productos = dataframe['Producto'].tolist()
    coincidencias = process.extract(producto, productos, limit=n)
    coincidencias = [item[0] for item in coincidencias if item[1] >= cutoff]
    return coincidencias
