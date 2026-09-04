import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import html


# ============================================================
# CREDIT CARD CUSTOMER INTELLIGENCE
# EXECUTIVE ANALYTICS DASHBOARD
#
# Architecture:
# HTML + CSS dashboard
# Individual Plotly charts embedded inside cards
# ============================================================


# ============================================================
# 1. LOAD DATA
# ============================================================

df = pd.read_csv("data/executive_dashboard_data.csv")


# ============================================================
# 2. DESIGN SYSTEM
# ============================================================

NAVY = "#17365D"
NAVY_LIGHT = "#284F78"

SLATE = "#667085"
DARK = "#1D2939"

LIGHT_BG = "#F5F7FA"
LIGHT_BLUE = "#EAF1F8"

BORDER = "#E4E7EC"
GRID = "#EAECF0"

RED = "#B42318"
RED_LIGHT = "#FDECEC"

WHITE = "#FFFFFF"

FONT = "Arial, Helvetica, sans-serif"


# ============================================================
# 3. PORTFOLIO KPIs
# ============================================================

total_customers = len(df)

avg_churn = (
    df["Churn_Probability"].mean() * 100
)

high_risk_customers = (
    df["Risk_Category"] == "High Risk"
).sum()

historical_attrition = (
    df["Attrition"].mean() * 100
)


# ============================================================
# 4. RISK SUMMARY
# ============================================================

risk_order = [
    "Low Risk",
    "Medium Risk",
    "High Risk"
]

risk_summary = (
    df.groupby("Risk_Category")
    .agg(
        Customers=("CLIENTNUM", "count"),
        Avg_Churn=("Churn_Probability", "mean"),
        Actual_Attrition=("Attrition", "mean")
    )
    .reindex(risk_order)
    .reset_index()
)


# ============================================================
# 5. SEGMENT SUMMARY
# ============================================================

segment_summary = (
    df.groupby("Customer_Segment")
    .agg(
        Customers=("CLIENTNUM", "count"),
        Avg_Churn=("Churn_Probability", "mean"),
        Actual_Attrition=("Attrition", "mean")
    )
    .reset_index()
)


# ============================================================
# 6. ENGAGEMENT SUMMARY
# ============================================================

engagement_summary = (
    df.groupby("Engagement_Category")
    .agg(
        Attrition_Rate=("Attrition", "mean"),
        Customers=("CLIENTNUM", "count")
    )
    .reset_index()
)

engagement_summary["sort"] = (
    engagement_summary["Engagement_Category"]
    .map({
        "Low Engagement": 1,
        "Moderately Engaged": 2,
        "Highly Engaged": 3
    })
)

engagement_summary = (
    engagement_summary
    .sort_values("sort")
)


# ============================================================
# 7. INACTIVITY SUMMARY
# ============================================================

inactivity_summary = (
    df.groupby("Months_Inactive_12_mon")
    .agg(
        Attrition_Rate=("Attrition", "mean"),
        Customers=("CLIENTNUM", "count")
    )
    .reset_index()
)


# ============================================================
# 8. CONTACT SUMMARY
# ============================================================

contact_summary = (
    df.groupby("Contacts_Count_12_mon")
    .agg(
        Attrition_Rate=("Attrition", "mean"),
        Customers=("CLIENTNUM", "count")
    )
    .reset_index()
)


# ============================================================
# 9. HIGH-RISK SEGMENT
# ============================================================

high_risk_segment = (
    df[df["Risk_Category"] == "High Risk"]
    .groupby("Customer_Segment")
    .agg(
        Customers=("CLIENTNUM", "count"),
        Avg_Churn=("Churn_Probability", "mean"),
        Actual_Attrition=("Attrition", "mean"),
        Avg_Transaction_Count=("Total_Trans_Ct", "mean")
    )
    .reset_index()
)


# ============================================================
# 10. HELPER: BASE CHART STYLE
# ============================================================

def base_layout(fig, height=300):

    fig.update_layout(

        height=height,

        margin=dict(
            l=55,
            r=25,
            t=15,
            b=50
        ),

        paper_bgcolor=WHITE,

        plot_bgcolor=WHITE,

        font=dict(
            family=FONT,
            color=DARK
        ),

        showlegend=False,

        hoverlabel=dict(
            font=dict(
                family=FONT,
                size=12
            )
        )
    )

    fig.update_xaxes(

        tickfont=dict(
            family=FONT,
            size=10,
            color=SLATE
        ),

        title_font=dict(
            family=FONT,
            size=10,
            color=SLATE
        ),

        showgrid=False,

        zeroline=False
    )

    fig.update_yaxes(

        tickfont=dict(
            family=FONT,
            size=10,
            color=SLATE
        ),

        title_font=dict(
            family=FONT,
            size=10,
            color=SLATE
        ),

        gridcolor=GRID,

        zeroline=False
    )

    return fig


# ============================================================
# 11. CHART 1 — RISK DISTRIBUTION
# ============================================================

risk_fig = go.Figure()

risk_fig.add_trace(

    go.Bar(

        x=risk_summary["Customers"],

        y=risk_summary["Risk_Category"],

        orientation="h",

        marker=dict(
            color=NAVY
        ),

        text=risk_summary["Customers"],

        texttemplate="%{text:,}",

        textposition="outside",

        hovertemplate=
        "<b>%{y}</b><br>"
        "Customers: %{x:,}"
        "<extra></extra>"
    )
)

risk_fig.update_xaxes(
    title="Customers",
    gridcolor=GRID
)

risk_fig.update_yaxes(
    categoryorder="array",
    categoryarray=risk_order
)

risk_fig = base_layout(
    risk_fig,
    280
)


# ============================================================
# 12. CHART 2 — CUSTOMER SEGMENT MIX
# ============================================================

segment_fig = go.Figure()

segment_fig.add_trace(

    go.Pie(

        labels=segment_summary["Customer_Segment"],

        values=segment_summary["Customers"],

        hole=0.68,

        textinfo="label+percent",

        textfont=dict(
            family=FONT,
            size=11,
            color=DARK
        ),

        marker=dict(

            colors=[
                NAVY,
                "#98A2B3"
            ],

            line=dict(
                color=WHITE,
                width=3
            )
        ),

        hovertemplate=
        "<b>%{label}</b><br>"
        "Customers: %{value:,}<br>"
        "Share: %{percent}"
        "<extra></extra>"
    )
)

segment_fig.update_layout(

    height=280,

    margin=dict(
        l=20,
        r=20,
        t=5,
        b=10
    ),

    paper_bgcolor=WHITE,

    plot_bgcolor=WHITE,

    font=dict(
        family=FONT
    ),

    showlegend=True,

    legend=dict(
        orientation="v",
        x=0.82,
        y=0.5,
        font=dict(
            family=FONT,
            size=10,
            color=SLATE
        )
    )
)


# ============================================================
# 13. CHART 3 — ENGAGEMENT & ATTRITION
# ============================================================

engagement_fig = go.Figure()

engagement_fig.add_trace(

    go.Scatter(

        x=engagement_summary["Engagement_Category"],

        y=engagement_summary["Attrition_Rate"] * 100,

        mode="lines+markers",

        line=dict(
            color=NAVY,
            width=3
        ),

        marker=dict(
            color=WHITE,
            size=9,
            line=dict(
                color=NAVY,
                width=3
            )
        ),

        hovertemplate=
        "<b>%{x}</b><br>"
        "Attrition: %{y:.1f}%"
        "<extra></extra>"
    )
)

engagement_fig.update_xaxes(
    title="Engagement Level"
)

engagement_fig.update_yaxes(
    title="Attrition (%)",
    gridcolor=GRID
)

engagement_fig = base_layout(
    engagement_fig,
    285
)


# ============================================================
# 14. CHART 4 — MODEL RISK PROFILE
# ============================================================

risk_profile_fig = go.Figure()

risk_profile_fig.add_trace(

    go.Scatter(

        x=risk_summary["Risk_Category"],

        y=risk_summary["Avg_Churn"] * 100,

        mode="lines+markers",

        line=dict(
            color=NAVY,
            width=3
        ),

        marker=dict(
            color=NAVY,
            size=9
        ),

        hovertemplate=
        "<b>%{x}</b><br>"
        "Predicted Churn: %{y:.1f}%"
        "<extra></extra>"
    )
)

risk_profile_fig.update_xaxes(
    title="Risk Category"
)

risk_profile_fig.update_yaxes(
    title="Predicted Churn (%)",
    gridcolor=GRID
)

risk_profile_fig = base_layout(
    risk_profile_fig,
    285
)


# ============================================================
# 15. CHART 5 — INACTIVITY & ATTRITION
# ============================================================

inactivity_fig = go.Figure()

inactivity_fig.add_trace(

    go.Scatter(

        x=inactivity_summary[
            "Months_Inactive_12_mon"
        ],

        y=inactivity_summary[
            "Attrition_Rate"
        ] * 100,

        mode="lines+markers",

        line=dict(
            color=NAVY,
            width=3
        ),

        marker=dict(
            color=NAVY,
            size=8
        ),

        hovertemplate=
        "<b>%{x} Months Inactive</b><br>"
        "Attrition: %{y:.1f}%"
        "<extra></extra>"
    )
)

inactivity_fig.update_xaxes(
    title="Months Inactive (Last 12 Months)"
)

inactivity_fig.update_yaxes(
    title="Attrition (%)",
    gridcolor=GRID
)

inactivity_fig = base_layout(
    inactivity_fig,
    285
)


# ============================================================
# 16. CHART 6 — CONTACT FREQUENCY
# ============================================================

contact_fig = go.Figure()

contact_fig.add_trace(

    go.Scatter(

        x=contact_summary[
            "Contacts_Count_12_mon"
        ],

        y=contact_summary[
            "Attrition_Rate"
        ] * 100,

        mode="lines+markers",

        line=dict(
            color=NAVY,
            width=3
        ),

        marker=dict(
            color=NAVY,
            size=8
        ),

        hovertemplate=
        "<b>%{x} Contacts</b><br>"
        "Attrition: %{y:.1f}%"
        "<extra></extra>"
    )
)

contact_fig.update_xaxes(
    title="Contacts in Last 12 Months"
)

contact_fig.update_yaxes(
    title="Attrition (%)",
    gridcolor=GRID
)

contact_fig = base_layout(
    contact_fig,
    285
)


# ============================================================
# 17. CHART 7 — HIGH-RISK CUSTOMERS
# ============================================================

high_risk_count_fig = go.Figure()

high_risk_count_fig.add_trace(

    go.Bar(

        x=high_risk_segment[
            "Customer_Segment"
        ],

        y=high_risk_segment[
            "Customers"
        ],

        marker=dict(
            color=NAVY
        ),

        text=high_risk_segment[
            "Customers"
        ],

        texttemplate="%{text:,}",

        textposition="outside",

        hovertemplate=
        "<b>%{x}</b><br>"
        "High-Risk Customers: %{y:,}"
        "<extra></extra>"
    )
)

high_risk_count_fig.update_xaxes(
    title="Customer Segment"
)

high_risk_count_fig.update_yaxes(
    title="Customers",
    gridcolor=GRID
)

high_risk_count_fig = base_layout(
    high_risk_count_fig,
    285
)


# ============================================================
# 18. CHART 8 — HIGH-RISK CHURN
# ============================================================

high_risk_churn_fig = go.Figure()

high_risk_churn_fig.add_trace(

    go.Bar(

        x=high_risk_segment[
            "Customer_Segment"
        ],

        y=high_risk_segment[
            "Avg_Churn"
        ] * 100,

        marker=dict(
            color=RED
        ),

        text=(
            high_risk_segment[
                "Avg_Churn"
            ] * 100
        ).round(1),

        texttemplate="%{text}%",

        textposition="outside",

        hovertemplate=
        "<b>%{x}</b><br>"
        "Predicted Churn: %{y:.1f}%"
        "<extra></extra>"
    )
)

high_risk_churn_fig.update_xaxes(
    title="Customer Segment"
)

high_risk_churn_fig.update_yaxes(
    title="Predicted Churn (%)",
    gridcolor=GRID
)

high_risk_churn_fig = base_layout(
    high_risk_churn_fig,
    285
)


# ============================================================
# 19. CONVERT PLOTLY FIGURES TO HTML
# ============================================================

def chart_html(fig, include_js=False):

    return pio.to_html(

        fig,

        full_html=False,

        include_plotlyjs=(
            True if include_js else False
        ),

        config={
            "displayModeBar": True,
            "responsive": True
        }
    )


risk_html = chart_html(
    risk_fig,
    True
)

segment_html = chart_html(
    segment_fig
)

engagement_html = chart_html(
    engagement_fig
)

risk_profile_html = chart_html(
    risk_profile_fig
)

inactivity_html = chart_html(
    inactivity_fig
)

contact_html = chart_html(
    contact_fig
)

high_risk_count_html = chart_html(
    high_risk_count_fig
)

high_risk_churn_html = chart_html(
    high_risk_churn_fig
)


# ============================================================
# 20. HIGH-RISK TABLE
# ============================================================

table_rows = ""

for _, row in high_risk_segment.iterrows():

    table_rows += f"""
    <tr>

        <td>
            {html.escape(str(row["Customer_Segment"]))}
        </td>

        <td>
            {int(row["Customers"]):,}
        </td>

        <td>
            {row["Avg_Churn"] * 100:.1f}%
        </td>

        <td>
            {row["Actual_Attrition"] * 100:.1f}%
        </td>

        <td>
            {row["Avg_Transaction_Count"]:.1f}
        </td>

    </tr>
    """


# ============================================================
# 21. HTML DASHBOARD
# ============================================================

dashboard_html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>
Credit Card Customer Intelligence
</title>


<style>


/* =========================================================
   GLOBAL
   ========================================================= */

* {{
    box-sizing: border-box;
}}

body {{

    margin: 0;

    background: {LIGHT_BG};

    font-family: {FONT};

    color: {DARK};
}}


/* =========================================================
   DASHBOARD CONTAINER
   ========================================================= */

.dashboard {{

    max-width: 1450px;

    margin: 0 auto;

    padding-bottom: 45px;
}}


/* =========================================================
   HEADER
   ========================================================= */

.header {{

    background: {NAVY};

    color: {WHITE};

    padding: 28px 38px;

    display: flex;

    justify-content: space-between;

    align-items: center;

    min-height: 125px;

    box-shadow:
        0 2px 8px rgba(0,0,0,0.10);
}}

.header-left h1 {{

    margin: 0;

    font-size: 29px;

    font-weight: 700;

    letter-spacing: -0.5px;
}}

.header-left p {{

    margin: 7px 0 0 0;

    font-size: 15px;

    opacity: 0.88;
}}

.header-right {{

    text-align: right;

    padding-left: 35px;

    border-left:
        1px solid rgba(255,255,255,0.35);
}}

.header-right .title {{

    font-size: 11px;

    font-weight: 700;

    letter-spacing: 0.8px;
}}

.header-right .subtitle {{

    margin-top: 7px;

    font-size: 10px;

    letter-spacing: 1.1px;

    opacity: 0.85;
}}


/* =========================================================
   MAIN CONTENT
   ========================================================= */

.content {{

    padding: 22px 24px 0 24px;
}}


/* =========================================================
   KPI GRID
   ========================================================= */

.kpi-grid {{

    display: grid;

    grid-template-columns:
        repeat(4, 1fr);

    gap: 16px;

    margin-bottom: 18px;
}}

.kpi-card {{

    background: {WHITE};

    border: 1px solid {BORDER};

    border-radius: 8px;

    min-height: 125px;

    padding: 20px 22px;

    box-shadow:
        0 2px 5px rgba(16,24,40,0.05);

    position: relative;
}}

.kpi-card::before {{

    content: "";

    position: absolute;

    left: 0;

    top: 0;

    bottom: 0;

    width: 4px;

    background: {NAVY};

    border-radius:
        8px 0 0 8px;
}}

.kpi-card.risk::before {{

    background: {RED};
}}

.kpi-title {{

    color: {SLATE};

    font-size: 10px;

    font-weight: 700;

    letter-spacing: 0.4px;

    margin-bottom: 9px;
}}

.kpi-value {{

    color: {NAVY};

    font-size: 28px;

    font-weight: 700;

    line-height: 1.1;
}}

.kpi-card.risk .kpi-value {{

    color: {RED};
}}

.kpi-subtitle {{

    color: {SLATE};

    font-size: 10px;

    margin-top: 8px;
}}


/* =========================================================
   SECTION GRID
   ========================================================= */

.chart-grid {{

    display: grid;

    grid-template-columns:
        repeat(2, minmax(0, 1fr));

    gap: 16px;

    margin-bottom: 16px;
}}


/* =========================================================
   CHART CARDS
   ========================================================= */

.chart-card {{

    background: {WHITE};

    border: 1px solid {BORDER};

    border-radius: 8px;

    box-shadow:
        0 2px 5px rgba(16,24,40,0.05);

    overflow: hidden;

    min-width: 0;
}}

.chart-header {{

    padding: 17px 18px 0 18px;
}}

.chart-title {{

    color: {NAVY};

    font-size: 15px;

    font-weight: 700;

    margin: 0;
}}

.chart-description {{

    color: {SLATE};

    font-size: 10px;

    margin-top: 4px;
}}

.chart-body {{

    padding: 0 8px 5px 8px;

    min-height: 295px;
}}


/* =========================================================
   TABLE CARD
   ========================================================= */

.table-card {{

    background: {WHITE};

    border: 1px solid {BORDER};

    border-radius: 8px;

    box-shadow:
        0 2px 5px rgba(16,24,40,0.05);

    margin-bottom: 16px;

    overflow: hidden;
}}

.table-header {{

    padding: 17px 18px 12px 18px;
}}

.table-title {{

    color: {NAVY};

    font-size: 15px;

    font-weight: 700;
}}

.table-description {{

    color: {SLATE};

    font-size: 10px;

    margin-top: 4px;
}}

table {{

    width: 100%;

    border-collapse: collapse;

    font-size: 12px;
}}

thead th {{

    background: {LIGHT_BLUE};

    color: {NAVY};

    font-weight: 700;

    padding: 12px 15px;

    border-bottom:
        1px solid {BORDER};

    text-align: center;
}}

tbody td {{

    padding: 12px 15px;

    border-bottom:
        1px solid {BORDER};

    text-align: center;

    color: {DARK};
}}

tbody tr:last-child td {{

    border-bottom: none;
}}

tbody td:first-child {{

    font-weight: 600;

    text-align: left;
}}


/* =========================================================
   MANAGEMENT TAKEAWAY
   ========================================================= */

.takeaway {{

    background: {LIGHT_BLUE};

    border: 1px solid #C9DDF0;

    border-radius: 8px;

    padding: 18px 22px;

    display: flex;

    align-items: center;

    gap: 18px;
}}

.takeaway-icon {{

    width: 42px;

    height: 42px;

    min-width: 42px;

    border-radius: 50%;

    background: {WHITE};

    display: flex;

    align-items: center;

    justify-content: center;

    color: {NAVY};

    font-size: 21px;

    border: 1px solid #C9DDF0;
}}

.takeaway-content h3 {{

    margin: 0;

    color: {NAVY};

    font-size: 13px;

    letter-spacing: 0.3px;
}}

.takeaway-content p {{

    margin: 5px 0 0 0;

    color: {NAVY_LIGHT};

    font-size: 11px;

    line-height: 1.5;
}}


/* =========================================================
   FOOTER
   ========================================================= */

.footer {{

    text-align: center;

    color: {SLATE};

    font-size: 9px;

    padding-top: 15px;
}}


/* =========================================================
   RESPONSIVE
   ========================================================= */

@media (max-width: 950px) {{

    .kpi-grid {{

        grid-template-columns:
            repeat(2, 1fr);
    }}

    .chart-grid {{

        grid-template-columns: 1fr;
    }}

    .header {{

        flex-direction: column;

        align-items: flex-start;

        gap: 18px;
    }}

    .header-right {{

        text-align: left;

        border-left: none;

        border-top:
            1px solid rgba(255,255,255,0.35);

        padding-left: 0;

        padding-top: 12px;
    }}
}}


@media (max-width: 600px) {{

    .kpi-grid {{

        grid-template-columns: 1fr;
    }}

    .content {{

        padding: 14px;
    }}

    .header {{

        padding: 22px;
    }}

    .header-left h1 {{

        font-size: 23px;
    }}

}}


</style>

</head>


<body>


<div class="dashboard">


    <!-- =====================================================
         HEADER
         ===================================================== -->

    <div class="header">

        <div class="header-left">

            <h1>
                Credit Card Customer Intelligence
            </h1>

            <p>
                Portfolio Risk &amp; Churn Analytics
            </p>

        </div>


        <div class="header-right">

            <div class="title">
                CUSTOMER ANALYTICS
            </div>

            <div class="subtitle">
                RISK &nbsp;|&nbsp; INSIGHTS &nbsp;|&nbsp; ACTION
            </div>

        </div>

    </div>


    <div class="content">


        <!-- =================================================
             KPI CARDS
             ================================================= -->

        <div class="kpi-grid">


            <div class="kpi-card">

                <div class="kpi-title">
                    CUSTOMERS ANALYZED
                </div>

                <div class="kpi-value">
                    {total_customers:,}
                </div>

                <div class="kpi-subtitle">
                    Total customer base
                </div>

            </div>


            <div class="kpi-card">

                <div class="kpi-title">
                    AVG. PREDICTED CHURN
                </div>

                <div class="kpi-value">
                    {avg_churn:.1f}%
                </div>

                <div class="kpi-subtitle">
                    Model predicted probability
                </div>

            </div>


            <div class="kpi-card risk">

                <div class="kpi-title">
                    HIGH-RISK CUSTOMERS
                </div>

                <div class="kpi-value">
                    {high_risk_customers:,}
                </div>

                <div class="kpi-subtitle">
                    {high_risk_customers / total_customers * 100:.1f}% of total customers
                </div>

            </div>


            <div class="kpi-card">

                <div class="kpi-title">
                    HISTORICAL ATTRITION
                </div>

                <div class="kpi-value">
                    {historical_attrition:.1f}%
                </div>

                <div class="kpi-subtitle">
                    Actual attrition rate
                </div>

            </div>


        </div>


        <!-- =================================================
             ROW 1
             ================================================= -->

        <div class="chart-grid">


            <div class="chart-card">

                <div class="chart-header">

                    <div class="chart-title">
                        Risk Distribution
                    </div>

                    <div class="chart-description">
                        Number of customers by risk category
                    </div>

                </div>

                <div class="chart-body">

                    {risk_html}

                </div>

            </div>


            <div class="chart-card">

                <div class="chart-header">

                    <div class="chart-title">
                        Customer Segment Mix
                    </div>

                    <div class="chart-description">
                        Share of customers by segment
                    </div>

                </div>

                <div class="chart-body">

                    {segment_html}

                </div>

            </div>


        </div>


        <!-- =================================================
             ROW 2
             ================================================= -->

        <div class="chart-grid">


            <div class="chart-card">

                <div class="chart-header">

                    <div class="chart-title">
                        Engagement &amp; Attrition
                    </div>

                    <div class="chart-description">
                        Actual attrition rate by engagement level
                    </div>

                </div>

                <div class="chart-body">

                    {engagement_html}

                </div>

            </div>


            <div class="chart-card">

                <div class="chart-header">

                    <div class="chart-title">
                        Model Risk Profile
                    </div>

                    <div class="chart-description">
                        Predicted churn probability by risk category
                    </div>

                </div>

                <div class="chart-body">

                    {risk_profile_html}

                </div>

            </div>


        </div>


        <!-- =================================================
             ROW 3
             ================================================= -->

        <div class="chart-grid">


            <div class="chart-card">

                <div class="chart-header">

                    <div class="chart-title">
                        Inactivity &amp; Attrition
                    </div>

                    <div class="chart-description">
                        Actual attrition rate by months inactive
                    </div>

                </div>

                <div class="chart-body">

                    {inactivity_html}

                </div>

            </div>


            <div class="chart-card">

                <div class="chart-header">

                    <div class="chart-title">
                        Contact Frequency &amp; Attrition
                    </div>

                    <div class="chart-description">
                        Actual attrition rate by number of contacts
                    </div>

                </div>

                <div class="chart-body">

                    {contact_html}

                </div>

            </div>


        </div>


        <!-- =================================================
             ROW 4
             ================================================= -->

        <div class="chart-grid">


            <div class="chart-card">

                <div class="chart-header">

                    <div class="chart-title">
                        High-Risk Customers
                    </div>

                    <div class="chart-description">
                        High-risk customers by segment
                    </div>

                </div>

                <div class="chart-body">

                    {high_risk_count_html}

                </div>

            </div>


            <div class="chart-card">

                <div class="chart-header">

                    <div class="chart-title">
                        High-Risk Churn
                    </div>

                    <div class="chart-description">
                        Predicted churn probability for high-risk customers
                    </div>

                </div>

                <div class="chart-body">

                    {high_risk_churn_html}

                </div>

            </div>


        </div>


        <!-- =================================================
             TABLE
             ================================================= -->

        <div class="table-card">


            <div class="table-header">

                <div class="table-title">
                    High-Risk Portfolio Details
                </div>

                <div class="table-description">
                    Key metrics for high-risk customers by segment
                </div>

            </div>


            <table>

                <thead>

                    <tr>

                        <th>
                            Customer Segment
                        </th>

                        <th>
                            High-Risk Customers
                        </th>

                        <th>
                            Predicted Churn
                        </th>

                        <th>
                            Actual Attrition
                        </th>

                        <th>
                            Avg. Transactions
                        </th>

                    </tr>

                </thead>


                <tbody>

                    {table_rows}

                </tbody>

            </table>


        </div>


        <!-- =================================================
             MANAGEMENT TAKEAWAY
             ================================================= -->

        <div class="takeaway">


            <div class="takeaway-icon">
                ✓
            </div>


            <div class="takeaway-content">

                <h3>
                    MANAGEMENT TAKEAWAY
                </h3>

                <p>
                    Low transaction engagement is strongly associated
                    with higher attrition. High-risk customers represent
                    the clearest retention priority.
                </p>

            </div>


        </div>


        <div class="footer">

            Credit Card Customer Intelligence &nbsp;•&nbsp;
            SQL &nbsp;•&nbsp;
            Statistical Testing &nbsp;•&nbsp;
            Customer Segmentation &nbsp;•&nbsp;
            Logistic Regression

        </div>


    </div>

</div>


</body>

</html>
"""


# ============================================================
# 22. WRITE FILE
# ============================================================

output_path = (
    "dashboard/executive_dashboard.html"
)

with open(
    output_path,
    "w",
    encoding="utf-8"
) as f:

    f.write(dashboard_html)


print()
print("================================================")
print("CREDIT CARD CUSTOMER INTELLIGENCE")
print("================================================")
print("Dashboard created successfully:")
print(output_path)
print("================================================")
print()