import streamlit as st
import plotly.express as px
import pandas as pd

import utils.data as data
import utils.graph as graph

st.set_page_config(layout="wide")

def main():
    st.markdown("<h1 style='text-align: center; margin-bottom: 40px;'>Ticket Overview</h1>", unsafe_allow_html=True)

    # Creating a structured layout
    _, left, right, _ = st.columns([0.5, 4, 4, 0.5])

    with left:
        cd_df = data.load_cd_data()
        cd_df = data.parse_cd_data(cd_df)

        st.markdown("<h2 style='text-align: center; color: white; font-weight: 200; margin-bottom: 0px;'>Classroom Down</h2>", unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style="text-align: center;
                background-color: #1e2129; 
                padding: 20px 20px 1px 20px;
                border-radius: 12px; 
                border: 1px solid #30363d;
                display: inline-block;
                min-width: 150px;
                margin-bottom: 10px;
            ">
                <p style="
                    color: #8b949e; 
                    font-size: 0.9rem;
                    margin: 0; 
                    font-weight: 500;
                    letter-spacing: 0.5px;
                ">Total Tickets</p>
                <h2 style="
                    color: #ffffff; 
                    font-size: 2.2rem; 
                    margin: -20px 0 0 0; 
                    font-weight: 700;
                ">{len(cd_df)}</h2>
            </div>
        """, unsafe_allow_html=True)

        st.plotly_chart(graph.draw_ticket_volumes(cd_df), width='stretch')
    
    with right:
        crt_df = data.load_crt_data()
        crt_df = data.parse_crt_data(crt_df)

        st.markdown("<h2 style='text-align: center; color: white; font-weight: 200; margin-bottom: 0px;'>Classroom Response Team</h2>", unsafe_allow_html=True)

        st.markdown(f"""
            <div style="text-align: center;
                background-color: #1e2129; 
                padding: 20px 20px 1px 20px;
                border-radius: 12px; 
                border: 1px solid #30363d;
                display: inline-block;
                min-width: 150px;
                margin-bottom: 10px;
            ">
                <p style="
                    color: #8b949e; 
                    font-size: 0.9rem;
                    margin: 0; 
                    font-weight: 500;
                    letter-spacing: 0.5px;
                ">Total Tickets</p>
                <h2 style="
                    color: #ffffff; 
                    font-size: 2.2rem; 
                    margin: -20px 0 0 0; 
                    font-weight: 700;
                ">{len(crt_df)}</h2>
            </div>
        """, unsafe_allow_html=True)

        st.plotly_chart(graph.draw_ticket_volumes(crt_df), width='stretch')

if __name__ == "__main__":
    main()