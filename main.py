import streamlit as st
import docx

st.set_page_config(page_title="🎙️ استخراج النصوص", layout="centered")

st.title("🎙️ استخراج النصوص من خانة 'النص الصوتي'")
uploaded_file = st.file_uploader("📁 ارفع ملف Word", type=["docx"])
prompt = st.text_input("📝 أدخل أمر PROMPT", value="فقط استخرج النصوص كما هي")

if uploaded_file and st.button("📤 استخراج النصوص"):
    doc = docx.Document(uploaded_file)
    results = []
    for table in doc.tables:
        headers = [cell.text.strip() for cell in table.rows[0].cells]
        if "النص الصوتي" in headers:
            index = headers.index("النص الصوتي")
            for row in table.rows[1:]:
                cell_text = row.cells[index].text.strip()
                if cell_text:
                    results.append(cell_text)

    if "شكل الحرف الأخير" in prompt:
        def shape_last(word):
            return word[:-1] + word[-1] + "َ" if len(word) > 1 else word + "َ"
        results = [" ".join([shape_last(w) for w in text.split()]) for text in results]

    st.success(f"تم استخراج {len(results)} نصًا:")
    for i, line in enumerate(results, 1):
        st.markdown(f"**{i}.** {line}")
