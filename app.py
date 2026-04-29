import streamlit as st

# 1. 塗料マスターデータ（データベース）
PAINT_DB = {
    "VトップH": {
        "base": 4, "hardener": 1, "vs": 50,
        "dilution": {"刷毛・ローラー": [5, 15], "エアレス": [10, 20], "カップガン": [20, 30]}
    },
    "エポニックス#20下塗り": {
        "base": 4, "hardener": 1, "vs": 55,
        "dilution": {"刷毛・ローラー": [5, 10], "エアレス": [10, 15], "カップガン": [15, 25]}
    },
    "ゼッタールOLHB": {
        "base": 9, "hardener": 1, "vs": 40,
        "dilution": {"刷毛・ローラー": [0, 5], "エアレス": [5, 10], "カップガン": [10, 15]}
    },
    "特注塗料(6:1例)": {
        "base": 6, "hardener": 1, "vs": 50,
        "dilution": {"刷毛・ローラー": [5, 10], "エアレス": [10, 15], "カップガン": [15, 25]}
    }
}

st.set_page_config(page_title="プロ塗装配合計算機", layout="centered")

st.title("🏗️ 塗装現場用・配合計算ツール")
st.caption("秤の数値（g）を入力するだけで、硬化剤とシンナー量を瞬時に算出します")

# --- 入力セクション ---
st.header("1. 条件選択")
col1, col2 = st.columns(2)

with col1:
    selected_paint = st.selectbox("塗料名を選択", list(PAINT_DB.keys()))

with col2:
    method = st.selectbox("工法を選択", ["刷毛・ローラー", "エアレス", "カップガン"])

# 選択されたデータの取得
data = PAINT_DB[selected_paint]
low_dil, high_dil = data["dilution"][method]

st.info(f"📌 **{selected_paint}** の指定配合比は **{data['base']} : {data['hardener']}** です。")

st.header("2. 計量（秤の数値を入力）")
weight_main = st.number_input("主剤の重さを入力 (g)", min_value=0, step=10, value=1000)

# --- 計算ロジック ---
# 硬化剤計算
weight_hardener = (weight_main / data["base"]) * data["hardener"]
# シンナー計算（主剤＋硬化剤の合計に対して）
total_base_hardener = weight_main + weight_hardener
thinner_low = total_base_hardener * (low_dil / 100)
thinner_high = total_base_hardener * (high_dil / 100)

# --- 結果表示セクション ---
st.header("3. 配合指示")

res_col1, res_col2 = st.columns(2)
with res_col1:
    st.metric("硬化剤の投入量", f"{weight_hardener:,.1f} g")
with res_col2:
    st.metric(f"シンナー ({method})", f"{thinner_low:,.0f} ～ {thinner_high:,.0f} g")

st.warning(f"💡 **秤の最終合計値目標:** {total_base_hardener + thinner_low:,.0f}g ～ {total_base_hardener + thinner_high:,.0f}g")

# ウェット管理等の付加情報
st.divider()
st.subheader("管理データ")
st.write(f"・**推奨工法:** {method}（希釈率: {low_dil}〜{high_dil}%）")
st.write(f"・**容積固形分:** {data['vs']}%")

