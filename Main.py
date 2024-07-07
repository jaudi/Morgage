import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def cuota(interest_rate, duration, amount):
    monthly_rate = interest_rate / 12
    num_payments = duration * 12
    cuota = amount * monthly_rate / (1 - (1 + monthly_rate) ** -num_payments)
    return cuota

def calculate_amortization_schedule(interest_rate, duration, amount):
    schedule = []
    monthly_rate = interest_rate / 12
    balance = amount
    Repayment = cuota(interest_rate, duration, amount)

    for period in range(1, duration * 12 + 1):
        interest_paid = balance * monthly_rate
        principal_paid = Repayment - interest_paid
        balance -= principal_paid  # Update balance for the next period
        balance = round(balance, 2)
        
        schedule.append([period, round(interest_paid, 2), round(principal_paid, 2), balance, round(Repayment, 2)])

    data = pd.DataFrame(schedule, columns=["Period", "Interest Paid", "Principal", "Balance", "Repayment"])
   
    total_interest_paid = data["Interest Paid"].sum()
    total_Repayment = data["Repayment"].sum()
    return data, total_interest_paid, total_Repayment

def savings(amount, period, interest):
    monthly_interest = interest / 12  # Monthly interest rate
    amount_periodic = amount * monthly_interest / ((1 + monthly_interest) ** period - 1)
    return amount_periodic

def main():
    st.title("Loan Amortization Calculator")
    st.sidebar.title("Input Parameters")
    
    interest_rate = st.sidebar.slider("Annual Interest Rate (%)", 0.1, 20.0, 5.0, 0.1)
    duration = st.sidebar.slider("Loan Duration (Years)", 1, 40, 10, 1)
    amount = st.sidebar.number_input("Loan Amount", min_value=1000, max_value=10000000, value=10000)
    savings_interest_rate = st.sidebar.slider("Annual Savings Interest Rate (%)", 0.1, 20.0, 7.0, 0.1)

    data, total_interest_paid, total_Repayment = calculate_amortization_schedule(interest_rate / 100, duration, amount)
    
    st.write(data)
    st.markdown(f"**Total Interest Paid:** {total_interest_paid:.2f}")
    st.markdown(f"**Total Repayments Paid:** {total_Repayment:.2f}")

    chart_data = pd.DataFrame({
        'Category': ['Total Interest Paid', 'Total Repayment'],
        'Amount': [total_interest_paid, total_Repayment]
    })
    st.bar_chart(chart_data.set_index('Category'))
    
    chart_data2 = pd.DataFrame({
        'Period': data['Period'],
        'Interest Paid': data['Interest Paid'],
        'Principal Paid': data['Principal']
    })
    
    plt.figure(figsize=(10, 5))
    plt.plot(chart_data2['Period'], chart_data2['Interest Paid'], label='Interest Paid')
    plt.plot(chart_data2['Period'], chart_data2['Principal Paid'], label='Principal Paid')
    plt.xlabel('Period')
    plt.ylabel('Amount')
    plt.title('Interest Paid vs Principal Paid')
    plt.legend()
    st.pyplot(plt)

    balance_last_5_year = data["Balance"]

    if len(balance_last_5_year) >= 60:
        amount_needed = balance_last_5_year.iloc[-60]
        period_savings = data['Period'].iloc[-60]
        recurrent_savings = int(savings(amount_needed, period_savings, savings_interest_rate / 100))
        total_saving_loan = int((data["Interest"].iloc[-60:].sum())
        
        st.markdown(f"**Amount Needed to Amortize 5 Years Earlier:** {amount_needed:.2f}")
        st.markdown(f"**Period for Savings:** {period_savings} months")
        st.markdown(f"**Monthly Savings Required:** {recurrent_savings:.2f}")
        st.markdown(f"**Total Savings from Early Amortization:** {total_saving_loan:.2f}")
        
        # Recommendation based on interest rates
        if savings_interest_rate > interest_rate:
            st.markdown("**Recommendation:** Paying off the loan 5 years earlier is beneficial because the savings interest rate is higher than the loan interest rate.")
        else:
            st.markdown("**Recommendation:** Paying off the loan 5 years earlier may not be beneficial because the savings interest rate is not higher than the loan interest rate.")
        
        # Chart for Savings
        months = list(range(1, period_savings + 1))
        savings_values = [recurrent_savings] * period_savings
        plt.figure(figsize=(10, 5))
        plt.plot(months, savings_values, label='Monthly Savings Required', color='green')
        plt.xlabel('Months')
        plt.ylabel('Savings Amount')
        plt.title('Monthly Savings Required for Early Amortization')
        plt.legend()
        st.pyplot(plt)
    else:
        st.markdown("The amortization schedule does not have 60 entries.")

if __name__ == "__main__":
    main()
