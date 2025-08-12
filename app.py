import streamlit as st
import os

st.title("3D Rendered Image Preview")

assets_folder = "assets"

if not os.path.exists(assets_folder):
    st.error("Assets folder not found. Please add rendered images to assets/")
else:
    images = [img for img in os.listdir(assets_folder) if img.lower().endswith(".png")]
    if not images:
        st.warning("No PNG images found in assets/")
    else:
        for img in images:
            st.image(os.path.join(assets_folder, img), caption=img)
