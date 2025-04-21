from flask import Flask, Response
import pandas as pd
import os
import json
from glob import glob

app = Flask(__name__)

DATA_DIR = r"C:\Users\tpl\OneDrive\inwave\data"

def get_latest_face_analysis():
    all_files = glob(os.path.join(DATA_DIR, "inw_*", "face_analysis_*.xlsx"))
    if not all_files:
        return {"error": "엑셀 파일을 찾을 수 없습니다."}

    latest_file = max(all_files, key=os.path.getmtime)
    df = pd.read_excel(latest_file, engine='openpyxl')

    # 분석 요약 통계 계산 (NumPy → Python 타입 변환 포함)
    try:
        total_people = int(df["ID"].nunique())
        avg_age = float(round(df["평균 나이"].mean(), 1))
        male_count = int((df["성별"] == "남").sum())
        female_count = int((df["성별"] == "여").sum())
        total_frames = int(df["검출 프레임 수"].sum())

        result = {
            "파일명": os.path.basename(latest_file),
            "전체 인원 수": total_people,
            "평균 나이": avg_age,
            "남성 수": male_count,
            "여성 수": female_count,
            "총 검출 프레임 수": total_frames
        }

        return result

    except Exception as e:
        return {"error": f"데이터 처리 오류: {str(e)}"}

@app.route("/api/summary")
def summary():
    try:
        data = get_latest_face_analysis()
        return Response(
            json.dumps(data, ensure_ascii=False),
            content_type="application/json; charset=utf-8"
        )
    except Exception as e:
        return Response(
            json.dumps({"error": str(e)}, ensure_ascii=False),
            content_type="application/json; charset=utf-8"
        )

if __name__ == "__main__":
    app.run(port=5000)
