import requests
import streamlit as st
import matplotlib.pyplot as plt

# Gọi API 
API_URL = "https://9a61-2001-ee0-5615-cfa0-9c60-b5d1-2271-4f22.ngrok-free.app/get_aqi"

st.title("📊 Mean AQI Dashboard (via API)")

try:
    response = requests.get(API_URL, timeout=10)
    data = response.json()

    if data:
        formatted_results = [[row[0], row[2], row[4], row[-1]] for row in data]
        years = [row[0] for row in formatted_results]
        quarters = [row[1] for row in formatted_results]
        states = [row[2] for row in formatted_results]
        mean_aqi = [row[3] for row in formatted_results]
        time_labels = [f"{y}-Q{q}" for y, q in zip(years, quarters)]

        fig, ax = plt.subplots(figsize=(10, 5))
        unique_states = list(set(states))
        for state in unique_states:
            state_aqi = [mean_aqi[i] for i in range(len(states)) if states[i] == state]
            state_labels = [time_labels[i] for i in range(len(states)) if states[i] == state]
            ax.plot(state_labels, state_aqi, marker="o", label=state)

        ax.set_xlabel("Thời gian (Year-Quarter)")
        ax.set_ylabel("Mean AQI")
        ax.set_title("📈 Mean AQI theo Thời gian")
        ax.legend(title="State")
        ax.grid(True)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    else:
        st.warning("⚠️ Không có dữ liệu trả về từ API.")

except Exception as e:
    st.error(f"Lỗi khi gọi API: {e}")
