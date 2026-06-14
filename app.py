import streamlit as st
import time
import os
import numpy as np
from PIL import Image
from PIL.ExifTags import TAGS

# YOLO 모델 임포트 (설치되어 있지 않을 경우를 대비한 안전 장치)
try:
    from ultralytics import YOLO
    HAS_YOLO = True
except ImportError:
    HAS_YOLO = False

# =================================================================
# 1. 레벨별 캐릭터 정보 데이터베이스 정의
# =================================================================
LEVEL_DATA = {
    1: {
        "name": "알속두루",
        "desc": "🌱 아직 알껍데기를 쓰고 있는 초경량 아기 오리입니다. 플로깅을 통해 에너지를 나누어 주세요!",
        "img_path": "images/duru_lv1.png",
        "next_xp": "100 XP"
    },
    2: {
        "name": "푸른두루",
        "desc": "🌿 플로깅 활동을 인지하고 안테나 새싹이 돋아난 두루! 대청호의 변화를 감지하기 시작했습니다.",
        "img_path": "images/duru_lv2.png",
        "next_xp": "300 XP"
    },
    3: {
        "name": "에코두루",
        "desc": "⚙️ 특수 테크 조끼를 장착한 에코두루! 쓰레기 종류를 정밀 스캔하며 정화 능력이 가속화됩니다.",
        "img_path": "images/duru_lv3.png",
        "next_xp": "500 XP"
    },
    4: {
        "name": "가디언 (최종)",
        "desc": "🛡️ 대청호를 완벽히 정화한 궁극의 수호자 모드입니다! 전통시장 VIP 혜택과 특별 에코 리워드가 해금됩니다.",
        "img_path": "images/duru_lv4.png",
        "next_xp": "MAX"
    }
}

# =================================================================
# 2. 메타데이터(EXIF) 추출 함수 정의
# =================================================================
def extract_metadata(uploaded_file):
    try:
        image = Image.open(uploaded_file)
        info = image._getexif()
        metadata = {}
        if info:
            for tag, value in info.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name != 'MakerNote' and len(str(value)) < 100:
                    metadata[tag_name] = str(value)
        return metadata
    except Exception as e:
        return {"에러": "메타데이터를 읽을 수 없는 파일 형식입니다."}

# =================================================================
# 3. 앱 시스템 세션 상태(Session State) 초기화
# =================================================================
if 'duru_level' not in st.session_state:
    st.session_state.duru_level = 1
if 'eco_points' not in st.session_state:
    st.session_state.eco_points = 0
if 'purity_rate' not in st.session_state:
    st.session_state.purity_rate = 24

if 'show_more_notice' not in st.session_state:
    st.session_state.show_more_notice = False
if 'show_more_news' not in st.session_state:
    st.session_state.show_more_news = False

# 모델을 캐싱하여 속도 최적화 (한 번만 로드)
@st.cache_resource
def load_yolo_model():
    if HAS_YOLO:
        return YOLO("yolov8n.pt")
    return None

# =================================================================
# 4. 스마트폰 화면 비율 및 커스텀 스타일 세팅
# =================================================================
st.set_page_config(page_title="RE:PLANET 대전 동구청", layout="centered")

st.markdown("""
    <style>
    .stApp { max-width: 480px; margin: 0 auto; background-color: #f9fafb; padding: 10px; }
    .main-title { font-size:26px; font-weight:bold; color: #1b4332; text-align: center; margin-bottom: 5px; }
    .sub-txt { font-size:13px; color: #6B7280; text-align: center; margin-bottom: 25px; }
    .detail-box { background-color: #f1f5f9; padding: 15px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #4b5563; font-size: 14px; line-height: 1.6; }
    .meta-box { background-color: #f8fafc; padding: 12px; border-radius: 6px; border: 1px solid #e2e8f0; font-family: monospace; font-size: 12px; }
    .result-box { background-color: #ecfdf5; border: 1px solid #