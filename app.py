import streamlit as st
import time
import os

# =================================================================
# 1. 레벨별 캐릭터 정보 데이터베이스 정의
# =================================================================
LEVEL_DATA = {
    1: {
        "name": "알속두루",
        "img_path": "images/duru_lv1.png",
        "description": "🌱 아직 알껍데기를 쓰고 있는 초경량 아기 오리입니다. 플로깅을 통해 에너지를 나누어 주세요!",
        "next_xp": "100 XP"
    },
    2: {
        "name": "푸른두루",
        "img_path": "images/duru_lv2.png",
        "description": "✨ 알껍데기를 벗고 머리에 귀여운 새싹 안테나가 자라났습니다! 대청호 행성이 반응하고 있습니다.",
        "next_xp": "300 XP"
    },
    3: {
        "name": "에코두루",
        "img_path": "images/duru_lv3.png",
        "description": "🤖 AI 환경 분석용 친환경 테크 조끼를 착용했습니다. 정밀 모니터링 기능이 활성화되었습니다.",
        "next_xp": "600 XP"
    },
    4: {
        "name": "가디언두루",
        "img_path": "images/duru_lv4.png",
        "description": "👑 대청호의 완벽한 최종 수호자 형태입니다! 생태 데이터 지팡이를 활용해 동구를 완벽히 정화합니다.",
        "next_xp": "MAX (최종 진화 완료)"
    }
}

# =================================================================
# 2. 앱 시스템 세션 상태(Session State) 초기화
# =================================================================
if 'duru_level' not in st.session_state:
    st.session_state.duru_level = 1
if 'eco_points' not in st.session_state:
    st.session_state.eco_points = 0
if 'purity_rate' not in st.session_state:
    st.session_state.purity_rate = 24

# 더보기 버튼 토글 상태 초기화
if 'show_more_notice' not in st.session_state:
    st.session_state.show_more_notice = False
if 'show_more_news' not in st.session_state:
    st.session_state.show_more_news = False

# =================================================================
# 3. 스마트폰 화면 비율 및 커스텀 스타일 세팅
# =================================================================
st.set_page_config(page_title="RE:PLANET 대전 동구청", layout="centered")

st.markdown("""
    <style>
    .main-title { font-size:26px; font-weight:bold; color: #1b4332; text-align: center; margin-bottom: 5px; }
    .sub-txt { font-size:13px; color: #6B7280; text-align: center; margin-bottom: 25px; }
    .detail-box { background-color: #f1f5f9; padding: 15px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #4b5563; font-size: 14px; line-height: 1.6; }
    </style>
""", unsafe_allow_html=True)

# =================================================================
# 4. 사이드바 내비게이션 및 발표 시연용 리셋 버튼
# =================================================================
st.sidebar.markdown("### 🏢 대전 동구청 스마트 뷰")
app_menu = st.sidebar.radio(
    "이동할 메뉴를 선택하세요", 
    ["🏠 동구 소식 & 행정", "🌱 RE:PLANET (리플레닛)", "🎁 내 에코 쿠폰함"]
)

st.sidebar.markdown("---")

st.sidebar.markdown("### 🛠️ 발표 시연용 컨트롤러")
if st.sidebar.button("🔄 시연 상태 초기화 (Lv.1 리셋)", use_container_width=True):
    st.session_state.duru_level = 1
    st.session_state.eco_points = 0
    st.session_state.purity_rate = 24
    st.session_state.show_more_notice = False
    st.session_state.show_more_news = False
    st.sidebar.success("시연 데이터 초기화 완료!")
    st.rerun()

# =================================================================
# [메뉴 1] 동구 소식 & 행정 화면
# =================================================================
if app_menu == "🏠 동구 소식 & 행정":
    st.markdown('<div class="main-title">🏢 대전광역시 동구청</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-txt">행정과 구민을 잇는 스마트 동구</div>', unsafe_allow_html=True)
    
    st.subheader("📌 실시간 동구 소식")
    
    # 📢 1. 공지사항 라인 (글자수와 버튼 높이 밸런스를 위해 5:1 비율 조정)
    col_notice, col_btn1 = st.columns([4.8, 1.2])
    with col_notice:
        st.info("📢 [공지] 2026 대청호 생태 보존 축제 청년 자원봉사자 모집")
    with col_btn1:
        st.markdown("<div style='padding-top: 4px;'></div>", unsafe_allow_html=True) # 알림창과 높이 맞추기용 패딩
        if st.button("더보기", key="btn_notice_more", use_container_width=True):
            st.session_state.show_more_notice = not st.session_state.show_more_notice
            st.rerun()
            
    # 공지사항 상세 내용 대화상자 (토글 동작)
    if st.session_state.show_more_notice:
        st.markdown("""
        <div class="detail-box">
            <strong>📋 [공지 상세] 대청호 생태 보존 축제 자원봉사 안내</strong><br>
            • <strong>활동 일시:</strong> 2026년 10월 12일 ~ 14일 (3일간)<br>
            • <strong>활동 내용:</strong> 생태 체험 부스 운영 보조 및 행사장 주변 친환경 '리플레닛' 투어 가이드<br>
            • <strong>참여 혜택:</strong> 1365 봉사시간 인정, 동구청장 명의 수료증, <b>RE:PLANET 500 에코 포인트</b> 즉시 적립
        </div>
        """, unsafe_allow_html=True)

    # 📰 2. 뉴스 라인
    col_news, col_btn2 = st.columns([4.8, 1.2])
    with col_news:
        st.success("📰 [뉴스] 대전역 역세권 개발 및 소제동 구도심 재생 사업 본격화")
    with col_btn2:
        st.markdown("<div style='padding-top: 4px;'></div>", unsafe_allow_html=True)
        if st.button("더보기", key="btn_news_more", use_container_width=True):
            st.session_state.show_more_news = not st.session_state.show_more_news
            st.rerun()
            
    # 뉴스 상세 내용 대화상자 (토글 동작)
    if st.session_state.show_more_news:
        st.markdown("""
        <div class="detail-box">
            <strong>📰 [뉴스 상세] 소제동 구도심 재생 및 에코 벨트 구축</strong><br>
            대전광역시 동구는 대전역 역세권 복합2구역의 조기 착공과 더불어 소제동 전통 한옥 거리를 '지속 가능한 상생 문화지구'로 지정했습니다.<br>
            특히 이번 재생 사업은 대청호 환경 보존 시스템인 <b>'RE:PLANET' 모바일 플랫폼과 연동</b>되어, 구민들이 소제동 제휴 카페에서 에코 쿠폰을 사용할 수 있는 로컬 순환 경제 메커니즘을 국내 최초로 도입합니다.
        </div>
        """, unsafe_allow_html=True)

# =================================================================
# [메뉴 2] RE:PLANET (핵심 AI 캐릭터 실시간 진화 화면)
# =================================================================
elif app_menu == "🌱 RE:PLANET (리플레닛)":
    st.markdown('<div class="main-title">🌱 RE:PLANET 동구</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-txt">지구를 다시 살리는 대청호 AI 플로깅 프로젝트</div>', unsafe_allow_html=True)
    
    current_lv = st.session_state.duru_level
    current_data = LEVEL_DATA[current_lv]
    
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
        st.write(f"*{current_data['description']}*")
        st.write(f"🔋 **다음 진화까지:** `{current_data['next_xp']}`")

    st.markdown("---")
    
    st.subheader("📸 플로깅 실시간 인증")
    
    if current_lv >= 4:
        st.balloons()
        st.success("🎉 축하합니다! 대청호 행성을 완벽하게 구원하여 두루가 최종 가디언 형태로 진화했습니다!")
    else:
        uploaded_file = st.file_uploader(f"Lv.{current_lv + 1}(으)로 진화하기 위한 플로깅 사진을 업로드하세요", type=["png", "jpg", "jpeg"])
        
        if uploaded_file is not None:
            st.image(uploaded_file, caption="인증 대기 이미지", use_container_width=True)
            
            if st.button(f"🚀 AI 그린 렌즈 분석 시작 (Lv.{current_lv} ➔ Lv.{current_lv + 1})"):
                with st.spinner("🤖 RE:PLANET 비전 AI가 종량제 봉투 부피 및 GPS 메타데이터를 정밀 검증 중입니다..."):
                    time.sleep(2.0)
                
                st.session_state.duru_level += 1
                st.session_state.eco_points += 500
                st.session_state.purity_rate = min(st.session_state.purity_rate + 15, 95)
                
                st.balloons()
                st.success(f"✔ AI 인증 성공! 두루가 `Lv.{st.session_state.duru_level} {LEVEL_DATA[st.session_state.duru_level]['name']}`(으)로 진화했습니다!")
                st.rerun()

# =================================================================
# [메뉴 3] 로컬 상생 에코 쿠폰함 화면
# =================================================================
elif app_menu == "🎁 내 에코 쿠폰함":
    st.markdown('<div class="main-title">🎁 로컬 상생 에코 마켓</div>', unsafe_allow_html=True)
    st.write("RE:PLANET 플로깅을 통해 획득한 포인트로 교환한 상생 리워드 내역입니다.")
    
    st.subheader("🎫 보유 중인 모바일 쿠폰")
    
    if st.session_state.duru_level == 1:
        st.info("🔒 아직 획득한 쿠폰이 없습니다. '두루'를 Lv.2 이상 진화시키면 첫 상생 쿠폰이 열립니다!")
    
    if st.session_state.duru_level >= 2:
        st.warning("🎫 [Level 2 보상] 대전 중앙시장 소상공인 상생 3,000원 모바일 할인권")
        st.code("||||| ||| |||| |||| 2026-REPLANET-LV2", language="")
        
    if st.session_state.duru_level >= 3:
        st.success("🎫 [Level 3 보상] 대전 동구 소제동 제휴 카페 에코 아메리카노 무료 교환권")
        st.code("||||| ||| |||| |||| 2026-REPLANET-LV3", language="")
        
    if st.session_state.duru_level >= 4:
        st.info("👑 [Level 4 보상] 대청호 환경 가디언 한정판 모바일 공식 인증서 발급")
        st.code("🏆 CERTIFICATE-REPLANET-DURU-FINAL", language="")
        
    st.caption("※ 본 바코드를 대전 동구 관내 전통시장 및 소제동 카페 가맹점에 제시하세요.")
    st.caption("🏢 재원 후원처: CNCITY 에너지 사회공헌 기금 / 소상공인시장진흥공단 협업 예산")