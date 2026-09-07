import streamlit as st
from datetime import datetime

st.set_page_config(page_title="AI 雙語工程電郵助手", page_icon="✉️", layout="centered")

st.title("✉️ AI 雙語工程電郵助手 (E&M Assistant)")
st.write("針對工程界設計：支援中英雙語對照、自選長短、Formal/Casual 語氣，並自動帶有 Nikki 專屬簽署！")

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
            "回覆報價邀請 / Quotation Invitation Response",
            "報價跟進 / Quotation Follow-up",
            "技術澄清 / Technical Clarification",
            "工程延誤解釋與方案 / Delay Explanation & Solution",
            "文件/圖則審批回覆 / Proposal Submission Reply",
            "夾位/現場協調通知 / Site Coordination Notice"
        ]
    )
    length_style = st.selectbox(
        "電郵長度 (Length)", 
        ["Brief (精簡扼要 - 適合快速回覆)", "Detailed (詳細完整 - 標準商務)"]
    )

st.divider()

# --- 2. 輸入對方稱呼與內容 ---
st.subheader("📝 2. 收件人與來信重點")

recipient_name = st.text_input(
    "對方稱呼 / 姓名 (例如: Mr. Wong / David / 留空則自動用 Sir/Madam)", 
    value="", 
    placeholder="例如: Mr. Chan"
)

other_party_content = st.text_area(
    "貼上對方的 Email 內容 (選填)：", 
    placeholder="例如：收到裝修單位發黎嘅 Quotation Invitation，要求就 Regent Hotel 3/F 進行 EL 系統改動報價..."
)

extra_notes = st.text_input("你想強調嘅核心訊息 (例如：預計三日內交到 / 需先夾位)", placeholder="例如：將於本週五前提交正式 Quotation")

st.divider()

# --- 3. 生成雙語電郵按鈕 ---
if st.button("✨ 一鍵生成雙語電郵範本", type="primary"):
    
    # 處理稱呼邏輯
    clean_name = recipient_name.strip()
    if clean_name != "":
        eng_salutation = f"Dear {clean_name},"
        chi_salutation = f"尊敬的 {clean_name}：" if "Formal" in tone_style else f"Hi {clean_name},"
    else:
        eng_salutation = "Dear Sir/Madam,"
        chi_salutation = "敬啟者 / Sir/Madam："

    if "內部" in recipient_type and clean_name == "":
        eng_salutation = "Hi Team,"
        chi_salutation = "Hi 各位同事："

    is_formal = "Formal" in tone_style
    
    eng_body = ""
    chi_body = "" 
    
    # --- 類別 1：回覆報價邀請 (Quotation Invitation Response) ---
    if "回覆報價邀請" in email_category:
        if is_formal:
            eng_body = f"""Thank you for your kind invitation to submit a quotation.\n\nWe acknowledge receipt of your request regarding the project requirements. Our team is currently reviewing the site details and scope of works (including FFL verification and relevant safety standards).\n\n{extra_notes if extra_notes else 'We will finalize and submit our formal quotation shortly.'}\n\nShould you require any preliminary site visit or coordination in the meantime, please feel free to let us know."""
            chi_body = f"""感謝閣下邀請我們提交報價。\n\n我們已收到關於項目要求的查詢。團隊正審視現場細節及工程範圍（包括 FFL 驗證及相關安全標準）。\n\n{extra_notes if extra_notes else '我們將盡快完成並提交正式報價單。'}\n\n如在此期間需要任何初步現場視察或協調，請隨時通知我們。"""
        else:
            eng_body = f"""Thanks for inviting us to quote! We've received your request and are looking into the details.\n\n{extra_notes if extra_notes else 'We will get the formal quotation over to you soon.'}\n\nLet us know if you need anything else before then."""
            chi_body = f"""多謝邀請報價！我們已經收到要求並正查看細節。\n\n{extra_notes if extra_notes else '我們好快會將正式報價交畀你。'}\n\n如果有其他需要請隨時出聲。"""

    # --- 類別 2：報價跟進 ---
    elif "報價跟進" in email_category:
        if is_formal:
            eng_body = f"""We are writing to follow up on the quotation previously submitted for your review.\n\nOur team has carefully evaluated the site conditions and engineering requirements. {extra_notes if extra_notes else 'Should you have any queries or require adjustments to the proposal, we remain at your disposal.'}\n\nWe look forward to your favorable response."""
            chi_body = f"""特此跟進早前提交以供審閱之報價單。\n\n我們已仔細評估現場條件及工程要求。{extra_notes if extra_notes else '如閣下有任何疑問或需調整方案，我們隨時樂意配合。'}\n\n期待閣下的佳音。"""
        else:
            eng_body = f"""Just following up on the quotation we sent earlier. {extra_notes if extra_notes else 'Let us know if you have any questions or want to discuss the details.'}\n\nCheers,"""
            chi_body = f"""簡單跟進一下之前發嘅報價單。{extra_notes if extra_notes else '如果有任何問題或想傾傾細節歡迎話我知。'}\n\n謝謝，"""

    # --- 類別 3：技術澄清 ---
    elif "技術澄清" in email_category:
        eng_body = f"""Thank you for your inquiry. Regarding the technical specifications and site configuration, please find our clarification below:\n\n1. Site Verification: {extra_notes if extra_notes else 'Our engineering team has verified that the installation complies with relevant E&M standards.'}\n2. Compliance: All works will be executed strictly in accordance with safety guidelines and statutory requirements.\n\nShould you need a coordination meeting, please advise your availability."""
        chi_body = f"""感謝查詢。關於技術規格及現場配置，現作以下澄清：\n\n1. 現場核實：{extra_notes if extra_notes else '工程團隊已核實安裝符合相關機電標準。'}\n2. 合規性：所有工程將嚴格按照安全指引及法定要求執行。\n\n如需安排夾位會議，請話我知你嘅時間。"""

    # --- 類別 4：工程延誤解釋 ---
    elif "工程延誤" in email_category:
        eng_body = f"""Thank you for your attention to the project progress. We would like to provide an update regarding the recent schedule adjustment:\n\n• Cause: {other_party_content[:100] if other_party_content else 'Unforeseen site conditions and coordination adjustments.'}\n• Mitigation & Solution: {extra_notes if extra_notes else 'We have deployed extra resources to catch up on the timeline safely.'}\n\nWe appreciate your understanding and cooperation."""
        chi_body = f"""感謝關注工程進度。現就近期的進度調整作以下匯報：\n\n• 原因：{other_party_content[:100] if other_party_content else '不可預見的現場條件及協調調整。'}\n• 應對與解決方案：{extra_notes if extra_notes else '我們已增派人手以安全方式追回進度。'}\n\n感謝閣下的理解與配合。"""

    # --- 類別 5：文件/圖則審批 ---
    elif "文件/圖則審批" in email_category:
        eng_body = f"""Please find attached our latest proposal/drawing for your review and approval.\n\nKey updates include adjustments based on site measurements and full compliance with relevant safety and insurance policies (EC/CAR).\n\n{extra_notes}\n\nWe look forward to your approval to proceed with the next phase."""
        chi_body = f"""隨信附上最新提案/圖則供閣下審批。\n\n主要更新包括根據現場尺寸作出調整，並完全符合相關安全及保險政策（EC/CAR）。\n\n{extra_notes}\n\n期待閣下批核以便進行下一階段工作。"""

    # --- 類別 6：夾位/現場協調 ---
    else:
        eng_body = f"""To ensure smooth coordination among different trades, we would like to arrange a site coordination session.\n\n• Focus Area: {extra_notes if extra_notes else 'Main routing and service zones'}\n• Objective: To prevent clash issues prior to installation.\n\nPlease let us know your preferred date and time."""
        chi_body = f"""為確保各工種順利協調，擬安排現場夾位工作。\n\n• 重點區域：{extra_notes if extra_notes else '主要喉管路線及服務區'}\n• 目的：在安裝前避免碰撞問題。\n\n請話我知閣下方便嘅日期同時間。"""

    # Nikki 專屬簽署水印
    eng_signoff = "Best regards,\nNikki\nE&M Maintenance Section"
    if is_formal and "業主" in recipient_type:
        eng_signoff = "Yours faithfully,\nNikki\nEngineering Department"

    final_email = f"{eng_salutation}\n\n{eng_body}\n\n{eng_signoff}"
    final_chi_ref = f"{chi_salutation}\n\n{chi_body}"

    # 顯示結果
    st.success("🎉 雙語電郵範本生成成功！")
    
    st.subheader("📤 英文版 (可直接 Copy 寄出)")
    st.text_area("English Output", value=final_email, height=220)
    
    st.subheader("🇨🇳 中文對照參考 (內部參閱)")
    st.text_area("Chinese Reference", value=final_chi_ref, height=180)
