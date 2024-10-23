import streamlit as st
import base64
st.set_page_config(page_title='Portfolio of Marc Rougagnou', page_icon = '👀')

st.write("<h1 style='text-align: center; color: Coral   ;'>📋 My Portfolio !📋</h1>", unsafe_allow_html=True)

#links
linkedin="https://www.linkedin.com/in/marc-rougagnou-data-science/"
github="https://github.com/Marc-Rougagnou"
CV_link = "./images/CV Marc ROUGAGNOU.pdf"
CSV_link = "./dataBacAcademie.csv"
Data_gouv_link = "https://www.data.gouv.fr/fr/datasets/le-baccalaureat-par-academie/"

#sidebar côté gauche
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: orange;'>🔎Summary of informations🔎</strong></h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='color: Darkorange;'><strong>Contact</strong></h4>", unsafe_allow_html=True)
    st.write(
        """
        - E-mail: marc.rougagnou@efrei.net 📧
        - Location: Saint-Maur-des-Fossés 🏠
        """
        )
    st.markdown("<h4 style='color: Darkorange;'><strong>Useful informations</strong></h4>", unsafe_allow_html=True)
    st.write(
        """
        - Driving licence - Vehicle 🚗
        - First aid certificate - PSE1 (2021) 🩺
        - PADI Rescue (scuba diving - 2021) 🤿
        - TOEIC : 720 / 990 📜
        """
        )
    
    st.markdown("<h4 style='color: Darkorange;'><strong>Links</strong></h4>", unsafe_allow_html=True)
    col1,col2 = st.columns(2)
    with col1:    
        st.image("./images/gitlogo.png", width=30)
        st.markdown("[My Github](%s)" %github)
    with col2:
        st.image("./images/link.png", width=30)
        st.markdown("[My Linkedin](%s)" %linkedin)

tab1, tab2 = st.tabs(["_About Me_", "_My projects_"])
 
with tab1:
    #Part Information about me
    st.markdown("<h2 style='color: orange;'><strong>Informations about me 🧑‍💻</strong></h2>", unsafe_allow_html=True)
    st.write("_My name is Marc ROUGAGNOU, I am a student in M1-Data-Engineering at EFREI Paris._")
    
    st.markdown("<h4 style='color: Darkorange;'><strong>My academic background 🏫</strong></h4>", unsafe_allow_html=True)
    st.write("I passed my Baccalaureat with honors before entering the EFREI engineering school. During this training, I chose to spend a semester abroad abroad at Concordia University in Montreal. The courses, taught exclusively in English, enabled me to perfect my language skills. What's more, I oriented my training towards the Data Engineering major. Now I am a student in M1-Data Engineering")
    
    st.markdown("<h4 style='color: Darkorange;'><strong>My professional experiences 🚧</strong></h4>", unsafe_allow_html=True)
    st.write("I have strengthened my ability to adapt within a team, as well as my contribution to group work. In this respect, please find enclosed the evaluations of my two previous internships.\n\nI have also been President of the school's 'LE CONTINENTAL' association for almost three years now. As well as discovering new fields, I've learned to manage all facets of association life: coordination between our members, other associations, our two clubs, the administration, suppliers and the bank; internal management of the association (recruitment, budgeting, stock management, organizing and running meetings, marketing).\n\nI'm also a member of EFREI's 'Le WEI' association, which helps new students integrate and livens up the campus for 1 month. This culminates in the WEI, which is an integration weekend for 1,000 EFREI students who get together on a camping site to have fun, make new friends,...")
    
    #liste de hard skills 
    st.markdown("<h5 style='color: Darkorange;'><strong>Here's one of my hard skills:</strong></h5>", unsafe_allow_html=True)
    st.write(
        """
        - Time management ⌛
        - Scheduling 📅
        - Team management 🤝
        - Listening skills 👂
        """
        )
    
    #part des links
    st.markdown("<h4 style='color: Darkorange;'><strong>My links</strong></h4>", unsafe_allow_html=True)
    col1, col2 = st.columns([0.1,1])
    with col1:
        st.image("./images/gitlogo.png", width=50)
        
    with col2:
        st.markdown("[My Github](%s)" %github)

    col3, col4 = st.columns([0.1,1])
    with col3:
        st.image("./images/link.png", width=50)
    with col4:
        st.markdown("[My Linkedin](%s)" %linkedin)
        
    
    with open(CV_link, "rb") as f: #rb c'est pour ouvrir en binaire
        CV = f.read()
    
    CV_base64 = base64.b64encode(CV).decode('utf-8')
        
        #Part CV
    st.markdown("<h2 style='color: orange;'><strong>If you want to dowload my CV</strong></h2>", unsafe_allow_html=True)
    st.download_button(
        label="Dowload in PDF",
        data=CV,
        file_name="CV_Marc_ROUGAGNOU.pdf",
        mime="application/pdf")

    #mettre *** c'est pour en gras et en italique et entre _ _ c'est en italique
    st.write("***Here is an overview of it:***")
    st.markdown(f'<iframe src="data:application/pdf;base64,{CV_base64}" width="400" height="600" type="application/pdf"></iframe>',unsafe_allow_html=True)


with tab2:
    st.markdown("<h2 style='color: orange;'><strong>My Projects</h2>", unsafe_allow_html=True)
    st.write("On that page there is some examples of my work.\n\nYou can have a look at it and try to do your analyses with the links of datasets.")
    
    with st.expander("***Project on the dataset 'Bac_Academie'***"):
        exec(open("Bac-Projet.py").read())

    with st.expander("***Work on Uber dataset***"):
        exec(open("Uber-dataset.py").read())
    
    
