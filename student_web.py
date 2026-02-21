import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="โปรแกรมจัดอันดับนักเรียน", layout="wide")

st.title("📊 โปรแกรมจัดอันดับนักเรียน")

# -------------------------
# SESSION
# -------------------------
if "students" not in st.session_state:
    st.session_state.students = []

# -------------------------
# INPUT (ไม่ใช้ form, ไม่ใช้ on_click)
# -------------------------
col1, col2, col3, col4 = st.columns([2,2,2,1])

with col1:
    fname = st.text_input("ชื่อ")

with col2:
    lname = st.text_input("นามสกุล")

with col3:
    score = st.number_input("คะแนน", min_value=0.0, step=1.0)

with col4:
    add_click = st.button("เพิ่มข้อมูล", use_container_width=True)

# 👇 เพิ่มข้อมูลเฉพาะตอนกดปุ่มจริง ๆ เท่านั้น
if add_click:
    if fname and lname:
        st.session_state.students.append({
            "ชื่อ": fname,
            "นามสกุล": lname,
            "คะแนน": score
        })
        st.success("เพิ่มข้อมูลแล้ว")
        st.rerun()
    else:
        st.warning("กรุณากรอกชื่อและนามสกุล")

# -------------------------
# TABLE
# -------------------------
if st.session_state.students:

    df = pd.DataFrame(st.session_state.students)
    df_sorted = df.sort_values(by="คะแนน", ascending=False).reset_index(drop=True)
    df_sorted.insert(0, "อันดับ", df_sorted.index + 1)

    st.subheader("📋 ตารางทั้งหมด")

    for index, row in df_sorted.iterrows():
        c1, c2, c3, c4, c5 = st.columns([1,2,2,2,1])

        c1.write(row["อันดับ"])
        c2.write(row["ชื่อ"])
        c3.write(row["นามสกุล"])
        c4.write(row["คะแนน"])

        if c5.button("🗑️", key=f"del_{index}"):
            st.session_state.students.remove({
                "ชื่อ": row["ชื่อ"],
                "นามสกุล": row["นามสกุล"],
                "คะแนน": row["คะแนน"]
            })
            st.rerun()

    # -------------------------
    # TOP 30
    # -------------------------
    st.divider()
    st.subheader("🏆 Top 30 คนคะแนนสูงสุด")

    top30 = df_sorted.head(30)
    st.dataframe(top30, use_container_width=True)

    # -------------------------
    # EXPORT
    # -------------------------
    def to_excel(dataframe):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            dataframe.to_excel(writer, index=False)
        return output.getvalue()

    st.divider()
    colA, colB = st.columns(2)

    colA.download_button(
        "📥 Export All (Excel)",
        data=to_excel(df_sorted),
        file_name="all_students.xlsx"
    )

    colB.download_button(
        "📥 Export Top 30 (Excel)",
        data=to_excel(top30),
        file_name="top30_students.xlsx"
    )

else:
    st.info("ยังไม่มีข้อมูลนักเรียน")