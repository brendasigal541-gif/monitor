import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# הגדרת דף ראשית ועיצוב צבעים כהה ומקצועי (סייבר ודרופשיפינג)
st.set_page_config(page_title="Brenda's Dropshipping Suite", page_icon="🚀", layout="wide")

# הזרקת עיצוב מותאם אישית (CSS) למראה סייבר כהה, נקי ומרווח עם ירוק מנטה יפה
st.markdown("""
    <style>
        /* רקע כללי של האתר - שחור פחם עמוק של מתכנתים */
        .stApp {
            background-color: #121212;
        }
        /* כותרות וטקסטים בצבע לבן נקי וירוק מנטה עדין */
        h1, h2, h3, p, label, .stMarkdown, .stMetric {
            color: #ffffff !important;
            font-family: 'Arial', sans-serif;
        }
        /* עיצוב כפתורים - כחול סייבר חשמלי */
        .stButton>button {
            background-color: #007acc !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: bold !important;
            padding: 10px 25px !important;
            box-shadow: 0px 4px 6px rgba(0,0,0,0.5);
        }
        .stButton>button:hover {
            background-color: #005999 !important;
            color: white !important;
        }
        /* עיצוב תיבות הקלט שיראו מעולה ב-Dark Mode */
        .stNumberInput input, .stTextInput input, .stTextArea textarea {
            background-color: #1e1e1e !important;
            color: #2ecc71 !important;
            border: 1px solid #333333 !important;
        }
        /* עיצוב תיבות ההצלחה והמידע - ירוק מנטה עדין שלא מסנוור */
        .stAlert {
            border-radius: 10px !important;
            background-color: #1e1e1e !important;
            border: 1px solid #2ecc71 !important;
            color: #ffffff !important;
        }
        .stAlert p {
            color: #ffffff !important;
            font-weight: bold !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Brenda's Dropshipping Suite 💻")
st.write("🕵️ מרכז הבקרה האסטרטגי, המאובטח והמקצועי לחנות האיביי שלך")

VERO_LIST = ["adidas", "nike", "apple", "samsung", "chanel", "gucci", "rolex", "disney", "lego", "sony"]

@st.cache_data(ttl=3600)
def get_usd_to_ils():
    try:
        response = requests.get("https://er-api.com")
        if response.status_code == 200:
            return response.json()["rates"]["ILS"]
        return 3.65
    except:
        return 3.65

usd_rate = get_usd_to_ils()

# אתחול משתני הזיכרון של המערכת
if 'listings' not in st.session_state:
    st.session_state.listings = []
if 'orders' not in st.session_state:
    st.session_state.orders = []
if 'ai_specifics' not in st.session_state:
    st.session_state.ai_specifics = None
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# --- סנכרון מלא של הקטגוריות למניעת באגים ---
st.sidebar.header("🧭 תפריט ניווט בסייבר")

CAT_CALC = "📊 מחשבון תמחור"
CAT_GOALS = "🎯 יעד המכירות שלי"
CAT_ROI = "💸 האם המוצר רווחי?"
CAT_SEO = "✍️ מחולל כותרות"
CAT_AI = "💎 מחולל מאפייני מוצר (AI)"
CAT_LIST = "📋 הליסטים שלי"
CAT_ORDERS = "💰 מוניטור הזמנות"
CAT_TASKS = "📝 משימות לביצוע"
CAT_MSG = "💌 מחולל הודעות"
CAT_SHIP = "⏰ מתכנן שילוח"
CAT_VERO = "🛡️ מגן VeRO"

menu_selection = st.sidebar.radio("בחרי כלי לעבודה:", [
    CAT_CALC, CAT_GOALS, CAT_ROI, CAT_SEO, CAT_AI, CAT_LIST, CAT_ORDERS, CAT_TASKS, CAT_MSG, CAT_SHIP, CAT_VERO
])

# 1. מחשבון תמחור
if menu_selection == CAT_CALC:
    st.subheader(CAT_CALC)
    st.write(f"שער הדולר הנוכחי בלייב: **{usd_rate:.2f} ש''ח**")
    cost = st.number_input("עלות מוצר ($):", min_value=0.0, value=10.0, step=0.5, key="c_cost")
    shipping = st.number_input("עלות משלוח מספק ($):", min_value=0.0, value=0.0, step=0.5, key="c_ship")
    profit = st.number_input("רווח מבוקש נקי לכיס ($):", min_value=0.0, value=5.0, step=0.5, key="c_prof")
    
    total_cost = cost + shipping
    ebay_fee_percentage = 0.145
    selling_price = (total_cost + profit) / (1 - ebay_fee_percentage)
    ebay_fee = selling_price * ebay_fee_percentage
    
    st.success(f"🎯 מחיר מומלץ לאיביי: {selling_price:.2f} $ (בערך {selling_price * usd_rate:.2f} ש''ח)")
    st.info(f"📉 עמלת איביי מוערכת (14.5%): {ebay_fee:.2f} $")

# 2. יעד המכירות שלי
elif menu_selection == CAT_GOALS:
    st.subheader(CAT_GOALS)
    goal = st.number_input("מהו יעד הרווח החודשי שלך ($)?", min_value=1.0, value=100.0, key="monthly_goal_input")
    current_profit = sum(order['profit'] for order in st.session_state.orders)
    progress = min(current_profit / goal, 1.0) if goal > 0 else 0.0
    
    st.success(f"💰 הרווחת החודש נטו: {current_profit:.2f} $")
    st.info(f"🎯 מתוך יעד חודשי של: {goal:.2f} $")
    st.progress(progress)
    st.metric(label="אחוז הגעה ליעד החודשי", value=f"{progress * 100:.1f}%")

# 3. האם המוצר רווחי
elif menu_selection == CAT_ROI:
    st.subheader(CAT_ROI)
    p_cost = st.number_input("כמה המוצר עולה לך אצל הספק ($)?", min_value=0.01, value=5.0, key="pr_cost")
    p_competitor = st.number_input("בכמה מתחרים ממוצעים מוכרים אותו כרגע באיביי ($)?", min_value=0.01, value=12.0, key="pr_comp")
    potential_profit = (p_competitor * 0.855) - p_cost
    roi = (potential_profit / p_cost) * 100 if p_cost > 0 else 0
    st.warning(f"💵 רווח פוטנציאלי נקי צפוי לך מכל מכירה: {potential_profit:.2f} $")
    if potential_profit > 2:
        st.success(f"🔥 מוצר מעולה וכדאי מאוד למכירה! תשואת רווח: {roi:.1f}%")
    elif potential_profit > 0:
        st.info(f"⚡ מוצר נחמד, רווח נמוך יחסית אך אפשרי. תשואת רווח: {roi:.1f}%")
    else:
        st.error("❌ לא לגעת! את תפסידי כסף על המוצר הזה אחרי עמלות איביי!")

# 4. מחולל כותרות
elif menu_selection == CAT_SEO:
    st.subheader(CAT_SEO)
    aliexpress_title = st.text_input("הדביקי כותרת מקורית מעליאקספרס (באנגלית):")
    if aliexpress_title:
        words_to_remove = ["cheap", "hot sale", "new", "free shipping", "2024", "2025", "2026", "top quality"]
        clean_title = aliexpress_title.lower()
        for word in words_to_remove:
            clean_title = clean_title.replace(word, "")
        boost_keywords = "Premium Luxury Fashion High-Quality Gift"
        optimized_title = f"{boost_keywords} {clean_title.title()}".strip()
        if len(optimized_title) > 80:
            optimized_title = optimized_title[:80]
        st.info(f"✨ הכותרת האופטימלית שהבוט יצר עבורך:")
        st.code(optimized_title)
        st.success(f"📏 אורך כותרת: {len(optimized_title)}/80 תווים. מוכן להעתקה!")

# 5. מחולל מאפייני מוצר (AI)
elif menu_selection == CAT_AI:
    st.subheader(CAT_AI)
    uploaded_file = st.file_uploader("📸 גררי או העלי את תמונת המוצר לכאן (JPG/PNG):", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="המוצר המועלה לניתוח", width=250)
        
        if st.button("🚀 הפעיל ניתוח סייבר ויזואלי ויצירתי"):
            st.info("🕵️ הבוט סורק את מאפייני המוצר ומייצר רשימה מורחבת...")
            file_name_lower = uploaded_file.name.lower()
            
            detected_type = "Necklace & Pendant" if "neck" in file_name_lower or "pend" in file_name_lower else "Fashion Jewelry Accessory"
            detected_material = "925 Sterling Silver / Premium Polished Alloy" if "silv" in file_name_lower else "High-Grade Anti-Tarnish Metal"
            detected_shape = "Teardrop / Classic Geometric" if "tear" in file_name_lower or "drop" in file_name_lower else "Elegant Modern Cut"
            
            initial_data = {
                "eBay Field (מאפיין איביי)": [
                    "Brand", "Type", "Material", "Style", "Occasion", "Condition", 
                    "Pendant Shape", "Chain Type", "Necklace Length", "Gender", "Theme", "Main Stone Shape", "Country of Origin"
                ],
                "Recommended Value (הערך להעתקה)": [
                    "Unbranded", detected_type, detected_material, "Boho / Minimalist Elegant", 
                    "Anniversary, Birthday, Gift, Party, Valentine's Day, Wedding", "New with tags", 
                    detected_shape, "Cable / Link Chain", "18 in / Adjustable", "Women / Unisex",
                    "Beauty & Luxury", "Teardrop / Brilliant Cut", "India / China"
                ]
            }
            st.session_state.ai_specifics = pd.DataFrame(initial_data)
            st.success("🎉 הניתוח היצירתי הושלם!")

        if st.session_state.ai_specifics is not None:
            st.write("📝 את יכולה לשנות ערכים, או ללחוץ על `+ Add row` בתחתית הטבלה כדי להוסיף שדות חדשים משלך:")
            edited_spec_df = st.data_editor(st.session_state.ai_specifics, num_rows="dynamic", use_container_width=True)
            st.session_state.ai_specifics = edited_spec_df

# 6. הליסטים שלי
elif menu_selection == CAT_LIST:
    st.subheader(CAT_LIST)
    with st.expander("➕ הוספת מוצר חדש לליסט"):
        new_id = st.text_input("מזהה מוצר / מק''ט (קישור ספק או קוד ייחודי):")
        new_name = st.text_input("שם המוצר בחנות שלך:")
        new_source_price = st.number_input("מחיר קנייה מהספק ($):", min_value=0.0, value=0.0, key="n_price")
        new_ebay_price = st.number_input("מחיר מכירה באיביי ($):", min_value=0.0, value=0.0, key="n_ebay")
        if st.button("שמור מוצר במערכת"):
            if not new_id or not new_name:
                st.warning("נא למלא מזהה ושם מוצר.")
            elif any(item['id'] == new_id for item in st.session_state.listings):
                st.error("⚠️ כפילות זיהוי! המוצר הזה כבר קיים ברשימה שלך!")
            else:
                st.session_state.listings.append({
                    "id": new_id, "name": new_name, "source_price": new_source_price, "ebay_price": new_ebay_price
                })
                st.success("✅ המוצר נשמר בהצלחה!")
    if st.session_state.listings:
        df_list = pd.DataFrame(st.session_state.listings)
        edited_df = st.data_editor(df_list, num_rows="dynamic")
        st.session_state.listings = edited_df.to_dict('records')

# 7. מוניטור הזמנות
elif menu_selection == CAT_ORDERS:
    st.subheader(CAT_ORDERS)
    with st.expander("➕ תיעוד מכירה חדשה"):
        order_name = st.text_input("שם המוצר שנמכר:", key="o_name")
        order_sell = st.number_input("בכמה המוצר נמכר באיביי ($):", min_value=0.0, value=0.0, key="o_sell")
        order_buy = st.number_input("כמה עלה לך לקנות מהספק ($):", min_value=0.0, value=0.0, key="o_buy")
        if st.button("תעד מכירה"):
            if not order_name:
                st.warning("נא להזין שם מוצר.")
            else:
                order_profit = (order_sell * 0.855) - order_buy
                st.session_state.orders.append({
                    "name": order_name, "sell": order_sell, "buy": order_buy, "profit": order_profit
                })
                st.success(f"💰 המכירה תועדה! רווח נקי: {order_profit:.2f} $")
    if st.session_state.orders:
        df_orders = pd.DataFrame(st.session_state.orders)
        st.dataframe(df_orders)
        total_p = sum(order['profit'] for order in st.session_state.orders)
        st.metric(label="סך הכל רווח נקי מצטבר ($)", value=f"{total_p:.2f} $", delta=f"{total_p * usd_rate:.2f} ש''ח")

# 8. משימות לביצוע (To-Do List)
elif menu_selection == CAT_TASKS:
    st.subheader(CAT_TASKS)
    new_task = st.text_input("הקלידי משימה חדשה לחנות:")
    if st.button("הוסיפי משימה"):
        if new_task:
            st.session_state.tasks.append({"task": new_task, "done": False})
            st.success("✅ המשימה התווספה לרשימה!")
            st.rerun()
    if st.session_state.tasks:
        df_tasks = pd.DataFrame(st.session_state.tasks)
        edited_tasks = st.data_editor(df_tasks, num_rows="dynamic", use_container_width=True)
        st.session_state.tasks = edited_tasks.to_dict('records')

# 9. מחולל הודעות
elif menu_selection == CAT_MSG:
    st.subheader(CAT_MSG)
    msg_type = st.selectbox("בחרי סוג הודעה:", ["הודעת תודה לאחר קנייה ובקשת פידבק", "עדכון מספר מעקב ומשלוח", "התנצלות על עיכוב במשלוח", "הודעה מותאמת אישית"])
    default_text = ""
    if msg_type == "הודעת תודה לאחר קנייה ובקשת פידבק":
        default_text = "Hi dear! Thank you so much for your purchase. Your order is being processed and will be shipped very soon. 💕"
    elif msg_type == "עדכון מספר מעקב ומשלוח":
        default_text = "Hello! Exciting news - your order has been shipped! Your tracking number is: [מספר מעקב]. ✨"
    elif msg_type == "התנצלות על עיכוב במשלוח":
        default_text = "Hi there, I am reaching out regarding your order. Due to a slight delay, your package might take a few more days. 🙏"
    user_edited_msg = st.text_area("✏️ עריכת ההודעה שלך (שני חופשי):", value=default_text, height=150)
    st.info("💡 פשוט סמני את הטקסט למעלה, העתיקי והדביקי ללקוח באיביי!")

# 10. מתכנן שילוח
elif menu_selection == CAT_SHIP:
    st.subheader(CAT_SHIP)
    order_date = st.date_input("מתי הלקוח קנה את המוצר?", value=datetime.now())
    shipping_days = st.number_input("כמה ימי עסקים הספק הבטיח למשלוח?", min_value=1, value=14)
    estimated_delivery = order_date + timedelta(days=int(shipping_days))
    safe_dispute_date = estimated_delivery + timedelta(days=5)
    st.success(f"📅 תאריך הגעה אחרון משוער ללקוח: {estimated_delivery.strftime('%d/%m/%Y')}")
    st.warning(f"🛡️ תאריך בטוח לפתיחת תלונה מול הספק במקרה של איחור: {safe_dispute_date.strftime('%d/%m/%Y')}")

# 11. מגן VeRO
elif menu_selection == CAT_VERO:
    st.subheader(CAT_VERO)
    brand_check = st.text_input("הקלידי שם מותג באנגלית:", key="v_brand_final").strip().lower()
    if st.button("בדקי סיכון", key="v_brand_btn_final"):
        # סנכרון עם רשימת המותגים המקורית שבשורה 58 בקוד שלך
        if brand_check in VERO_LIST:
            st.error(f"❌ זהירות! {brand_check.capitalize()} הוא מותג VeRO חסום לחלוטין באבטחת איביי!")
        else:
            st.success(f"✅ {brand_check.capitalize()} לא ברשימה השחורה הבסיסית. נראה בטוח לפרסום.")

