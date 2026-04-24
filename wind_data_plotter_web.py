import streamlit as st
import pandas as pd
import io

# 列名翻译
COLUMN_CN_MAP = {
    "timestamp": "时间戳",
    "wind_speed": "风速",
    "WindSpeed": "风速",
    "grid_active_power": "电网有功功率",
    "GridPower": "电网功率",
    "yaw_position": "偏航位置"
}

def get_name(col, cn):
    return COLUMN_CN_MAP.get(col, col) if cn else col

def main():
    st.set_page_config(page_title="风机绘图工具", layout="wide")
    st.title("金风风机B文件绘图工具")

    # 上传文件
    f = st.file_uploader("上传B文件(txt/csv)", type=["txt","csv"])
    if f:
        try:
            f.seek(0)
            df = pd.read_csv(f, sep=";", comment="#", on_bad_lines="skip")
            st.success(f"成功：{df.shape[0]}行 {df.shape[1]}列")
            
            # 控制面板
            with st.sidebar:
                cn = st.checkbox("中文列名", True)
                x = st.selectbox("X轴", df.columns)
                ys = st.multiselect("Y轴(可多选)", df.columns)
                t = st.radio("图表类型", ["折线图", "散点图"])

                if st.button("绘图") and ys:
                    d = df[[x]+ys].dropna()
                    c = st.columns(len(ys))
                    for i,y in enumerate(ys):
                        with c[i]:
                            st.subheader(get_name(y, cn))
                            if t == "折线图":
                                st.line_chart(d, x=x, y=y)
                            else:
                                st.scatter_chart(d, x=x, y=y)
        except:
            st.error("文件解析失败")

if __name__ == "__main__":
    main()