# flask_server.py
from flask import Flask, Response
import pandas as pd
import os
from glob import glob
import json

app = Flask(__name__)

# 데이터 폴더 경로
DATA_DIR = r"C:\Users\tpl\OneDrive\inwave\data"

def get_latest_face_analysis():
    all_files = glob(os.path.join(DATA_DIR, "inw_*", "face_analysis_*.xlsx"))
    if not all_files:
        return {"오류": "분석 파일이 존재하지 않습니다."}
    
    latest_file = max(all_files, key=os.path.getmtime)
    df = pd.read_excel(latest_file)

    # 예시: 컬럼 존재 여부 검사 후 통계 추출
    summary = {
        "파일명": os.path.basename(latest_file),
        "전체적으로 수": int(df.shape[0]),
        "중년": round(df["평균 나이"].mean(), 1) if "평균 나이" in df else 0,
        "남성 수": int((df["성별"] == "남성").sum()) if "성별" in df else 0,
        "여성 수": int((df["성별"] == "여성").sum()) if "성별" in df else 0,
        "총 기록 수": int(df.count().sum())
    }

    return summary

@app.route("/api/summary")
def summary():
    try:
        data = get_latest_face_analysis()
        # 인코딩된 JSON 반환 (ensure_ascii=False 로 한글 깨짐 방지)
        json_str = json.dumps(data, ensure_ascii=False)
        return Response(json_str, content_type="application/json; charset=utf-8")
    except Exception as e:
        err = {"오류": str(e)}
        return Response(json.dumps(err, ensure_ascii=False), content_type="application/json; charset=utf-8")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
