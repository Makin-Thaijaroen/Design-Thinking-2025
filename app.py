# เป็นไลบารีสำหรับสร้างเว็ปแอปด้วย python แบบง่าย
import streamlit as st
# ไลบารีสำหรับจัดการข้อมูลตาราง อ่านไฟล์ csv
import pandas as pd
# เป็นการตั้งค่าหน้าเว็ป(ชื่อบนบราวเชอร์,ทำให้เนื้อหาในเว็ปอยู่ตรงกลางจอ)
st.set_page_config(page_title="ระบบประเมินความดัน", layout="centered")
# สร้างหัวข้อใหญ่หน้าเว็ป
st.title("🩺 ระบบประเมินระดับความดันโลหิต")

# โหลดไฟล์ CSV
#ใช้เพื่อแคชข้อมูลหรือเก็บผลลัพธ์ไว้ชั่วคราว
@st.cache_data
# สร้างฟังก์ชั่นชื่อ load_data เพื่อโหลดข้อมูลจากไฟล์ csv
def load_data():
# ทำการอ่านไฟล์และเก็บไว้ในตัวแปร df และลบช่องว่างข้างหน้าและข้างหลังของคอลั่ม ถ้าทุกอย่างปกติจะทำการส่ง DataFrame กลับไปใช้งาน
    try:
        df = pd.read_csv("table_1.csv")
        df.columns = df.columns.str.strip()
        return df
# ถ้าเกิด error หาไฟล์ไม่เจอ,ไฟล์เสีย,อ่านไม่ได้ ก็จะส่ง DataFram ว่างกลับไป
    except Exception:
        return pd.DataFrame()
# เอาผลลัพธ์ที่ได้มาเก็บไว้ในฟังก์ชั่น df
df = load_data()
# เป็นการตรวจสอบว่าตารางว่างไหมเพื่อเช็คว่าข้อมูลที่เราดึงมาใช้ได้ไหม ถ้าไม่ได้จะแสดงคำว่าไม่พบไฟล์และหยุดการทำงานทันที
if df.empty:
    st.error("❌ ไม่พบไฟล์ table_1.csv")
    st.stop()
# สร้างตัวแปรเก็บชื่อคอลั่ม
category_col = "BLOOD PRESSURE CATEGORY"

# รับค่าความดัน
#สร้างช่องกรอกตัวเลขที่มีทั้งกรอกตัวเลขและลูกศรเพิ่มลดตัวเลข และกำหนดค่าน้อยที่สุด,มากที่สุดและค่าเริ่มต้น
sys = st.number_input("ค่า SYSTOLIC (ตัวบน)", min_value=0, max_value=300, value=120)
dia = st.number_input("ค่า DIASTOLIC (ตัวล่าง)", min_value=0, max_value=200, value=80)

# สร้างฟังก์ชันประเมินระดับ
# สร้าง evaluate_bp เพื่อรับค่า sys,dia
def evaluate_bp(sys, dia):

    # กันค่าที่ไม่สมเหตุสมผล ถ้ามีคนกรอกเป็น 0 อันใดอันหนึ่ง
    if sys == 0 or dia == 0:
        return "Invalid", "invalid"

    # 1️⃣ วิกฤต
    if sys >= 180 or dia >= 120:
        return df.iloc[4][category_col], "crisis"

    # 2️⃣ ระดับ 2
    elif sys >= 140 or dia >= 90:
        return df.iloc[3][category_col], "stage2"
        
    # 4️⃣ ความดันต่ำ 
    elif sys < 90 or dia < 60:
        return "LOW BLOOD PRESSURE", "low"

    # 3️⃣ ระดับ 1
    elif sys >= 130 or dia >= 80:
        return df.iloc[2][category_col], "stage1"
        
    # 5️⃣ ความดันสูงกว่าปกติ
    elif 120 <= sys <= 129 and dia < 80:
        return df.iloc[1][category_col], "elevated"

    # 6️⃣ ถ้าไม่อยู่ในเงื่อนไขไหนเลยแสดงว่า ปกติ
    else:
        return df.iloc[0][category_col], "normal"

# ปุ่มตรวจสอบ ถ้ากดจะเริ่มตรวจสอบเงื่่อนไขข้างล่าง
if st.button("🔍 ตรวจสอบระดับความดัน"):
# ถ้าส่งค่า sys,dia ไปในฟังก์ชั่นโค้ดนี้คืนค่าไปใน stage_name, level ตามโค้ดข้างบน
    stage_name, level = evaluate_bp(sys, dia)
# เป็นการสร้างเส้นแบ่ง
    st.markdown("---")
# สร้างหัวข้อผลลัพธ์
    st.markdown("### 📌 ผลการประเมิน")
# แสดงชื่อระยะจาก stage_name ระยะของโรค
    st.write(f"🔹 ระยะจากไฟล์: **{stage_name}**")
# แสดงค่าที่กรอก
    st.write(f"🔹 ค่าที่กรอก: **{sys} / {dia} mmHg**")
    st.markdown("---")

    # แสดงผลตามระดับและข้อแนะนำเบื้องต้น
    if level == "invalid":
        st.error("❌ ค่าความดันไม่สมเหตุสมผล กรุณาตรวจสอบใหม่")

    elif level == "crisis":
        st.error("🚨 ภาวะวิกฤตความดันโลหิตสูง")
        st.error("ควรพบแพทย์ทันที")

    elif level == "stage2":
        st.error("🚨 ความดันโลหิตสูง ระดับที่ 2")
        st.warning("ควรปรึกษาแพทย์และควบคุมอาหารอย่างจริงจัง")

    elif level == "stage1":
        st.warning("⚠️ ความดันโลหิตสูง ระดับที่ 1")
        st.info("ควรลดเค็ม ออกกำลังกาย และติดตามอาการ")

    elif level == "elevated":
        st.info("📈 ความดันสูงกว่าปกติเล็กน้อย")
        st.info("ควรปรับพฤติกรรมสุขภาพ")

    elif level == "low":
        st.warning("⚠️ ความดันโลหิตต่ำ")
        st.info("อาจเวียนหัว เป็นลม ควรพักผ่อนและดื่มน้ำ")

    elif level == "normal":
        st.success("✅ ความดันโลหิตปกติ")
        st.success("รักษาพฤติกรรมสุขภาพที่ดีต่อไป")
