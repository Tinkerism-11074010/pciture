import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO

# # 缓存数据加载过程
# @st.cache
# def load_data(file_path):
#     return pd.read_excel(file_path)

# # 缓存图片加载过程
# @st.cache
# def load_image(image_url):
#     try:
#         response = requests.get(image_url)
#         img = Image.open(BytesIO(response.content))
#         return img
#     except Exception as e:
#         return None

# GitHub 文件 URL
github_file_url = "https://raw.githubusercontent.com/Tinkerism-11074010/pciture/main/streamlit专用-阉割版.xlsx"

# 发送 GET 请求
response = requests.get(github_file_url)
file_content = BytesIO(response.content)
df = pd.read_excel(file_content)

# 获取类别计数
category_counts = df['聚类类别'].value_counts()

# 根据计数排序类别
sorted_categories = category_counts.index.tolist()
# 显示标题
st.title('图片与聚类类别看板')

# 使用 selectbox 让用户选择聚类类别
selected_category = st.selectbox('选择一个聚类类别：', sorted_categories)

# 过滤选中的类别的数据
filtered_df = df[df['聚类类别'] == selected_category]

# 显示选择的类别
st.subheader(f'聚类类别 {selected_category} 的图片')

# 显示该类别下的所有图片
for _, row in filtered_df.iterrows():
    image_url = row['商品主图']  # 假设图片链接列的名字是 '图片链接'
    product_link = row['商品详情页链接']  # 假设产品链接列的名字是 '产品链接
    product_name = row['商品标题']

    try:
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        st.image(img, caption=f'图片 {selected_category}', use_container_width=True)
    except Exception as e:
        st.write(f'无法加载图片: {image_url}，错误: {e}')

    # 使用 st.columns 来同时显示产品标题和产品链接
    col1, col2 = st.columns([3, 1])  # 分为两列，标题占 3，链接占 1
    with col1:
        st.write(product_name)  # 显示产品标题
    with col2:
        if pd.notna(product_link):  # 如果产品链接不为空
            st.markdown(f"[点击查看产品链接]({product_link})")  # 显示超链接
        else:
            st.write("产品链接不可用")  # 如果产品链接不可用
