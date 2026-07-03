import streamlit as st
import pandas as pd
import requests  


from importnb import Notebook

with Notebook():
    import sample

# Cấu hình giao diện chế độ hiển thị rộng (wide) để xếp các poster nằm ngang
st.set_page_config(page_title="Hệ Thống Gợi Ý Phim", page_icon="🎬", layout="wide")
st.title("Gợi Ý Phim Dành Riêng Cho Bạn")



@st.cache_resource
def init_system():
    return sample.load_and_train_model()


with st.spinner("Đang tải dữ liệu và khởi tạo mô hình AI... Vui lòng chờ..."):
    model, trainset, movie_titles, rmse_score = init_system()

st.sidebar.title("Hiệu suất Mô hình")
st.sidebar.metric(label="Độ lỗi RMSE", value=f"{rmse_score:.4f}")
st.sidebar.info("💡 Điểm RMSE càng thấp, mô hình dự đoán sở thích người dùng càng chính xác!")
st.sidebar.divider()


def get_movie_poster(movie_title):

    api_key = "8265bd1679663a7ea12ac168da84d2e8"


    cleaned_title = movie_title.split(' (')[0]

    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={cleaned_title}"
    fallback_image = "https://dummyimage.com/500x750/cccccc/000000.png&text=No+Poster"

    try:
        response = requests.get(url, timeout=3).json()
        if response.get('results'):
            poster_path = response['results'][0].get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except Exception:
        pass
    return fallback_image



user_id = st.text_input(label="Nhập User ID (VD: 196, 250):", value="196")

if st.button(" Gợi Ý Ngay", width='stretch'):

    top_n = sample.get_top_n_recommendations(user_id, model, trainset, movie_titles, n=10)

    if top_n:
        st.success(f"Danh sách phim gợi ý dành cho User {user_id}:")


        columns_per_row = 5
        cols = st.columns(columns_per_row)

        for idx, movie in enumerate(top_n):

            col_idx = idx % columns_per_row

            with cols[col_idx]:

                with st.spinner("Đang tải poster..."):
                    poster_url = get_movie_poster(movie['Tên Phim'])


                st.image(poster_url, width='stretch')


                st.markdown(f"**{movie['Tên Phim']}**")
                st.caption(f"⭐ Dự đoán: {movie['Điểm Dự Đoán']}/5")
    else:
        st.warning("Không có dữ liệu cho User này!")