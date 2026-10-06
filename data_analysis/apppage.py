import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="Netflix Analysis", layout="wide")
st.title("Netflix Movies & TV Shows Analysis Dashboard")


#1.LOAD DATA -Direct from internet , no csv needed

@st.cache_data
def load_data():
    url="C:\\Users\\shrav\\OneDrive\\ドキュメント\\netflix_titles.csv"
    df = pd.read_csv(url)
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    df['age_when_added'] = df['year_added']-df['release_year']
    return df
df = load_data()

#2.SIDEBAR FILTER

st.sidebar.header("Filters")
type_filter = st.sidebar.multiselect("Select Type",df['type'].unique(),default=df['type'].unique())
df_filtered = df[df['type'].isin(type_filter)]

#3.KPIS

st.subheader("Key Metrics")
col1,col2,col3,col4 = st.columns(4)
col1.metric("Total Titles",f"{df_filtered.shape[0]:,}")
col2.metric("Movies",df_filtered[df_filtered['type']=='Movie'].shape[0])
col3.metric("TV Shows",df_filtered[df_filtered['type']=='TV Show'].shape[0])
col4.metric("Avg Release Year", int(df_filtered['release_year'].mean()))


st.subheader(" Contented Added Each Year")
yearly=df_filtered.groupby(['year_added','type']).size().reset_index(name='count')
yearly=yearly.dropna()
fig1=px.line(yearly,x='year_added',y='count',color='type',markers=True)
st.plotly_chart(fig1,use_container_width=True)


st.subheader("Top 10 Countries with Most Content")
country_df=df_filtered['country'].dropna().str.split(',').explode().value_counts().head(10)
fig2,ax=plt.subplots()
sns.barplot(x=country_df.values,y=country_df.index,ax=ax,palette='Reds_r')
st.pyplot(fig2)


st.subheader("Most Popular Genres")
df_filtered['genres']=df_filtered['listed_in'].str.split(',')
genres=df_filtered.explode('genres')['genres'].value_counts().head(10)
fig3=px.bar(genres,x=genres.values,y=genres.index,orientation='h')
st.plotly_chart(fig3,use_container_width=True)


st.subheader("How old is content to Netflix? ")
fig4=px.histogram(df_filtered.dropna(subset=['age_when_added']),x='age_when_added',nbins=30)
st.plotly_chart(fig4,use_container_width=True)


st.subheader("Search Movie / TV Shows")
search=st.text_input("Enter Movie / TV Shows name")
if search:
    result=df_filtered[df_filtered['title'].str.contains(search,case=False,na=False)]
    st.dataframe(result[['title','type','country','release_year','rating','listed_in']].head(22))