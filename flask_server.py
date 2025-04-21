# flask_server.py
from flask import Flask, jsonify
import pandas as pd
import os
from glob import glob

app = Flask(__name__)

# ✅ 분석 데이터가 저장된 폴더 경로 (Windows 기준 OneDrive 폴더)
DATA_DIR = r"C:\Users\tpl\OneDrive\inwave\data"

def get_latest_face_analysis():
    """
    가장 최근의 face_analysis_*.xlsx 파일을 찾아서 요약 통계를 반환하는 함수
    """
    all_files = glob(os.path.join(DATA_DIR, "inw_*", "face_analysis_*.xlsx"))
    
    if not all_files:
        return {"error": "파일이 존재하지 않습니다."}
    
    latest_file = max(all_files, key=os.path.getmtime)
    df = pd.read_excel(latest_file)

    # 🔎 컬럼 확인 후 통계 계산
    summary = {
        "파일명": os.path.basename(latest_file),
        "전체적으로 수": int(df.shape[0]),
        "중년": round(df["평균 나이"].mean(), 1) if "평균 나이" in df.columns else 0,
        "남성 수": int((df["성별"] == "남").sum()) if "성별" in df.columns else 0,
        "여성 수": int((df["성별"] == "여").sum()) if "성별" in df.columns else 0,
        "총 기록 수": int(df.count().sum())
    }

    return summary

@app.route("/api/summary")
def summary():
    """
    API로 요약 정보를 JSON 형태로 제공
    """
    try:
        data = get_latest_face_analysis()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})

# ✅ Render 호환을 위한 실행 설정
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # Render에서 제공하는 포트를 사용
    app.run(host="0.0.0.0", port=port)   