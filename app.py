import streamlit as st
import time # 導入 time 函式庫用於模擬延遲
import re # 導入正則表達式函式庫
import io # 導入 io 函式庫處理檔案

# --- 配置 ---
# 此應用程式專門運行於本機模擬模式，不使用外部 API。

# 預設範例文章 (供參考)
DEFAULT_TEXT = "請上傳一個 .txt 檔案進行分析。檔案內容建議至少 50 字以上。"

# --- 本地輔助函數 ---

def calculate_ttr(text):
    """計算 Type-Token Ratio (詞彙多樣性)，使用單字作為 Token (簡化)。"""
    # 移除標點符號，將所有文本轉為小寫
    text = re.sub(r'[^\w\s]', '', text).lower()
    tokens = text.split()
    if not tokens:
        return 0.0
    # Type (不同詞彙的數量) / Token (總詞彙數量)
    return len(set(tokens)) / len(tokens)

def calculate_function_word_density(text):
    """計算功能詞（連接詞/轉折詞）密度。"""
    # 常用 LLM 模板詞/轉折詞 (Stylometry 指標)
    function_words = ["然而", "因此", "此外", "總而言之", "值得注意的是", "除此之外", "同時", "總結來說", "並且"]
    
    text_length = len(text)
    if text_length == 0:
        return 0.0
        
    count = 0
    for word in function_words:
        # 使用正則表達式尋找單詞
        count += len(re.findall(r'\b' + re.escape(word) + r'\b', text))
        
    # 密度：功能詞數量 / 總字符數 (簡化)
    return count / text_length

# --- 模擬分析函數 ---
def simulate_text_analysis(text_input):
    """模擬 AI 偵測分析的結果，返回結構化數據。"""
    
    # 模擬網路延遲，讓使用者感受到處理過程
    time.sleep(1.5)
    
    # --- 全局指標計算 ---
    overall_ttr = calculate_ttr(text_input)
    ttr_threshold = 0.35 # 假設低 TTR 傾向 AI
    
    overall_fwd = calculate_function_word_density(text_input)
    fwd_threshold = 0.005 # 假設高 FWD (約 0.5% 以上) 傾向 AI
    
    # --- 逐句分析 ---
    mock_breakdown = []
    sentences = re.split(r'(?<=[。！？])', text_input) # 使用正則表達式保留分隔符
    
    ai_segment_count = 0
    total_count = 0
    
    for i, sentence in enumerate(sentences):
        sentence = sentence.strip()
        if not sentence:
            continue
            
        total_count += 1
        
        # --- 本地模擬規則 (基於簡報理論) ---
        is_ai_score = 0
        
        # 1. 句長穩定性 (Burstiness/Perplexity):
        # 句子長度適中 (30-60字) 缺乏爆發性 -> 傾向 AI
        if 30 <= len(sentence) <= 60:
            is_ai_score += 1.0 # 權重：中
        # 句子長度過短 (少於15字) -> 傾向 Human
        elif len(sentence) < 15:
            is_ai_score -= 1.0 # 權重：中
            
        # 2. 詞彙多樣性 (Stylometry / Zipf's Law):
        if overall_ttr < ttr_threshold:
            is_ai_score += 1.0 # TTR 偏低，句子傾向 AI
        
        # 3. 功能詞密度 (Function Word Density):
        if overall_fwd > fwd_threshold:
            is_ai_score += 1.5 # 功能詞密度過高 -> 傾向 AI (高權重)

        # 4. 標點符號不規則性 (Noise/Emotion):
        # 如果句子包含多個問號/驚嘆號/括號，模擬為 Human 傾向
        if len(re.findall(r'[!?()（）]', sentence)) > 1:
            is_ai_score -= 1.5 # 權重：高 (人類情感爆發)
            
        # 最終判斷：只要 AI 傾向得分略高於 Human 傾向得分，即判為 AI。
        segment_is_ai = is_ai_score > 0.5 
        
        if segment_is_ai:
            ai_segment_count += 1
            
        mock_breakdown.append({
            "text": sentence,
            "is_ai": segment_is_ai
        })
    
    if total_count > 0:
        base_prob = ai_segment_count / total_count
        # 移除機率限制，讓機率可以從 0% 波動到 100%
        ai_prob = base_prob
    else:
        ai_prob = 0.5
        
    mock_result = {
        "is_ai_generated": ai_prob > 0.5,
        "ai_probability": ai_prob,
        "analysis_summary": f"（本地模擬結果）本應用程式使用詞彙多樣性 ({overall_ttr:.2f})、長度穩定性與功能詞密度 ({overall_fwd:.4f}) 進行判斷。AI 傾向評分門檻已調低，使結果更具波動性。",
        "analysis_breakdown": mock_breakdown
    }
    return mock_result


# --- Streamlit 視覺化函數 ---

def render_probability_bar(ai_prob):
    """
    渲染自訂的兩色機率條（Streamlit Markdown/HTML）。
    """
    human_prob = 1.0 - ai_prob
    ai_percent = ai_prob * 100
    human_percent = human_prob * 100

    html_bar = f"""
    <div style="display: flex; justify-content: space-between; font-weight: bold; font-size: 0.9em; margin-bottom: 5px;">
        <span style="color: #10b981;">人類撰寫</span>
        <span style="color: #ef4444;">AI 生成</span>
    </div>
    <div style="height: 30px; border-radius: 15px; overflow: hidden; display: flex; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <!-- Human Bar -->
        <div style="width: {human_percent}%; background-color: #10b981; display: flex; align-items: center; justify-content: flex-start;">
            <span style="color: white; padding-left: 10px;">{human_percent:.1f}%</span>
        </div>
        <!-- AI Bar -->
        <div style="width: {ai_percent}%; background-color: #ef4444; display: flex; align-items: center; justify-content: flex-end;">
            <span style="color: white; padding-right: 10px;">{ai_percent:.1f}%</span>
        </div>
    </div>
    """
    st.markdown(html_bar, unsafe_allow_html=True)

def render_highlighted_text(breakdown):
    """
    渲染高亮顯示的文本區塊（Streamlit Markdown/HTML）。
    """
    html_content = []
    # 定義高亮顏色 (接近 tailwind 的 red-200/emerald-200)
    ai_color = "#fecaca"
    human_color = "#a7f3d0"
    ai_text_color = "#991b1b"
    human_text_color = "#065f46"


    for segment in breakdown:
        is_ai = segment.get('is_ai', False)
        text = segment.get('text', '')

        bg_color = ai_color if is_ai else human_color
        text_color = ai_text_color if is_ai else human_text_color
        
        # 使用 inline-block 和 padding/margin 模擬 JustDone 的方塊樣式
        html_content.append(f"""
            <span style="background-color: {bg_color}; color: {text_color}; padding: 0.2em 0.5em; margin-right: 0.4em; border-radius: 0.375rem; line-height: 2.5; display: inline-block;">
                {text}
            </span>
        """)
    
    st.markdown("".join(html_content), unsafe_allow_html=True)
    
    # 渲染圖例
    st.markdown(f"""
    <div style="display: flex; gap: 20px; font-size: 0.9em; margin-top: 15px;">
        <span style="display: flex; align-items: center; color: {human_text_color};">
            <span style="width: 10px; height: 10px; border-radius: 50%; background-color: {human_color}; margin-right: 5px; border: 1px solid {human_text_color};"></span> - 人類撰寫傾向
        </span>
        <span style="display: flex; align-items: center; color: {ai_text_color};">
            <span style="width: 10px; height: 10px; border-radius: 50%; background-color: {ai_color}; margin-right: 5px; border: 1px solid {ai_text_color};"></span> - AI 生成傾向
        </span>
    </div>
    """, unsafe_allow_html=True)

# --- Streamlit 主應用程式 ---
st.set_page_config(
    page_title="AI/人類文章偵測模擬器",
    layout="centered",
    initial_sidebar_state="auto"
)

st.title("🤖 AI 偵測模擬器 (本機運算)")

st.caption("🔴 **運行模式：** 本地模擬。所有分析結果基於詞彙多樣性、長度穩定性與標點符號不規則性、**功能詞密度**，不進行實際的 AI 模型推理。")


# 檔案上傳區
uploaded_file = st.file_uploader(
    "上傳 TXT 檔案進行分析", 
    type="txt", 
    help="請上傳一個 .txt 文件，內容建議至少 50 字以上。"
)

# 狀態變數，用於儲存文本
text_input = ""
if uploaded_file is not None:
    # 讀取上傳的檔案
    string_data = io.StringIO(uploaded_file.getvalue().decode("utf-8")).read()
    text_input = string_data
    st.success(f"檔案 '{uploaded_file.name}' 上傳成功，等待分析。")

# 文本預覽區
if text_input:
    st.subheader("檔案內容預覽")
    st.text_area("Uploaded Text", text_input, height=150, disabled=True)
    
    # 檢查長度
    if len(text_input) < 50:
        st.error("警告：文本內容少於 50 字，模擬結果可能不準確。")

# 執行分析
if st.button("開始分析", use_container_width=True, type="primary"):
    if not text_input:
        st.warning("請先上傳一個 .txt 檔案或等待檔案讀取完成。")
    elif len(text_input) < 50:
        st.error("警告：文本內容少於 50 字，無法進行有效分析。")
    else:
        with st.spinner("模型分析中... 正在評估句子結構、詞彙多樣性與功能詞密度..."):
            analysis_result = simulate_text_analysis(text_input) # 使用本地模擬函數

        if analysis_result:
            st.success("分析完成！")
            
            ai_prob = analysis_result.get('ai_probability', 0.5)
            summary = analysis_result.get('analysis_summary', "未提供總結。")
            breakdown = analysis_result.get('analysis_breakdown', [])

            # --- 視覺化結果區 ---
            st.markdown("---")
            st.header("📊 分析結果與機率分佈")

            # 1. 機率條
            render_probability_bar(ai_prob)

            # 2. 裁決總結
            st.subheader("💡 模型裁決")
            is_human = 1.0 - ai_prob > 0.5
            
            if is_human:
                st.markdown(f"<div style='background-color: #a7f3d0; padding: 15px; border-radius: 10px; border-left: 5px solid #065f46;'><h3>人類撰寫機率較高</h3><p>{summary}</p></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='background-color: #fecaca; padding: 15px; border-radius: 10px; border-left: 5px solid #991b1b;'><h3>AI 生成機率較高</h3><p>{summary}</p></div>", unsafe_allow_html=True)
            
            # 3. 文本高亮顯示
            st.markdown("---")
            st.header("📝 文本結構分析（逐句高亮）")
            st.caption("紅色區塊傾向 AI 生成；綠色區塊傾向人類撰寫。")
            
            st.markdown("<div style='border: 1px solid #e5e7eb; padding: 20px; border-radius: 10px; background-color: white;'>", unsafe_allow_html=True)
            render_highlighted_text(breakdown)
            st.markdown("</div>", unsafe_allow_html=True)
            
        st.markdown("---")
        st.caption("免責聲明：偵測結果僅用於 UI 測試，不具絕對證據效力。")