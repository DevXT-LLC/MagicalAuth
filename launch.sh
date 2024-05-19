#!/bin/sh
sleep 10
python3 DB.py &
sleep 15
streamlit run UI.py