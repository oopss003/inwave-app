# flask_server.py
from flask import Flask, jsonify, Response
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
        raise FileNotFoundError("face_analysis_*.xlsx 파일을 찾을 수 없습니다.")

    latest_file = max(all_files, key=os.path.getmtime)
    df = pd.read_excel(latest_file)

    summary = {
        "파일명": os.path.basename(latest_file),
        "전체적으로 수": int(len(df)),
        "중년": float(df["평균 나이"].mean()) if "평균 나이" in df else 0,
        "남성 수": int((df["성별"] == "남성").sum()) if "성별" in df else 0,
        "여성 수": int((df["성별"] == "여성").sum()) if "성별" in df else 0,
        "총 기록 수": int(df.shape[0])
    }

    return summary

@app.route("/api/summary")
def summary():
    try:
        data = get_latest_face_analysis()
        # 한글을 JSON에 그대로 포함시키기 위해 ensure_ascii=False 설정
        return Response(json.dumps(data, ensure_ascii=False), content_type="application/json; charset=utf-8")
    except Exception as e:
        return jsonify({"오류": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
