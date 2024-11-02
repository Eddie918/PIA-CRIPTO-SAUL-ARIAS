#importamos las librerias necesarias para el funcionamiento del programa
import streamlit as st
import numpy as np
import math


#declaramos las funciones necesarias para el algoritmo RSA
def mcd(a,b):
    if b == 0:
        return a
    else:
        return mcd(b, a%b)
    
def is_prime(n):
    if n <= 1:
        return False
    else:
        for i in range((2), int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

def generar_num_primo():
    num = np.random.randint(2, 10000)
    while is_prime(num) == False:
        num = np.random.randint(2, 10000)
    return num

def generar_claves():
    p = generar_num_primo()
    q = generar_num_primo()
    while p == q:
        q = generar_num_primo()
    n = p*q
    phi = (p-1)*(q-1)
    #encontrar un exponente publico e | 1 < e < phi
    e = np.random.randint(2,phi)
    while mcd(e,phi) != 1:
        e = np.random.randint(2,phi)
    #encontrar un exponente privado d (inverso multiplicativo  de e mod phi)
    d = pow(e,-1,phi) #d = e^-1 mod phi
    return ((e,n),(d,n))

def cifrar(message, public_key):
    e, n = public_key
    cipher = [hex(pow(ord(char), e, n)) for char in message]
    return ' '.join(cipher)

def descifrar(cipher, private_key):
    d, n = private_key
    plain = ''.join([chr(pow(int(char, 16), d, n)) for char in cipher.split()])
    return plain


alfabeto = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZabcdefghijklmnñopqrstuvwxyz"


def cifrado_cesar(message, desplazamiento):
    cifrado = ""
    for char in message:
        if char in alfabeto:
            cifrado += alfabeto[(alfabeto.index(char) + desplazamiento) % len(alfabeto)]
        else:
            cifrado += char
    return cifrado

def descrifrado_cesar(cifrado, desplazamiento):
    return cifrado_cesar(cifrado, -desplazamiento)


    

# Diseño de streamlit para la interfaz gráfica
st.set_page_config(page_title="Proyecto Integrador de Criptografía", page_icon="🔐", layout="centered")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
        
        /* Fondo principal en negro */
        body {
            background-color: #000000;
            color: #d3d3d3; 
            font-family: 'Montserrat', sans-serif;
        }

        /* Contenedor principal */
        .main-container {
            background-color: #1a1a1a; 
            padding: 30px; 
            border-radius: 15px; 
            box-shadow: 0 0 15px rgba(255, 255, 255, 0.2);
        }

        /* Botones estándar */
        .stButton>button {
            background-color: #007acc; /* Azul elegante */
            color: #ffffff; /* Texto en blanco */
            font-size: 16px;
            font-weight: 600;
            border-radius: 8px;
            padding: 12px 24px; 
            border: none;
            width: 100%;
            box-shadow: 0px 4px 10px rgba(0, 122, 204, 0.5);
            transition: background-color 0.3s ease, transform 0.2s ease;
        }
        .stButton>button:hover {
            background-color: #005b99; /* Azul más oscuro */
            transform: translateY(-3px);
            box-shadow: 0px 6px 12px rgba(0, 91, 153, 0.6);
        }

        /* Inputs de texto */
        .stTextInput>div>div>input, .stNumberInput>div>div>input {
            background-color: #2c2c2c;
            color: #ffffff;
            border-radius: 8px;
            padding: 12px;
            border: 1px solid #555;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.5);
        }

        /* Títulos */
        h1, h2, h3 {
            color: #ffffff; /* Blanco */
            text-align: center;
            font-weight: 700;
        }
        
        /* Texto de ayuda y subtítulos */
        .stMarkdown p, .stMarkdown h4 {
            color: #bfbfbf;
            font-weight: 500;
        }

        /* Estilo de barra lateral */
        .css-1d391kg {
            background-color: #000000;
            color: #d3d3d3;
        }

        /* Mensajes de advertencia y resultado */
        .stAlert {
            background-color: #333333;
            border-radius: 10px;
            padding: 12px;
            color: #d3d3d3;
        }
    </style>
""", unsafe_allow_html=True)



# Inicializar claves en la sesión de Streamlit
if "public_key" not in st.session_state or "private_key" not in st.session_state:
    st.session_state["public_key"], st.session_state["private_key"] = None, None

# Título y bienvenida
st.title("Proyecto Integrador para la Materia de Criptografía")
st.header("🔑 Algoritmo RSA y Cifrado César")

# Menú principal con botones en dos columnas
st.header("Opciones Disponibles")
col1, col2 = st.columns(2)

with col1:
    if st.button("Encriptar con RSA"):
        st.session_state["opcion"] = "rsa_encriptar"
    if st.button("Desencriptar con RSA"):
        st.session_state["opcion"] = "rsa_desencriptar"
    if st.button("Mostrar codigo fuente"):
        st.session_state["opcion"] = "codigo_fuente"

with col2:
    if st.button("Información del Autor"):
        st.session_state["opcion"] = "autor"
    if st.button("Cifrado César"):
        st.session_state["opcion"] = "cesar"
    if st.button("Desencritar César"):
        st.session_state["opcion"] = "descifrado_cesar"

# Contenido según la opción seleccionada
if st.session_state.get("opcion") == "rsa_encriptar":
    st.subheader("Encriptar Mensaje con RSA")
    # Generar claves si no existen
    if st.session_state["public_key"] is None or st.session_state["private_key"] is None:
        st.session_state["public_key"], st.session_state["private_key"] = generar_claves()
        st.write("🔓 Clave pública generada:", st.session_state["public_key"])
        st.write("🔑 Clave privada generada:", st.session_state["private_key"])
        
    # Encriptar mensaje
    message = st.text_input("Ingrese el mensaje que desea encriptar")
    if st.button("Cifrar Mensaje"):
        if message:
            encrypted_message = cifrar(message, st.session_state["public_key"])
            st.session_state['encrypted_message'] = encrypted_message
            st.write("🔒 Mensaje encriptado:", encrypted_message)

elif st.session_state.get("opcion") == "rsa_desencriptar":
    st.subheader("Desencriptar Mensaje con RSA")
    if 'encrypted_message' in st.session_state:
        encrypted_input = st.text_input("Ingrese el mensaje encriptado (lista de valores hex)", value=st.session_state['encrypted_message'])
        if st.button("Desencriptar"):
            decrypted_message = descifrar(encrypted_input, st.session_state["private_key"])
            st.write("🔓 Mensaje desencriptado:", decrypted_message)
    else:
        st.write("No hay mensaje encriptado disponible. Primero encripte un mensaje.")

elif st.session_state.get("opcion") == "autor":
    st.subheader("Información del Autor")
    st.write("Nombre: Saúl Edwin Arias Trejo")
    st.write("Correo: saul.ariast@uanl.edu.mx")
    st.write("Este proyecto fue desarrollado como parte del curso de Criptografía y Seguridad en la Información.")
    st.subheader("Método de cifrado RSA")
    st.write("Elmetodo de cifrado RSA es un algoritmo de encriptacion que utiliza el algoritmo extendido de euclides para generar claves publicas y privadas")
    st.subheader("Método de cifrado César")
    st.write("El cifrado César es un tipo de cifrado por sustitución en el que una letra en el texto original es reemplazada por otra letra que se encuentra un número fijo de posiciones más adelante en el alfabeto.")
    st.image("https://media.giphy.com/media/GkD4U3VfiIbzcBhQNu/giphy.gif", use_column_width=True)
    
elif st.session_state.get("opcion") == "codigo_fuente":
    st.subheader("Código Fuente del Proyecto")
    with st.expander("Mostrar Código Fuente"):
        with open("cripto_pia_saul.py", "r") as file:
            st.code(file.read(), language="python")

if st.session_state.get("opcion") == "cesar":
    st.subheader("Cifrado César")
    message = st.text_input("Ingrese el mensaje que desea cifrar")
    desplazamiento = st.number_input("Ingrese el desplazamiento deseado", min_value=1, max_value=25, value=3)
    if st.button("Cifrar Mensaje"):
        if message:
            encrypted_message = cifrado_cesar(message, desplazamiento)
            st.session_state['encrypted_message'] = encrypted_message
            st.write("🔒 Mensaje cifrado:", encrypted_message)

elif st.session_state.get("opcion") == "descifrado_cesar":
    st.subheader("Desencriptar César")
    message = st.text_input("Ingrese el mensaje que desea descifrar", value=st.session_state['encrypted_message'])
    desplazamiento = st.sidebar.number_input("Ingrese el desplazamiento deseado", min_value=1, max_value=25, value=3)
    if st.button("Descifrar Mensaje"):
        if message:
            decrypted_message = descrifrado_cesar(message, desplazamiento)
            st.write("🔓 Mensaje descifrado:", decrypted_message)
            
    
# streamlit run cripto_pia_saul.py




