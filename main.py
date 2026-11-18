import os
from google import genai
from google.genai import types

def main():
    # 確保從 GitHub Secrets 讀取 API Key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("未找到 GEMINI_API_KEY 環境變數，請確認是否已在 GitHub Settings 中設定 Secrets。")

    # 初始化 Gemini 客戶端
    client = genai.Client(api_key=api_key)

    # 你指定的產業分析師提示詞與任務
    prompt = """
    你是 hinge 轉軸產業情報分析師。請執行以下任務：
    1. 搜尋「過去 1天」這些主題的新聞：新產品發表、企業導入案例。
    2. 過濾掉內容農場、舊聞、純廣告。
    3. 挑最重要的 5 則，每則用「事實 → 為什麼重要」呈現。
    4. 開頭給一句本週主軸，全文用繁體中文、台灣用語。
    5. 只根據實際查到的內容，不確定就標註、不要臆測。
    """

    print("🤖 AI Agent 正在搜尋並分析 Hinge 轉軸產業情報...")

    # 呼叫 Gemini 2.5 Flash 模型並啟用 Google Search 聯網工具
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[{"google_search": {}}],
            temperature=0.3,
        ),
    )

    print("\n================ 本週 Hinge 轉軸產業情報報告 ================\n")
    print(response.text)
    print("\n===========================================================\n")

if __name__ == "__main__":
    main()
