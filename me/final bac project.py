import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import missingno as msno
import altair as alt

CSV_link = "./dataBacAcademie.csv"
Data_gouv_link = "https://www.data.gouv.fr/fr/datasets/le-baccalaureat-par-academie/"

st.markdown("<h1 style='color: orange;'><strong>Bac-Academic data set project</strong></h1>", unsafe_allow_html=True)
st.write("This project was carried out by me in September 2024 when I was in M1-Data Engineering at EFREI Paris.\n\nI had to analyze a dataset I had found on the government website.\n\nI only had a few hours of class and a few labs for this course when I started this project, my first use of streamlit and some data analysis libraries.")

#%%history

st.markdown("<h3 style='color: orange;'>The Dataset :</h3>", unsafe_allow_html=True)

st.markdown("<h5 style='color: DarkOrange;'>A bit of history</h5>", unsafe_allow_html=True)

st.write("""
The baccalaureat, often abbreviated to 'bac', is a fundamental diploma in the French education system, marking the end of secondary studies. 

Created in 1808 by Napoleon Bonaparte, it has long been considered a prerequisite for entering the adult world and pursuing higher education. It also opens the door to a wide range of professional opportunities. 

Every year, thousands of students prepare for this exam which, despite its reforms, remains an important landmark in school life.

***DIFFERENT ROUTES:***
    
There are three main routes to the baccalauréat in France: the bac general, the bac technologique and the bac professionnel. The bac general is designed for students who wish to pursue longer higher education studies, notably at university or in preparatory classes. 

The bac technologique, on the other hand, is geared more towards technical and applied studies.

The vocational bac, on the other hand, prepares students directly for the world of work, although BTS or IUT studies are also possible.

***MENTIONS:***
    
To pass the baccalaureat, students need an overall average of at least 10/20. 

Depending on the results, students can obtain a mention: 

    - 'assez bien' between 12 and 13.99
    - 'bien' between 14 and 15.99
    - 'tres bien' above 16. 
    
Students with an average of between 8 and 9.99 can take remedial exams to try and validate their diploma.
""")

#Links

st.markdown("<h5 style='color: DarkOrange;'>Links</h5>", unsafe_allow_html=True)


st.markdown("If you want to get more information about the dataset click on that [**Link**](%s)" %Data_gouv_link)

df = pd.read_csv(CSV_link)  
csv = df.to_csv(index=False).encode('utf-8')

st.write("If you want to dowload the file (csv) of my project. You can press that button :")
st.download_button(
    label="**Dowload CSV**",
    data=csv,
    file_name="Dataset_Bac_Academie.csv",
    mime="text/csv")

#%%

st.markdown("<h3 style='color: orange;'>1. Analyze data to make changes if necessary</h3>", unsafe_allow_html=True)

#%%

path = "./dataBacAcademie.csv"
df = pd.read_csv(path, delimiter=";")
path_code = '''
df = pd.read_csv(path, delimiter=";")
'''
st.code(path_code,language='python')

st.write("We find the first lines of the file.")
st.write(df.head())

#%%missing data

st.markdown("<h5 style='color: DarkOrange;'><center>Missing data?</h5>", unsafe_allow_html=True)

st.write("I check if there is some empty/ missing data")
st.write("Missing data is one of the most problematic issues, as there is no correct and efficient way of solving this problem. It all depends on how you see the project and the dataset.")
st.write("I use the **'missingno'** library to display each column and the number of values it contains.")
st.write("You can see the result of the library here:")

fig, ax = plt.subplots()
msno.bar(df, ax=ax)
st.pyplot(fig)
plt.clf()

st.write("We can see that there are no missing data, so no modifications are required, so it's good for me.")

#%%duplicates

st.markdown("<h5 style='color: DarkOrange;'><center>Duplicate lines?</h5>", unsafe_allow_html=True)

st.write("Duplicate data can be easily managed, but it's important to do so because it can influence results and lead to erroneous results.")

dupli = '''
    #with the code :
    import pandas as pd
    st.code(df.duplicated().sum())
    #I can get the summation of the duplicates rows.
    """
    This is the syntax of the function :
    DataFrame.duplicated(subset=None, keep='first')
    """
    '''
st.code(dupli, language='python')
st.code(df.duplicated().sum())

dupli_res = '''
    """
    I get the answer '0', 
    Luckily, we can see that there are no duplicate lines, 
    so there's no need to delete anything or adapt the lines.
    """
    '''
st.code(dupli_res, language='python')

#%%

st.markdown("<h3 style='color: orange;'>2. View dataset data in graphical form</h3>", unsafe_allow_html=True)

#%%
admis_gender = df.groupby('sexe')['nombre_d_admis_totaux'].sum()
refus_gender = df.groupby('sexe')['nombre_de_refuses_totaux'].sum()
total_prs = pd.concat([admis_gender, refus_gender], axis=1)#on réunnit les 2 tables pour avoir tout le monde
total_prs['tot'] = total_prs["nombre_d_admis_totaux"]+total_prs["nombre_de_refuses_totaux"]

mentions = ['nombre_d_admis_avec_mention_tb_avec_les_felicitations_du_jury','nombre_d_admis_avec_mention_tb_sans_les_felicitations_du_jury','nombre_d_admis_avec_mention_b', 'nombre_d_admis_avec_mention_ab', 'nombre_d_admis_sans_mention']
mentions_total = df[mentions].sum()

voie_sum = df.groupby(['academie', 'sexe'])['nombre_d_inscrits'].sum().reset_index(name='students')

second_tour_ref = df.groupby(['academie'])['nombre_de_refuses_totaux'].sum().reset_index(name='refu+admis')
second_tour_ad = df.groupby(['academie'])['nombre_d_admis_totaux'].sum().reset_index(name='refu+admis')
second_tour_ad['type'] = 'Admission'
second_tour_ref['type'] = 'Refusal'

admissions_by_route_gender = df.groupby(['voie', 'sexe'])['nombre_d_admis_totaux'].sum().reset_index()

success_rate_academy = df.groupby('academie')[['nombre_d_admis_totaux', 'nombre_de_refuses_totaux']].sum()
success_rate_academy['success_rate'] = success_rate_academy['nombre_d_admis_totaux'] / (success_rate_academy['nombre_d_admis_totaux'] + success_rate_academy['nombre_de_refuses_totaux']) *100

gender_ratio_by_series = df.groupby(['serie', 'sexe'])['nombre_d_inscrits'].sum().unstack()

performance_by_series = df.groupby('serie')[['nombre_d_admis_totaux', 'nombre_de_refuses_totaux']].sum().reset_index()

#%%

st.markdown("<h4 style='color: Orange;'><center>Part of the girls/boys distribution:</h4>", unsafe_allow_html=True)

#%%
st.markdown("<h5 style='color: DarkOrange;'>What is the ratio of boys to girls in the database?</h5>", unsafe_allow_html=True)

st.write("First, I want to see the number of boys and girls in the database")

total_prs['tot'].plot(kind='bar', width=0.1, color=['darkblue','darkred'])
plt.title("Number of students by gender")
plt.ylabel("Number of students")
plt.xlabel("Gender")
st.pyplot(plt)
plt.clf()

st.write(total_prs['tot'])
st.write("You can see it through a graph and numbers, that we got quite the same number of boys and girls.")

#%%
st.write("")
st.markdown("<h5 style='color: DarkOrange;'>What is the ratio within each branch of the bac?</h5>", unsafe_allow_html=True)

st.write("As we've already seen, there are different types of baccalaureat, but within each branch there are different possibilities.\n\nFor example, STMG: science and technology of management and administration series")

fig, ax = plt.subplots()
gender_ratio_by_series.plot(kind='barh', stacked=True, ax=ax, color=['darkblue','darkred'])
ax.set_title("Gender ratio by sub-branch", fontsize=16)
ax.set_xlabel("Number of Students", fontsize=12)
ax.set_ylabel("Series", fontsize=12)
st.pyplot(fig)

st.write("As you can see, the majority of students take the general baccalaureate, as this is the route that currently closes the fewest doors to students. Most of them are grils.")

#%%
st.write("")
st.markdown("<h5 style='color: DarkOrange;'>How many students are there by gender and academic?</h5>", unsafe_allow_html=True)

st.write("In the database, you can see that there are academies that are groups of high schools, so I decided to see the ratio of girls to boys within each one.")
st.write("You can choose to view by number of girls, number of boys or both.")

fig = px.histogram(voie_sum, x='academie', y='students', color='sexe', barmode='group',title="Students by academy and by gender")

fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="down",
            buttons=list([
                dict(
                    args=[{"visible": [True, True]}],
                    label="All",
                    method="update"
                ),
                dict(
                    args=[{"visible": [True, False]}],
                    label="Only women",
                    method="update"
                ),
                dict(
                    args=[{"visible": [False, True]}],
                    label="Only men",
                    method="update"
                )
            ]),
            showactive=True
        )
    ]
)

st.plotly_chart(fig)
plt.clf() 

st.write("Overall, we can see that there is quite the same number of boys than girls.\n\nThere are also considerable discrepancies, such as in NANTES, the academy with the biggest gap -> 43.554k girls / 41.498k boys.")

#%%

st.markdown("<h4 style='color: Orange;'><center>Part on the different mentions:</h4>", unsafe_allow_html=True)

#%%
st.markdown("<h5 style='color: DarkOrange;'>What is the distribution of the mentions?</h5>", unsafe_allow_html=True)

st.write("I want to see the distribution of mentions in the database, what better way than with a pie chart!")

plt.pie(mentions_total, labels=mentions_total.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("Set1"))
plt.title("Mentions distribution in %").set_size(30)
st.pyplot(plt)
plt.clf() 

st.write("As you can see, very few people obtained a mention 'tres bien' with congratulations.\n\nThe percentages are fairly representative, since it's easier to get a 'assez-bien' (ab) than a 'bien' (b) mention, and even harder to get a 'tres bien' (tb). \n\nAs for the jury's congratulations, it's the same story: it's quite rare to get them in addition to a mention.")

#%%
st.write("")
st.markdown("<h5 style='color: DarkOrange;'>In percentage it's good to know but in number!!</h5>", unsafe_allow_html=True)

mentions_total.T.plot(kind='bar', stacked=True, figsize=(10, 6), color=sns.color_palette("Set1"))
plt.title("Distribution of mentions in number").set_size(20)
plt.xlabel("Type of mention").set_size(15)
plt.xticks(rotation=45)
st.pyplot(plt)
plt.clf() 

st.write("In terms of number, we're back to something coherent, and we can realize the gap between each mention")

#%%

st.markdown("<h4 style='color: Orange;'><center>Admissions and refusals section:</h4>", unsafe_allow_html=True)

#%%
st.markdown("<h5 style='color: DarkOrange;'>How many people were admitted/refused over the years of the dataset?</h5>", unsafe_allow_html=True)

st.write("I want to see the total number of admissions and rejections in the database, compared to the total of girls and boys.")

total_prs.plot(kind='bar',color=['purple', 'orange','black'], width=0.1)
plt.title("Number of refusals/admissions by gender")
plt.ylabel("Number of refusals/admissions")
plt.xlabel("Gender")
st.pyplot(plt)
plt.clf()

st.write("As we know, there are more girls than boys, and it's the same for admission. We have slightly more girls than boys who pass the BAC.\n\nHowever, in terms of rejections, boys come out on top, there are more boys who are rejected and of course who don't get the diploma.\n\n I can conclude that girls are better than boys at school.")

#%%
st.write("")
st.markdown("<h5 style='color: DarkOrange;'>Admissions by Gender and Baccalaureate Route</h5>", unsafe_allow_html=True)

st.write("Knowing the distribution over the entire database is all well and good, but if we limit ourselves to the 3 branches of the Bac:")

fig, ax = plt.subplots()
sns.barplot(x='voie', y='nombre_d_admis_totaux', hue='sexe', data=admissions_by_route_gender, ax=ax)
ax.set_title("Admissions by gender and baccalaureate route", fontsize=16)
ax.set_xlabel("Baccalaureate route", fontsize=12)
ax.set_ylabel("Number of admitted students", fontsize=12)
st.pyplot(fig)

st.write("This chart displays the total number of students admitted by gender across different baccalaureate routes. \n\nIt highlights the difference in performance between boys and girls in the General, Technological, and Professional pathways.")

#%%
st.write("")
st.markdown("<h5 style='color: DarkOrange;'>How many students were admitted, and how many of those were rejected after being part of this group?</h5>", unsafe_allow_html=True)

second_tour = pd.concat([second_tour_ad, second_tour_ref], ignore_index=True)

fig = px.histogram(second_tour, x='academie', y='refu+admis', color='type', barmode='group', color_discrete_map={'Refusal': 'pink', 'Admission': 'black'})

fig.update_layout(
    width=680,
    title={'text':"Admissions and refusals by academy",'x':0.2, 'font':dict(size=19, color='#FF8C00')},
    plot_bgcolor='darkgrey',
    paper_bgcolor='grey',
    xaxis=dict(title_font=dict(size=16, color='#FF8C00'), tickfont=dict(size=12, color='orange')),
    yaxis=dict(title_font=dict(size=16, color='#FF8C00'), tickfont=dict(size=12, color='orange')),
)

st.plotly_chart(fig)
st.write("This interactive bar chart shows the total number of students admitted (black bars) and refused (pink bars) in each academy.\n\nFor every academy, the bars are grouped to allow easy comparison between admissions and refusals. Hovering over the bars provides precise numbers. \n\nThis graph helps visualize success rates across academies, revealing patterns of higher or lower admissions relative to refusals.")

#%%
st.write("")
st.markdown("<h5 style='color: DarkOrange;'>What is the reprensentation per series?</h5>", unsafe_allow_html=True)

st.write("We've seen this in general, by academy, but if we focus on the Bac sub-branch.")

fig, ax = plt.subplots()
performance_by_series.set_index('serie').plot(kind='bar', ax=ax, color=['green', 'red'])
ax.set_title("Ratio by series", fontsize=16)
ax.set_xlabel("Series", fontsize=12)
ax.set_ylabel("Number of students", fontsize=12)
plt.xticks(rotation=90)
st.pyplot(fig)

st.write("As you can see, the 'Generale' series is the best-known and most popular, and has done very well on the test.")

#%%
st.write("")
st.markdown("<h5 style='color: DarkOrange;'>In terms of percentage who comes first?</h5>", unsafe_allow_html=True)

st.write("You'd think that the one with the most admissions would have the highest success rate, but is that really the case?")

fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(success_rate_academy[['success_rate']].sort_values(by='success_rate', ascending=False), cmap='coolwarm', annot=True, ax=ax)
ax.set_title("Success rate by academy", fontsize=16)
st.pyplot(fig)

st.write("We can therefore observe that although Versailles is the academy with the highest number of admissions, it ranks far behind others.\n\nOn the other hand, RENNES didn't stand out all that much, but it did come in first place, which is very surprising, with 95%.\n\nFinally, Mayotte is the academy with the lowest success rate, but it's also one of the smallest in terms of people enrolled, with a rate of 74%.")

#%%

st.markdown("<h4 style='color: Orange;'><center>Conclusion:</h4>", unsafe_allow_html=True)

st.write("This Streamlit project has provided an in-depth analysis of the baccalaureate dataset, revealing key trends in student admissions and performance.\n\nWe found that girls outperform boys, challenging some traditional perceptions. Although academies such as Versailles had a high number of admissions, their success rate was lower than others such as Rennes, which posted the best rate.\n\nThis project underlines the importance of ongoing evaluation of educational strategies to improve student outcomes in France.")

st.write("Marc Rougagnou")




