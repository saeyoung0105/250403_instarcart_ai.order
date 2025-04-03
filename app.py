import streamlit as st
import pandas as pd
import ast  # 문자열을 리스트로 안전하게 변환

# ------------------------------
# 1. 데이터 불러오기 함수
# ------------------------------
@st.cache_data
def load_data():
    file_path = file_path = "충성고객_추천데이터.xlsx"

    return pd.read_excel(file_path)

df = load_data()

# ------------------------------
# 2. 타이틀 및 소개 문구
# ------------------------------
st.title("Instacart 고객 맞춤형 AI 장바구니 트레져봇 🤖")
st.markdown("""
### 안녕하세요 👋  
Instacart 고객 맞춤형 AI 장바구니 트레져봇입니다!  
고객님께 꼭 맞는 상품을 추천해드릴게요 😊
""")

# ------------------------------
# 3. 핸드폰 번호 입력 (user_id로 사용)
# ------------------------------
phone_number = st.text_input("📱 핸드폰 번호를 입력해주세요 (고객 식별용):")

# ------------------------------
# 4. 고객 데이터 조회
# ------------------------------
if phone_number:
    try:
        user_id = int(phone_number)  # 예: 전화번호를 user_id로 사용
        user_data = df[df['user_id'] == user_id]

        if not user_data.empty:
            st.success(f"{user_id}번 고객님, 환영합니다!")

            # 1) 최근 장바구니 top 5 aisles
            st.subheader("🧺 최근 장바구니 Top 5 Aisles")
            st.write(user_data.iloc[0]['top_5_aisles'])

            # 2) 번들 추천 UI
            st.subheader("🎁 추천 번들 상품")

            bundle_options = [
                "아침 루틴 번들", "건강 채소 번들", "간편 도시락 번들", "간식 타임 번들", "어린이 간식 번들",
                "냉동식품 세트", "디저트 번들", "저탄고지 번들", "육류 주말 번들", "채식주의 번들",
                "클린홈 번들", "유제품 묶음", "아시안 푸드 번들", "냉장 필수 번들", "해장 세트",
                "와인 안주 번들", "뷰티 케어 번들", "반려동물 번들", "디톡스 번들", "비상상비약 번들" ]

            try:
                # 문자열이면 리스트로 변환
                bundle_value = user_data.iloc[0]['번들추천상품']
                prev_bundles = ast.literal_eval(bundle_value) if isinstance(bundle_value, str) else bundle_value
            except:
                prev_bundles = []

            selected_bundles = st.multiselect(
                "👇 원하시는 번들을 선택해주세요 (최대 3개)",
                bundle_options,
                default=prev_bundles,
                max_selections=3
            )

            # 3) 고객 입력란
            st.subheader("📋 고객님의 취향을 알려주세요")

            allergy = st.text_area("❗ 알러지가 있으신가요?", placeholder="예: 견과류, 해산물 등")
            dislike = st.text_area("🙅 싫어하는 음식이나 재료", placeholder="예: 콩, 건포도 등")
            like = st.text_area("👍 좋아하는 음식이나 재료", placeholder="예: 초콜릿, 닭고기 등")
            feedback = st.text_area("🛠️ 개선되었으면 하는 점", placeholder="자유롭게 작성해주세요")

            # 4) 제출 버튼
            if st.button("✅ 제출하기"):
                st.success("감사합니다! 고객님의 정보가 제출되었습니다 🙌")
                st.write("**선택한 번들 추천 상품:**", selected_bundles)
                st.write("**알러지:**", allergy)
                st.write("**싫어하는 항목:**", dislike)
                st.write("**좋아하는 항목:**", like)
                st.write("**개선사항:**", feedback)

        else:
            st.error("❌ 해당 고객 번호에 대한 데이터를 찾을 수 없습니다.")

    except ValueError:
        st.warning("⚠️ 숫자로 된 핸드폰 번호를 입력해주세요.")
