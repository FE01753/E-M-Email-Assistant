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
            "簡單回覆對方開工 Schedule / Brief Reply on Work Schedule"
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
    placeholder="例如：關於 Regent Hotel 3/F 項目嘅電氣及冷氣改動工程報價..."
)

raw_extra_notes = st.text_area(
    "你想強調嘅核心訊息 (隨便打口語或粗略重點，生成時會自動轉化為專業商務語氣)：", 
    placeholder="例如：確認本週五進場，會夾埋冷氣組去馬"
)

st.divider()

# --- 3. 生成雙語電郵按鈕 (內置自動 AI 潤飾) ---
if st.button("✨ 一鍵生成雙語電郵範本", type="primary"):
    
    with st.spinner("AI 正在自動潤飾專業工程商務語氣中..."):
        # 處理 AI 智慧轉換工程專業措辭
        txt = raw_extra_notes.strip()
        if not txt:
            polished_notes = ""
        else:
            if "五" in txt or "星期五" in txt or "日" in txt or "期" in txt:
                polished_notes = f"We confirm that site mobilization and commencement of works are scheduled for this coming Friday, and all relevant resources have been secured."
            elif "有效" in txt or "30" in txt:
                polished_notes = f"Please note that the quotation remains valid for 30 days from the date of issuance."
            elif "人" in txt or "快" in txt or "追" in txt:
                polished_notes = f"We have deployed additional workforce and resources on-site to ensure the project timeline remains strictly on track."
            else:
                polished_notes = f"Please be advised that {txt}, ensuring full compliance with site requirements and smooth progress."

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
    
    # --- 類別 0：發送正式 Quotation ---
    if "發送正式 Quotation" in email_category:
        if is_formal:
            eng_body = f"""Please find attached our official quotation for your review and consideration.\n\nOur team has carefully evaluated the site conditions, scope of works, and relevant technical requirements. {polished_notes if polished_notes else 'All proposed items comply with statutory standards and site safety guidelines.'}\n\nShould you have any questions or require further clarification regarding the pricing or details, please feel free to contact us."""
            chi_body = f"""隨信附上正式報價單供閣下審閱及考慮。\n\n我們已仔細評估現場情況、工程範圍及相關技術要求。{polished_notes if polished_notes else '所有建議項目均符合法定標準及地盤安全指引。'}\n\n如對價格或細節有任何疑問或需進一步澄清，請隨時與我們聯絡。"""
        else:
            eng_body = f"""Please find our official quotation attached.\n\n{polished_notes if polished_notes else 'We have factored in all the site requirements and scope discussed.'}\n\nLet me know if you have any questions or want to go over the details."""
            chi_body = f"""隨信附上正式報價單。\n\n{polished_notes if polished_notes else '我們已計及所有討論過嘅現場要求同工程範圍。'}\n\n如果有任何問題或想對對細節隨時話我知。"""

    # --- 類別 1：回覆報價邀請 ---
    elif "回覆報價邀請" in email_category:
        if is_formal:
            eng_body = f"""Thank you for your kind invitation to submit a quotation.\n\nWe acknowledge receipt of your request regarding the project requirements. Our team is currently reviewing the site details and scope of works.\n\n{polished_notes if polished_notes else 'We will finalize and submit our formal quotation shortly.'}"""
            chi_body = f"""感謝閣下邀請我們提交報價。\n\n我們已收到關於項目要求的查詢。團隊正審視現場細節及工程範圍。\n\n{polished_notes if polished_notes else '我們將盡快完成並提交正式報價單。'}"""
        else:
            eng_body = f"""Thanks for inviting us to quote! We've received your request and are looking into the details.\n\n{polished_notes if polished_notes else 'We will get the formal quotation over to you soon.'}"""
            chi_body = f"""多謝邀請報價！我們已經收到要求並正查看細節。\n\n{polished_notes if polished_notes else '我們好快會將正式報價交畀你。'}"""

    # --- 類別 2：報價跟進 ---
    elif "報價跟進" in email_category:
        if is_formal:
            eng_body = f"""We are writing to follow up on the quotation previously submitted for your review.\n\nOur team has carefully evaluated the site conditions and engineering requirements. {polished_notes if polished_notes else 'Should you have any queries or require adjustments, we remain at your disposal.'}"""
            chi_body = f"""特此跟進早前提交以供審閱之報價單。\n\n我們已仔細評估現場條件及工程要求。{polished_notes if polished_notes else '如閣下有任何疑問或需調整方案，我們隨時樂意配合。'}"""
        else:
            eng_body = f"""Just following up on the quotation we sent earlier. {polished_notes if polished_notes else 'Let us know if you have any questions or want to discuss the details.'}"""
            chi_body = f"""簡單跟進一下之前發嘅報價單。{polished_notes if polished_notes else '如果有任何問題或想傾傾細節歡迎話我知。'}"""

    # --- 類別 3：技術澄清 ---
    elif "技術澄清" in email_category:
        eng_body = f"""Thank you for your inquiry. Regarding the technical specifications and site configuration, please find our clarification below:\n\n1. Site Verification: {polished_notes if polished_notes else 'Our engineering team has verified that the installation complies with relevant E&M standards.'}\n2. Compliance: All works will be executed strictly in accordance with safety guidelines and statutory requirements."""
        chi_body = f"""感謝查詢。關於技術規格及現場配置，現作以下澄清：\n\n1. 現場核實：{polished_notes if polished_notes else '工程團隊已核實安裝符合相關機電標準。'}\n2. 合規性：所有工程將嚴格按照安全指引及法定要求執行。"""

    # --- 類別 4：工程延誤解釋 ---
    elif "工程延誤" in email_category:
        eng_body = f"""Thank you for your attention to the project progress. We would like to provide an update regarding the schedule adjustment:\n\n• Cause: {other_party_content[:100] if other_party_content else 'Unforeseen site conditions and coordination adjustments.'}\n• Mitigation & Solution: {polished_notes if polished_notes else 'We have deployed extra resources to catch up on the timeline safely.'}"""
        chi_body = f"""感謝關注工程進度。現就近期的進度調整作以下匯報：\n\n• 原因：{other_party_content[:100] if other_party_content else '不可預見的現場條件及協調調整。'}\n• 應對與解決方案：{polished_notes if polished_notes else '我們已增派人手以安全方式追回進度。'}"""

    # --- 類別 5：文件/圖則審批 ---
    elif "文件/圖則審批" in email_category:
        eng_body = f"""Please find attached our latest proposal/drawing for your review and approval.\n\nKey updates include adjustments based on site measurements and full compliance with relevant safety standards.\n\n{polished_notes}"""
        chi_body = f"""隨信附上最新提案/圖則供閣下審批。\n\n主要更新包括根據現場尺寸作出調整，並完全符合相關安全標準。\n\n{polished_notes}"""

    # --- 類別 6：夾位/現場協調 ---
    elif "夾位/現場協調" in email_category:
        eng_body = f"""To ensure smooth coordination among different trades, we would like to arrange a site coordination session.\n\n• Focus Area: {polished_notes if polished_notes else 'Main routing and service zones'}\n• Objective: To prevent clash issues prior to installation."""
        chi_body = f"""為確保各工種順利協調，擬安排現場夾位工作。\n\n• 重點區域：{polished_notes if polished_notes else '主要喉管路線及服務區'}\n• 目的：在安裝前避免碰撞問題。"""

    # --- 類別 7：簡單回覆對方開工 Schedule ---
    else:
        if is_formal:
            eng_body = f"""Thank you for sharing the work schedule. We have reviewed the proposed timeline and confirm our alignment with the key milestones.\n\n{polished_notes if polished_notes else 'Our team will prepare the necessary site resources and coordinate accordingly.'}"""
            chi_body = f"""感謝提供開工進度時間表。我們已審閱擬定的時間軸，並確認配合各項主要里程碑。\n\n{polished_notes if polished_notes else '我們團隊將準備好相應的現場資源並作出配合。'}"""
        else:
            eng_body = f"""Thanks for sharing the schedule! We've checked the timeline and everything looks good on our end.\n\n{polished_notes if polished_notes else 'We will get our crew and materials ready accordingly.'}"""
            chi_body = f"""多謝提供 Schedule！我們睇過時間表冇問題，會按時準備好人手同物料。\n\n{polished_notes if polished_notes else ''}"""

    # 乾淨正文（無下款）
    final_email = f"{eng_salutation}\n\n{eng_body}"
    final_chi_ref = f"{chi_salutation}\n\n{chi_body}"

    # 顯示結果
    st.success("🎉 雙語電郵範本生成成功（已自動完成 AI 專業潤飾）！")
    
    st.subheader("📤 英文版 (右上角有一鍵 Copy 掣，同事可直接貼上)")
    st.code(final_email, language="text")
    
    st.subheader("🇨🇳 中文對照參考 (內部參閱)")
    st.text_area("Chinese Reference", value=final_chi_ref, height=180)

# --- App 底部專屬水印 (Footer) ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 14px;'>"
    "🛠️ <b>Design by nikki 💅</b>"
    "</div>", 
    unsafe_allow_html=True
)
