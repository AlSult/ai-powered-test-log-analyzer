import hashlib
import json
from pathlib import Path

import pandas as pd
import streamlit as st

from ai_analyzer import analyze_failure
from log_parser import parse_log_lines
from data_analyzer import (
    create_dataframe,
    analyze_tests,
    associate_errors,
)

st.set_page_config(
    page_title="AI Test Log Analyzer",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 AI-Powered Test Log Analyzer")

st.write(
    "Analyze automated test logs, identify failures, "
    "and generate AI-powered troubleshooting recommendations."
)


# Find the JSON report.
report_path = Path(__file__).parent / "reports" / "analysis.json"

# Check that the report exists.
if not report_path.exists():
    st.error("Report not found. Run python report_generator.py first.")
    st.stop()

# Read the JSON report.
with report_path.open("r", encoding="utf-8") as file:
    report = json.load(file)

# Extract the summary.
summary = report["summary"]


st.subheader("📊 Test Execution Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Tests", summary["total_tests"])

with col2:
    st.metric("Passed", summary["passed"])

with col3:
    st.metric("Failed", summary["failed"])

with col4:
    st.metric("Pass Rate", f"{summary['pass_rate']}%")


# Display a chart of passed and failed tests.
st.subheader("📈 Test Results Overview")

# Prepare the chart data.
chart_data = {
    "Test Status": ["Passed", "Failed"],
    "Number of Tests": [
        summary["passed"],
        summary["failed"]
    ]
}

# Convert the dictionary into a Pandas DataFrame.
chart_df = pd.DataFrame(chart_data)

# Display the bar chart.
st.bar_chart(
    chart_df,
    x="Test Status",
    y="Number of Tests"
)


# Display failed test details.
st.subheader("❌ Failed Test Details")

failures = report["failures"]

if not failures:
    st.success("No failed tests found!")
else:
    for failure in failures:
        test_name = failure["test_name"]
        error_message = failure.get("error") or "No error details available"

        with st.expander(f"❌ {test_name}"):
            st.write(f"**Status:** {failure['status']}")
            st.write(f"**Error:** {error_message}")

            st.divider()
            st.markdown("### 🤖 AI Analysis")

            ai_analysis = failure.get("ai_analysis")

            if ai_analysis:
                st.markdown("**Explanation**")
                st.write(ai_analysis["explanation"])

                st.markdown("**Possible Root Causes**")
                for cause in ai_analysis["possible_causes"]:
                    st.write(f"- {cause}")

                st.markdown("**Troubleshooting Steps**")
                for step_number, step in enumerate(
                    ai_analysis["troubleshooting_steps"],
                    start=1
                ):
                    st.write(f"{step_number}. {step}")

            else:
                st.warning(
                    "AI analysis is not available for this test."
                )




# Allow users to upload or paste test logs.
st.subheader("📂 Analyze Your Test Logs")

input_method = st.radio(
    "How would you like to provide your logs?",
    ["📁 Upload File", "📋 Paste Logs"],
    horizontal=True,
    key="log_input_method"
)

log_content = None
source_name = None

if input_method == "📁 Upload File":
    uploaded_file = st.file_uploader(
        "Choose a .log or .txt file",
        type=["log", "txt"],
        key="test_log_upload"
    )

    if uploaded_file is not None:
        try:
            log_content = uploaded_file.getvalue().decode("utf-8")
            source_name = uploaded_file.name
        except UnicodeDecodeError:
            st.error("Please upload a UTF-8 text file.")

else:
    pasted_text = st.text_area(
        "Paste log lines here",
        height=200,
        key="pasted_test_logs",
        placeholder=(
            "2026-11-23 11:00:01 PASS LoginTest\n"
            "2026-11-23 11:00:02 FAIL CheckoutTest\n"
            "2026-11-23 11:00:03 ERROR Payment gateway timeout"
        )
    )

    if pasted_text.strip():
        log_content = pasted_text
        source_name = "Pasted Logs"


if log_content is not None:
    st.success(f"Log input ready: {source_name}")

    # Identify the current log content.
    log_id = hashlib.sha256(
        log_content.encode("utf-8")
    ).hexdigest()

    # Clear AI results if the input has changed.
    if st.session_state.get("current_log_id") != log_id:
        st.session_state["current_log_id"] = log_id
        st.session_state.pop("uploaded_ai_results", None)


    # Split the text into individual lines.
    lines = log_content.splitlines()

    # Reuse the existing analysis functions.
    parsed_logs = parse_log_lines(lines)
    df = create_dataframe(parsed_logs)
    uploaded_summary = analyze_tests(df)
    uploaded_failures = associate_errors(df)

    if not parsed_logs:
        st.warning(
            "No valid log entries were found. "
            "Please check the log format."
        )
    else:
        st.subheader("📊 Uploaded Log Results")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Tests", uploaded_summary["total_tests"])

        with col2:
            st.metric("Passed", uploaded_summary["passed"])

        with col3:
            st.metric("Failed", uploaded_summary["failed"])

        with col4:
            st.metric(
                "Pass Rate",
                f"{uploaded_summary['pass_rate']}%"
            )

        st.subheader("❌ Uploaded Log Failures")

        if not uploaded_failures:
            st.success("No failed tests found!")
        else:
            for failure in uploaded_failures:
                with st.expander(f"❌ {failure['test_name']}"):
                    st.write(
                        f"**Error:** "
                        f"{failure['error'] or 'No error details available'}"
                    )

        # Optional AI analysis for uploaded failures.
        if uploaded_failures:
            st.subheader("🤖 AI-Powered Troubleshooting")

            st.caption(
                "Only request AI analysis for sample or sanitized logs. "
                "Test names and error messages will be sent to GroqCloud."
            )

            if st.button("✨ Analyze Failures with AI"):
                with st.spinner("Analyzing failed tests..."):
                    ai_results = []

                    for failure in uploaded_failures:
                        try:
                            analysis = analyze_failure(failure)

                            ai_results.append({
                                "test_name": failure["test_name"],
                                "analysis": analysis,
                                "error": None
                            })

                        except Exception as error:
                            ai_results.append({
                                "test_name": failure["test_name"],
                                "analysis": None,
                                "error": str(error)
                            })

                    st.session_state["uploaded_ai_results"] = ai_results

            # Display results after the button has been clicked.
            if "uploaded_ai_results" in st.session_state:
                for result in st.session_state["uploaded_ai_results"]:
                    st.markdown(f"### {result['test_name']}")

                    if result["analysis"] is None:
                        st.warning(
                            f"AI analysis unavailable: {result['error']}"
                        )
                        continue

                    analysis = result["analysis"]

                    st.markdown("**Explanation**")
                    st.write(analysis["explanation"])

                    st.markdown("**Possible Root Causes**")
                    for cause in analysis["possible_causes"]:
                        st.write(f"- {cause}")

                    st.markdown("**Troubleshooting Steps**")
                    for number, step in enumerate(
                        analysis["troubleshooting_steps"],
                        start=1
                    ):
                        st.write(f"{number}. {step}")

