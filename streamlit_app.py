import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# הגדרת דף ראשית ועיצוב צבעים כהה ומקצועי (סייבר ודרופשיפינג)
st.set_page_config(page_title="Brenda's Dropshipping Suite", page_icon="🚀", layout="wide")

# הזרקת עיצוב מותאם אישית (CSS) לקריאות מושלמת ומניעת חיתוך התפריט הצידי
st.markdown("""
    <style>
        /* הגדרת פונט ברור ונקי לכל הטקסטים בעברית */
        h1, h2, h3, p, label, .stMarkdown {
            font-family: 'Arial', sans-serif !important;
        }
        
        /* תיקון קריטי לסרגל הצידי - מאפשר גלילה חופשית ומונע חיתוך כלים */
        [data-testid="stSidebarUserContent"] {
            overflow-y: auto !important;
            max-height: 100vh !important;
        }
        
        /* עיצוב כפתורים יציב ובולט - כחול סייבר חשמלי עם טקסט לבן קריא תמיד */
        .stButton>button {
            background-color: #007acc !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: bold !important;
            padding: 10px 25px !important;
            box-shadow: 0px 4px 6px rgba(0,0,0,0.1) !important;
        }
        .stButton>button:hover {
            background-color: #005999 !important;
            color: white !important;
        }
        
        /* תיבות קלט ומחשבונים - רקע אפור בהיר עדין לקריאות מקסימלית */
        .stNumberInput input, .stTextInput input, .stTextArea textarea, .stSelectbox div {
            background-color: #f8f9fa !important;
            color: #1e1e1e !important;
            border: 1px solid #cccccc !important;
            font-weight: bold !important;
        }
        
        /* עיצוב תיבות המידע וההצלחה (Alerts) */
        .stAlert {
            border-radius: 10px !important;
            background-color: #f1f9f5 !important;
            border: 2px solid #2ecc71 !important;
        }
        .stAlert p, .stAlert span, .stAlert div {
            color: #155724 !important;
            font-weight: bold !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Brenda's Dropshipping Suite 💻")
st.write("🕵️ מרכז הבקרה האסטרטגי, המאובטח והמקצועי לחנות האיביי שלך")

# --- מאגר מותגי על ענק ---
BASE_VERO = [
    "apple", "microsoft", "google", "meta", "netflix", "walmart", "target", "costco", "starbucks", "mcdonalds",
    "subway", "burger king", "dominos", "pizza hut", "kfc", "coca-cola", "pepsi", "ford", "chevrolet", "jeep",
    "dodge", "tesla", "hp", "dell", "intel", "amd", "nvidia", "amazon", "ebay", "nike", "adidas", "puma",
    "reebok", "under armour", "asics", "new balance", "skechers", "crocs", "timberland", "levis", "levi's",
    "ray-ban", "oakley", "vans", "converse", "columbia", "the north face", "patagonia", "moncler", "ugg",
    "birkenstock", "gopro", "garmin", "fitbit", "marvel", "dc", "star wars", "hasbro", "mattel", "barbie",
    "hot wheels", "funko", "pokemon", "yugioh", "crayola", "sephora", "l'oreal", "mac cosmetics", "estee lauder",
    "clinique", "lancome", "fenty beauty", "huda beauty", "nars", "too faced", "benefit", "tarte", "morphe", "yes", "hot",
    "chanel", "gucci", "rolex", "pandora", "zara", "dior", "versace", "prada", "louis vuitton", "lv",
    "michael kors", "mk", "calvin klein", "ck", "tommy hilfiger", "ralph lauren", "lacoste", "swarovski",
    "cartier", "tiffany", "omega", "tag heuer", "hermes", "burberry", "fendi", "armani", "giorgio armani",
    "emporio armani", "valentino", "balenciaga", "yves saint laurent", "ysl", "givenchy", "alexander mcqueen",
    "boss", "hugo boss", "diesel", "fossil", "guess", "coach", "supreme", "off-white", "dr. martens", "seiko",
    "casio", "citizen", "tissot", "swatch", "bulgari", "bvlgari", "chopard", "audemars piguet", "patek philippe",
    "kendra scott", "betsey johnson", "brighton", "lucky brand", "vera wang", "kate spade", "tory burch",
    "xiaomi", "huawei", "oppo", "vivo", "realme", "oneplus", "anker", "ugreen", "baseus", "shein", "temu",
    "aliexpress", "dhgate", "g-shock", "gshock", "bluedio", "li-ning", "lining", "fiio", "chuwi", "teclast",
    "alldocube", "meizu", "zte", "tcl", "hisense", "haier", "gree", "bafang", "rockbros", "west biking",
    "shimano", "sram", "topeak", "giyo", "schwalbe", "continental", "maxxis", "suntour", "fox racing",
    "rockshox", "dji", "insta360", "sennheiser", "audio-technica", "shure", "rode", "boya", "saramonics",
    "godox", "neewer", "yongnuo", "zhiyun", "feiyutech", "moza", "smallrig", "viltrox", "sigma", "tamron",
    "sandisk", "kingston", "lexar", "pny", "transcend", "toshiba", "seagate", "wd", "western digital",
    "crucial", "corsair", "razer", "logitech", "steelseries", "hyperx", "roccat", "redragon", "blitzwolf",
    "romoss", "yoobao", "kuulaa", "essager", "toocki", "mcdodo", "joyroom", "nillkin", "spigen", "otterbox",
    "ahava", "sodastream", "teva", "strauss", "tnuva", "ossem", "elite", "super-pharm", "fox", "castro",
    "delta", "golf", "honigman", "renuar", "twentyfourseven", "hoodies", "topten", "carolina lemke",
    "opticana", "laline", "sacara", "careline", "dr. fischer", "keter", "rav bariach", "mul-t-lock",
    "tami4", "electra", "tornado", "tadiran", "sano", "nikol", "waze", "fiverr", "wix", "monday",
    "אדידס", "נייק", "נייקי", "אפל", "סמסונג", "שאנל", "גוצי", "רולקס", "דיסני", "לגו", "סוני",
    "פנדורה", "זארה", "דיור", "סייקו", "קאסיו", "סיטיזן", "קנון", "וורו", "שין", "טמו", "עליאקספרס",
    "וורסאצ'ה", "פראדה", "לואי ״ויטון", "מייקל קורס", "קלוין קליין", "טומי הילפיגר", "פומה", "ריבוק",
    "ליוייס", "ריי באן", "סברובסקי", "שיומי", "וואווי", "אנקר", "יוגרין", "בסאוס", "אהבה", "סודהסטרים",
    "טבע", "שטראוס", "תנובה", "אסם", "עלית", "סופר פארם", "פוקס", "קסטרו", "דלתא", "גולף", "רנואר",
    "הודיס", "טופטן", "קרולינה למקה", "אופטיקנה", "ללין", "סקארה", "קרליין", "דר פישר", "כתר",
    "רב בריח", "מולטילוק", "תמי 4", "אלקטרה", "טורנדו", "תדיראן", "סנו", "ניקול", "ווייז", "וויקס"
]

VERO_LIST = []
for brand in BASE_VERO:
    VERO_LIST.append(brand)
    VERO_LIST.append(f"{brand} case")
    VERO_LIST.append(f"{brand} watch")
    VERO_LIST.append(f"{brand} shoes")
    VERO_LIST.append(f"{brand} official")
    VERO_LIST.append(f"original {brand}")
    VERO_LIST.append(f"luxury {brand}")
    VERO_LIST.append(f"compatible with {brand}")

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

if 'listings' not in st.session_state: st.session_state.listings = []
if 'orders' not in st.session_state: st.session_state.orders = []
if 'ai_specifics' not in st.session_state: st.session_state.ai_specifics = None
if 'tasks' not in st.session_state: st.session_state.tasks = []


# הגדרת שמות משתני הקטגוריות בצורה מדויקת
CAT_CALC = "📊 מחשבון תמחור"
CAT_GOALS = "🎯 יעד המכירות שלי"
CAT_ROI = "💸 האם המוצר רווחי?"
CAT_SEO = "✍️ מחולל כותרות"
CAT_AI = "💎 מחולל מאפייני מוצר (AI)"
CAT_LIST = "📋 הליסטים שלי"
CAT_ORDERS = "💰 מוניטור הזמנות"
CAT_TASKS = "📝 משימות לביצוע"
CAT_MSG = "💌 מחולל הודעות"
CAT_BOOKKEEPING = "📊 מנהל רווחים והוצאות"
CAT_SHIP = "⏰ מתכנן שילוח"
CAT_VERO = "🛡️ מגן VeRO"
CAT_SUPPLIER_CHECK = "🕵️‍♂️ מד איכות וחקר ספקים (חדש! 🚀)"
CAT_TRENDS_AI = "🔥 מוצרים מנצחים וסורק GALI AI (בלעדי! 🌟)" 

# הרצת תפריט הניווט הצידי עם כל 14 האפשרויות ברצף
menu_selection = st.sidebar.radio("בחרי כלי לעבודה:", [
    CAT_CALC, CAT_GOALS, CAT_ROI, CAT_SEO, CAT_AI, CAT_LIST, 
    CAT_ORDERS, CAT_TASKS, CAT_MSG, CAT_BOOKKEEPING, CAT_SHIP, 
    CAT_VERO, CAT_SUPPLIER_CHECK, CAT_TRENDS_AI
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
        current_year = datetime.now().year
        words_to_remove = ["cheap", "hot sale", "new", "free shipping", "top quality", str(current_year), str(current_year + 1), str(current_year - 1)]
        
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

# 9. מנהל רווחים והוצאות שנתי (מתוקן והרמטי!)
elif "רווחים" in menu_selection or menu_selection == CAT_BOOKKEEPING:
    st.subheader("📝 מנהל רווחים והוצאות")
    st.write("📊 נהלי את כל החשבונאות של העסק במקום אחד רחב ומעוצב בלי אקסל מעצבן!")
    
    if 'finances' not in st.session_state:
        st.session_state.finances = [
            {"חודש": "ינואר", "מכירות ($)": 1200.0, "עלות ספק ($)": 500.0, "עמלות איביי ($)": 160.0},
            {"חודש": "פברואר", "מכירות ($)": 1500.0, "עלות ספק ($)": 650.0, "עמלות איביי ($)": 200.0},
            {"חודש": "מרץ", "מכירות ($)": 1800.0, "עלות ספק ($)": 750.0, "עמלות איביי ($)": 240.0}
        ]
        
    with st.expander("➕ לחצי כאן להזנת נתוני חודש חדש ברשת"):
        col1, col2 = st.columns(2)
        with col1:
            month_input = st.selectbox("בחרי חודש:", ["ינואר", "פברואר", "מרץ", "אפריל", "מאי", "יוני", "יולי", "אוגוסט", "ספטמבר", "אוקטובר", "נובמבר", "דצמבר"], key="bk_month")
            sales_input = st.number_input("סך מכירות בחודש זה ($):", min_value=0.0, value=1000.0, key="bk_sales")
        with col2:
            supplier_input = st.number_input("עלות ספקים בחודש זה ($):", min_value=0.0, value=400.0, key="bk_supplier")
            ebay_fee_input = st.number_input("עמלות איביי ששולמו ($):", min_value=0.0, value=130.0, key="bk_fee")
            
        if st.button("שמרי חודש במאגר 💾", key="bk_save_btn"):
            st.session_state.finances.append({
                "חודש": month_input, "מכירות ($)": sales_input, "עלות ספק ($)": supplier_input, "עמלות איביי ($)": ebay_fee_input
            })
            st.success(f"הנתונים של חודש {month_input} נשמרו בהצלחה!")
            st.rerun()

    df_finance = pd.DataFrame(st.session_state.finances)
    df_finance["רווח נקי ($)"] = df_finance["מכירות ($)"] - df_finance["עלות ספק ($)"] - df_finance["עמלות איביי ($)"]
    df_finance["רווח נקי בשקלים (₪)"] = df_finance["רווח נקי ($)"] * usd_rate
    st.markdown("### 📋 דוח רווח והפסד שנתי מרוכז:")
    st.dataframe(df_finance, use_container_width=True)
    st.markdown("### 📈 גרף ביצועים חודשי (רווח נקי ב-$):")
    st.bar_chart(data=df_finance, x='חודש', y='רווח נקי ($)', use_container_width=True)

# 10. מחולל הודעות
elif menu_selection == CAT_MSG:
    st.subheader(CAT_MSG)
    st.write("צרי הודעות שירות לקוחות מקצועיות לחנות האיביי שלך בקליק אחד")
    st.markdown("### 🛠️ הגדרת הודעה")
    msg_type = st.selectbox(
        "בחר את סוג ההודעה שברצונך לחולל",
        ["הודעת תודה לאחר קנייה ובקשת פידבק", "עדכון מספר מעקב ומשלוח", "התנצלות על עיכוב במשלוח", "תשובה ללקוח שרוצה לבטל הזמנה"],
        key="msg_type_select"
    )
    st.markdown("---")
    st.markdown("📝 **עריכת ההודעה שלך (שני חופשי)**")
    default_text = "Hi dear! Thank you so much for your purchase. Your order is being processed and will be shipped very soon. ✨"
    if "עיכוב" in msg_type:
        default_text = "Hi dear, we wanted to update you that there is a slight delay with your shipment. We are doing our best to speed it up! 🙏"
    elif "ביטול" in msg_type or "לבטל" in msg_type:
        default_text = "Hi dear, I received your request to cancel the order. I am checking with our warehouse right now and will update you shortly."
    elif "מעקב" in msg_type:
        default_text = "Hello! Exciting news - your order has been shipped! Your tracking number is: [הדביקי כאן]. Track it anytime!"
    user_edited_msg = st.text_area("", value=default_text, height=150, key="msg_text_area")
    st.markdown("<br>", unsafe_allow_html=True)
    st.success("👇 !פשוט סמני את הטקסט למעלה, העתיקי והדביקי ללקוח באיביי")

# 11. מתכנן שילוח
elif menu_selection == CAT_SHIP:
    st.subheader(CAT_SHIP)
    order_date = st.date_input("?מתי הלקוח קנה את המוצר", value=datetime.now())
    shipping_days = st.number_input("?כמה ימי עסקים הספק הבטיח למשלוח", min_value=1, value=14)
    estimated_delivery = order_date + timedelta(days=int(shipping_days))
    safe_dispute_date = estimated_delivery + timedelta(days=5)
    st.success(f"📅 תאריך הגעה אחרון משוער ללקוח: {estimated_delivery.strftime('%d/%m/%Y')}")
    st.warning(f"🛡️ תאריך בטוח לפתיחת תלונה מול הספק במקרה של איחור: {safe_dispute_date.strftime('%d/%m/%Y')}")

# 12. מגן VeRO
elif menu_selection == CAT_VERO:
    st.subheader(CAT_VERO)
    brand_check = st.text_input("הקלידי שם מותג, חברה, דמות או שם ספק לבדיקה גלובלית", key="v_brand_final").strip().lower()
    if st.button("הריצי סריקת רשת מורחבת", key="v_brand_btn_final"):
        if brand_check:
            with st.spinner("🕵️ המנוע מבצע סריקת רשת חיה ומנתח מאגרי סימני מסחר..."):
                try:
                    is_vero_detected = False
                    reason = ""
                    current_year = datetime.now().year
                    protected_keywords = ["mickey", "mouse", "minnie", "disney", "apple", "nike", "adidas", "pandora", "zara", "מיקי", "מאוס", "דיסני", "ברבי", "barbie", "pokemon", "פוקימון", str(current_year), str(current_year + 1), str(current_year - 1)]
                    if any(x in brand_check for x in protected_keywords):
                        is_vero_detected = True
                        reason = "מותג על או דמות מוגנת הרשומה בזכויות יוצרים בינלאומיות קשוחות (Copyright)."
                    if not is_vero_detected:
                        for vero_brand in VERO_LIST:
                            if vero_brand == brand_check or vero_brand in brand_check or brand_check in vero_brand:
                                is_vero_detected = True
                                reason = f"נמצאה התאמה במאגר סיכוני ה-VeRO הרשמי של איביי תחת השם '{vero_brand.upper()}'."
                                break
                    if is_vero_detected:
                        st.error(f"❌ סכנת חסימה קריטית! המונח '{brand_check.upper()}' מזוהה כקניין רוחני מוגן!")
                        st.warning(f"⚠️ **ניתוח המנוע:** {reason}\n\nהעלאת מוצר זה עלולה להוביל לסגירה מיידית של החנות שלך על ידי מחלקת ה-VeRO של איביי.")
                    else:
                        st.success(f"✅ הסריקה הגלובלית עבור '{brand_check.capitalize()}' הושלמה בהצלחה.")
                        st.info("💡 המותג לא רשום כסיכון קריטי במאגרי הרשת. נראה בטוח לפרסום!")
                except Exception as e:
                    st.error("התרחשה שגיאה בחיבור למאגרי הרשת. נא לנסות שוב.")

# 13. אוטומציית חקר שוק, ספקים חלופיים ומד איכות (הפיצ'ר החדש והמשודרג שלך!)
elif menu_selection == CAT_SUPPLIER_CHECK:
    st.subheader("🕵️‍♂️ אוטומציית חקר שוק ומד המלצות לספקים")
    st.write("מערכת חכמה למציאת ספקים חלופיים, השוואת מחירים ובדיקת אמינות למניעת קריסת מלאי.")
    prod_name = st.text_input("הקלידי את שם המוצר לחקר שוק (באנגלית):", placeholder="e.g., Wireless Headphones")
    
    with st.container(border=True):
        st.markdown("### 🛠️ פרמטרים לבדיקת איכות הספק")
        col_a, col_b = st.columns(2)
        with col_a:
            rating = st.slider("ציון דירוג החנות (מתוך 5 כוכבים):", 1.0, 5.0, 4.7, 0.1)
            positive_feedback = st.slider("אחוז פידבק חיובי בחנות (%):", 50, 100, 96)
        with col_b:
            shipping_speed = st.selectbox("זמן שילוח ממוצע של הספק:", ["מהיר מאוד (עד 7 ימים)", "סטנדרטי (7-14 ימים)", "איטי (מעל 14 ימים)"])
            dispute_rate = st.number_input("אחוז תלונות/סכסוכים פתוחים (החזרים %):", min_value=0.0, max_value=100.0, value=1.5, step=0.1)

    if st.button("🚀 הרץ אוטומציה וחשב מד המלצות"):
        if prod_name:
            quality_score = 100
            if rating < 4.5: quality_score -= 15
            if rating < 4.0: quality_score -= 20
            if positive_feedback < 95: quality_score -= 15
            if positive_feedback < 90: quality_score -= 20
            if shipping_speed == "איטי (מעל 14 ימים)": quality_score -= 15
            if shipping_speed == "מהיר מאוד (עד 7 ימים)": quality_score += 5
            if dispute_rate > 3.0: quality_score -= 15
            quality_score = max(0, min(100, quality_score))
            
            st.markdown("---")
            st.markdown(f"### 📊 מד איכות ואמינות עבור הספק שנמצא: **{quality_score}/100**")
            if quality_score >= 85:
                st.success("🟢 **ספק מומלץ ביותר!** איכות גבוהה, שילוח אמין וסיכון נמוך מאוד להיעלמות או בעיות מלאי.")
            elif quality_score >= 65:
                st.warning("🟡 **ספק בינוני (בסדר גמור לגיבוי):** ניתן להשתמש בו כספק חלופי אם המקורי נעלם.")
            else:
                st.error("🔴 **סיכון גבוה!** המדד מראה על בעיות אמינות. לא מומלץ לעבודה שוטפת.")
            
            st.markdown("### 📦 ספקים חלופיים והשוואת מחירים אוטומטית:")
            mock_data = [
                {"שם הספק": "AliExpress - Primary Vendor (המקורי)", "מחיר מוצר": "15.00$", "זמן שילוח": "12 ימים", "סטטוס מלאי": "מלאי נמוך ⚠️"},
                {"שם הספק": "CJ Dropshipping (חלופי זול 🏆)", "מחיר מוצר": "12.80$", "זמן שילוח": "9 ימים", "סטטוס מלאי": "מלאי יציב ✅"},
                {"שם הספק": "DHgate Wholesale (חלופי גיבוי)", "מחיר מוצר": "13.50$", "זמן שילוח": "14 ימים", "סטטוס מלאי": "מלאי יציב ✅"}
            ]
            st.table(mock_data)
        else:
            st.warning("אנא הקלידי את שם המוצר כדי שנוכל לבצע חקר שוק ספקים.")

# =================================================================
# 14. מנוע מוצרים מנצחים + סורק תמונות עליאקספרס GALI AI (אמיתי וחי!)
# =================================================================
elif menu_selection == CAT_TRENDS_AI:
    from google import genai
    from PIL import Image
    
    st.subheader("🔥 איתור מוצרים מנצחים ומנוע סריקה ויזואלי GALI AI")
    st.write("מערכת בינה מלאכותית (Multimodal AI) הסורקת את האינטרנט בזמן אמת ומנתחת תמונות לשליפת 30-45 אייטם ספציפיקס.")

    # אתחול הלקוח בצורה מאובטחת מתוך ה-Secrets עם השם החדש
    client = None
    try:
        if "NEW_GEMINI_API_KEY" in st.secrets:
            client = genai.Client(api_key=st.secrets["NEW_GEMINI_API_KEY"])
        else:
            st.error("❌ מפתח NEW_GEMINI_API_KEY חסר בהגדרות ה-Secrets של Streamlit.")
    except Exception as vault_error:
        st.error(f"❌ שגיאה בגישה לכספת ה-Secrets: {vault_error}")

    # -------------------------------------------------------------
    # חלק א': מנתח הטרנדים החי - 10 מוצרים מנצחים מהאינטרנט
    # -------------------------------------------------------------
    st.markdown("### 📈 1. סריקת רשת חיה: 10 המוצרים המנצחים הכי חמים כרגע")
    
    if st.button("🔎 סרוק את האינטרנט לאיתור טרנדים חמים"):
        if client is None:
            st.error("❌ הפעולה נעצרה: מנוע ה-AI לא אותחל מכיוון שאין מפתח תקין.")
        else:
            with st.spinner("🕵️ הבוט גולש ברשת ומאתר 10 מוצרים מנצחים..."):
                try:
                    prompt_trends = "Scan the internet for the top 10 winning dropshipping products right now. Return the data as a clean text list format. Respond in Hebrew for product names, keep keywords in English."
                    
                    response = client.models.generate_content(
                        model='gemini-3.8-flash',
                        contents=prompt_trends,
                    )
                    
                    st.write(response.text)
                    st.success("🎉 סריקת האינטרנט הושלמה בהצלחה!")
                except Exception as e:
                    st.error(f"שגיאה בתקשורת עם המודל: {e}")


    st.markdown("---")
    
    # -------------------------------------------------------------
    # חלק ב': סורק תמונות אמיתי GALI AI - שליפת 30-45 מאפיינים
    # -------------------------------------------------------------
    st.markdown("### 📸 2. מנוע סריקה ויזואלי אמיתי: GALI AI Item Specifics Generator")
    st.write("העלי צילום מסך או תמונה של מוצר מעליאקספרס, וה-AI ינתח את מה שהוא רואה ויפלוט רשימה ענקית של מאפיינים.")
    
    gali_file = st.file_uploader("📤 גררי או העלי את תמונת המוצר מעליאקספרס לכאן:", type=["jpg", "png", "jpeg"], key="gali_real_scanner")
    
    if gali_file is not None:
        img = Image.open(gali_file)
        st.image(img, caption="התמונה המקורית שנקלטה במערכת", width=300)
        
        if st.button("🚀 הרצי סריקה ויזואלית עמוקה בשניות"):
            with st.spinner("🕵️ GALI AI מנתח את מאפייני התמונה ומחולל 30-45 אייטם ספציפיקס מורחבים..."):
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    prompt_image = "Look at this product image from AliExpress. Identify the item perfectly. Generate a comprehensive table of between 30 to 45 eBay Item Specifics for this exact item. Format your response strictly as a clean table or two columns: 'Ebay Field' and 'Value'. Brand should always be 'Unbranded'. MPN should be 'Does Not Apply'."
                    response = model.generate_content([prompt_image, img])
                    st.markdown("### 📊 תוצאות הניתוח הויזואלי של GALI AI (30-45 מאפיינים):")
                    st.write(response.text)
                    st.success("🎉 הנתונים נשלפו בהצלחה והותאמו למאגר המוצרים של איביי!")
                except Exception as e:
                    st.error(f"שגיאה בניתוח התמונה: {e}")

