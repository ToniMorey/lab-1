import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import StandardScaler
from sklearn.mixture import GaussianMixture
from fuzzywuzzy import process
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

def generate_warnings(producto, data):
    percentiles = data[['Kcal', 'Grasa', 'Grasas saturadas', 'Carbohidratos', 'Azucares', 'Proteina', 'Sal']].quantile([0.25, 0.75])
    warnings = []
    for column in ['Kcal', 'Grasa', 'Grasas saturadas', 'Azucares', 'Sal']:
        if producto[column].values[0] > percentiles.loc[0.75, column]:
            warnings.append(f'❌ Alto contenido en {column}')
        elif producto[column].values[0] < percentiles.loc[0.25, column]:
            warnings.append(f'✔️ Bajo contenido en {column}')

    for column in ['Proteina']:
        if producto[column].values[0] > percentiles.loc[0.75, column]:
            warnings.append(f'✔️ Alto contenido en {column}')
    
    return warnings

def plot_macros(producto):
    macros = producto[['Grasa', 'Carbohidratos', 'Proteina']].sum(axis=0)
    labels = ['Grasa', 'Carbohidratos', 'Proteina']
    sizes = [macros['Grasa'], macros['Carbohidratos'], macros['Proteina']]
    
    fig, ax = plt.subplots()
    fig.patch.set_facecolor((0.14,0.17,0.23))  # Cambiar el fondo de la figura
    pie = ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    for text in pie[1]:
        text.set_color('white')

    ax.axis('equal')  # Asegurar que el gráfico de pie sea un círculo
    
    return fig

def Predict(producto, data):
    fila_producto = data['Producto'] == producto
    producto_data = data[fila_producto]
    if len(producto_data) > 1 and supermercado:
        mascarilla = (data['Producto'] == producto) & (data['Supermercado'] == supermercado)
    else:
        mascarilla = data['Producto'] == producto

    producto_data = data[mascarilla]

    col1, col2 = st.columns(2)
    warnings = generate_warnings(producto_data, data)
    if warnings:
        col1.write('Resumen nutricional:')
        for warning in warnings:
            col1.write('- ' + warning)
    
    col2.write('Composición nutricional:')
    col2.pyplot(plot_macros(producto_data))

    producto_data.reset_index(drop = True, inplace = True)
    st.dataframe(producto_data.drop(columns = ['Saturada%', 'Azucares%','Cluster_Kmeans']))

    tab1, tab2 = st.tabs(['Recomendacion Saludable', 'Productos similares'])
    # Opción 1: Recomendación. (Score) --> Mirar de los 50 productos más cercanos según pairwise_distance
    tab1.write('### Productos similares más saludables:')
    with tab1:
        fila = data[mascarilla]
        cluster_producto = fila['Cluster_Kmeans'].values[0]
        cat = fila['Categoria'].values[0]

        filtrado = data[(data['Cluster_Kmeans'] == cluster_producto) & (data['Producto'] != producto) & (data['Categoria'] == cat)]
        filtrado_values = filtrado.drop(columns=['Producto', 'Supermercado', 'Cluster_Kmeans', 'Categoria']).values
        fila_values = fila.drop(columns=['Producto', 'Supermercado', 'Cluster_Kmeans', 'Categoria']).values

        # Verificar y reemplazar valores infinitos y NaN
        filtrado_values[np.isinf(filtrado_values)] = 0
        fila_values[np.isinf(fila_values)] = 0
        filtrado_values = np.nan_to_num(filtrado_values, nan=0.0)
        fila_values = np.nan_to_num(fila_values, nan=0.0)

        distances = pairwise_distances(fila_values, filtrado_values).flatten()
        
        filtrado['Distancia'] = distances
        filtrado = filtrado.sort_values(by='Distancia').head(50)
        ranking = filtrado.copy()
        

        nutrient_columns = ['Proteina', 'Grasa', 'Grasas saturadas', 'Carbohidratos', 'Azucares', 'Sal', 'Kcal']

        # Normalizar para los pesos
        scaler = MinMaxScaler()
        ranking[nutrient_columns] = scaler.fit_transform(ranking[nutrient_columns])

        weights = {
            'proteina': 1.5, 
            'grasa': -1,  
            'grasas_saturadas': -2,  
            'carbohidratos': 1,  
            'azucares': -2,  
            'sal': -1.5,  
            'Kcal': -1 }
        filtrado['score_salud'] = (
            weights['proteina'] * ranking['Proteina'] +
            weights['grasa'] * ranking['Grasa'] +
            weights['grasas_saturadas'] * ranking['Grasas saturadas'] +
            weights['carbohidratos'] * ranking['Carbohidratos'] +
            weights['azucares'] * ranking['Azucares'] +
            weights['sal'] * ranking['Sal'] +
            weights['Kcal'] * ranking['Kcal'])
        
        ranking10 = filtrado.sort_values(by='score_salud', ascending = False).head(10)
        ranking10 = ranking10.reset_index(drop = True)
        
        st.dataframe(ranking10.drop(columns=['Categoria','Saturada%','Azucares%','Cluster_Kmeans','Distancia','score_salud']))

    # Opción 2: Productos nutricionalmente similares (GMM)
    tab2.write('### Productos más similares:')
    with tab2:
        X = data.drop(['Producto', 'Supermercado', 'Categoria', 'Sal', 'Kcal', 'Cluster_Kmeans','Grasas saturadas','Azucares'], axis=1)
        min_samples = 2 * len(X.columns)
        k = min_samples

        scaler = StandardScaler()
        scaler.fit(X)

        X_scaled = scaler.transform(X)

        X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)
        model = GaussianMixture(n_components=k)
        model.fit(X_scaled_df)
        clusters = model.predict(X_scaled_df)
        data['Cluster_GMM'] = clusters

        fila = data[mascarilla]
        cluster_producto = fila['Cluster_GMM'].values[0]

        filtrado = data[(data['Cluster_GMM'] == cluster_producto) & (data['Producto'] != producto)]
        filtrado_values = filtrado.drop(columns=['Producto', 'Supermercado', 'Cluster_Kmeans', 'Categoria', 'Cluster_GMM']).values
        fila_values = fila.drop(columns=['Producto', 'Supermercado', 'Cluster_Kmeans', 'Categoria', 'Cluster_GMM']).values

        # Verificar y reemplazar valores infinitos y NaN
        filtrado_values[np.isinf(filtrado_values)] = 0
        fila_values[np.isinf(fila_values)] = 0
        filtrado_values = np.nan_to_num(filtrado_values, nan=0.0)
        fila_values = np.nan_to_num(fila_values, nan=0.0)

        distances = pairwise_distances(fila_values, filtrado_values).flatten()
        ranking = filtrado.copy()
        ranking['Distancia'] = distances

        ranking10 = ranking.sort_values(by='Distancia').head(10)
        ranking10 = ranking10.reset_index(drop = True)
        
        st.dataframe(ranking10.drop(columns=['Categoria', 'Cluster_GMM','Saturada%','Distancia','Azucares%','Cluster_Kmeans']))

# Streamlit UI
st.set_page_config(page_title='NutriFacts', page_icon=':pineapple:')
st.title('Recomendador de productos :pineapple:')

# Cargar datos
data = pd.read_excel('Dataset/Data_clust.xlsx')  # CAMBIAR POR EL DATASET REAL.

data = data.reindex(columns=['Producto', 'Kcal', 'Proteina', 'Grasa','Grasas saturadas', 'Saturada%', 'Carbohidratos','Azucares', 'Azucares%', 'Sal', 'Supermercado', 'Cluster_Kmeans', 'Categoria'])

numer = data.select_dtypes(float)
for i in list(numer.columns):
    data[i] = data[i].round(1)

# Entrada del usuario
producto_input = st.text_input('Empieza escribiendo un producto:')

if producto_input:
    lista_productos = data['Producto'].tolist()
    coincidencias = process.extract(producto_input, lista_productos, limit=10)
    coincidencias = [item[0] for item in coincidencias if item[1] >= 60]

    if coincidencias:
        producto = st.selectbox('Te refieres a alguno de estos productos?', coincidencias)

        macarrones = data[data['Producto'] == producto]
        if len(macarrones) > 1:
            supermercados = macarrones['Supermercado'].unique()
            supermercado = st.selectbox('Tenemos el mismo producto en varios supermercados, ¿cuál de ellos quieres ver?:', supermercados)

        if st.button('Ver productos'):
            Predict(producto, data)
    else:
        st.write("No se encontraron coincidencias suficientes. Por favor, intente con otro producto.")