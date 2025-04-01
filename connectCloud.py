import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# URL của API chạy trên máy Windows (thay bằng IP nếu chạy trên server)
API_URL = "http://172.20.10.2:5000"

st.title("📊 Mean AQI Dashboard")

# Gọi API
st.write("🔄 Đang lấy dữ liệu từ API...")
response = requests.get(API_URL)

if response.status_code == 200:
    data = response.json()
    if "error" in data:
        st.error(f"Lỗi API: {data['error']}")
    else:
        # Chuyển đổi dữ liệu thành DataFrame
        df = pd.DataFrame(data, columns=["Year", "Quarter", "State", "Mean AQI"])
        st.table(df)

        # Vẽ biểu đồ
        plt.figure(figsize=(10, 5))
        for state in df["State"].unique():
            state_data = df[df["State"] == state]
            plt.plot(
                state_data["Year"].astype(str) + "-Q" + state_data["Quarter"].astype(str),
                state_data["Mean AQI"],
                marker="o",
                label=state
            )

        plt.xlabel("Thời gian")
        plt.ylabel("Mean AQI")
        plt.legend()
        st.pyplot(plt)

else:
    st.error("❌ Lỗi lấy dữ liệu từ API!")
