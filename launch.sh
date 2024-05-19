#!/bin/sh
python3 DB.py &
sleep 15
streamlit run UI.py