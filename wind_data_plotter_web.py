import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import io
import platform

# ================== 保留原列名映射 ==================
COLUMN_CN_MAP = {
    "timestamp": "时间戳",
    "grid_U1": "电网电压U1",
    "grid_U2": "电网电压U2",
    "grid_U3": "电网电压U3",
    "grid_I1": "电网电流I1",
    "grid_I2": "电网电流I2",
    "grid_I3": "电网电流I3",
    "grid_frequency": "电网频率",
    "converter_in_power": "变流器输入有功功率",
    "converter_in_reactive_power": "变流器输入无功功率",
    # 复制原代码中所有COLUMN_CN_MAP的映射项（此处省略，需补全）
    "WindSpeed": "风速",
    "WindDirction": "风向",
    "PowerLimitDemand": "功率限制需求",
}

# 解决matplotlib中文显示问题
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']  # Linux
# plt.rcParams['font.sans-serif'] = ['SimHei']     # Windows

# ================== 核心工具函数 ==================
def detect_encoding(file_path):
    encodings = ['utf-8', 'gbk', 'gb2312', 'utf-16', 'latin1']
    for enc in encodings:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                f.read(1000)
            return enc
        except UnicodeDecodeError:
            continue
    return 'utf-8'

def parse_file_sections(file_path, encoding):
    with open(file_path, 'r', encoding=encoding, errors='replace') as f:
        lines = f.readlines()

    analog_col_line = None
    analog_start = None
    analog_end = None
    digital_col_line = None
    digital_start = None
    digital_end = None

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith('#'):
            break
        if stripped.count(';') >= 10:
            lower = stripped.lower()
            if any(kw in lower for kw in ['buffersave', 'version', '-------', 'analog signals']):
                continue
            analog_col_line = i
            break

    if analog_col_line is None:
        raise ValueError("未找到模拟信号列名行")

    analog_start = analog_col_line + 1
    while analog_start < len(lines) and lines[analog_start].strip().startswith('#'):
        analog_start += 1
    if analog_start >= len(lines):
        raise ValueError("模拟信号无数据行")

    for i in range(analog_start, len(lines)):
        line = lines[i].strip()
        if '# ------- digital signals' in line.lower():
            for j in range(i+1, min(i+20, len(lines))):
                l = lines[j].strip()
                if l.startswith('#') and l.count(';') >= 10 and not any(kw in l.lower() for kw in ['buffersave', 'version', '-------']):
                    digital_col_line = j
                    break
            if digital_col_line is not None:
                digital_start = digital_col_line + 1
                while digital_start < len(lines) and lines[digital_start].strip().startswith('#'):
                    digital_start += 1
                digital_end = len(lines)
            break

    if digital_col_line is not None:
        analog_end = digital_col_line - 1
    else:
        analog_end = len(lines)

    analog_col_line_raw = lines[analog_col_line].lstrip('#').strip()
    analog_col_names = [c.strip() for c in analog_col_line_raw.split(';') if c.strip()]

    digital_col_names = []
    if digital_col_line is not None:
        digital_col_line_raw = lines[digital_col_line].lstrip('#').strip()
        digital_col_names = [c.strip() for c in digital_col_line_raw.split(';') if c.strip()]

    return (analog_col_names, analog_start, analog_end,
            digital_col_names, digital_start, digital_end)

def get_display_name(eng_name, translate=True):
    if not translate:
        return eng_name
    cn = COLUMN_CN_MAP.get(eng_name, "")
    return f"{cn} ({eng_name})" if cn else eng_name

# ================== Streamlit页面逻辑 ==================
st.set_page_config(page_title="金风风机B文件绘图工具", layout="wide")
st.title("金风风机B文件绘图工具 (Web版)")

# 1. 文件上传
uploaded_file = st.file_uploader("选择B文件（.txt/.csv）", type=["txt", "csv"])
if uploaded_file is not None:
    # 临时保存上传文件
    with open("temp_data.txt", "wb") as f:
        f.write(uploaded_file.getbuffer())
    file_path = "temp_data.txt"

    try:
        # 2. 解析文件
        encoding = detect_encoding(file_path)
        (analog_col_names, analog_start, analog_end,
         digital_col_names, digital_start, digital_end) = parse_file_sections(file_path, encoding)

        # 3. 读取模拟信号数据
        with open(file_path, 'r', encoding=encoding) as f:
            lines = f.readlines()
        analog_data_lines = lines[analog_start:analog_end]
        analog_str = ''.join(analog_data_lines)
        analog_io = io.StringIO(analog_str)
        df_analog_raw = pd.read_csv(analog_io, sep=';', header=None, low_memory=False, na_values=["", " ", "NA", "N/A"])
        actual_analog_cols = df_analog_raw.shape[1]
        if actual_analog_cols != len(analog_col_names):
            if actual_analog_cols > len(analog_col_names):
                df_analog_raw = df_analog_raw.iloc[:, :len(analog_col_names)]
            else:
                analog_col_names = analog_col_names[:actual_analog_cols]
        df_analog_raw.columns = analog_col_names
        df_analog = df_analog_raw.apply(pd.to_numeric, errors='coerce')

        # 4. 读取数字信号数据（如有）
        df_digital = None
        has_digital = (digital_start is not None and digital_end is not None and len(digital_col_names) > 0)
        if has_digital:
            digital_data_lines = lines[digital_start:digital_end]
            digital_str = ''.join(digital_data_lines)
            digital_io = io.StringIO(digital_str)
            df_digital_raw = pd.read_csv(digital_io, sep=';', header=None, low_memory=False, na_values=["", " ", "NA", "N/A"])
            actual_digital_cols = df_digital_raw.shape[1]
            if actual_digital_cols != len(digital_col_names):
                if actual_digital_cols > len(digital_col_names):
                    df_digital_raw = df_digital_raw.iloc[:, :len(digital_col_names)]
                else:
                    digital_col_names = digital_col_names[:actual_digital_cols]
            df_digital_raw.columns = digital_col_names
            df_digital = df_digital_raw.apply(pd.to_numeric, errors='coerce')

        # 5. 显示读取状态
        st.success(
            f"读取成功：模拟信号 {len(df_analog)}行 x {len(df_analog.columns)}列" +
            (f"，数字信号 {len(df_digital)}行 x {len(df_digital.columns)}列" if has_digital else "")
        )

        # 6. 核心交互控件
        col1, col2, col3 = st.columns(3)
        with col1:
            # 数据集选择
            dataset_options = ["模拟信号"]
            if has_digital:
                dataset_options.append("数字信号")
            selected_dataset = st.selectbox("选择数据集", dataset_options)
            df = df_analog if selected_dataset == "模拟信号" else df_digital

        with col2:
            # 汉译开关
            translate = st.checkbox("显示中文列名", value=True)
            # 处理列名显示映射
            display_cols = [get_display_name(col, translate) for col in df.columns]
            col_mapping = {disp: orig for disp, orig in zip(display_cols, df.columns)}

        with col3:
            # 绘图类型选择
            plot_type = st.radio("绘图类型", ["折线图", "散点图"], horizontal=True)

        # 7. X/Y轴选择
        col_x, col_y = st.columns(2)
        with col_x:
            x_col_display = st.selectbox("选择X轴列", display_cols)
            x_col = col_mapping[x_col_display]

        with col_y:
            y_cols_display = st.multiselect("选择Y轴列（可多选）", display_cols, default=display_cols[1] if len(display_cols)>1 else None)
            y_cols = [col_mapping[disp] for disp in y_cols_display]

        # 8. 生成图表
        if st.button("生成图表", type="primary") and y_cols:
            # 清理缺失值
            plot_df = df[[x_col] + y_cols].dropna()
            if len(plot_df) == 0:
                st.error("所选列无有效数据（全为缺失值），无法绘图！")
            else:
                # Matplotlib静态图表
                st.subheader("静态图表（Matplotlib）")
                fig, ax = plt.subplots(figsize=(12, 6))
                colors = plt.cm.tab10.colors  # 颜色循环
                for idx, y_col in enumerate(y_cols):
                    y_display = get_display_name(y_col, translate)
                    if plot_type == "折线图":
                        ax.plot(plot_df[x_col], plot_df[y_col], label=y_display, color=colors[idx % len(colors)])
                    else:
                        ax.scatter(plot_df[x_col], plot_df[y_col], label=y_display, color=colors[idx % len(colors)], s=1)
                ax.set_xlabel(get_display_name(x_col, translate))
                ax.set_ylabel("数值")
                ax.set_title(f"{selected_dataset} - {plot_type}")
                ax.legend()
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)

                # Plotly交互式图表（支持缩放/下载）
                st.subheader("交互式图表（Plotly）")
                for idx, y_col in enumerate(y_cols):
                    y_display = get_display_name(y_col, translate)
                    if plot_type == "折线图":
                        fig_plotly = px.line(
                            plot_df, x=x_col, y=y_col, title=y_display,
                            labels={x_col: get_display_name(x_col, translate), y_col: y_display}
                        )
                    else:
                        fig_plotly = px.scatter(
                            plot_df, x=x_col, y=y_col, title=y_display,
                            labels={x_col: get_display_name(x_col, translate), y_col: y_display}
                        )
                    st.plotly_chart(fig_plotly, use_container_width=True)

        # 9. 数据预览
        with st.expander("数据预览（前20行）"):
            st.dataframe(df.head(20), use_container_width=True)

    except Exception as e:
        st.error(f"文件处理失败: {str(e)}")
        st.exception(e)  # 显示详细异常堆栈
