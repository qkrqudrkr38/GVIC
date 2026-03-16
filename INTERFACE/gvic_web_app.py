"""
================================================================================
[GVIC Standard Operating Procedure]
파일명: gvic_web_app.py | 버전: v8.2.3 (Full Scale) | 생성일자: 2026-03-14
--------------------------------------------------------------------------------
최종 통합 지침:
1. 7대 기둥(LINK~SPINE) 하부 로직 및 8대악(8-Evils) 타격 공식 전체 포함.
2. 사이드바(Commander Bar) 동기화 피드백 슬라이더(30초 주기) 기능 복구.
3. 데이터 수신 센터 사이드바 하단 고정 및 초밀착 레이아웃 준수.
4. Slate Navy (#0f172a) 고대비 디자인 및 점멸 경고 시스템 적용.
================================================================================
"""

import streamlit as st
import time
from datetime import datetime

# [1. 시스템 설정 및 시각적 프레임워크]
st.set_page_config(page_title="GVIC COMMAND CENTER", page_icon="🏰", layout="wide")

st.markdown("""
    <style>
    /* 기본 배경 및 고대비 텍스트 */
    .stApp { background-color: #0f172a; }
    header { visibility: hidden; }
    .block-container { padding-top: 1rem !important; }
    h1, h2, h3, h4, .stMarkdown { color: #f1f5f9 !important; }

    /* 사이드바 초밀착 레이아웃 */
    [data-testid="stSidebar"] { background-color: #1e293b !important; border-right: 1px solid #334155; }
    hr { margin: 0.4rem 0 !important; border-color: #334155; }
    .stSelectbox, .stSlider, .stExpander, .stFileUploader { margin-bottom: -10px !important; }

    /* 전술 행동 카드 디자인 */
    .action-card {
        background-color: #1e293b; padding: 18px; border-radius: 12px;
        border: 1px solid #334155; margin-bottom: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .action-title { color: #3b82f6; font-weight: 800; font-size: 1.1rem; margin-bottom: 8px; }
    .instruction-text { 
        background-color: #0f172a; padding: 10px; border-radius: 6px; 
        color: #fbbf24; font-size: 0.85rem; border-left: 4px solid #fbbf24; margin-bottom: 10px;
    }

    /* 위기 점멸 애니메이션 */
    @keyframes blinker { 50% { border-color: #ef4444; background-color: #450a0a; } }
    .blink-active { 
        animation: blinker 0.8s linear infinite; 
        border: 2px solid #ef4444 !important; border-radius: 8px; padding: 10px; 
    }

    /* 8대악 레이더 유닛 */
    .evil-detector { 
        background-color: #450a0a; border: 1px solid #ef4444; 
        padding: 8px; border-radius: 6px; margin-bottom: 5px; font-size: 0.85rem; 
    }
    
    /* 요약 지표 박스 */
    .summary-box {
        background-color: #0f172a; padding: 15px; border-radius: 8px; 
        border: 1px solid #334155; margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# [2. 세션 상태 관리]
if 'metrics' not in st.session_state:
    st.session_state.metrics = {
        "LINK":  {"val": "98%", "status": "CRISIS", "idx": 0, "icon": "🛡️"},
        "GATE":  {"val": "Locked", "status": "NORMAL", "idx": 1, "icon": "🏰"},
        "FIN":   {"val": "18%", "status": "WARNING", "idx": 2, "icon": "💸"},
        "HEART": {"val": "8대악 감지", "status": "CRISIS", "idx": 3, "icon": "❤️"},
        "IMMU":  {"val": "Safe", "status": "NORMAL", "idx": 4, "icon": "⚖️"},
        "BRAIN": {"val": "분석중", "status": "NORMAL", "idx": 5, "icon": "🧠"},
        "SPINE": {"val": "Active", "status": "NORMAL", "idx": 6, "icon": "🦴"}
    }
if 'expanded_pillar' not in st.session_state: st.session_state.expanded_pillar = None
if 'active_tab_idx' not in st.session_state: st.session_state.active_tab_idx = 0
if 'sync_interval' not in st.session_state: st.session_state.sync_interval = 30
if 'last_sync' not in st.session_state: st.session_state.last_sync = datetime.now().strftime("%H:%M:%S")

# --- 🛰️ 통합 제어 사이드바 (Commander Bar) ---
with st.sidebar:
    st.title("🛰️ COMMANDER")
    
    st.markdown("#### ⏱️ 동기화 관제")
    st.session_state.sync_interval = st.select_slider(
        "피드백 주기(s)", 
        options=[1, 5, 10, 30, 60], 
        value=st.session_state.sync_interval
    )
    st.caption(f"동기화 엔진: {st.session_state.sync_interval}초 간격으로 피드백 수신 중")
    st.divider()

    st.markdown("#### ⚙️ 노드 권한 설정")
    for p in st.session_state.metrics.keys():
        is_exp = (st.session_state.expanded_pillar == p)
        with st.expander(f"📍 {p}", expanded=is_exp):
            if is_exp:
                st.markdown('<div class="blink-active">⚠️ 작전 수행 중</div>', unsafe_allow_html=True)
                if st.button(f"💾 {p} 조치 저장", key=f"side_save_{p}"):
                    st.session_state.metrics[p]["status"] = "NORMAL"
                    st.session_state.expanded_pillar = None
                    st.rerun()
            else: st.caption(f"{p} 보안 폐쇄")
    
    st.divider()

    st.markdown("#### 📁 데이터 수신 센터")
    purpose = st.selectbox("수신 목적", ["선택", "🎯 광고", "💰 판매", "📦 재고"], label_visibility="collapsed")
    if purpose != "선택":
        st.file_uploader(f"[{purpose}] 투입", type=['csv', 'xlsx'], label_visibility="collapsed")
        if st.button("🚀 데이터 바인딩", use_container_width=True):
            st.session_state.last_sync = datetime.now().strftime("%H:%M:%S")
            st.toast(f"{purpose} 데이터 신경망 동기화 완료.")

# --- 🏰 메인 레이어 ---
st.title("🏰 GVIC INTEGRATED COMMAND")

# 상태 배너
st.markdown(f"""
    <div style="background-color:#1e293b; padding:12px; border-radius:10px; border:1px solid #334155; margin-bottom:15px; font-size:0.9rem; color:#94a3b8;">
        🛰️ <b>동기화:</b> {st.session_state.sync_interval}s &nbsp;&nbsp; | &nbsp;&nbsp; 🕒 <b>마지막 갱신:</b> {st.session_state.last_sync} &nbsp;&nbsp; | &nbsp;&nbsp; 🛡️ <b>상태:</b> {'🚨 위기 대응 중' if st.session_state.expanded_pillar else '✅ 정상 운영'}
    </div>
    """, unsafe_allow_html=True)

# [SECTION A] 실시간 타격 전광판 (7열 배치)
cols = st.columns(7)
for i, key in enumerate(st.session_state.metrics.keys()):
    with cols[i]:
        m = st.session_state.metrics[key]
        status = "🔴" if m['status'] == "CRISIS" else "🟡" if m['status'] == "WARNING" else "✅"
        if st.button(f"{m['icon']} {key}\n{m['val']} {status}", key=f"warp_{key}"):
            st.session_state.active_tab_idx = m['idx']
            st.session_state.expanded_pillar = key
            st.rerun()

st.divider()

# [SECTION B] 7대 기둥 분석 및 행동 지침 탭
tabs = st.tabs([f"{m['icon']} {k}" for k, m in st.session_state.metrics.items()])

# --- 🛡️ TAB 1: GVIC LINK ---
with tabs[0]:
    st.subheader("🛡️ GVIC LINK: 제국 무결성 관리")
    l1, l2 = st.columns(2)
    with l1:
        st.markdown('<div class="action-card"><div class="action-title">1.1 Verification Center</div><div class="instruction-text">💡 지침: NTS API 연동 및 대표자 인증을 완료하십시오.</div></div>', unsafe_allow_html=True)
        st.button("🔍 NTS API 연동 확인", use_container_width=True, key="link_nts")
        st.button("📱 대표자 생체인증", use_container_width=True, key="link_auth")
    with l2:
        st.markdown('<div class="action-card"><div class="action-title">1.3 Sync Health</div><div class="instruction-text">💡 지침: API 심장박동을 점검하십시오.</div></div>', unsafe_allow_html=True)
        st.success("💓 API Heartbeat: ACTIVE (Latency 180ms)")
        st.metric("📊 D.I.S 지수", st.session_state.metrics["LINK"]["val"])

# --- 🏰 TAB 2: GATEKEEPER ---
with tabs[1]:
    st.subheader("🏰 GATEKEEPER: 성문 진입 및 금융 설정")
    g1, g2 = st.columns(2)
    with g1:
        st.markdown('<div class="action-card"><div class="action-title">2.1 Advanced Filter (15대 적격성)</div><div class="instruction-text">💡 지침: 플랫폼 입점 적격성을 판정하십시오.</div></div>', unsafe_allow_html=True)
        items = ["상표권 확보", "KC인증 여부", "마진율 30%+", "경쟁사 분석", "물류 최적화", "CS 대응 체계", "상세페이지 완결", "키워드 추출", "광고 예산 확보", "반품 프로세스", "재고 안정성", "법적 고지 준수", "결제 시스템 연동", "서버 부하 테스트", "카테고리 승인"]
        c_cols = st.columns(3)
        checked = 0
        for j, item in enumerate(items):
            with c_cols[j % 3]:
                if st.checkbox(item, key=f"gate_check_{j}"): checked += 1
        st.progress(checked / 15, text=f"적격성: {checked}/15")
    with g2:
        st.markdown('<div class="action-card"><div class="action-title">2.2 Setup Fee & Billing</div><div class="instruction-text">💡 지침: 마켓 수수료 및 고정비를 각인하십시오.</div></div>', unsafe_allow_html=True)
        fee = st.number_input("마켓 수수료 (%)", 10.5, key="gate_fee")
        labor = st.number_input("고정 인건비 (원)", 3500000, key="gate_labor")
        st.markdown(f'<div class="summary-box"><p style="margin:0; font-size:0.8rem; color:#94a3b8;">월 고정 지출액</p><h3 style="margin:0; color:#3b82f6;">₩ {labor:,}</h3></div>', unsafe_allow_html=True)

# --- 💸 TAB 3: FINANCIAL ---
with tabs[2]:
    st.subheader("💸 FINANCIAL: 자금 흐름 및 정체 방어")
    f1, f2 = st.columns(2)
    with f1:
        st.markdown('<div class="action-card"><div class="action-title">3.1 Settlement Optimization</div><div class="instruction-text">💡 지침: 미정산금 규모와 자금 회전 주기를 추적하십시오.</div></div>', unsafe_allow_html=True)
        pending = st.number_input("총 미정산금 (원)", 15000000, key="fin_pending")
        sales = st.number_input("일 평균 매출 (원)", 1000000, key="fin_sales")
        st.metric("자금 회전 주기", f"{pending/sales if sales > 0 else 0:.1f} 일")
    with f2:
        st.markdown('<div class="action-card"><div class="action-title">3.2 Financial Cost Audit</div><div class="instruction-text">💡 지침: 선정산 및 외환 수수료 누수를 감지하십시오.</div></div>', unsafe_allow_html=True)
        leak = st.number_input("금융 비용 누수액 (원)", 62000, key="fin_leak")
        st.error(f"누수율 감지: {(leak/pending*100) if pending > 0 else 0:.2f} %")

# --- ❤️ TAB 4: HEART ---
with tabs[3]:
    st.subheader("❤️ HEART: 8대악 박멸 및 ROAS 타격")
    st.markdown("#### 📡 8-Evils Monitoring Radar")
    e_cols = st.columns(4)
    evils = ["1. 역마진", "2. 광고 누수", "3. 정산 누락", "4. 품절(손실)", "5. 장기 재고", "6. 역구매", "7. 패널티", "8. CS 과부하"]
    for idx, evil in enumerate(evils):
        with e_cols[idx % 4]:
            st.markdown(f'<div class="evil-detector">👹 {evil}</div>', unsafe_allow_html=True)
    
    st.divider()
    h1, h2 = st.columns(2)
    with h1:
        st.markdown('<div class="action-card"><div class="action-title">4.1 Ad Kill-Switch</div><div class="instruction-text">💡 지침: ROAS 미달 시 즉시 킬-스위치를 가동하십시오.</div></div>', unsafe_allow_html=True)
        target = st.slider("목표 ROAS (%)", 100, 1000, 400, key="heart_target")
        if 85 < target: # 시뮬레이션 ROAS 85
            st.markdown('<div class="blink-active" style="text-align:center; color:white;">🚨 ROAS 위험: 85% <br> 킬-스위치 가동 대기</div>', unsafe_allow_html=True)
            st.button("🔥 전 캠페인 타격(중단)", key="heart_kill")
    with h2:
        st.markdown('<div class="action-card"><div class="action-title">4.2 Margin Guard</div><div class="instruction-text">💡 지침: 실시간 공헌이익을 산출하여 마진을 방어하십시오.</div></div>', unsafe_allow_html=True)
        price = st.number_input("판매가", 50000, key="heart_price")
        cost = st.number_input("원가", 22000, key="heart_cost")
        margin = price - cost - (price * 0.15) 
        st.metric("순공헌이익", f"₩ {margin:,.0f}", delta=f"{(margin/price*100):.1f}%")

# --- ⚖️ TAB 5: IMMUNITY ---
with tabs[4]:
    st.subheader("⚖️ IMMUNITY: 관세·세무 및 법적 방패")
    i1, i2 = st.columns(2)
    with i1:
        st.markdown('<div class="action-card"><div class="action-title">5.1 Tax Refund Automation</div><div class="instruction-text">💡 지침: 영세율 증빙 데이터를 추출하고 환급액을 확정하십시오.</div></div>', unsafe_allow_html=True)
        purchase = st.number_input("매입 증빙 금액 (원)", 85000000, key="immu_purchase")
        st.success(f"예상 부가세 환급: ₩ {purchase * 0.1:,.0f}")
    with i2:
        st.markdown('<div class="action-card"><div class="action-title">5.2 Purge Execution</div><div class="instruction-text">💡 지침: 위협 탐지 시 적극 방어 액션을 수행하십시오.</div></div>', unsafe_allow_html=True)
        st.button("🚫 계정 영구 정지 / IP 대역 차단", key="immu_purge")

# --- 🧠 TAB 6: BRAIN ---
with tabs[5]:
    st.subheader("🧠 BRAIN: 경영 지능 및 레버리지 분석")
    b1, b2 = st.columns(2)
    with b1:
        st.markdown('<div class="action-card"><div class="action-title">6.1 Leverage (매출 vs 누수)</div><div class="instruction-text">💡 지침: 매출 증대와 누수 차단 중 이익 기여도를 대조하십시오.</div></div>', unsafe_allow_html=True)
        st.info("💡 분석결과: 누수 5% 차단이 매출 5% 상승보다 순이익에 2.4배 더 기여합니다.")
    with b2:
        st.markdown('<div class="action-card"><div class="action-title">6.2 AI Forecast</div><div class="instruction-text">💡 지침: 선제적 발주량 산출을 통해 기회 손실을 방지하십시오.</div></div>', unsafe_allow_html=True)
        st.metric("AI 권장 발주량", "1,250 ea", delta="안전재고 포함")

# --- 🦴 TAB 7: SPINE ---
with tabs[6]:
    st.subheader("🦴 SPINE: 공급망 및 물류 척추")
    s1, s2 = st.columns(2)
    with s1:
        st.markdown('<div class="action-card"><div class="action-title">7.1 Logistics Partnership</div><div class="instruction-text">💡 지침: 운송사 사고율 기반 파트너 교체 지수를 점검하십시오.</div></div>', unsafe_allow_html=True)
        st.slider("배송 사고율 (%)", 0.0, 10.0, 1.2, key="spine_logis")
    with s2:
        st.markdown('<div class="action-card"><div class="action-title">7.2 Chargeback Invoice</div><div class="instruction-text">💡 지침: 불량 데이터를 근거로 매입가 차감을 청구하십시오.</div></div>', unsafe_allow_html=True)
        st.button("📄 불량 기반 매입가 차감(Chargeback) 청구서 발행", key="spine_cb")