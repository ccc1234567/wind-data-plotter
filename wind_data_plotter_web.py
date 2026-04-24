# 固定顺序：先配置后端，再导入！解决云端报错
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import io

# 颜色配置
COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

# 列名映射（精简版，不影响运行）
COLUMN_CN_MAP = {
    "timestamp": "时间戳",
    "wind_speed": "风速",
    "WindSpeed": "风速",
    "grid_active_power": "电网有功功率",
    "GridPower": "电网功率",
    "yaw_position": "偏航位置"
}

# ------------------- 工具函数 -------------------
def get_display_name(col, translate):
    if not translate:
        return col
    return COLUMN_CN_MAP.get(col, col)

# ------------------- 主界面 -------------------
def main():
    st.set_page_config(page_title="风机B文件绘图工具", layout="wide")
    st.title("金风风机B文件绘图工具")

    # 初始化
    if 'df' not in st.session_state:
        st.session_state.df = None

    # 上传文件
    uploaded = st.file_uploader("上传B文件", type=["txt", "csv"])
    if uploaded:
        try:
            # 读取数据
            uploaded.seek(0)
            df = pd.read_csv(uploaded, sep=";", comment="#", header=0, on_bad_lines='skip')
            st.session_state.df = df
            st.success(f"读取成功：{df.shape[0]} 行，{df.shape[1]} 列")
        except:
            st.error("文件读取失败")

    # 绘图区域
    if st.session_state.df is not None:
        df = st.session_state.df
        with st.sidebar:
            translate = st.checkbox("中文列名", True)
            x = st.selectbox("X轴", df.columns)
            ys = st.multiselect("Y轴（可多选）", df.columns)
            plot_type = st.radio("类型", ["折线图", "散点图"])
            
            if st.button("开始绘图") and ys:
                fig, ax = plt.subplots(figsize=(12,5))
                for i, y in enumerate(ys):
                    data = df[[x,y]].dropna()
                    if plot_type == "折线图":
                        ax.plot(data[x], data[y], label=get_display_name(y, translate), color=COLORS[i%len(COLORS)])
                    else:
                        ax.scatter(data[x], data[y], s=2, label=get_display_name(y, translate), color=COLORS[i%len(COLORS)])
                
                ax.legend()
                ax.grid(alpha=0.3)
                st.pyplot(fig)

if __name__ == "__main__":
    main()