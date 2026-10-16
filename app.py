import streamlit as st
import json
from urllib.request import urlopen

# إعدادات صفحة التطبيق
st.set_page_config(page_title="إحصاء ومقارنة ألفاظ القرآن الكريم", layout="centered")

st.title("📖 تضافر الكلمات والإحصاء القرآني")
st.write("هذا التطبيق يتيح لك مقارنة عدد مرات تكرار أي كلمتين في القرآن الكريم واكتشاف التوافق الإحصائي بدقة.")

# تحميل بيانات القرآن الكريم المضمونة
@st.cache_data
def load_quran():
    # استخدام مستودع بيانات نصي مباشر ومستقر للقرآن الكريم
    url = "https://raw.githubusercontent.com/risan/quran-json/main/dist/quran.json"
    response = urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    return data

with st.spinner("جاري تحميل بيانات القرآن الكريم وتجهيز محرك البحث..."):
    quran_data = load_quran()

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

        # البحث في السور والآيات
        for surah in quran_data:
            surah_name = surah.get('name', '')
            for ayah in surah.get('verses', []):
                text = ayah.get('text', '')
                ayah_num = ayah.get('id', '')
                
                # حساب تكرار الكلمة الأولى
                if word1 in text:
                    c = text.count(word1)
                    count1 += c
                    matches1.append(f"سورة {surah_name} - الآية {ayah_num}")
                    
                # حساب تكرار الكلمة الثانية
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
            if matches1:
                for m in matches1:
                    st.write(m)
            else:
                st.write("لم تُعثر مطابقات دقيقة للكلمة (تأكد من خلوها من التشكيل المعقد أو الهمقات المختلفة).")

        with st.expander(f"عرض الآيات التي وردت فيها كلمة ({word2})"):
            if matches2:
                for m in matches2:
                    st.write(m)
            else:
                st.write("لم تُعثر مطابقات دقيقة للكلمة.")
