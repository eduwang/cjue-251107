import random
import streamlit as st

st.set_page_config(page_title="덧셈·뺄셈 연습", page_icon="🧮")

st.title("🧮 간단한 덧셈·뺄셈 연습")
st.write("3문제를 연속으로 풀고 최종적으로 맞춘 개수를 알려줍니다.")


def generate_problem():
    """0~20 범위의 간단한 덧셈 또는 뺄셈 문제(결과가 음수인 경우를 피함)."""
    a = random.randint(0, 20)
    b = random.randint(0, 20)
    op = random.choice(["+", "-"])
    # 뺄셈일 때 음수를 피하려면 a >= b
    if op == "-" and b > a:
        a, b = b, a
    question = f"{a} {op} {b}"
    answer = a + b if op == "+" else a - b
    return question, answer


def reset_quiz():
    st.session_state.problems = [generate_problem() for _ in range(3)]
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.last_feedback = ""
    st.session_state.user_answer = ""


if "problems" not in st.session_state:
    reset_quiz()


def submit_answer():
    idx = st.session_state.index
    question, correct = st.session_state.problems[idx]
    raw = st.session_state.user_answer
    if raw is None or raw == "":
        st.session_state.last_feedback = "정답을 입력해주세요."
        return
    try:
        user = int(raw)
    except ValueError:
        st.session_state.last_feedback = "숫자만 입력할 수 있어요."
        return

    if user == correct:
        st.session_state.score += 1
        st.session_state.last_feedback = "정답! 🎉"
    else:
        st.session_state.last_feedback = f"아쉽네요. 정답은 {correct} 입니다."

    st.session_state.index += 1
    st.session_state.user_answer = ""


## Quiz UI
if st.session_state.index < 3:
    st.markdown(f"**문제 {st.session_state.index + 1} / 3**")
    q_text, _ = st.session_state.problems[st.session_state.index]
    st.write(f"문제: **{q_text}**")

    st.text_input("정답을 숫자로 입력하세요", key="user_answer")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("제출", on_click=submit_answer)
    with col2:
        st.button("초기화", on_click=reset_quiz)

    if st.session_state.last_feedback:
        st.info(st.session_state.last_feedback)

else:
    # 결과 화면
    st.subheader("결과")
    st.write(f"총 3문제 중 **{st.session_state.score}** 문제를 맞혔습니다.")
    st.write("문제와 정답:")
    for i, (q, a) in enumerate(st.session_state.problems, start=1):
        st.write(f"{i}. {q} = {a}")

    if st.button("다시 풀기"):
        reset_quiz()

