import streamlit as st
import numpy as np
import pandas as pd

# Set the layout to wide
st.set_page_config(layout="wide")

def calculate_future_value(principal, annual_rate, years):
    return principal * (1 + annual_rate)**years

def parse_input(input_str):
    if isinstance(input_str, int):
        return input_str
    return int(input_str.replace(",", ""))

def house_buying_calculator(header_text, column, key_suffix):
    # Initial assets
    column.header(header_text)
    col1, col2 = column.columns(2)
    initial_assets_raw = col1.number_input("Initial Assets (£)", 0, 1000000, step=1000, value=290000, key=f"init_assets_{key_suffix}_1")
    initial_assets = col2.slider(" ", 0, 1000000, parse_input(initial_assets_raw), 290000, key=f"init_assets_{key_suffix}_2")

    # House Value
    col1, col2 = column.columns(2)
    house_value_raw = col1.number_input("House Value (£)", 100000, 1000000, step=5000, value=215000, key=f"house_value_{key_suffix}_1")
    house_value = col2.slider(" ", 0, 1000000, parse_input(house_value_raw), 215000, key=f"house_value_{key_suffix}_2")

    # Down Payment Percentage
    col1, col2 = column.columns(2)
    down_payment_percentage_raw = col1.number_input("Down Payment Percentage (%)", 1, 100, value=20, key=f"downpayment_{key_suffix}_1")
    down_payment_percentage = col2.slider(" ", 1, 100, parse_input(down_payment_percentage_raw), 1, key=f"downpayment_{key_suffix}_2")
    down_payment = house_value * down_payment_percentage / 100

    # Mortgage Interest Rate
    col1, col2 = column.columns(2)
    mortgage_interest_rate = col1.number_input("Mortgage Interest Rate (%)", 1.0, 10.0, format="%.1f", value=2.0, key=f"mortgage_rate_{key_suffix}_1")
    mortgage_interest_rate = col2.slider(" ", 1.0, 10.0, 4.0, 0.1, key=f"mortgage_rate_{key_suffix}_2")
    loan_amount = house_value - down_payment

    # Loan Term (Years)
    col1, col2 = column.columns(2)
    loan_term_years = col1.number_input("Loan Term (Years)", 1, 30, value=20, key=f"loanterm_{key_suffix}_1")
    loan_term_years = col2.slider(" ", 1, 30, 20, 1, key=f"loanterm_{key_suffix}_2")

    # Inflation Rate 
    col1, col2 = column.columns(2)
    inflation_rate = col1.number_input("Inflation Rate (%)", 0.1, 10.0, value=2.0, key=f"inflationrate_{key_suffix}_1")
    inflation_rate = col2.slider(" ", 0.1, 10.0, 2.0, 0.1, key=f"inflationrate_{key_suffix}_2")

    # Investment Return Rate 
    col1, col2 = column.columns(2)
    investment_return_rate = col1.number_input("Investment Return Rate (%)", 0.1, 10.0, value=2.0, key=f"investment_return_rate_{key_suffix}_1")
    investment_return_rate = col2.slider(" ", 0.1, 10.0, 2.0, 0.1, key=f"investment_return_rate_{key_suffix}_2")

    # House Appreciation Rate
    col1, col2 = column.columns(2)
    house_appreciation_rate = col1.number_input("Investment Return Rate (%)", 0.1, 10.0, value=2.0, key=f"house_appreciation_rate_{key_suffix}_1")
    house_appreciation_rate = col2.slider(" ", 0.1, 10.0, 2.0, 0.1, key=f"house_appreciation_rate_{key_suffix}_2")

    remaining_assets = initial_assets - (house_value-down_payment)

    # Monthly Payment
    col1, col2 = column.columns(2)
    monthly_payment = col1.number_input("Monthly Payment (£)", 1, 5000, value=2000, key=f"monthly_payment_{key_suffix}_1")
    monthly_payment = col2.slider("Monthly Payment (£)", 1, 5000, 2000, 1, key=f"monthly_payment_{key_suffix}_2")

    # Number of Years in the Future
    col1, col2 = column.columns(2)
    future_years = col1.number_input("Number of Years in the Future", 1, 30, value=20, key=f"years_future_{key_suffix}_1")
    future_years = col2.slider(" ", 1, 30, 20, 1, key=f"years_future_{key_suffix}_2")                                    

    # Calculate future values
    total_payment = monthly_payment * 12 * loan_term_years
    total_investment = total_payment * (1 + inflation_rate / 100)

    years = np.arange(1, future_years + 1)
    future_values_house = [calculate_future_value(house_value, house_appreciation_rate / 100, year) for year in years]
    future_values_investment = [calculate_future_value(remaining_assets, investment_return_rate / 100, year) for year in years]
    
# Display results centrally
    column.header(f"Results after {loan_term_years} years for {header_text}:")
    column.write("Future Value of House: £{:,.2f}".format(future_values_house[-1]))
    column.write("Future Value of Investments: £{:,.2f}".format(future_values_investment[-1]))
    column.write("Total Payment over {} years: £{:,.2f}".format(loan_term_years, total_payment))

# Display graph of results in the specified column
    column.header(f"Graph of results for {header_text}:")
    df = pd.DataFrame({
        'Year': years,
        'House Value': future_values_house,
        'Investment Value': future_values_investment
    })

    # Use the column object to display the line chart
    column.line_chart(df.set_index('Year'))

def main():
    st.title("Side-by-Side House Buying Calculators")
    col1, col2 = st.columns(2)

    # Create two instances of the house buying calculator side by side
    house_buying_calculator("Calculator 1", col1, "calc1")
    house_buying_calculator("Calculator 2", col2, "calc2")

if __name__ == "__main__":
    main()
