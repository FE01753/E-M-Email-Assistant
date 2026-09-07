import streamlit as st
from datetime import datetime
from PIL import Image
import io

st.title("📸 Sleek-Industrial 進度記錄器")

# --- 0. 設定 Job Title (工程項目名稱) ---
st.subheader("📌 項目基本資料")
job_title = st.text_input("Job Title / 工程項目名稱", value="", placeholder="例如: Regent Hotel F3 改善工程")

st.divider()

# 1. 初始化 Session State 黎暫存記錄
if 'records' not in st.session_state:
    st.session_state['records'] = []

# --- 輸入當前記錄 ---
st.subheader("1️⃣ 新增現場記錄")

floor = st.text_input("樓層 (Floor) [選填]", placeholder="例如: B2 / G/F / 3/F (可留空)")
room = st.text_input("房間 / 區域 (Room / Area) [選填]", placeholder="例如: Function Room A / 掣房 (可留空)")
category = st.selectbox("工程類別", ["AC", "FS", "P&D", "EL", "OTHER"])
remarks = st.text_area("工作備忘", placeholder="請輸入工作內容或備忘...")

# 拍照或上傳相片
photo = st.file_uploader("拍攝或上傳現場相片", type=['jpg', 'jpeg', 'png', 'heic'])

# 加入暫存清單按鈕
if st.button("➕ 新增到今日清單"):
    if photo is not None:
        try:
            img = Image.open(photo)
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # 暫存縮圖用以預覽
            photo_bytes = io.BytesIO()
            img.save(photo_bytes, format='JPEG', quality=90)
            photo_bytes.seek(0)
            
            f_val = floor.strip() if floor else ""
            r_val = room.strip() if room else ""
            
            st.session_state['records'].append({
                "floor": f_val,
                "room": r_val,
                "category": category,
                "remarks": remarks,
                "photo": photo_bytes
            })
            st.success("成功新增現場記錄！")
        except Exception as e:
            st.error(f"相片處理失敗: {e}")
    else:
        st.warning("請上傳或拍攝現場相片！")

st.divider()

# --- 2. 顯示已記錄嘅清單 ---
st.subheader("📋 今日已記錄項目")
if len(st.session_state['records']) > 0:
    for i, rec in enumerate(st.session_state['records']):
        loc_parts = []
        if rec['floor']: loc_parts.append(f"樓層: {rec['floor']}")
        if rec['room']: loc_parts.append(f"區域: {rec['room']}")
        loc_str = " - ".join(loc_parts) if loc_parts else "未註明位置"
        
        with st.expander(f"項目 #{i+1}: {loc_str} ({rec['category']})"):
            st.write(f"備忘：{rec['remarks']}")
            
            rec['photo'].seek(0)
            st.image(rec['photo'], width=300)
            
            if st.button(f"刪除此項 #{i+1}", key=f"del_{i}"):
                st.session_state['records'].pop(i)
                st.rerun()
                
    if st.button("🗑️ 清空所有記錄"):
        st.session_state['records'] = []
        st.rerun()
else:
    st.info("暫時未有記錄，請喺上面新增。")

st.divider()

# --- 3. 一鍵生成文字報告並提供複製 ---
st.subheader("3️⃣ 生成報告並複製")

if st.button("📋 生成文字報告"):
    if len(st.session_state['records']) == 0:
        st.warning("請先新增至少一個記錄先可以生成報告！")
    else:
        display_title = job_title if job_title.strip() != "" else "Unnamed Project"
        
        report_lines = []
        report_lines.append(f"【工程進度巡檢報告】")
        report_lines.append(f"Job Title: {display_title}")
        report_lines.append(f"生成日期：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report_lines.append(f"總記錄項目數：{len(st.session_state['records'])} 項")
        report_lines.append("-" * 30)
        
        for i, rec in enumerate(st.session_state['records']):
            loc_parts = []
            if rec['floor']: loc_parts.append(f"樓層 {rec['floor']}")
            if rec['room']: loc_parts.append(f"區域 {rec['room']}")
            loc_str = " - ".join(loc_parts) if loc_parts else "未註明位置"
            
            report_lines.append(f"\n項目 {i+1}: {loc_str}")
            report_lines.append(f"• 工程類別：{rec['category']}")
            report_lines.append(f"• 工作備忘：{rec['remarks']}")
            report_lines.append("-" * 20)
            
        report_lines.append("\n[E&M Maintenance Section | Confidential]")
        
        full_report_text = "\n".join(report_lines)
        
        st.success("🎉 文字報告已生成！你可以直接在下方框框內一鍵複製：")
        st.text_area("Report Text (可以直接 Copy)", value=full_report_text, height=250)
