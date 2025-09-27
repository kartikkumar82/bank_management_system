import streamlit as st
import random
from main import Bank  # assume your Bank class is saved in bank.py

st.set_page_config(page_title="Bank Management System", page_icon="💳", layout="centered")

st.title("💳 Simple Bank Management System")

menu = ["Create Account", "Deposit Money", "Withdraw Money", "Balance Enquiry", "Update Account", "Close Account"]
choice = st.sidebar.selectbox("Select Action", menu)

bank = Bank()

if choice == "Create Account":
    st.subheader("📝 Create a New Account")
    name = st.text_input("Enter your name")
    age = st.number_input("Enter your age", min_value=1, max_value=100, step=1)
    email = st.text_input("Enter your email")
    pin = st.text_input("Enter a 4-digit pin", type="password")

    if st.button("Create Account"):
        if age < 18 or age > 65:
            st.error("❌ You are not eligible to create an account")
        elif len(pin) != 4 or not pin.isdigit():
            st.error("❌ Pin must be a 4-digit number")
        else:
            accnumber = ''.join(random.choices("0123456789", k=10))
            info = {"name": name, "age": age, "email": email, "pin": pin,
                    "account_number": accnumber, "balance": 0}
            Bank.data.append(info)
            Bank._Bank__update()
            st.success("✅ Account created successfully!")
            st.write(info)

elif choice == "Deposit Money":
    st.subheader("💰 Deposit Money")
    acc = st.text_input("Account Number")
    pin = st.text_input("Pin", type="password")
    amount = st.number_input("Amount to deposit", min_value=1, max_value=100000, step=100)
    if st.button("Deposit"):
        user = bank._find_user(acc, pin)
        if not user:
            st.error("❌ No account found")
        else:
            user[0]['balance'] += amount
            Bank._Bank__update()
            st.success(f"✅ Dear {user[0]['name']}, deposit successful!")
            st.info(f"💰 New Balance: {user[0]['balance']}")

elif choice == "Withdraw Money":
    st.subheader("🏧 Withdraw Money")
    acc = st.text_input("Account Number")
    pin = st.text_input("Pin", type="password")
    amount = st.number_input("Amount to withdraw", min_value=1, step=100)
    if st.button("Withdraw"):
        user = bank._find_user(acc, pin)
        if not user:
            st.error("❌ No account found")
        elif user[0]['balance'] < amount:
            st.error("❌ Insufficient balance")
        else:
            user[0]['balance'] -= amount
            Bank._Bank__update()
            st.success(f"✅ Dear {user[0]['name']}, Withdrawal successful!")
            st.info(f"💰 New Balance: {user[0]['balance']}")

elif choice == "Balance Enquiry":
    st.subheader("📋 Balance Enquiry")
    acc = st.text_input("Account Number")
    pin = st.text_input("Pin", type="password")
    if st.button("Check Balance"):
        user = bank._find_user(acc, pin)
        if not user:
            st.error("❌ No account found")
        else:
            st.write("### Your Account Details:")
            st.json(user[0])

elif choice == "Update Account":
    st.subheader("✏️ Update Account")

    # store fetched account number in session
    if "fetched_acc" not in st.session_state:
        st.session_state.fetched_acc = None

    acc = st.text_input("Account Number", key="acc_update")
    pin = st.text_input("Pin", type="password", key="pin_update")

    if st.button("Fetch Account"):
        user = bank._find_user(acc, pin)
        if not user:
            st.error("❌ No account found")
            st.session_state.fetched_acc = None
        else:
            st.success("✅ Account found, you can update details below")
            st.session_state.fetched_acc = user[0]['account_number']

    # If account is fetched, display update form
    if st.session_state.fetched_acc:
        # find actual user dict
        user = next(u for u in Bank.data if u['account_number'] == st.session_state.fetched_acc)

        with st.form("update_form"):
            new_name = st.text_input("New Name", value=user['name'])
            new_email = st.text_input("New Email", value=user['email'])
            new_pin = st.text_input("New Pin", value=str(user['pin']))

            submitted = st.form_submit_button("Update")

            if submitted:
                if len(new_pin) != 4 or not new_pin.isdigit():
                    st.error("❌ Pin must be a 4-digit number")
                else:
                    user['name'] = new_name
                    user['email'] = new_email
                    user['pin'] = new_pin
                    Bank._Bank__update()
                    st.success(f"✅ Dear {user['name']}, your account updated successfully!")
                    st.session_state.fetched_acc = None   # reset after update

elif choice == "Close Account":
    st.subheader("❌ Close Account")

    # session storage
    if "close_acc" not in st.session_state:
        st.session_state.close_acc = None
    if "close_confirm" not in st.session_state:
        st.session_state.close_confirm = "No"

    acc = st.text_input("Account Number", key="acc_close")
    pin = st.text_input("Pin", type="password", key="pin_close")

    if st.button("Fetch Account"):
        user = bank._find_user(acc, pin)
        if not user:
            st.error("❌ No account found")
            st.session_state.close_acc = None
        else:
            st.success("✅ Account found")
            st.session_state.close_acc = user[0]['account_number']

    # If account is fetched, show details + confirmation + final button
    if st.session_state.close_acc:
        user = next(u for u in Bank.data if u['account_number'] == st.session_state.close_acc)

        st.write("### Account Details")
        st.json(user)

        # Yes/No choice
        st.session_state.close_confirm = st.radio(
            "Are you sure you want to close your account?",
            ("No", "Yes"),
            index=0,
            key="close_confirm_radio"
        )

        # Final Close button
        if st.button("Close Account Now"):
            if st.session_state.close_confirm == "Yes":
                Bank.data.remove(user)
                Bank._Bank__update()
                st.success(f"✅ Dear {user['name']}, your account has been closed successfully!")
            else:
                st.info("❌ Account closure cancelled")

            # Reset session state
            st.session_state.close_acc = None
            st.session_state.close_confirm = "No"

