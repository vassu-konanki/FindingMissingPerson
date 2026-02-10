import uuid
import json
import numpy as np
import streamlit as st

from pages.helper import db_queries
from pages.helper.data_models import PublicSubmissions
from pages.helper.utils import image_obj_to_numpy, extract_face_embedding
from pages.helper.streamlit_helpers import require_login, save_image


st.set_page_config("Mobile UI", initial_sidebar_state="collapsed")
st.title("Make a submission")

image_col, form_col = st.columns(2)
image_obj = None
save_flag = 0
image_numpy = None
image_path = None
face_mesh = None

with image_col:
    image_obj = st.file_uploader(
        "Image", type=["jpg", "jpeg", "png"], key="user_submission"
    )

    if image_obj:
        with st.spinner("Processing..."):
            st.image(image_obj, width=200)

            image_numpy = image_obj_to_numpy(image_obj)
            face_mesh = extract_face_embedding(image_numpy)

            # 🔥 THE REAL FIX
            image_path = save_image(image_numpy)

if image_obj:
    with form_col.form(key="new_user_submission"):
        name = st.text_input("Your Name")
        mobile_number = st.text_input("Your Mobile Number")
        email = st.text_input("Your Email")
        address = st.text_input("Address / Location last seen")

        color = st.text_input("Color (Skin / Hair / Eye)")
        height = st.text_input("Height (in cm)")
        birth_marks = st.text_input("Birth Marks")

        submit_bt = st.form_submit_button("Submit")

        if submit_bt:
            public_submission_details = PublicSubmissions(
                submitted_by=name,
                mobile=mobile_number,
                email=email,
                location=address,
                color=color,
                height=height,
                face_mesh=json.dumps(face_mesh),
                image_path=image_path,      # 🔥 REQUIRED
                birth_marks=birth_marks,
                status="NF",
            )

            db_queries.new_public_case(public_submission_details)
            save_flag = 1

    if save_flag == 1:
        st.success("Successfully Submitted")
