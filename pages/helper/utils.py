import numpy as np
import cv2
import PIL
import streamlit as st
from insightface.app import FaceAnalysis

# Load InsightFace model once (global singleton)
app = FaceAnalysis(
    name="buffalo_l",
    providers=["CPUExecutionProvider"]
)
app.prepare(ctx_id=0, det_size=(640, 640))


def image_obj_to_numpy(image_obj) -> np.ndarray:
    """
    Convert Streamlit image object to RGB numpy array
    (for correct UI display)
    """
    image = PIL.Image.open(image_obj).convert("RGB")
    return np.array(image)


def extract_face_embedding(image_rgb: np.ndarray):
    """
    Extract 512-D identity embedding using InsightFace.
    Converts RGB → BGR internally (required by InsightFace).
    """
    try:
        # 🔥 CRITICAL FIX: RGB → BGR for model
        image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

        faces = app.get(image_bgr)

        if faces is None or len(faces) == 0:
            st.error("No face detected. Please upload a clear face image.")
            return None

        embedding = faces[0].embedding  # (512,)
        return embedding.astype(float).tolist()

    except Exception as e:
        st.error(f"Face extraction failed: {str(e)}")
        return None
