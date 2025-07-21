
import streamlit as st
import pandas as pd
from PIL import Image
import os

if "year" not in st.session_state:
    st.session_state.year = 1
    st.session_state.max_years = 5
    st.session_state.budget = 10000
    st.session_state.carbon = 0
    st.session_state.satisfaction = 50
    st.session_state.history = []

df = pd.read_csv("data/policies.csv")

st.set_page_config(page_title="탄소 헌터", layout="wide")
st.title("🌍 탄소 헌터: CO₂ 타이쿤")

st.markdown(f"**📅 연도:** {st.session_state.year} / {st.session_state.max_years}")
st.markdown(f"**💰 예산:** {st.session_state.budget:,}원")
st.markdown(f"**🌍 누적 탄소 감축:** {st.session_state.carbon}톤")
st.markdown(f"**😊 시민 만족도:** {st.session_state.satisfaction}")

if st.session_state.year <= st.session_state.max_years:
    policies = df.sample(3)
    cols = st.columns(3)

    for i, row in policies.iterrows():
        with cols[i]:
            st.image(f"assets/{row['image']}", use_column_width=True)
            st.subheader(row['name'])
            st.markdown(f"💰 비용: {row['cost']:,}원")
            st.markdown(f"🌍 탄소감축: -{row['carbon_reduction']}톤")
            st.markdown(f"😊 만족도 변화: +{row['satisfaction']}")
            if st.button(f"선택하기 {i+1}", key=f"btn{i}"):
                if st.session_state.budget < row['cost']:
                    st.warning("예산이 부족합니다!")
                else:
                    st.session_state.budget -= row['cost']
                    st.session_state.carbon += row['carbon_reduction']
                    st.session_state.satisfaction += row['satisfaction']
                    st.session_state.history.append(row['name'])
                    st.session_state.year += 1
                    st.experimental_rerun()
else:
    st.success("🎉 게임 종료!")
    st.markdown(f"**총 탄소 감축량:** {st.session_state.carbon}톤")
    st.markdown(f"**최종 시민 만족도:** {st.session_state.satisfaction}")
    st.markdown("**선택한 정책들:**")
    for h in st.session_state.history:
        st.markdown(f"- {h}")
    st.button("🔁 다시 시작", on_click=lambda: st.session_state.clear())
