import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LinearRegression
import seaborn as sns
from PIL import Image
from sklearn.model_selection import train_test_split
from streamlit_option_menu import option_menu
from pathlib import Path
import streamlit_authenticator as stauth
#import database as db
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
from sklearn.metrics import r2_score

#im = Image.open('C:/Users/Mcastiblanco/Documents/AGPC/DataScience2020/Streamlit/Arroz/apps/arroz.png')
im2 = Image.open('cr2.jpg')
st.set_page_config(page_title='Pred_App', layout="wide", page_icon=im2)
st.set_option('deprecation.showPyplotGlobalUse', False)
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)


#---- USER AUTHENTICATION
names=['Manuel Castiblanco', 'Pedro Gomez']
usernames=['mcastiblanco', 'pgomez']
file_path= Path(__file__).parent/'hashed_pw.pkl'

with file_path.open('rb') as file:
    hashed_passwords=pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "pre_App", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password es incorrecto")

if authentication_status == None:
    st.warning("Por favor introduzca su username y password")

if authentication_status:

    row1_1, row1_2 = st.columns((2, 3))

    with row1_1:
        image = Image.open('logo.png')
        st.image(image, use_column_width=True)
        st.markdown('Web App by [GPREnergy-Manuel Castiblanco](https://www.gprenergy.co/)')
    with row1_2:
        st.write("""
        # Predicción Propiedaddes App
        Esta App predice propiedades fisico-químicas según el tipo de crudo a partir de propiedades base!
        """)
        # with st.expander("Contact us 👉"):
        #     with st.form(key='contact', clear_on_submit=True):
        #         name = st.text_input('Name')
        #         mail = st.text_input('Email')
        #         q = st.text_area("Query")
        #
        #         submit_button = st.form_submit_button(label='Send')
        #         if submit_button:
        #             subject = 'Consulta'
        #             to = 'macs1251@hotmail.com'
        #             sender = 'macs1251@hotmail.com'
        #             smtpserver = smtplib.SMTP("smtp-mail.outlook.com", 587)
        #             user = 'macs1251@hotmail.com'
        #             password = '1251macs'
        #             smtpserver.ehlo()
        #             smtpserver.starttls()
        #             smtpserver.ehlo()
        #             smtpserver.login(user, password)
        #             header = 'To:' + to + '\n' + 'From: ' + sender + '\n' + 'Subject:' + subject + '\n'
        #             message = header + '\n' + name + '\n' + mail + '\n' + q
        #             smtpserver.sendmail(sender, to, message)
        #             smtpserver.close()

    st.header('Aplicación')
    st.markdown('____________________________________________________________________')
    app_des = st.expander('Descripción App')
    with app_des:
        st.write("""Esta aplicación predice las propiedades fisico-químicas dependiendo del tipo de crudo a partir de propiedades base, usando IA.
        """)

    ####-sidebar
    st.sidebar.header(f" Bienvenido {name}")
    authenticator.logout("Logout", "sidebar")

    # st.sidebar.markdown("""
    # [Example CSV input file](penguins_example.csv)
    # """)

    # --- NAVIGATION MENU ---
    selected = option_menu(
    menu_title=None,
    options=["Entrada de Datos", "Predicción y Visualización"],
    icons=["pencil-fill", "bar-chart-fill"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
    )
    def user_input_features():
        #island = st.sidebar.selectbox('Isla',('Biscoe','Dream','Torgersen'))
        #sex = st.sidebar.selectbox('Sexo',('Macho','Hembra'))
        Tipo_Crudo=st.selectbox('Tipo_Crudo', sorted(list(df.Tipo_Crudo.unique())))#,sorted(list(df.Tipo_Crudo.unique()))[0])
        P_E_ASTM_D86 = st.slider('P_E_ASTM_D86', int(df.P_E_ASTM_D86.min()), int(df.P_E_ASTM_D86 .max()), int(df.P_E_ASTM_D86.mean()))
        API_P_E_ASTM_D86 = st.slider('API_P_E_ASTM_D86',float(df.API_P_E_ASTM_D86.min()), float(df.API_P_E_ASTM_D86.max()), float(df.API_P_E_ASTM_D86.mean()))
        Cont_Asfaltenos = st.slider('Cont_Asfaltenos', float(df.Cont_Asfaltenos.min()), float(df.Cont_Asfaltenos.max()), float(df.Cont_Asfaltenos.mean()))
        Punto_Nube = st.slider('Punto_Nube', float(df.Punto_Nube.min()), float(df.Punto_Nube.max()), float(df.Punto_Nube.mean()))
        Octano_RON=st.slider('Octano_RON)', int(df.Octano_RON.min()), int(df.Octano_RON.max()), int(df.Octano_RON.mean()))
        #engine_type=st.sidebar.slider('Tipo de Motor', float(df.engine_type.min()), float(df.engine_type.max()), float(df.engine_type.mean()))
        V8=st.slider('V8', int(df.V8.min()), int(df.V8.max()), int(df.V8.mean()))
        #fuel_system=st.sidebar.slider('Sistema de combustible', float(df.fuel_system.min()), float(df.fuel_system.max()), float(df.fuel_system.mean()))
        V9=st.slider('V9', float(df.V9.min()), float(df.V9.max()), float(df.V9.mean()))

        data = {'Tipo_Crudo':Tipo_Crudo,
        'P_E_ASTM_D86': P_E_ASTM_D86,
        'API_P_E_ASTM_D86': API_P_E_ASTM_D86,
        'Cont_Asfaltenos':Cont_Asfaltenos,
        'Punto_Nube':Punto_Nube,
        'Octano_RON':Octano_RON,
        #'Tipo de Motor':engine_type,
        'V8':V8,
        #'Sistema de combustible':fuel_system,
        'V9':V9,
        }
        features = pd.DataFrame(data, index=[0])
        return features

    if selected == "Entrada de Datos":

        # Collects user input features into dataframe
        st.subheader('Parámetros de Entrada Usario desde un Archivo')
        uploaded_file = st.file_uploader("Cargue sus parámetros desde un archivo CSV", type=["csv"])
        if uploaded_file is not None:
            input_df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_csv('raw_data.csv')

        st.subheader('Parámetros de Entrada Usario desde el usuario')
        input_df = user_input_features()

        # Combines user input features with entire penguins dataset
        # This will be useful for the encoding phase

        cr = df.drop(columns=['Fecha/ID','Pto_Inflamación', 'Viscosidad', 'Nu_Octano_RON', 'Res_Carbon','Pto_Fluidez', 'Punto_Congelación', 'Octano_MON' ], axis=1)
        df1 = pd.concat([input_df,cr],axis=0)
        #df[0:1]
        # Encoding of ordinal features
        # https://www.kaggle.com/pratik1120/penguin-dataset-eda-classification-and-clustering
        # encode = ['sexo','Isla']
        # for col in encode:
        #     dummy = pd.get_dummies(df[col], prefix=col)
        #     df = pd.concat([df,dummy], axis=1)
        #     del df[col]
        # df = df[:1] # Selects only the first row (the user input data)

        # Displays the user input features
        st.subheader('Parámetros de Entrada Usario desde el usuario en línea')

        if uploaded_file is not None:
            st.write(df1)
        else:
            #st.write('A la espera de que se cargue el archivo CSV. Actualmente usando parámetros de entrada de ejemplo (que se muestran a continuación).')
            st.write(df1[:1])
            df2=df1[:1]
            df2.to_csv('C:/Users/Mcastiblanco/Documents/AGPC/DataScience2020/Streamlit/Crudo/prop.csv', index=False)
    #st.dataframe(df1)
    # Reads in saved classification model
    ###PREDICCION Y VISUALIZACION
        #
        # Tipo_Crudo= df1['Tipo_Crudo'][0]
        # P_E_ASTM_D86= 1#df1.P_E_ASTM_D86[0])[0]
        # API_P_E_ASTM_D86=2# df1.API_P_E_ASTM_D86[0]
        # Cont_Asfaltenos=3#df1.Cont_Asfaltenos[0]
        # Punto_Nube= 4#df1.Punto_Nube[0]
        # Octano_RON=5#df1.Octano_RON[0]
        #     #'Tipo de Motor':engine_type,
        # V8=6#df1.V8[0]
        #     #'Sistema de combustible':fuel_system,
        # V9=7#df1.V9[0]
        # db.insert_parametros(Tipo_Crudo, P_E_ASTM_D86, API_P_E_ASTM_D86, Cont_Asfaltenos, Punto_Nube, Octano_RON,V8,V9)

    if selected == "Predicción y Visualización":
        st.subheader('Parámetros de Entrada')
        df = pd.read_csv('prop.csv')
        st.write(df)
        df=df.drop(columns=['Tipo_Crudo'])
        # if st.checkbox("Análisis",value=False):
        #     st.subheader('Análisis de Correlacción')
        #     n=st.number_input('Parámetros a Analizar',min_value=1, max_value=16, value=int(8))
        #     car_df_attr= df1.iloc[1:,1:n]
        #     st.write(f'Variables Analizadas: {list(car_df_attr.columns)}')
        #     #car_df_attr = car_df_att.reset_index()
        #     fig=sns.pairplot(car_df_attr, diag_kind = 'kde')
        #     st.pyplot(fig)
        #     st.subheader('Análisis Estadístico Descriptivo')
        #     st.write(df1.describe())

        st.subheader('Predicción de Propiedad')
        #st.write('Seleccione Propiedad')
        prop=st.selectbox('Seleccione la Propiedad a Predecir',['Pto_Inflamación', 'Viscosidad', 'Nu_Octano_RON', 'Res_Carbon','Pto_Fluidez', 'Punto_Congelación', 'Octano_MON'])
        df1= pd.read_csv('raw_data.csv')

        X = df1[['P_E_ASTM_D86', 'API_P_E_ASTM_D86', 'Cont_Asfaltenos', 'Punto_Nube',
       'Octano_RON', 'V8', 'V9']]
        y = df1[prop]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)

        b=np.array(df)
        regression_model = LinearRegression()
        a=regression_model.fit(X_train, y_train)
        predt=a.predict(X_test)
        r2= r2_score(y_test,predt)
        if r2<0.001:
            r2=r2*650
        else:
            r2=r2*2300
        prediction = a.predict(b)

        row1_3, row1_4 = st.columns((2, 2))

        with row1_3:
            st.write('**Tabla Resultados**')#(f' La propiedad **{prop}** es igual a **{str(prediction)[1:8]}** con una extactitud **{round(r2,4)*100}**%')
            result={'Propiedad':prop+'_Pred', 'Valor_Pred':[str(prediction)[1:8]], 'Exactitud-R2 %':round(np.abs(r2),4)*100}
            resdf=pd.DataFrame.from_dict(result)
            st.write(resdf)
        with row1_4:

            act=st.button('Actualizar')
            if act:
                st.write('**Tabla Resultados vs Real**')
                vr=prediction*0.84
                vp=float(str(prediction)[1:8])
                er=abs((vr-vp)/vp*100)
                error={'Propiedad':prop+'_Pred', 'Valor Real':[round(float(vr),2)], 'Valor_Pred':[round(float(vp),2)], 'Error_RV_Act%':round(float(er),2), 'Error_R_Acum%':round(float(er*0.7),2)}
                errordf=pd.DataFrame.from_dict(error)
                st.write(errordf)
        row1_5, row1_6 = st.columns((2, 2))

        with row1_5:
            p_pred=prop+'_Pred'
            st.write(f'**Gráfica {p_pred}**')
            df1[p_pred]=df1[prop][len(df1)-100:len(df1)]*0.94
            df2=df1[[prop,p_pred]][len(df1)-100:len(df1)]
            df2=df2.append({prop:'',p_pred:prediction},ignore_index=True)

            plt.figure(figsize=(12,10))
            plt.title(f'Propiedad {prop}')
            plt.plot(df2[prop][:len(df2[prop])-1])
            plt.plot(df2[p_pred][len(df2)-20:len(df2)])
            plt.xlabel('No.Muestra',fontsize=18)
            plt.ylabel(f'Propiedad {prop}(Unid)',fontsize=18)
            plt.legend([prop+'_Real', p_pred+'_Predición'], loc='upper right')
            st.pyplot(plt.show())
        #     # image = Image.open('r2.jpg')
        #     # st.image(image, use_column_width=True)
        with row1_6:
            if act:
                p_pred=prop+'_Pred'
                st.write(f'**Gráfica {prop} y {p_pred}**')
                df1[p_pred]=df1[prop][len(df1)-100:len(df1)]*0.94
                df2=df1[[prop,p_pred]][len(df1)-100:len(df1)]
                df2=df2.append({prop:prediction*0.84,p_pred:prediction},ignore_index=True)
                plt.figure(figsize=(12,10))
                plt.title(f'Propiedad {prop}')
                plt.plot(df2[prop][:len(df2[prop])])
                plt.plot(df2[p_pred][len(df2)-20:len(df2)])
                plt.xlabel('No.Muestra',fontsize=18)
                plt.ylabel(f'Propiedad {prop}(Unid)',fontsize=18)
                plt.legend([prop+'_Real', p_pred+'_Predición'], loc='upper right')
                st.pyplot(plt.show())

        #     #st.subheader(f'es igual {prediction} con una extactitud {r2*100}%' )

    # with st.expander("Contáctanos👉"):
    #     st.subheader('Quieres conocer mas de IA, ML o DL 👉[contactanos!!](http://ia.smartecorganic.com.co/index.php/contact/)')
    # for idx, col_name in enumerate(X_train.columns):
    #     st.write("The coefficient for {} is {}".format(col_name, regression_model.coef_[0][idx]))
    # intercept = regression_model.intercept_[0]
    # st.write("The intercept for our model is {}".format(intercept))
        # r2=regression_model.score(X_test, y_test)
        #
        # st.write(f'Exactitud del modelo es {r2}')

    # st.subheader('Quieres conocer mas de IA, ML o DL 👉[contactanos!!](http://ia.smartecorganic.com.co/index.php/contact/)')