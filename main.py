import streamlit as st
import time 
st.header('Geomerty Calculator')
area=None
perimeter=None
st.sidebar.title("configuration")
with st.sidebar:
    shape=st.selectbox("choose shape",["cercle" ,"rectangle"])

    
if shape=='cercle':
    radius=st.number_input('radius',min_value=0,max_value=100,step=1)
    area=radius*radius*3.14
    perimeter=2-3.14*radius   
if shape=='rectangle':
    width=st.number_input('widh',0.,step=0.1)
    heihgt=st.number_input('height',0.,step=0.1)  
    perimeter=2*(width+heihgt) 
    area=width*heihgt
compute_btn=st.button("compute area and perimeter")
if compute_btn:
    with st.spinner("In Progress"):
        time.sleep(2)
        st.write("area",area)
        st.write("perimter",perimeter)

