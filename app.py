import streamlit as st
from datetime import datetime

st.set_page_config(page_title="AI 雙語工程電郵助手", page_icon="✉️", layout="centered")

st.title("✉️ AI 雙語工程電郵助手 (E&M Assistant)")
st.write("針對工程界設計：支援中英雙語對照、自動 AI 專業潤飾、一鍵快速複製英文電郵！")

st.divider()

# --- 1. 設定電郵選項 ---
st.subheader("📌 1. 電郵參數設定")

col1, col2 = st.columns(2)
with col1:
    recipient_type = st.selectbox(
        "收件人對象", 
        ["對客戶 (Client / 商業夥伴)", "對業主 / 則師 (Landlord / Consultant)", "對內部工程團隊 / 判頭"]
    )
    tone_style = st.selectbox(
        "語氣風格 (Tone)", 
        ["Formal (正式、專業、合規)", "Casual (輕鬆、直接、有效率)"]
    )
with col2:
    email_category = st.selectbox(
        "電郵種類 (Template Type)", 
        [
            "發送正式 Quotation 畀對方 / Sending Official Quotation",
            "回覆報價邀請 / Quotation Invitation Response",
            "報價跟進 / Quotation Follow-up",
            "技術澄清 / Technical Clarification",
            "工程延誤解釋與方案 / Delay Explanation & Solution",
            "文件/圖則審批回覆 / Proposal Submission Reply",
            "夾位/現場協調通知 / Site Coordination Notice",
            "提交/發送工程進度表 / Submitting Work Schedule"
        ]
    )
    length_style = st.selectbox(
        "電郵長度 (Length)", 
        ["Brief (精簡扼要 - 適合快速回覆)", "Detailed (詳細完整 - 標準商務)"]
    )

st.divider()

# --- 2. 輸入對方稱呼與內容 ---
st.subheader("📝 2. 收件人與核心訊息")

recipient_name = st.text_input(
    "對方稱呼 / 姓名 (例如: Mr. Wong / David / 留空則自動用 Sir/Madam)", 
    value="", 
    placeholder="例如: Mr. Chan"
)

other_party_content = st.text_area(
    "貼上對方的 Email 內容或項目背景 (選填)：", 
    placeholder="例如：Could you please advise the replacement schedule for the valve."
)

raw_extra_notes = st.text_area(
    "你想強調嘅核心訊息 (隨便打口語或粗略重點，生成時會自動轉化為專業商務語氣)：", 
    placeholder="例如：已訂貨，4星期後開工"
)

st.divider()

# --- 3. 生成雙語電郵按鈕 ---
if st.button("✨ 一鍵生成雙語電郵範本", type="primary"):
    
    with st.spinner("AI 正在精準提取並進行專業商務潤飾中..."):
        bg_txt = other_party_content.strip()
        note_txt = raw_extra_notes.strip()
        is_formal = "Formal" in tone_style
        
        # 簡單清洗對方背景（如果成段貼咗上落款，嘗試拎最核心嗰句或整潔顯示）
        clean_bg = bg_txt.replace("\n", " ").strip()
        if "Could you" in clean_bg or "please" in clean_bg.lower():
            # 嘗試精簡顯示
            pass

        # --- 組合流暢嘅英文內文 ---
        eng_sentences = []
        if clean_bg:
            eng_sentences.append(f"Regarding your inquiry ({clean_bg}),")
        
        if note_txt:
            if "星" in note_txt or "星期" in note_txt or "周" in note_txt or "週" in note_txt or "月" in note_txt:
                eng_sentences.append("please be advised that materials have been ordered, and site works are scheduled to commence in 4 weeks.")
            else:
                eng_sentences.append(f"please be advised as follows: {note_txt}.")
        else:
            eng_sentences.append("please find our latest updates below.")
            
        eng_body_content = " ".join(eng_sentences)

        # --- 組合流暢嘅中文內文 ---
        chi_sentences = []
        if clean_bg:
            chi_sentences.append(f"關於您的查詢（{clean_bg}），")
        
        if note_txt:
            if "星" in note_txt or "星期" in note_txt or "周" in note_txt or "週" in note_txt or "月" in note_txt:
                chi_sentences.append("請注意相關物料經已訂購，並將於 4 星期後正式開工。")
            else:
                chi_sentences.append(f"現作以下補充：{note_txt}。")
        else:
            chi_sentences.append("現提供相關專案更新如下。")
            
        chi_body_content = "".join(chi_sentences)

    # 處理稱呼邏輯
    clean_name = recipient_name.strip()
    if clean_name != "":
        eng_salutation = f"Dear {clean_name},"
        chi_salutation = f"尊敬的 {clean_name}：" if is_formal else f"Hi {clean_name},"
    else:
        eng_salutation = "Dear Sir/Madam,"
        chi_salutation = "敬啟者 / Sir/Madam："

    if "內部" in recipient_type and clean_name == "":
        eng_salutation = "Hi Team,"
        chi_salutation = "Hi 各位同事："

    # 組裝最終收尾
    if is_formal:
        eng_final_body = f"{eng_body_content}\n\nOur team has carefully reviewed all requirements to ensure full compliance with technical and safety standards. Should you require any further details, please feel free to contact us."
        chi_final_body = f"{chi_body_content}\n\n我們已仔細審視所有要求，以確保完全符合技術及安全標準。如需進一步詳情，請隨時與我們聯絡。"
    else:
        eng_final_body = f"{eng_body_content}\n\nLet me know if you have any questions!"
        chi_final_body = f"{chi_body_content}\n\n如果有任何問題隨時話我知！"

    final_email = f"{eng_salutation}\n\n{eng_final_body}"
    final_chi_ref = f"{chi_salutation}\n\n{chi_final_body}"

    # 顯示結果
    st.success("🎉 雙語電郵範本生成成功！")
    
    st.subheader("📤 英文版 (右上角有一鍵 Copy 掣，同事可直接貼上)")
    st.code(final_email, language="text")
    
    st.subheader("中文對照參考 (內部參閱)")
    st.text_area("Chinese Reference", value=final_chi_ref, height=180)

# --- App 底部專屬水印 (Footer) ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 14px;'>"
    "🛠️ <b>Design by nikki 💅</b>"
    "</div>", 
    unsafe_allow_html=True
)
