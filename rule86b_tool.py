import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Rule 86B — ITC & Cash Calculator", layout="centered")

st.title("GST Rule 86B — ITC / Cash Payment Calculator")

st.write("Enter the below values to check whether Rule 86B applies and how much cash must be paid.")

# User Inputs
taxable_value = st.number_input(
    "Taxable value of supplies for the month (₹) excluding exempt & zero-rated:",
    min_value=0.0, format="%.2f"
)

output_tax = st.number_input(
    "Total Output Tax Liability for the month (₹):",
    min_value=0.0, format="%.2f"
)

cum_cash_paid = st.number_input(
    "Cumulative Cash Paid in current FY till previous month (₹):",
    min_value=0.0, format="%.2f"
)

cum_tax_liability = st.number_input(
    "Cumulative Output Tax Liability till previous month (₹):",
    min_value=0.0, format="%.2f"
)

refund_prev_year = st.number_input(
    "Refund received in previous year due to zero-rated/inverted duty (₹):",
    min_value=0.0, format="%.2f"
)

income_tax_flag = st.checkbox("Income-Tax paid > ₹1,00,000 in last 2 FY")

st.markdown("---")

# Computations
rule_applies = taxable_value > 5000000  # ₹50 lakh test

required_cumulative_cash = 0.01 * (cum_tax_liability + output_tax)
shortfall_cash = max(0, required_cumulative_cash - cum_cash_paid)

# If already eligible exemption
exemption = False

if refund_prev_year > 100000:
    exemption = True

if income_tax_flag:
    exemption = True

if cum_cash_paid >= required_cumulative_cash:
    exemption = True

# Final applicability
final_rule = rule_applies and not exemption

max_itc_use = output_tax - shortfall_cash
if max_itc_use < 0:
    max_itc_use = 0

# Output section
st.subheader("Result:")

if not final_rule:
    st.success("Rule 86B does NOT apply based on your given data.")
else:
    st.error("Rule 86B applies this month.")

st.markdown("### Minimum Cash Required This Month")
st.info(f"₹ {shortfall_cash:,.2f}")

st.markdown("### Maximum ITC Allowed This Month")
st.success(f"₹ {max_itc_use:,.2f}")

st.markdown("---")

st.markdown("### Understanding the Reason:")
if not rule_applies:
    st.write("✔ Monthly taxable value is less than ₹50,00,000.")
if refund_prev_year > 100000:
    st.write("✔ Refund > ₹1 lakh in previous FY – exemption applicable.")
if income_tax_flag:
    st.write("✔ Income-tax > 1 lakh paid in last 2 FY – exemption applicable.")
if cum_cash_paid >= required_cumulative_cash:
    st.write("✔ You already paid >= 1% cash in FY – exemption applicable.")

st.write("Calculation done based on commonly followed interpretation of Rule 86B.")
