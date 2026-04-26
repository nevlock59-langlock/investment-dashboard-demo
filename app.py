from pathlib import Path
from html import escape

import pandas as pd
import streamlit as st
import altair as alt
import re
from datetime import date, datetime

st.set_page_config(
    page_title="함수철의 데모공장",
    page_icon="🐹",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 3.5rem;
        padding-bottom: 2rem;
    }

    .app-title {
        font-size: 1.05rem;
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: 0.15rem;
    }
    
    .upload-header {
        font-size: 0.78rem;
        color: #6b7280;
        font-weight: 600;
        line-height: 1;
        margin-bottom: 6px;
    }

    [data-testid="stFileUploader"] {
        margin-top: 0rem;
    }

    [data-testid="stFileUploaderDropzone"] {
        min-height: 78px;
        padding: 0.85rem 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        box-sizing: border-box;
    }

    .upload-file-name {
        margin-top: -0.75rem;
        padding-left: 0.15rem;
        font-size: 0.78rem;
        color: #6b7280;
        line-height: 1.2;
        height: 18px;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
    }

    .insight-wrap {
        display: flex;
        flex-direction: column;
        gap: 6px;
        padding-bottom: 0.35rem;
    }

    .insight-header {
        grid-column: 1 / -1;
        font-size: 0.78rem;
        color: #6b7280;
        font-weight: 600;
        line-height: 1;
    }

    .insight-card {
        min-height: 58px;
        padding: 0.55rem 0.75rem;
        border: 1px solid #BFE8D2;
        border-left: 4px solid #009845;
        border-radius: 0.55rem;
        background-color: #EEF8F3;
        overflow: hidden;
        box-sizing: border-box;
        color: #374151;

        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: flex-start;
    }

    .insight-card-caption {
        font-size: 0.72rem;
        color: #007A38;
        font-weight: 700;
        line-height: 1.1;
        margin-bottom: 0.25rem;
        white-space: nowrap;
    }

    .insight-card-value {
        font-size: 0.98rem;
        color: #102A1F;
        font-weight: 600;
        line-height: 1.25;
        text-align: left;
        overflow: hidden;
        word-break: keep-all;
    }
    
    [data-testid="stExpander"] [data-testid="stMarkdownContainer"] {
        font-size: 0.78rem;
        line-height: 1.45;
        color: #4b5563;
    }

    [data-testid="stExpander"] h1 {
        font-size: 1rem;
    }

    [data-testid="stExpander"] h2 {
        font-size: 0.9rem;
    }

    [data-testid="stExpander"] h3 {
        font-size: 0.84rem;
    }

    [data-testid="stExpander"] ul {
        padding-left: 1rem;
    }

    [data-testid="stExpander"] li {
        margin-bottom: 0.15rem;
    }

    .section-gap {
        height: 1.25rem;
    }

    .insight-wrap.no-header {
        height: auto;
        grid-template-columns: 1fr 1fr;
        padding-bottom: 0.35rem;
    }

    .rank-title,
    .section-title {
        font-size: 1.05rem;
        font-weight: 700;
        line-height: 1.2;
        margin-top: -0.35rem;
        margin-bottom: 0.45rem;
    }

    .section-title-left {
        font-size: 1.05rem;
        font-weight: 700;
        line-height: 1.2;
        margin-top: 0.7rem;
        margin-bottom: 0.45rem;
    }

    .section-title-after-upload {
        font-size: 1.05rem;
        font-weight: 700;
        line-height: 1.2;
        margin-top: 1rem;
        margin-bottom: 0.45rem;
    }

    .section-title-tight {
        font-size: 1.05rem;
        font-weight: 700;
        line-height: 1.2;
        margin-top: -0.9rem;
        margin-bottom: 0.45rem;
    }

    .raw-page-nav {
        margin-top: -0.1rem;
    }

    .page-nav-text {
        text-align: center;
        font-size: 0.9rem;
        font-weight: 100;
        color: #4b5563;
        line-height: 2rem;
        white-space: nowrap;
    }

    /* 원본 데이터 페이지네이션 버튼 압축 */
    [data-testid="stButton"] button {
        min-height: 1.75rem;
        height: 2rem;
        padding: 0.1rem 0.1rem;
        font-size: 0.82rem;
        line-height: 0.75;
    }

    /* 상품 선택 버튼 compact */
    .asset-count-caption {
        font-size: 0.78rem;
        color: #6b7280;
        line-height: 1.2;
        margin-top: 0.15rem;
    }

    /* Expander 제목: Skills.md 보기 */
    [data-testid="stExpander"] details summary,
    [data-testid="stExpander"] details summary p,
    [data-testid="stExpander"] details summary [data-testid="stMarkdownContainer"] {
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        color: #374151 !important;
        line-height: 1.25 !important;
    }

    /* 대상기간 입력칸 */
    [data-testid="stTextInput"] input {
        background-color: #ffffff !important;
        border: 1px solid #BFE8D2 !important;
        border-radius: 0.5rem !important;
        color: #102A1F !important;
        font-size: 0.82rem !important;
        height: 2rem !important;
        padding: 0.25rem 0.55rem !important;
    }

    /* 대상기간 입력칸 focus */
    [data-testid="stTextInput"] input:focus {
        border-color: #009845 !important;
        box-shadow: 0 0 0 1px #009845 !important;
    }

    /* 시작일/종료일 라벨 */
    [data-testid="stTextInput"] label {
        color: #6b7280 !important;
        font-size: 0.76rem !important;
        font-weight: 600 !important;
    }

    .category-badge {
        display: inline-block;
        padding: 0.12rem 0.42rem;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 450;
        line-height: 1.2;
        margin-right: 0.35rem;
    }

    .category-equity {
        background-color: #EEF8F3;
        color: #007A38;
        border: 1px solid #BFE8D2;
    }

    .category-commodity {
        background-color: #FFF7D6;
        color: #8A5A00;
        border: 1px solid #F2D16B;
    }

    .category-bond {
        background-color: #F1ECFF;
        color: #5B3FA3;
        border: 1px solid #CFC2FF;
    }

    .category-currency {
        background-color: #EAF4FF;
        color: #1D5F99;
        border: 1px solid #B9DCF8;
    }

    .category-default {
        background-color: #F3F4F6;
        color: #4B5563;
        border: 1px solid #D1D5DB;
    }

    .recent-table-wrap {
        width: 100%;
        overflow-x: auto;
    }

    /* 모바일에서 date_input 2개가 들어간 columns만 한 줄 유지 */
    @media (max-width: 640px) {
        div[data-testid="stHorizontalBlock"]:has(div[data-testid="stDateInput"]) {
            flex-wrap: nowrap !important;
            gap: 0.35rem !important;
        }

        div[data-testid="stHorizontalBlock"]:has(div[data-testid="stDateInput"]) 
        > div[data-testid="column"] {
            min-width: 0 !important;
            flex: 1 1 0 !important;
        }

        div[data-testid="stDateInput"] input {
            font-size: 0.78rem !important;
            padding-left: 0.35rem !important;
            padding-right: 0.35rem !important;
        }

        div[data-testid="stDateInput"] label {
            font-size: 0.78rem !important;
        }
    }

    @media (max-width: 640px) {
        /* 시작일/종료일 그룹만 2칸 grid로 고정 */
        .st-key-date_range_group div[data-testid="stHorizontalBlock"] {
            display: grid !important;
            grid-template-columns: minmax(0, 1fr) minmax(0, 1fr) !important;
            gap: 0.35rem !important;
            width: 100% !important;
        }

        .st-key-date_range_group div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
            width: 100% !important;
            min-width: 0 !important;
            max-width: 100% !important;
            flex: none !important;
        }

        .st-key-date_range_group div[data-testid="stTextInput"] {
            width: 100% !important;
            min-width: 0 !important;
        }

        .st-key-date_range_group input {
            width: 100% !important;
            min-width: 0 !important;
            font-size: 0.72rem !important;
            padding-left: 0.32rem !important;
            padding-right: 0.32rem !important;
        }

        .st-key-date_range_group label {
            font-size: 0.75rem !important;
            white-space: nowrap !important;
        }
    }
    
    @media (max-width: 640px) {
        /* 상품 선택 제목 + reset 버튼 row만 한 줄 유지 */
        .st-key-asset_title_reset_group div[data-testid="stHorizontalBlock"] {
            display: grid !important;
            grid-template-columns: minmax(0, 1fr) 2.4rem !important;
            gap: 0.35rem !important;
            width: 100% !important;
            align-items: center !important;
        }

        .st-key-asset_title_reset_group div[data-testid="stHorizontalBlock"] 
        > div[data-testid="column"] {
            width: 100% !important;
            min-width: 0 !important;
            max-width: 100% !important;
            flex: none !important;
        }

        .st-key-asset_title_reset_group .section-title-left {
            white-space: nowrap !important;
            margin-bottom: 0 !important;
        }

        .st-key-asset_title_reset_group .stButton button {
            width: 100% !important;
            min-width: 0 !important;
            height: 2rem !important;
            min-height: 2rem !important;
            padding: 0 !important;
            font-size: 0.9rem !important;
        }
    }
    
    </style>
    """,
    unsafe_allow_html=True,
)


def load_skills_text() -> str:
    skills_path = Path("Skills.md")

    if not skills_path.exists():
        return "Skills.md 파일이 없습니다."

    return skills_path.read_text(encoding="utf-8")


def load_data(uploaded_file):
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file)

    return pd.read_csv("sample_data.csv")


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    required_columns = ["date", "asset_name", "price", "volume", "category"]

    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(f"필수 컬럼이 없습니다: {missing_columns}")

    result = df.copy()

    result["date"] = pd.to_datetime(result["date"])
    result["price"] = pd.to_numeric(result["price"], errors="coerce")
    result["volume"] = pd.to_numeric(result["volume"], errors="coerce")

    result = result.dropna(subset=["date", "asset_name", "price"])
    result = result.sort_values(["asset_name", "date"])

    return result


def calculate_metrics(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()

    result["daily_return"] = result.groupby("asset_name")["price"].pct_change()
    result["base_price"] = result.groupby("asset_name")["price"].transform("first")
    result["cumulative_return"] = result["price"] / result["base_price"] - 1
    result["trading_value"] = result["price"] * result["volume"]

    return result


def summarize_by_asset(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby("asset_name")
        .agg(
            category=("category", "first"),
            first_price=("price", "first"),
            last_price=("price", "last"),
            cumulative_return=("cumulative_return", "last"),
            recent_return=("daily_return", "last"),
            volatility=("daily_return", "std"),
            total_volume=("volume", "sum"),
            total_trading_value=("trading_value", "sum"),
        )
        .reset_index()
    )

    summary["cumulative_return_pct"] = summary["cumulative_return"] * 100
    summary["recent_return_pct"] = summary["recent_return"] * 100
    summary["volatility_pct"] = summary["volatility"] * 100

    return summary


def make_ranked_table(
    summary: pd.DataFrame,
    sort_column: str,
    ascending: bool = False,
) -> pd.DataFrame:
    ranked = summary.sort_values(sort_column, ascending=ascending).copy()
    ranked.insert(0, "rank", range(1, len(ranked) + 1))

    return ranked


def format_number(value: float) -> str:
    if pd.isna(value):
        return "-"

    if abs(value) >= 100_000_000:
        return f"{value / 100_000_000:.1f}억"
    if abs(value) >= 10_000:
        return f"{value / 10_000:.1f}만"

    return f"{value:,.0f}"


def format_percent(value: float) -> str:
    if pd.isna(value):
        return "-"

    return f"{value:.2f}%"


def make_ranked_table(
    summary: pd.DataFrame,
    sort_column: str,
    ascending: bool = False,
) -> pd.DataFrame:
    ranked = summary.sort_values(sort_column, ascending=ascending).copy()
    ranked.insert(0, "rank", range(1, len(ranked) + 1))

    return ranked


def show_rank_cards(
    ranked: pd.DataFrame,
    metric_column: str,
    metric_label: str,
    metric_type: str = "number",
    top_n: int = 6,
):
    display_df = ranked.head(top_n).reset_index(drop=True)

    for _, row in display_df.iterrows():
        if metric_type == "percent":
            metric_value = format_percent(row[metric_column])
        else:
            metric_value = format_number(row[metric_column])

        with st.container(border=True):
            st.markdown(
                f"**{int(row['rank'])}위 · {row['asset_name']}**"
            )

            category_label = format_category(row["category"])
            category_class = get_category_class(row["category"])

            st.markdown(
                f"""
                <span class="category-badge {category_class}">{category_label}</span>
                <strong>{metric_label}: {metric_value}</strong>
                """,
                unsafe_allow_html=True,
            )

            st.caption(
                f"수익률 {format_percent(row['cumulative_return_pct'])} · "
                f"변동성 {format_percent(row['volatility_pct'])} · "
                f"거래량 {format_number(row['total_volume'])}"
            )


def show_ranking_tabs(summary: pd.DataFrame):
    tab_value, tab_volume, tab_up, tab_down, tab_market_cap = st.tabs(
        ["거래대금", "거래량", "상승", "하락", "시가총액"]
    )

    with tab_value:
        ranked = make_ranked_table(summary, "total_trading_value", ascending=False)
        show_rank_cards(
            ranked=ranked,
            metric_column="total_trading_value",
            metric_label="거래대금",
            metric_type="number",
        )

    with tab_volume:
        ranked = make_ranked_table(summary, "total_volume", ascending=False)
        show_rank_cards(
            ranked=ranked,
            metric_column="total_volume",
            metric_label="거래량",
            metric_type="number",
        )

    with tab_up:
        ranked = make_ranked_table(summary, "cumulative_return_pct", ascending=False)
        show_rank_cards(
            ranked=ranked,
            metric_column="cumulative_return_pct",
            metric_label="누적 수익률(%)",
            metric_type="percent",
        )

    with tab_down:
        ranked = make_ranked_table(summary, "cumulative_return_pct", ascending=True)
        show_rank_cards(
            ranked=ranked,
            metric_column="cumulative_return_pct",
            metric_label="누적 수익률",
            metric_type="percent",
        )

    with tab_market_cap:
        if "market_cap" in summary.columns:
            ranked = make_ranked_table(summary, "market_cap", ascending=False)
            show_rank_cards(
                ranked=ranked,
                metric_column="market_cap",
                metric_label="시가총액",
                metric_type="number",
            )
        else:
            st.info("시가총액 컬럼이 없어 시가총액 순위는 표시하지 않습니다.")

def make_insights(
    summary: pd.DataFrame,
    asset_count: int,
    best_return: float,
    avg_volatility: float,
) -> list[dict[str, str]]:
    top_asset = summary.sort_values("cumulative_return", ascending=False).iloc[0]
    risk_asset = summary.sort_values("volatility", ascending=False).iloc[0]

    recent_summary = summary.dropna(subset=["recent_return"])

    if recent_summary.empty:
        recent_value = "-"
    else:
        recent_top_asset = recent_summary.sort_values(
            "recent_return",
            ascending=False,
        ).iloc[0]
        recent_value = (
            f"{recent_top_asset['asset_name']} "
            f"({recent_top_asset['recent_return_pct']:.2f}%)"
        )

    return [
        {
            "caption": "누적 수익률 1위",
            "value": f"{top_asset['asset_name']} ({top_asset['cumulative_return_pct']:.2f}%)",
        },
        {
            "caption": "최고 누적 수익률",
            "value": f"{best_return:.2f}%",
        },
        {
            "caption": "변동성 1위(위험)",
            "value": f"{risk_asset['asset_name']} ({risk_asset['volatility_pct']:.2f}%)",
        },
        {
            "caption": "평균 변동성",
            "value": f"{avg_volatility:.2f}%",
        },
        {
            "caption": "최근 수익률 1위",
            "value": recent_value,
        },
    ]

def parse_flexible_date(value: str) -> date | None:
    text = str(value).strip()
    text = re.sub(r"\s+", "", text)

    if not text:
        return None

    try:
        # 20260430
        if re.fullmatch(r"\d{8}", text):
            return datetime.strptime(text, "%Y%m%d").date()

        # 2026.04.30 / 2026-04-30 / 2026/04/30
        normalized = re.sub(r"[./]", "-", text)

        if re.fullmatch(r"\d{4}-\d{1,2}-\d{1,2}", normalized):
            year_text, month_text, day_text = normalized.split("-")
            return date(
                int(year_text),
                int(month_text),
                int(day_text),
            )

    except ValueError:
        return None

    return None


def format_date(value: date) -> str:
    return value.strftime("%Y-%m-%d")


def make_safe_key(value: str) -> str:
    return re.sub(r"[^0-9a-zA-Z_]+", "_", value)


def normalize_date_input(input_key: str, min_date: date, max_date: date):
    parsed_date = parse_flexible_date(st.session_state.get(input_key, ""))

    if parsed_date is None:
        return

    if parsed_date < min_date:
        parsed_date = min_date

    if parsed_date > max_date:
        parsed_date = max_date

    st.session_state[input_key] = format_date(parsed_date)

def show_period_selector(raw_df: pd.DataFrame, source_key: str) -> pd.DataFrame:
    if "date" not in raw_df.columns:
        st.warning("date 컬럼이 없어 대상기간 선택 기능을 사용할 수 없습니다.")
        return raw_df

    result = raw_df.copy()
    result["_filter_date"] = pd.to_datetime(result["date"], errors="coerce").dt.date

    valid_dates = result["_filter_date"].dropna()

    if valid_dates.empty:
        st.warning("유효한 날짜 데이터가 없어 대상기간 선택 기능을 사용할 수 없습니다.")
        return raw_df

    min_date = valid_dates.min()
    max_date = valid_dates.max()

    safe_source_key = make_safe_key(source_key)
    start_key = f"start_date_{safe_source_key}"
    end_key = f"end_date_{safe_source_key}"

    if st.session_state.get("period_source_key") != source_key:
        st.session_state.period_source_key = source_key
        st.session_state[start_key] = format_date(min_date)
        st.session_state[end_key] = format_date(max_date)

    with st.container(key="date_range_group"):
        start_col, end_col = st.columns(2, gap="small")
    
        with start_col:
            start_text = st.text_input(
                "시작일",
                key=start_key,
                placeholder="YYYY-MM-DD",
                on_change=normalize_date_input,
                args=(start_key, min_date, max_date),
            )
    
        with end_col:
            end_text = st.text_input(
                "종료일",
                key=end_key,
                placeholder="YYYY-MM-DD",
                on_change=normalize_date_input,
                args=(end_key, min_date, max_date),
            )
    
    start_date = parse_flexible_date(start_text)
    end_date = parse_flexible_date(end_text)

    if start_date is None or end_date is None:
        st.warning("날짜는 YYYY-MM-DD, YYYYMMDD, YYYY.MM.DD 형식으로 입력해주세요.")
        return raw_df

    if start_date > end_date:
        st.warning("시작일은 종료일보다 늦을 수 없습니다.")
        return raw_df

    filtered = result[
        (result["_filter_date"] >= start_date)
        & (result["_filter_date"] <= end_date)
    ].copy()

    filtered = filtered.drop(columns=["_filter_date"])

    return filtered

def show_asset_selector(raw_df: pd.DataFrame, source_key: str) -> pd.DataFrame:
    if "asset_name" not in raw_df.columns:
        st.warning("asset_name 컬럼이 없어 상품 선택 기능을 사용할 수 없습니다.")
        return raw_df

    asset_names = sorted(raw_df["asset_name"].dropna().unique().tolist())

    if not asset_names:
        st.warning("선택 가능한 상품이 없습니다.")
        return raw_df

    if st.session_state.get("asset_source_key") != source_key:
        st.session_state.asset_source_key = source_key
        st.session_state.asset_selector = asset_names.copy()

    selected_assets = st.pills(
        "분석할 상품",
        options=asset_names,
        selection_mode="multi",
        key="asset_selector",
        label_visibility="collapsed",
    )

    if not selected_assets:
        st.caption("선택된 항목이 없어 전체 상품을 기준으로 표시합니다.")
        selected_assets = asset_names

    st.caption(f"표시된 항목: {len(selected_assets)}개 / 전체 {len(asset_names)}개")

    return raw_df[raw_df["asset_name"].isin(selected_assets)].copy()

def show_paginated_dataframe(df: pd.DataFrame, page_size: int = 10):
    total_rows = len(df)
    total_pages = max((total_rows - 1) // page_size + 1, 1)

    if "raw_data_page" not in st.session_state:
        st.session_state.raw_data_page = 1

    current_page = st.session_state.raw_data_page

    start_idx = (current_page - 1) * page_size
    end_idx = start_idx + page_size

    page_df = df.iloc[start_idx:end_idx].copy()
    page_df.insert(0, "순위", range(start_idx + 1, start_idx + len(page_df) + 1))

    if "category" in page_df.columns:
        page_df["category"] = page_df["category"].map(format_category)

    page_df = page_df.rename(
        columns={
            "date": "일자",
            "asset_name": "상품명",
            "price": "가격",
            "volume": "거래량",
            "category": "자산군",
        }
    )

    if "가격" in page_df.columns:
        page_df["가격"] = pd.to_numeric(page_df["가격"], errors="coerce").map(
            lambda value: "-" if pd.isna(value) else f"${value:,.4f}"
        )

    if "거래량" in page_df.columns:
        page_df["거래량"] = pd.to_numeric(page_df["거래량"], errors="coerce").map(
            lambda value: "-" if pd.isna(value) else f"{value:,.0f}"
        )

    render_recent_table(page_df)

    spacer_left, prev_col, page_col, next_col, spacer_right = st.columns(
        [0.6, 1, 1.6, 1, 0.6],
        gap="small",
    )

    with prev_col:
        if st.button(
            "← 이전",
            disabled=current_page <= 1,
            use_container_width=True,
        ):
            st.session_state.raw_data_page -= 1
            st.rerun()

    with page_col:
        st.markdown(
            f"""
            <div class="page-nav-text">
                {current_page} / {total_pages} · 총 {total_rows}건
            </div>
            """,
            unsafe_allow_html=True,
        )

    with next_col:
        if st.button(
            "다음 →",
            disabled=current_page >= total_pages,
            use_container_width=True,
        ):
            st.session_state.raw_data_page += 1
            st.rerun()
    

def show_insight_cards(insights: list[dict[str, str]]):
    cards_html = ""

    for insight in insights:
        caption = escape(insight["caption"])
        value = escape(insight["value"])

        # 예: "QQQ (12.34%)" → "QQQ<br>(12.34%)"
        value = value.replace(" (", "<br>(")

        cards_html += f"""
        <div class="insight-card">
            <div class="insight-card-caption">{caption}</div>
            <div class="insight-card-value">{value}</div>
        </div>
        """

    st.markdown(
        f"""
        <div class="insight-wrap">
            {cards_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

def format_category(category: str) -> str:
    category_map = {
        "Equity": "주가",
        "Commodity": "상품",
        "Bond": "채권",
        "Currency": "외환",
    }

    return category_map.get(str(category), str(category))

def get_category_cell_style(category: str) -> str:
    category_style_map = {
        "주가": "background-color: #EEF8F3; color: #007A38; font-weight: 700;",
        "상품": "background-color: #FFF7D6; color: #8A5A00; font-weight: 700;",
        "채권": "background-color: #F1ECFF; color: #5B3FA3; font-weight: 700;",
        "외환": "background-color: #EAF4FF; color: #1D5F99; font-weight: 700;",
    }

    return category_style_map.get(
        str(category),
        "background-color: #F3F4F6; color: #4B5563;",
    )

def make_recent_table_width_styles(display_df: pd.DataFrame) -> list[dict]:
    column_width_map = {
        "순위": "46px",
        "일자": "100px",
        "상품명": "190px",
        "가격": "160px",
        "거래량": "105px",
        "자산군": "70px",
    }

    styles = []

    for index, column_name in enumerate(display_df.columns):
        width = column_width_map.get(column_name, "90px")

        styles.append(
            {
                "selector": f".col{index}",
                "props": [
                    ("width", width),
                    ("min-width", width),
                    ("max-width", width),
                ],
            }
        )

    return styles

def render_recent_table(display_df: pd.DataFrame):
    table_styles = [
        {
            "selector": "table",
            "props": [
                ("width", "100%"),
                ("min-width", "680px"),
                ("border-collapse", "collapse"),
                ("font-size", "0.82rem"),
                ("table-layout", "fixed"),
            ],
        },
        {
            "selector": "th",
            "props": [
                ("text-align", "center"),
                ("font-weight", "700"),
                ("background-color", "#F8FAFC"),
                ("border-bottom", "1px solid #E5E7EB"),
                ("padding", "0.22rem 0.35rem"),
                ("line-height", "1.5"),
                ("white-space", "nowrap"),
            ],
        },
        {
            "selector": "td",
            "props": [
                ("text-align", "center"),
                ("border-bottom", "1px solid #F1F5F9"),
                ("padding", "0.18rem 0.35rem"),
                ("line-height", "1.65"),
                ("white-space", "nowrap"),
                ("overflow", "hidden"),
                ("text-overflow", "ellipsis"),
            ],
        },
    ]

    table_styles.extend(make_recent_table_width_styles(display_df))

    styled = (
        display_df.style
        .hide(axis="index")
        .map(
            get_category_cell_style,
            subset=["자산군"] if "자산군" in display_df.columns else None,
        )
        .set_table_styles(table_styles)
    )

    st.html(
        f"""
        <div class="recent-table-wrap">
            {styled.to_html()}
        </div>
        """
    )

def style_category_column(display_df: pd.DataFrame):
    category_column = None

    if "자산군" in display_df.columns:
        category_column = "자산군"
    elif "category" in display_df.columns:
        category_column = "category"

    styled = display_df.style.set_table_styles(
        [
            {
                "selector": "th",
                "props": [
                    ("text-align", "center"),
                    ("font-weight", "700"),
                ],
            }
        ]
    )

    if category_column is None:
        return styled

    return styled.map(
        get_category_cell_style,
        subset=[category_column],
    )

def get_category_class(category: str) -> str:
    category_class_map = {
        "Equity": "category-equity",
        "Commodity": "category-commodity",
        "Bond": "category-bond",
        "Currency": "category-currency",
    }

    return category_class_map.get(str(category), "category-default")
        
if __name__ == "__main__":
    metric_col, main_col, raw_col = st.columns(
        [0.95, 2.025, 2.025],
        gap="medium",
    )

    # 1. 왼쪽 단: 제목
    with metric_col:
        st.markdown(
            '<div class="app-title">🐹 함수철의 데모공장</div>',
            unsafe_allow_html=True,
        )
        st.caption("Skills.md 기반 투자 데이터 분석 대시보드")

    # 2. 오른쪽 단: 데이터 업로드
    with raw_col:
        st.markdown(
            '<div class="upload-header">데이터 업로드</div>',
            unsafe_allow_html=True,
        )

        uploaded_file = st.file_uploader(
            "투자 데이터 CSV 업로드",
            type=["csv"],
            label_visibility="collapsed",
        )

        current_file_name = uploaded_file.name if uploaded_file is not None else "sample_data.csv"

        st.markdown(
            f"""
            <div class="upload-file-name">
                현재 파일: <b>{current_file_name}</b>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 3. 전체 데이터 로드
    raw_df_all = load_data(uploaded_file)
    source_key = uploaded_file.name if uploaded_file is not None else "sample_data.csv"

    # 4. 왼쪽 단: 상품 선택 + 대상기간 선택
    with metric_col:
        with st.container(key="asset_title_reset_group"):
            asset_title_col, asset_reset_col = st.columns([0.65, 0.35], gap="small")
    
            with asset_title_col:
                st.markdown(
                    '<div class="section-title-left">상품 선택</div>',
                    unsafe_allow_html=True,
                )
    
            with asset_reset_col:
                if st.button(
                    "↻",
                    help="상품 선택 초기화",
                    use_container_width=True,
                    key="reset_asset_selection",
                ):
                    asset_names = sorted(raw_df_all["asset_name"].dropna().unique().tolist())
                    st.session_state.asset_selector = asset_names.copy()
                    st.rerun()
    
        period_df = show_period_selector(raw_df_all, source_key=source_key)
        raw_df = show_asset_selector(period_df, source_key=source_key)

    # 5. 선택된 데이터 기준 계산
    df = clean_data(raw_df)
    df = calculate_metrics(df)
    summary = summarize_by_asset(df)

    best_return = summary["cumulative_return_pct"].max()
    avg_volatility = summary["volatility_pct"].mean()
    asset_count = summary["asset_name"].nunique()

    # 6. 왼쪽 단: 투자 인사이트 + README
    with metric_col:
        st.markdown(
            '<div class="section-title-left">투자 인사이트</div>',
            unsafe_allow_html=True,
        )

        insights = make_insights(
            summary=summary,
            asset_count=asset_count,
            best_return=best_return,
            avg_volatility=avg_volatility,
        )

        show_insight_cards(insights)

        st.markdown(
            '<div class="section-title-left">분석 기준 README</div>',
            unsafe_allow_html=True,
        )

        with st.expander("Skills.md 보기"):
            st.markdown(load_skills_text())

    # 7. 가운데 단: 상품별 순위
    with main_col:
        st.markdown(
            '<div class="rank-title">상품별 순위</div>',
            unsafe_allow_html=True,
        )

        show_ranking_tabs(summary)

    # 8. 오른쪽 단: 누적 수익률 표식 차트 + 원본 데이터
    with raw_col:
        st.markdown(
            '<div class="section-title-after-upload">누적 수익률(%)</div>',
            unsafe_allow_html=True,
        )

        chart_df = summary[["asset_name", "cumulative_return_pct"]].copy()
        chart_df["zero"] = 0
        chart_df["return_label"] = chart_df["cumulative_return_pct"].map(
            lambda value: f"{value:.2f}%"
        )

        base_chart = alt.Chart(chart_df).encode(
            y=alt.Y(
                "asset_name:N",
                title=None,
                sort=alt.EncodingSortField(
                    field="cumulative_return_pct",
                    order="descending",
                ),
                axis=alt.Axis(
                    labelLimit=0,
                    labelFontSize=11,
                    labelPadding=6,
                ),
            ),
            tooltip=[
                alt.Tooltip("asset_name:N", title="상품명"),
                alt.Tooltip(
                    "cumulative_return_pct:Q",
                    title="누적 수익률(%)",
                    format=".2f",
                ),
            ],
        )

        x_axis_hidden = alt.Axis(
            title=None,
            labels=False,
            ticks=False,
            domain=False,
            grid=False,
        )

        return_rule = base_chart.mark_rule(
            strokeWidth=3,
            color="#BFE8D2",
        ).encode(
            x=alt.X(
                "zero:Q",
                title=None,
                axis=x_axis_hidden,
            ),
            x2="cumulative_return_pct:Q",
        )

        return_point = base_chart.mark_circle(
            size=95,
            color="#009845",
        ).encode(
            x=alt.X(
                "cumulative_return_pct:Q",
                title=None,
                axis=x_axis_hidden,
            ),
        )
        
        return_label = base_chart.mark_text(
            align="center",
            baseline="bottom",
            dy=-8,
            fontSize=12,
            fontWeight="bold",
            color="#102A1F",
        ).encode(
            x="cumulative_return_pct:Q",
            text="return_label:N",
        )
        
        return_chart = (
            alt.layer(
                return_rule,
                return_point,
                return_label,
            )
            .resolve_scale(x="shared")
            .properties(height=190)
        )

        st.altair_chart(return_chart, use_container_width=True)

        st.markdown(
            '<div class="section-title-tight">최근 거래내역</div>',
            unsafe_allow_html=True,
        )

        show_paginated_dataframe(raw_df, page_size=10)
