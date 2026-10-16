import streamlit as st
import json
from urllib.request import urlopen

# إعدادات صفحة التطبيق
st.set_page_config(page_title="إحصاء ومقارنة ألفاظ القرآن الكريم", layout="centered")

st.title("📖 تضافر الكلمات والإحصاء القرآني")
st.write("هذا التطبيق يتيح لك مقارنة عدد مرات تكرار أي كلمتين في القرآن الكريم واكتشاف التوافق الإحصائي بدقة.")

# تحميل بيانات القرآن الكريم مؤقتاً مع التخزين المؤقت لتسريع التطبيق
@st.cache_data
def load_quran():
    url = "https://api.alquran.cloud/v1/quran/quran-uthmani"
    response = urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    return data['data']['surahs']

with st.spinner("جاري تحميل بيانات القرآن الكريم وتجهيز محرك البحث..."):
    surahs_data = load_quran()

# خانات الإدخال للمستخدم
col1, col2 = st.columns(2)
with col1:
    word1 = st.text_input("أدخل الكلمة الأولى:", "الملائكة")
with col2:
    word2 = st.text_input("أدخل الكلمة الثانية:", "الشياطين")

# زر البدء بالمقارنة
if st.button("إجراء الإحصاء والمقارنة 🔍"):
    if not word1 or not word2:
        st.warning("الرجاء إدخال الكلمتين معاً لإتمام المقارنة.")
    else:
        count1 = 0
        count2 = 0
        matches1 = []
        matches2 = []

        # البحث في سور الآيات
        for surah in surahs_data:
            surah_name = surah['name']
            for ayah in surah['ayahs']:
                text = ayah['text']
                ayah_num = ayah['numberInSurah']
                
                if word1 in text:
                    c = text.count(word1)
                    count1 += c
                    matches1.append(f"سورة {surah_name} - الآية {ayah_num}")
                    
                if word2 in text:
                    c = text.count(word2)
                    count2 += c
                    matches2.append(f"سورة {surah_name} - الآية {ayah_num}")

        # عرض النتائج بطريقة بصرية جميلة
        st.markdown("---")
        st.subheader("📊 نتائج المقارنة الإحصائية:")
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.metric(label=f"تكرار لفظ: ({word1})", value=f"{count1} مرة")
        with col_res2:
            st.metric(label=f"تكرار لفظ: ({word2})", value=f"{count2} مرة")

        # التحقق من التطابق
        if count1 == count2:
            st.success(f"✨ توافق إحصائي تام! الكلمتان متساويتان تماماً ({count1} = {count2}).")
        else:
            diff = abs(count1 - count2)
            st.info(f"الفرق بينهما هو: {diff} مرة.")

        # عرض أماكن الآيات
        with st.expander(f"عرض الآيات التي وردت فيها كلمة ({word1})"):
            for m in matches1:
                st.write(m)

        with st.expander(f"عرض الآيات التي وردت فيها كلمة ({word2})"):
            for m in matches2:
                st.write(m)
