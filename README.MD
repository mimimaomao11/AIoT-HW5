🤖 AI 文章偵測模擬器 (本地運算版)

專案簡介

這個 Streamlit 應用程式是一個 AI / 人類文本偵測模擬器。它基於高階語言學指標（如：詞彙多樣性、句子節奏、功能詞密度）的原理，在本地進行模擬運算，以視覺化方式（機率條與逐句高亮）展示文本傾向於 AI 生成或人類撰寫的程度。

核心特點：

純本地運算： 不依賴任何外部 API Key，完全在您的機器上運行。

視覺化高亮： 模仿專業偵測工具，將文本區塊標記為 AI（紅色）或人類（綠色）。

理論模擬： 應用程式的判斷邏輯參考了 Perplexity、Burstiness 和 Stylometry 等 AI 偵測的關鍵理論指標。

🚨 啟動與安裝指南

步驟 1: 安裝依賴項

請確保您已安裝 Python (建議 3.8 或以上版本)。然後在您的終端機中，切換到包含 app.py 和 requirements.txt 檔案的目錄，並執行以下指令安裝必要的函式庫：

pip install -r requirements.txt


(如果您沒有 requirements.txt 檔案，可以直接執行 pip install streamlit)

步驟 2: 運行應用程式

安裝完成後，使用 Streamlit 啟動應用程式。

python -m streamlit run app.py


注意： 如果您直接執行 streamlit run app.py 遇到問題，請務必使用 python -m streamlit run app.py 繞過 PATH 環境變數問題。

步驟 3: 開啟網頁

Streamlit 啟動後，它會自動在瀏覽器中開啟一個網頁視窗 (通常是 http://localhost:8501)。

模擬邏輯說明

本應用程式的判斷基於以下三個主要本地可計算的指標：

詞彙多樣性 (TTR)： 數值越高，越傾向人類。

功能詞密度 (FWD)： 規律的轉折詞（如「然而」、「因此」）密度越高，越傾向 AI。

句子穩定性 / 標點不規則性： 句長波動大、非正規標點符號多（如 !!、??）則傾向人類。

最終的 AI 機率是通過綜合這三個指標的分數計算得出。