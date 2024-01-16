import streamlit as st
import pandas as pd
import PIL 
from PIL import Image
from streamlit_option_menu import option_menu
import plotly.express as px
import mysql.connector 
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt


# Setting up page configuration
icon = Image.open(r"C:/Users/sujit/vs inside/th.jpg")
st.set_page_config(page_title= "PhonePe Pulse Data Visualization and Exploration",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About':"This dashboard app is created by Clinton N!"}
                   )

#-----------------------------------------------Creating dashboard-----------------#

st.sidebar.header(":violet[Hey! Welcome to the dashboard]")

with st.sidebar:
    selected = option_menu("Menu", ["Home","Basic Insights","Top Charts","Geo Visual","Explore Data","About"], 
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "15px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})
#--------------------------------Connecting to Mysql--------------#

mydb = mysql.connector.connect(
                        host = "127.0.0.1",
                        user = "root",
                        password = "Sujithra@20",
                        database = "phonepe_pulse")
cursor=mydb.cursor(buffered=True)

#--------------------------------------------------------------------------#
img=Image.open(r"C:\Users\sujit\vs inside\th.jpg")

if selected == "Home":
    st.subheader(":violet[PhonePe Pulse Data Visualization and Exploration]")
    col1,col2 = st.columns([3.5,2],gap="medium")
    with col1:
        st.markdown(":violet[PhonePe has become one of the most popular digital payment platforms in India, with millions of users relying on it for their day-to-day transactions. The app is known for its simplicity, user-friendly interface, and fast and secure payment processing. It has also won several awards and accolades for its innovative features and contributions to the digital payments industry.]")
      
        st.markdown(":blue[India's top fintech platform, announced the debut of PhonePe Pulse, India's first interactive website providing statistics, insights, and trends on digital payments in the country, on September 3, 2021. The PhonePe Pulse website displays over 2000 crores in customer transactions on an interactive map of India. PhonePe's data, with over 45% market share, is typical of the country's digital payment habits.]")

        st.markdown(":violet[This web app is built to analyse the Phonepe transaction and users depending on various Years, Quarters, States, and Types of transaction and give a Geo visualization output based on given requirements.]")
  
    with col2:
         st.write("")
         st.write("")
         st.image(img,width=550)

#-------------------------------------------------Get some informtion from mysql data ---------------------------------------#
        

if selected == "Basic Insights":
    st.subheader(":violet[BASIC INSIGHTS]")
    st.subheader(":violet[Let's know some basic insights about the data]")
    options = ["--select--",
               "Top 10 States or Union Territory  based on transaction year and amount of transaction",
               "Top 10 Registered-users based on States or Union Territory and Pincodes",
               "Top 10 Districts based on States or Union Territory and Count of transaction",
               "List of 10 States or Union Territory based on District and Count of transaction",
               "List of 10 Transaction_Count based on Districts and States or Union Territory",
               "List of 10 States or Union Territory based on Transaction Type and Amount of transaction"]

    select = st.selectbox("Select the option",options)
    if select=="Top 10 States or Union Territory  based on transaction year and amount of transaction":
        cursor.execute("SELECT DISTINCT State, Year, SUM(Transaction_amount) AS Total_Transaction_Amount FROM top_trans GROUP BY State, Year ORDER BY Total_Transaction_Amount DESC LIMIT 10");
        df=pd.DataFrame(cursor.fetchall(), columns=['States_OR_Union_Territory','Transaction_Year', 'Transaction_amount'])
        df.index = np.arange(1, len(df)+1)
        st.write(df)
      
    elif select=="Top 10 Registered-users based on States or Union Territory and Pincodes":
        cursor.execute("SELECT DISTINCT State,Pincode,SUM(Registered_users) AS Registered_users FROM top_user GROUP BY State,Pincode ORDER BY Registered_users DESC LIMIT 10");
        df=pd.DataFrame(cursor.fetchall(), columns=['States_OR_Union_Territory','Pincode','Registered_users'])     
        df.index = np.arange(1, len(df)+1)
        st.write(df)

    elif select=="Top 10 Districts based on States or Union Territory and Count of transaction":
        cursor.execute("SELECT DISTINCT Pincode,State,SUM(Transaction_Count) AS Transaction_Counts FROM top_trans GROUP BY Pincode,State ORDER BY Transaction_Counts DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns=['Pincode','States_OR_Union_Territory','Transaction_Count'])  
        df.index = np.arange(1, len(df)+1)
        st.write(df)

    
    elif select=="List of 10 States or Union Territory based on District and Count of transaction":
        cursor.execute("SELECT DISTINCT State,District,SUM(Count) AS Transaction_count FROM map_trans GROUP BY  State,District order by Transaction_count Desc limit 10");
        df = pd.DataFrame(cursor.fetchall(), columns=['States_OR_Union_Territory','District','Transaction_count'])
        df.index = np.arange(1, len(df)+1)
        st.write(df)

    elif select=="List of 10 Transaction_Count based on Districts and States or Union Territory":
        cursor.execute("SELECT DISTINCT State , District, SUM(Count) AS Transaction_count FROM map_trans GROUP BY State,District ORDER BY Transaction_count ASC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns=['States_OR_Union_Territory ','District','Transaction_Count'])
        df.index = np.arange(1, len(df)+1)
        st.write(df)
      
    elif select=="List of 10 States or Union Territory based on Transaction Type and Amount of transaction":
        cursor.execute("SELECT DISTINCT State,Transaction_Type, SUM(Transaction_count) as Transaction_count FROM agg_tran GROUP BY State,Transaction_Type ORDER BY Transaction_count DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns=['States_OR_Union_Territory ','Transaction_Type','Transaction_Count'])
        df.index = np.arange(1, len(df)+1)
        st.write(df)    


if selected=="Top Charts":
    st.subheader(":violet[Top Charts]")
    Type = st.selectbox("**Type**", ("Transactions", "Users"))
   
    Year = st.slider("**Year**", min_value=2018, max_value=2022)
    Quarter = st.slider("Quarter", min_value=1, max_value=4)
    

    if Type == "Transactions":
      with st.sidebar:
          a=st.checkbox("Top 10 State or Union_Territory based on Total number of transaction and Total amount spent on phonepe.")
          b=st.checkbox('Top 10 Transaction_Count based on Districts and States or Union Territory')
          c=st.checkbox('Top 10 Districts based on States or Union Territory and Count of transaction')
      if a:
        cursor.execute(f"select State, sum(Transaction_Count) as Total_Transactions_Count, sum(Transaction_Amount) as Total from agg_tran where Year = {Year} and Quarter = {Quarter} group by State order by Total DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(), columns=['States_OR_Union_Territory', 'Transactions_Count','Transaction_Amount'])
        fig = px.pie(df, values='Transaction_Amount',
                     names='States_OR_Union_Territory',
                     color_discrete_sequence=px.colors.sequential.Agsunset)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)
      if b:
        cursor.execute(f'SELECT State,District,SUM(Count) AS Transaction_count FROM map_trans where Year = {Year} and Quarter = {Quarter} GROUP BY State,District ORDER BY Transaction_count DESC LIMIT 10');
        df = pd.DataFrame(cursor.fetchall(), columns=['States_OR_Union_Territory','District','Transaction_Count'])
        fig = px.pie(df, values='Transaction_Count',
                     names='States_OR_Union_Territory',
                     color_discrete_sequence=px.colors.sequential.Agsunset)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)
      if c:
        cursor.execute(f'SELECT distinct State,District,sum(Count) as transaction_count from map_trans where Year = {Year} and Quarter = {Quarter} group by state, district  order by transaction_count Desc limit 10');  
        df = pd.DataFrame(cursor.fetchall(),columns=['District','States_OR_Union_Territory','Transaction_Count'])
        fig=px.bar(df,x="Transaction_Count",y="District",color = 'District', color_continuous_scale  = 'viridis')
        fig.update_traces(textposition='inside')
        st.plotly_chart(fig,use_container_width=True)

    if Type=='Users':
      with st.sidebar:
          a=st.checkbox("Top 10 Registered-users based on States or Union Territory.")
          b=st.checkbox('Top 10 District based on Registered _Users')
          c=st.checkbox('Top 10 states or Union Territory based on Phone-pe Appopens by users.')
      if a:
        cursor.execute(f"SELECT State,Pincode,SUM(Registered_users) AS Registered_users FROM top_user where Year = {Year} and Quarter = {Quarter} GROUP BY State,Pincode ORDER BY Registered_users DESC LIMIT 10");
        df=pd.DataFrame(cursor.fetchall(), columns=['States_OR_Union_Territory','Pincode','Registered_users'])
        fig = px.pie(df, values='Registered_users',
                     names='States_OR_Union_Territory',
                     color_discrete_sequence=px.colors.sequential.Agsunset)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)
      if b:
        cursor.execute(f"SELECT  State, District,Registered_user FROM map_user where Year = {Year} and Quarter = {Quarter} ORDER BY Registered_user DESC LIMIT 10");
        df=pd.DataFrame(cursor.fetchall(), columns=['State', 'District','Registered_user'])
        fig = px.pie(df, values='Registered_user',
                     names='District',
                     color_discrete_sequence=px.colors.sequential.Agsunset)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)
      if c:
        cursor.execute(f'SELECT DISTINCT Brands,State,SUM(Count) AS Transaction_Counts FROM agg_user where Year = {Year} and Quarter = {Quarter}  GROUP BY Brands,State ORDER BY Transaction_Counts DESC LIMIT 10');
        df = pd.DataFrame(cursor.fetchall(),columns=['Brands','States_OR_Union_Territory','Transaction_Count'])
        fig=px.bar(df,x="Brands",y="Transaction_Count",color = 'Brands', color_continuous_scale  = 'viridis')
        fig.update_traces(textposition='inside')
        st.plotly_chart(fig,use_container_width=True)

if selected =="Explore Data":
    st.subheader(":violet[Explore Data]")
    with st.sidebar:
        Type = st.selectbox("**Type**", ("Transaction", "Users"))
   
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
    st.markdown(" :white[Select any State to explore more]")
    selected_state = st.selectbox("",
                           ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                            'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                            'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                            'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                            'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                            'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
     
    if Type == "Transaction":
       st.write(":violet[Explore overall state data based on transactions from various years and quarters.]")
       cursor.execute(f"select State,Year,Quarter,District,sum(Count) as Total_Count, sum(Amount) as Total_amount  from map_trans where Year  = {Year} and Quarter = {Quarter} and State = '{selected_state}' group by State ,District,Year,Quarter order by State ,District")
       df = pd.DataFrame(cursor.fetchall(), columns=['States_OR_Union_Territory ','Transaction_Year', 'Quarters', 'District','Transaction_Count','Transaction_Amount'])
       fig = px.bar(df,
               title=selected_state,
               x="District",
               y="Transaction_Count",
               orientation='v',
               color='Transaction_Count',
               color_continuous_scale=px.colors.sequential.Agsunset)
       st.plotly_chart(fig,use_container_width=True)

    if Type == "Users":
      st.write(":violet[Explore overall state data based on users from various years and quarters.]")


      cursor.execute(f"select State,Year,Quarter,District,sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where Year  = {Year} and Quarter = {Quarter} and State = '{selected_state}' group by State, District,Year, Quarter order by State ,District")

      df = pd.DataFrame(cursor.fetchall(), columns=['States_OR_Union_Territory ','Transaction_Year', 'Quarter', 'District', 'Registered_user','App_opens'])

      fig = px.bar(df,
                   title=selected_state,
                   x="District",
                   y="Registered_user",
                   orientation='v',
                   color='Registered_user',
                  color_continuous_scale=px.colors.sequential.Agsunset)
      st.plotly_chart(fig,use_container_width=True)
      
if selected == "About":
    st.subheader(":violet[About PhonePe]")
    st.markdown("India's top financial platform, PhonePe, has more than 300 million registered customers. Users of PhonePe can send and receive money, recharge mobile phones and DTH, pay for goods and services at merchant locations, purchase gold, and make investments.")
    
    st.subheader(":violet[About Project:]")
    st.write("The website's insights and the report's findings were derived from two important sources: the whole transaction data of PhonePe and merchant and customer interviews. The report is freely downloadable from GitHub and the PhonePe Pulse website.")
    st.write("The outcome of this project is a complete and user-friendly solution for extracting, processing, and visualizing data from the Phonepe pulse Github repository.")

    st.write(":violet[Thank you for visiting and exploring this website!!!]")

if selected == "Geo Visual":
  all_states = [
    'Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal pradesh', 'Assam',
    'Bihar', 'Chandigarh', 'Chhattisgarh', 'Dadra & Nagar Haveli & Daman & Diu', 
    'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir', 
    'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh', 
    'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry',
    'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 
    'Uttarakhand', 'West Bengal'
    ]
  df2 = pd.DataFrame(all_states)
  def GeoVisualization(data_Frame,location,color):
      fig = px.choropleth(
          data_Frame,
          geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
          featureidkey='properties.ST_NM',
          locations=location,
          color=color,
          color_continuous_scale='sunset',
          )
      return fig.update_geos(fitbounds="locations", visible=False)
  geo_Choice = st.selectbox('Choose the data to display',['Select Any',
                                                            'Total Transaction Amount By Each State',
                                                            'Total Registered Users By Each State',
                                                            'Total App Opens By Each State'
                                                        ])
    
  if geo_Choice == 'Total Transaction Amount By Each State':
    Year = st.slider("**Year**", min_value=2018, max_value=2022)
    Quarter = st.slider("**Quarter**", min_value=1, max_value=4)

    st.markdown("## :violet[Total Transaction Amount By Each State]")

    cursor.execute(f"select state, sum(Count) as Total_Transactions, sum(Amount) as Total_Amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
    df1 = pd.DataFrame(cursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_Amount'])

    df1.State = df2

    col1,col2 = st.columns(2)

    with col1:
        st.markdown("### GEO-VISUALIZATION")
        fig = GeoVisualization(df1,'State','Total_Amount')
        st.plotly_chart(
            fig,
            use_container_width=True
        )
    with col1:
      st.markdown("### DATAFRAME")
      st.dataframe(df1)
          
  if geo_Choice == 'Total Registered Users By Each State':
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("**Quarter**", min_value=1, max_value=4)

        st.markdown("## :violet[Total Registered Users By Each State]")

        cursor.execute(f"select State, sum(Registered_users) as Registered_User from top_user where year = {Year} and quarter = {Quarter} group by State order by State")
        df1 = pd.DataFrame(cursor.fetchall(),columns= ['State', 'Registered_User'])
    
        df1.State = df2

        col1,col2 = st.columns(2)

        with col1:
            st.markdown("### GEO-VISUALIZATION")
            fig = GeoVisualization(df1,'State','Registered_User')
            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with col2:
            st.markdown("### DATAFRAME")
            st.dataframe(df1)
            
  if geo_Choice == 'Total App Opens By Each State':
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("**Quarter**", min_value=1, max_value=4)

        st.markdown("## :violet[Total Registered Users By Each State]")

        cursor.execute(f"select State, sum(Registered_user) as Registered_User, sum(App_opens) as App_Opens from map_user where year = {Year} and quarter = {Quarter} group by State order by State")
        df1 = pd.DataFrame(cursor.fetchall(),columns= ['State', 'Registered_User', 'App_Opens'])
    
        df1.State = df2

        col1,col2 = st.columns(2)

        with col1:
            st.markdown("### GEO-VISUALIZATION")
            fig = GeoVisualization(df1,'State','App_Opens')
            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with col2:
            st.markdown("### DATAFRAME")
            st.dataframe(df1)

                           



