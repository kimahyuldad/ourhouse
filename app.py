import streamlit as st
import base64
import os
import math
from datetime import datetime

# Set Page Config
st.set_page_config(
    page_title="AssetFlow - 내 집 마련 자산 관리",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Base64 Image Helper
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
            return f"data:image/png;base64,{encoded}"
    return ""

real_estate_img = get_image_base64("stitch_project/real_estate_trend.png")
finance_img = get_image_base64("stitch_project/finance_trend.png")

# Custom CSS
st.markdown("""<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet">
<style>
.stMainBlockContainer { max-width: 680px; padding-bottom: 4rem; }
body, .stApp { font-family: 'Inter', sans-serif; }
.material-symbols-outlined { font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24; vertical-align: middle; }
.af-card { background: #ffffff; padding: 1.25rem; border-radius: 0.75rem; box-shadow: 0 4px 20px rgba(0,0,0,0.05); border: 1px solid rgba(195,197,215,0.3); margin-bottom: 1rem; }
.af-primary { background: #003fb1; color: #fff; padding: 1.25rem; border-radius: 0.75rem; box-shadow: 0 10px 25px rgba(0,63,177,0.15); position: relative; overflow: hidden; margin-bottom: 1rem; }
.af-green { background: #005439; color: #fff; padding: 1.25rem; border-radius: 0.75rem; box-shadow: 0 10px 25px rgba(0,84,57,0.15); position: relative; overflow: hidden; margin-bottom: 1rem; }
.scroll-none::-webkit-scrollbar { display: none; }
.scroll-none { -ms-overflow-style: none; scrollbar-width: none; }
</style>""", unsafe_allow_html=True)

# ── User Input Section ──
st.subheader("🎯 자산 정보 입력")
col1, col2 = st.columns(2)
with col1:
    goal_price_input = st.number_input("목표 주택 가격 (억원)", min_value=0.1, max_value=100.0, value=8.5, step=0.1, format="%.1f")
    cash_input = st.number_input("현재 현금성 자산 (억원)", min_value=0.0, max_value=100.0, value=2.0, step=0.1, format="%.1f")
with col2:
    stock_input = st.number_input("주식 자산 (억원)", min_value=0.0, max_value=100.0, value=1.0, step=0.1, format="%.1f")
    other_input = st.number_input("기타 자산 (기존 부동산 등) (억원)", min_value=0.0, max_value=100.0, value=0.57, step=0.01, format="%.2f")

total_assets = cash_input + stock_input + other_input
needed_loan = goal_price_input - total_assets

# ── Loan Button ──
if st.button("💸 대출금 계산하기", use_container_width=True):
    if total_assets >= goal_price_input:
        st.success("🎉 축하합니다! 자산 총합이 목표 주택 가격을 초과하여 대출이 필요 없습니다!")
        needed_loan = 0.0
    else:
        st.error(f"🚨 필요한 대출 금액은 **{needed_loan:.2f}억원** 입니다.")

# ── Tabs ──
tab_dash, tab_plan, tab_sim = st.tabs(["📊 대시보드", "💸 저축 및 대출 플랜", "🔮 목표 시뮬레이션"])

achievement_rate = min(int((total_assets / goal_price_input) * 100), 100)
remaining_amount = max(goal_price_input - total_assets, 0.0)

# ═══════════════════════════════════════
# 1. Dashboard Tab
# ═══════════════════════════════════════
with tab_dash:
    dashoffset = 251.3 * (1 - achievement_rate / 100)

    dash_html = f"""<div>
<h2 style="font-size:1.25rem;font-weight:700;margin:0;">반가워요, 아율이네</h2>
<p style="font-size:0.875rem;color:#434654;margin:0.25rem 0 0 0;">오늘의 자산 현황을 확인해보세요.</p>
</div>

<div class="af-card">
<h3 style="font-size:1.125rem;font-weight:600;color:#191c1d;margin:0 0 1.5rem 0;">내 집 마련 목표 달성률</h3>
<div style="position:relative;width:10rem;height:10rem;margin:0 auto 1.5rem auto;display:flex;align-items:center;justify-content:center;">
<svg style="width:100%;height:100%;transform:rotate(-90deg);" viewBox="0 0 100 100">
<circle cx="50" cy="50" r="40" stroke="#d6e4f3" stroke-width="8" fill="transparent"/>
<circle cx="50" cy="50" r="40" stroke="#003fb1" stroke-width="8" fill="transparent" stroke-dasharray="251.3" stroke-dashoffset="{dashoffset}" stroke-linecap="round" style="transition:stroke-dashoffset 1s ease-in-out;"/>
</svg>
<div style="position:absolute;text-align:center;">
<span style="display:block;font-size:2.25rem;font-weight:800;color:#003fb1;line-height:1;">{achievement_rate}%</span>
<span style="font-size:0.75rem;color:#434654;font-weight:600;">달성률</span>
</div>
</div>
<div style="margin-bottom:1.5rem;">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">
<span style="font-size:0.875rem;font-weight:600;color:#434654;">현재 자산</span>
<span style="font-size:0.875rem;font-weight:700;color:#003fb1;">{total_assets:.2f}억원</span>
</div>
<div style="width:100%;background:#d6e4f3;height:0.625rem;border-radius:9999px;overflow:hidden;">
<div style="background:#003fb1;height:100%;width:{achievement_rate}%;transition:width 1s ease-out;"></div>
</div>
</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.75rem;">
<div style="background:#f3f4f5;padding:1rem;border-radius:0.75rem;">
<span style="display:block;font-size:0.75rem;color:#434654;margin-bottom:0.25rem;">목표 금액</span>
<span style="font-size:1.125rem;font-weight:700;color:#191c1d;">{goal_price_input:.1f}억원</span>
</div>
<div style="background:#f3f4f5;padding:1rem;border-radius:0.75rem;">
<span style="display:block;font-size:0.75rem;color:#434654;margin-bottom:0.25rem;">남은 금액</span>
<span style="font-size:1.125rem;font-weight:700;color:#006f4d;">{remaining_amount:.2f}억원</span>
</div>
</div>
</div>

<div class="af-primary">
<div style="position:absolute;right:-2rem;top:-2rem;width:8rem;height:8rem;background:rgba(255,255,255,0.1);border-radius:50%;filter:blur(20px);"></div>
<div style="position:relative;">
<span style="display:block;font-size:0.75rem;font-weight:600;letter-spacing:0.05em;opacity:0.85;margin-bottom:0.25rem;">TOTAL ASSETS</span>
<h2 style="font-size:1.125rem;font-weight:600;color:#ffffff;margin:0 0 0.5rem 0;">총 자산 현황</h2>
<div style="display:flex;align-items:baseline;gap:0.5rem;margin-bottom:1rem;">
<span style="font-size:1.875rem;font-weight:700;">{total_assets * 10000:.0f}만원</span>
<span style="background:#006f4d;color:#fff;font-size:0.75rem;font-weight:600;padding:0.125rem 0.5rem;border-radius:0.25rem;display:inline-flex;align-items:center;gap:0.125rem;">
<span class="material-symbols-outlined" style="font-size:10px;font-variation-settings:'FILL' 1;">trending_up</span>+2.4%</span>
</div>
</div>
</div>

<div style="margin-top:1.5rem;margin-bottom:1rem;display:flex;justify-content:space-between;align-items:center;">
<h3 style="font-size:1.125rem;font-weight:600;color:#191c1d;margin:0;">부동산 시장 트렌드</h3>
<span style="font-size:0.875rem;color:#003fb1;font-weight:600;cursor:pointer;">전체보기</span>
</div>
<div style="display:flex;gap:1rem;overflow-x:auto;padding-bottom:0.5rem;" class="scroll-none">
<div style="flex-shrink:0;width:16rem;height:12rem;border-radius:0.75rem;overflow:hidden;position:relative;border:1px solid rgba(195,197,215,0.3);">
<img style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;" alt="Real Estate" src="{real_estate_img}">
<div style="position:absolute;inset:0;background:linear-gradient(to top,rgba(0,0,0,0.8) 0%,rgba(0,0,0,0.3) 60%,transparent 100%);display:flex;justify-content:flex-end;padding:1rem;flex-direction:column;">
<span style="color:#b5c4ff;font-size:0.75rem;font-weight:600;margin-bottom:0.25rem;">서울 부동산</span>
<p style="color:#fff;font-weight:700;font-size:0.875rem;margin:0;line-height:1.3;">마포구 아파트 실거래가 추이</p>
</div>
</div>
<div style="flex-shrink:0;width:16rem;height:12rem;border-radius:0.75rem;overflow:hidden;position:relative;border:1px solid rgba(195,197,215,0.3);">
<img style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;" alt="Finance" src="{finance_img}">
<div style="position:absolute;inset:0;background:linear-gradient(to top,rgba(0,0,0,0.8) 0%,rgba(0,0,0,0.3) 60%,transparent 100%);display:flex;justify-content:flex-end;padding:1rem;flex-direction:column;">
<span style="color:#b5c4ff;font-size:0.75rem;font-weight:600;margin-bottom:0.25rem;">금융 트렌드</span>
<p style="color:#fff;font-weight:700;font-size:0.875rem;margin:0;line-height:1.3;">주택담보대출 금리 인하 전망</p>
</div>
</div>
</div>"""
    st.markdown(dash_html, unsafe_allow_html=True)

# ═══════════════════════════════════════
# 2. Saving & Loan Plan Tab
# ═══════════════════════════════════════
with tab_plan:
    st.markdown("""<div>
<h2 style="font-size:1.25rem;font-weight:700;margin:0;">목표 달성을 위한 플랜</h2>
<p style="font-size:0.875rem;color:#434654;margin:0.25rem 0 0 0;">대출금 규모에 맞춰 월 상환 계획을 검토하세요.</p>
</div>""", unsafe_allow_html=True)

    if needed_loan > 0.0:
        st.markdown(f"""<div class="af-primary" style="margin-bottom:1.5rem;">
<p style="font-size:0.75rem;font-weight:600;opacity:0.9;margin:0 0 0.5rem 0;">REQUIRED LOAN AMOUNT</p>
<h2 style="font-size:1.75rem;font-weight:700;color:#fff;margin:0 0 0.5rem 0;">필요 대출금: {needed_loan:.2f}억원</h2>
<div style="font-size:0.875rem;background:rgba(255,255,255,0.15);padding:0.5rem 0.75rem;border-radius:0.5rem;display:inline-flex;align-items:center;gap:0.25rem;">
<span class="material-symbols-outlined" style="font-size:16px;">info</span>
자산 총합 대비 부족한 자금을 대출 시뮬레이션에 자동 연동합니다.</div>
</div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div class="af-green" style="margin-bottom:1.5rem;">
<p style="font-size:0.75rem;font-weight:600;opacity:0.9;margin:0 0 0.5rem 0;">LOAN STATUS</p>
<h2 style="font-size:1.75rem;font-weight:700;color:#fff;margin:0 0 0.5rem 0;">대출이 필요 없습니다!</h2>
<div style="font-size:0.875rem;background:rgba(255,255,255,0.15);padding:0.5rem 0.75rem;border-radius:0.5rem;display:inline-flex;align-items:center;gap:0.25rem;">
<span class="material-symbols-outlined" style="font-size:16px;">check_circle</span>
현재 보유 자산으로 목표 주택을 즉시 매입할 수 있습니다.</div>
</div>""", unsafe_allow_html=True)

    st.subheader("🏦 대출 상환액 계산기")
    loan_val = needed_loan if needed_loan > 0.0 else 1.0

    col_loan1, col_loan2 = st.columns(2)
    with col_loan1:
        interest_rate = st.slider("대출 금리 (%)", min_value=2.0, max_value=7.0, value=3.8, step=0.1, key="interest_rate_slider")
    with col_loan2:
        repayment_years = st.slider("상환 기간 (년)", min_value=10, max_value=40, value=30, step=1, key="repayment_years_slider")

    P = loan_val * 100000000
    r_monthly = (interest_rate / 100) / 12
    n_payments = repayment_years * 12

    if r_monthly > 0:
        monthly_repayment = P * (r_monthly * (1 + r_monthly)**n_payments) / ((1 + r_monthly)**n_payments - 1)
    else:
        monthly_repayment = P / n_payments

    monthly_repayment_manwon = monthly_repayment / 10000

    st.markdown(f"""<div class="af-card" style="border-left:5px solid #003fb1;background:rgba(26,86,219,0.03);">
<div style="display:flex;justify-content:space-between;align-items:center;">
<span style="font-size:1rem;font-weight:600;color:#191c1d;">월 예상 상환액</span>
<span style="font-size:1.5rem;font-weight:700;color:#003fb1;">약 {monthly_repayment_manwon:.0f}만원</span>
</div>
<p style="font-size:0.75rem;color:#737686;margin:0.5rem 0 0 0;text-align:right;">* 원리금균등상환 기준 (대출 규모 {loan_val:.2f}억원 적용)</p>
</div>""", unsafe_allow_html=True)

    st.markdown("""<div style="margin-top:2rem;margin-bottom:1rem;">
<h3 style="font-size:1.125rem;font-weight:600;color:#191c1d;margin:0;">추천 금융 상품</h3>
</div>
<div style="display:flex;flex-direction:column;gap:0.75rem;">
<div class="af-card" style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0;cursor:pointer;">
<div style="display:flex;align-items:center;gap:1rem;">
<div style="width:2.75rem;height:2.75rem;background:#d6e4f3;border-radius:0.5rem;display:flex;align-items:center;justify-content:center;">
<span class="material-symbols-outlined" style="color:#003fb1;">home_work</span></div>
<div>
<h4 style="font-size:0.95rem;font-weight:700;color:#191c1d;margin:0;">주택청약종합저축</h4>
<p style="font-size:0.825rem;color:#005439;font-weight:bold;margin:0.125rem 0 0 0;">최대 금리 4.5%</p>
</div></div>
<span class="material-symbols-outlined" style="color:#737686;">chevron_right</span>
</div>
<div class="af-card" style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0;cursor:pointer;">
<div style="display:flex;align-items:center;gap:1rem;">
<div style="width:2.75rem;height:2.75rem;background:#7ad9ad;border-radius:0.5rem;display:flex;align-items:center;justify-content:center;">
<span class="material-symbols-outlined" style="color:#002114;">savings</span></div>
<div>
<h4 style="font-size:0.95rem;font-weight:700;color:#191c1d;margin:0;">ISA 만기 연계 적금</h4>
<p style="font-size:0.825rem;color:#434654;margin:0.125rem 0 0 0;">비과세 혜택 및 높은 우대 금리</p>
</div></div>
<span class="material-symbols-outlined" style="color:#737686;">chevron_right</span>
</div>
</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════
# 3. Simulation Tab
# ═══════════════════════════════════════
with tab_sim:
    st.markdown("""<div>
<h2 style="font-size:1.25rem;font-weight:700;margin:0;">내 집 마련 시뮬레이션</h2>
<p style="font-size:0.875rem;color:#434654;margin:0.25rem 0 0 0;">매월 저축금액에 따른 달성 예측일을 시뮬레이션해 보세요.</p>
</div>""", unsafe_allow_html=True)

    st.subheader("⚙️ 저축 조건 조정")
    col_sim1, col_sim2 = st.columns(2)
    with col_sim1:
        monthly_saving = st.slider("매월 저축액 (만원)", min_value=50, max_value=1000, value=350, step=50)
    with col_sim2:
        expected_yield = st.slider("기대 수익률 (연 %)", min_value=1.0, max_value=15.0, value=4.5, step=0.1)

    S = monthly_saving * 10000
    R = remaining_amount * 100000000
    i_monthly = (expected_yield / 100) / 12
    months_needed = 0

    if R <= 0:
        months_needed = 0
    else:
        if i_monthly > 0:
            value_to_log = 1 + (R * i_monthly) / S
            months_needed = math.ceil(math.log(value_to_log) / math.log(1 + i_monthly))
        else:
            months_needed = math.ceil(R / S)

    target_month = 6 + (months_needed % 12)
    target_year = 2026 + (months_needed // 12)
    if target_month > 12:
        target_month -= 12
        target_year += 1

    if remaining_amount <= 0:
        pred_text = "현재 보유 자산만으로 목표를 즉시 달성할 수 있어요!"
    else:
        pred_text = f'현재 저축 속도라면 <span style="color:#fff;font-weight:800;text-decoration:underline;">{target_year}년 {target_month}월</span>에 목표를 달성할 수 있어요'

    st.markdown(f"""<div class="af-primary" style="margin-bottom:1.5rem;">
<div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">
<span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1;">stars</span>
<span style="font-size:0.75rem;font-weight:600;letter-spacing:0.05em;opacity:0.9;">GOAL PREDICTION</span>
</div>
<p style="font-size:1.25rem;font-weight:600;line-height:1.4;margin:0 0 1.25rem 0;">{pred_text}</p>
<div style="width:100%;background:rgba(255,255,255,0.2);height:0.5rem;border-radius:9999px;overflow:hidden;margin-bottom:0.5rem;">
<div style="background:#fff;height:100%;width:{achievement_rate}%;transition:width 0.5s;"></div>
</div>
<div style="display:flex;justify-content:space-between;font-size:0.75rem;opacity:0.85;">
<span>현재: {total_assets:.2f}억</span>
<span>목표: {goal_price_input:.1f}억</span>
</div>
</div>""", unsafe_allow_html=True)

    st.markdown("""<div class="af-card">
<h3 style="font-size:1.125rem;font-weight:600;color:#191c1d;margin:0 0 1rem 0;">시뮬레이션 분석 리포트</h3>
<ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:1rem;">
<li style="display:flex;align-items:flex-start;gap:0.75rem;padding-bottom:0.75rem;border-bottom:1px solid #edeeef;">
<span class="material-symbols-outlined" style="color:#005439;margin-top:2px;">trending_up</span>
<div>
<p style="font-size:0.9rem;font-weight:700;color:#191c1d;margin:0;">저축액 50만원 증액 시</p>
<p style="font-size:0.8rem;color:#434654;margin:0.125rem 0 0 0;">목표 달성 시기가 크게 단축됩니다.</p>
</div></li>
<li style="display:flex;align-items:flex-start;gap:0.75rem;padding-bottom:0.75rem;border-bottom:1px solid #edeeef;">
<span class="material-symbols-outlined" style="color:#003fb1;margin-top:2px;">account_balance</span>
<div>
<p style="font-size:0.9rem;font-weight:700;color:#191c1d;margin:0;">추천 대출 상품</p>
<p style="font-size:0.8rem;color:#434654;margin:0.125rem 0 0 0;">생애최초 주택자금대출 활용 시 LTV 최대 80% 완화 가능.</p>
</div></li>
<li style="display:flex;align-items:flex-start;gap:0.75rem;">
<span class="material-symbols-outlined" style="color:#53606c;margin-top:2px;">info</span>
<div>
<p style="font-size:0.9rem;font-weight:700;color:#191c1d;margin:0;">부대 비용 고려</p>
<p style="font-size:0.8rem;color:#434654;margin:0.125rem 0 0 0;">취득세 및 복비(중개수수료) 약 3,200만원 별도 고려 필요.</p>
</div></li>
</ul>
</div>""", unsafe_allow_html=True)
