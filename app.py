
import streamlit as st
import cv2
import numpy as np
from PIL import Image

from detector import detect_objects
from inventory import count_inventory


st.set_page_config(
    page_title="Smart Inventory Counter",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Smart Inventory Counter")
st.caption("YOLO-powered visual inventory analysis")


confidence = st.sidebar.slider(
    "Confidence Threshold",
    0.10, 0.90, 0.35, 0.05
)

uploaded_file = st.file_uploader(
    "Upload shelf image",
    type=["jpg", "jpeg", "png"]
)


if "scan_result" not in st.session_state:
    st.session_state.scan_result = None


if uploaded_file:

    image = Image.open(uploaded_file).convert("RGB")

    image_array = cv2.cvtColor(
        np.array(image),
        cv2.COLOR_RGB2BGR
    )

    st.image(image, caption="Original Image", use_container_width=True)

    if st.button("🔍 Scan Inventory", type="primary"):

        with st.spinner("Analyzing image..."):

            annotated_image, detections = detect_objects(
                image_array,
                confidence
            )

            inventory_df, total_objects = count_inventory(
                detections
            )

            st.session_state.scan_result = {
                "annotated_image": annotated_image,
                "detections": detections,
                "inventory_df": inventory_df,
                "total_objects": total_objects
            }


result = st.session_state.scan_result

if result is not None:

    st.divider()
    st.subheader("Analysis Results")

    col1, col2 = st.columns(2)

    col1.metric(
        "Total Objects",
        result["total_objects"]
    )

    col2.metric(
        "Unique Categories",
        len(result["inventory_df"])
    )

    st.subheader("Detection Visualization")

    annotated_rgb = cv2.cvtColor(
        result["annotated_image"],
        cv2.COLOR_BGR2RGB
    )

    st.image(
        annotated_rgb,
        use_container_width=True
    )

    st.subheader("Inventory Breakdown")

    df = result["inventory_df"]

    if not df.empty:

        st.dataframe(
            df,
            hide_index=True,
            use_container_width=True
        )

        st.bar_chart(
            df.set_index("Object")["Quantity"]
        )

        csv_data = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "📥 Download CSV Report",
            csv_data,
            "inventory_report.csv",
            "text/csv"
        )

    else:

        st.warning("No objects detected in the image.")
