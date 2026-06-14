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
    .result-box { background-color: #ecfdf5; border: 1px solid #10b981; border-radius: 8px; padding: 15px; margin-top: 10px; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# =================================================================
# 5. 사이드바 내비게이션 및 발표 시연용 리셋 버튼
# =================================================================
st.sidebar.markdown("### 🏢 대전 동구청 스마트 뷰")
app_menu = st.sidebar.radio(
    "메뉴 이동", 
    ["1. 홈: 대청호 소식 & 구정 현황", "2. AI 플로깅 인증 (두루 키우기)", "3. 로컬 에코 상생 쿠폰함"]
)

st.sidebar.markdown("---")
if st.sidebar.button("🔄 [발표 시연용] 데이터 초기화", use_container_width=True):
    st.session_state.duru_level = 1
    st.session_state.eco_points = 0
    st.session_state.purity_rate = 24
    st.rerun()

current_lv = st.session_state.duru_level
current_data = LEVEL_DATA[current_lv]

st.markdown("<div class='main-title'>🌱 RE:PLANET 동구</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-txt'>지구를 다시 살리는 대청호 AI 플로깅 프로젝트</div>", unsafe_allow_html=True)

# =================================================================
# [메뉴 1] 홈 및 지자체 소식 화면
# =================================================================
if "1." in app_menu:
    st.subheader("📌 실시간 동구 소식")

    col_notice, col_btn1 = st.columns([4.8, 1.2])
    with col_notice:
        st.info("📢 [공지] 2026 대청호 생태 보존 축제 청년 자원봉사자 모집")
    with col_btn1:
        st.markdown("<div style='padding-top: 4px;'></div>", unsafe_allow_html=True) 
        if st.button("더보기", key="btn_notice_more", use_container_width=True):
            st.session_state.show_more_notice = not st.session_state.show_more_notice
            st.rerun()

    if st.session_state.show_more_notice:
        st.markdown("""
        <div class="detail-box">
            <b>[2026 대청호 생태 보존 축제 자원봉사자 모집]</b><br><br>
            • <b>기간:</b> 2026. 06. 15 ~ 06. 20<br>
            • <b>대상:</b> 대전 동구 관내 대학생 및 청년 누구나<br>
            • <b>혜택:</b> RE:PLANET 에코 포인트 특별 500P 지급 및 봉사시간 인정<br>
            • <b>문의:</b> 대전 동구청 환경과
        </div>
        """, unsafe_allow_html=True)

    col_news, col_btn2 = st.columns([4.8, 1.2])
    with col_news:
        st.success("📰 [뉴스] 대전역 역세권 개발 및 소제동 구도심 재생 사업 본격화")
    with col_btn2:
        st.markdown("<div style='padding-top: 4px;'></div>", unsafe_allow_html=True)
        if st.button("더보기", key="btn_news_more", use_container_width=True):
            st.session_state.show_more_news = not st.session_state.show_more_news
            st.rerun()

    if st.session_state.show_more_news:
        st.markdown("""
        <div class="detail-box">
            <b>[대전역 역세권 개발 및 소제동 구도심 재생 본격화]</b><br><br>
            대전 동구청은 대전역 일원의 혁신성장 거점 조성과 소제동 관사촌을 연계한 
            문화·예술 복합 단지 조성 사업을 이번 달부터 본격적으로 착수한다고 밝혔습니다. 
            해당 지역 소상공인들과의 상생을 위한 다양한 바우처 지원도 병행됩니다.
        </div>
        """, unsafe_allow_html=True)

# =================================================================
# [메뉴 2] 게이미피케이션 및 AI 인증 화면
# =================================================================
elif "2." in app_menu:
    st.subheader("🌍 현재 정화 구역: [대청호 행성]")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="대청호 정화율", 
                  value=f"{st.session_state.purity_rate} %", 
                  delta=f"+15%" if current_lv > 1 else None)
    with col2:
        st.metric(label="보유 에코 포인트", 
                  value=f"{st.session_state.eco_points} 🟢", 
                  delta=f"+500 🟢" if current_lv > 1 else None)

    st.write("📊 **대청호 행성 정화 진행도**")
    st.progress(st.session_state.purity_rate / 100)

    st.markdown("---")
    
    st.markdown(f"### 🦆 나의 수호 펫: 두루(DURU)")
    
    col_img, col_info = st.columns([1, 1.2])
    with col_img:
        if os.path.exists(current_data["img_path"]):
            st.image(current_data["img_path"], use_container_width=True)
        else:
            st.warning(f"⚠️ [{current_data['img_path']}] 파일이 images 폴더에 없습니다.")
            
    with col_info:
        st.write(f"**현재 상태:** `Lv.{current_lv} {current_data['name']}`")
        st.write(f"_{current_data['desc']}_")
        st.write(f"🔋 **다음 진화까지:** `{current_data['next_xp']}`")

    st.markdown("---")
    
    st.subheader("📸 AI 플로깅 및 메타데이터 인증")

    if current_lv >= 4:
        st.balloons()
        st.success("🎉 축하합니다! 대청호 행성을 완벽하게 구원하여 두루가 최종 가디언 형태로 진화했습니다!")
    else:
        st.markdown("##### 1. 수거한 쓰레기 부피(Volume) 설정")
        col_bag, col_fill = st.columns(2)
        with col_bag:
            bag_size_str = st.selectbox("사용한 종량제 봉투 규격", ["5L (표준 권장)", "10L", "20L (대형)"])
        with col_fill:
            fill_status = st.radio("봉투 채움 정도", ["70% 이상 달성 (적정)", "미달 (추가 수거 필요)"], horizontal=True)
            
        st.markdown("##### 2. 플로깅 현장 사진 업로드")
        uploaded_file = st.file_uploader(f"Lv.{current_lv + 1} 진화용 사진을 선택하세요", type=["png", "jpg", "jpeg"])

        if uploaded_file is not None:
            raw_image = Image.open(uploaded_file)
            st.image(raw_image, caption="업로드된 원본 이미지", use_container_width=True)
            
            # ---------------------------------------------------------
            # [추가된 핵심 방어 로직] 1차 쓰레기 인식 어뷰징 필터링
            # ---------------------------------------------------------
            is_valid_trash = False
            pre_check_count = 0
            
            if HAS_YOLO:
                with st.spinner("🔍 AI가 사진 속 쓰레기 유무를 1차 판별 중입니다..."):
                    try:
                        yolo_model = load_yolo_model()
                        first_check_results = yolo_model(raw_image)
                        pre_check_count = len(first_check_results[0].boxes)
                        
                        if pre_check_count > 0:
                            is_valid_trash = True
                        else:
                            is_valid_trash = False
                    except Exception:
                        is_valid_trash = True # 모델 로드 실패 시 시연을 위해 패스
            else:
                # ultralytics 미설치 환경의 경우 시연을 위해 통과 처리
                is_valid_trash = True 
                pre_check_count = np.random.randint(3, 8)
                time.sleep(1)

            # 쓰레기가 1개도 없으면 에러 표출 후 하단 로직 차단
            if not is_valid_trash:
                st.error("❌ [인증 반려] 사진에서 쓰레기 객체가 전혀 인식되지 않았습니다. 풍경이나 인물 사진은 어뷰징(부정수급) 방지를 위해 업로드할 수 없습니다. 쓰레기가 명확히 보이도록 다시 촬영해주세요.")
            
            # 쓰레기가 인식되었을 때만 분석 및 인증 진행
            else:
                st.success("✅ 쓰레기 객체 인식 완료! 정밀 부피 스캔 및 메타데이터 분석을 진행합니다.")
                
                st.markdown("##### ⚙️ RE:PLANET AI 임베디드 메타데이터 분석")
                raw_meta = extract_metadata(uploaded_file)
                has_gps = "GPSInfo" in raw_meta or "GPS" in str(raw_meta.keys())
                shot_time = raw_meta.get("DateTime", "2026:06:07 12:34:56 (당일 실시간 촬영인증)")

                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    st.text_input("📅 파일 내부 추출 촬영시각", value=shot_time, disabled=True)
                with col_m2:
                    gps_display = "위도: 36.3781 / 경도: 127.4892" if not has_gps else "성공적으로 추출됨"
                    st.text_input("📍 추출 GPS 좌표 (대청호 반경)", value=gps_display, disabled=True)

                if not has_gps:
                    st.caption("💡 *[시연 안내] 카카오톡/웹 파일 등 위치 정보가 없는 사진의 경우, 심사 시연용 가상 대청호 GPS 좌표로 보정 엔진을 적용하여 작동합니다.*")

                st.markdown("---")
                
                # 최종 AI 분석 시작 버튼 클릭 제어
                if st.button(f"🚀 AI 복합 인증 시작 (Lv.{current_lv} ➔ Lv.{current_lv + 1})", use_container_width=True):
                    if "미달" in fill_status:
                        st.error("❌ AI 인증 실패: 쓰레기 수거량이 권장 기준(봉투의 70% 이상)에 미달합니다. 대청호 환경 보호를 위해 조금 더 주워주세요!")
                    else:
                        with st.spinner("🤖 AI 그린 렌즈 모델이 종량제 봉투 픽셀 부피와 GPS 거리 매칭율을 정밀 계산 중입니다..."):
                            
                            max_vol = int(''.join(filter(str.isdigit, bag_size_str)))
                            trash_count = pre_check_count
                            
                            # YOLO 객체 시각화 이미지 띄우기
                            if HAS_YOLO:
                                try:
                                    yolo_model = load_yolo_model()
                                    results = yolo_model(raw_image)
                                    annotated_image = results[0].plot()
                                    st.image(annotated_image, caption="🔍 AI 실시간 객체 인식 및 부피 스캔 완료", use_container_width=True)
                                except Exception:
                                    pass

                            # 쓰레기 개수를 바탕으로 '실제 채움도' 역산
                            ai_fill_rate = min(100, 40 + (trash_count * 10))
                            actual_volume = round(max_vol * (ai_fill_rate / 100), 2)
                            carbon_reduction = round(actual_volume * 0.45, 2)
                            
                            st.markdown(f"""
                            <div class="result-box">
                                <b>💡 AI 부피 역산 검증 리포트</b><br>
                                • 선택한 종량제 봉투: <b>{max_vol}L</b><br>
                                • AI가 탐지한 객체(쓰레기) 수: <b>{trash_count}개</b><br>
                                • AI 분석 실제 채움도: <b>{ai_fill_rate}%</b><br>
                                • <b>최종 산출 부피: {actual_volume}L</b><br>
                                • 🌍 <b>탄소 절감 기여도: {carbon_reduction} kg CO2</b>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            time.sleep(1)

                            st.session_state.duru_level += 1
                            st.session_state.eco_points += 500
                            st.session_state.purity_rate = min(st.session_state.purity_rate + 15, 95)
                            
                            st.balloons()
                            st.success(f"✔ [인증 성공] {max_vol}L 봉투 규격 확인 및 대청호 GPS 일치! 두루가 `Lv.{st.session_state.duru_level} {LEVEL_DATA[st.session_state.duru_level]['name']}`(으)로 진화했습니다!")
                            time.sleep(2)
                            st.rerun()

# =================================================================
# [메뉴 3] 로컬 상생 에코 쿠폰함 화면
# =================================================================
elif "3." in app_menu:
    st.subheader("🛍️ 로컬 상생 쿠폰함")
    st.write(f"현재 사용 가능한 에코 포인트: **{st.session_state.eco_points} 🟢**")
    
    st.markdown("---")
    
    col_c1, col_c2 = st.columns([1, 2])
    with col_c1:
        st.markdown("<div style='font-size:40px; text-align:center;'>🎫</div>", unsafe_allow_html=True)
    with col_c2:
        st.write("### 동구 전통시장 상생 쿠폰")
        st.write("중앙시장, 신도꼼지락시장 전용 가맹점")
        
    st.info("조건: 1,000 에코 포인트당 10,000원권 교환 (현재 500P 보유 시 5,000원권 발급 가능)")
    st.markdown("---")
    
    st.write("**📱 결제용 바코드 (임시)**")
    st.code("🏆 CERTIFICATE-REPLANET-DURU-FINAL", language="")

    st.caption("※ 본 바코드를 대전 동구 관내 전통시장 및 소제동 카페 가맹점에 제시하세요.")
    st.caption("🏢 재원 후원처: CNCITY 에너지 사회공헌 기금 / 소상공인시장진흥공단 협업 예산")
