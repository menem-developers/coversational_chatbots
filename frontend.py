import streamlit as st
import requests
from datetime import datetime
API_URL_MOTOR_CREATE = "http://127.0.0.1:8000/api/v1/chatbot/create_motor_insurance"
API_URL_MOTOR_FILES = "http://127.0.0.1:8000/api/v1/chatbot/parse_user_vehicle_info"

# Initialize session states
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "selected_service" not in st.session_state:
    st.session_state["selected_service"] = ""

if "selected_product" not in st.session_state:
    st.session_state["selected_product"] = "" 

if "selected_entry" not in st.session_state:
    st.session_state["selected_entry"] = "" 

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

def select_service(service_name):
    st.session_state["selected_service"] = service_name

def select_product(product):
    st.session_state["selected_product"] = product    

def select_entry(entry):
    st.session_state["selected_entry"] = entry

def show_chat():
    prompt = st.chat_input(placeholder="Your message")

    if prompt:
        if prompt.lower() in ["hi", "hello"]:
            st.write("Hi welcome!!!....Please select a service:")
            st.button("Apply Insurance", on_click=select_service, args=("Apply Insurance",))
            st.button("Renewal", on_click=select_service, args=("Renewal",))
            st.button("Support", on_click=select_service, args=("Support",))

    if st.session_state["selected_service"]:
        st.button("Apply Insurance", on_click=select_service, args=("Apply Insurance",))
        st.button("Renewal", on_click=select_service, args=("Renewal",))
        st.button("Support", on_click=select_service, args=("Support",))
        st.write(f"You selected Service: {st.session_state['selected_service']}") 
        if st.session_state["selected_service"] == "Apply Insurance":
            if st.session_state["selected_product"]: 
                st.button("Motor", on_click=select_product, args=("Motor",))
                st.button("Home", on_click=select_product, args=("Home",))
                st.button("Life", on_click=select_product, args=("Life",))
                st.write(f"You selected Product: {st.session_state['selected_product']}") 
                if st.session_state["selected_product"] == "Motor":
                        st.button("Manual Entry", on_click=select_entry, args=("Manual Entry",))
                        st.button("Files Uploads", on_click=select_entry, args=("Files Uploads",))

                        if st.session_state["selected_entry"] == "Manual Entry":
                            with st.form("Customer Entry"):
                                st.subheader("Customer Information")
                                name = st.text_input("Name", max_chars=200)
                                dob = st.date_input(
                                    "Date of Birth",
                                    value=datetime.today(),
                                    min_value=datetime(1900, 1, 1),
                                    max_value=datetime.today()
                                )
                                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                                mobile = st.text_input("Mobile", max_chars=10)
                                address = st.text_area("Address")
                                occupation = st.text_input("Occupation", max_chars=200)
                                licensenumber = st.text_input("License Number", max_chars=200)

                                st.subheader("Motor Insurance Details")
                                chassisno = st.text_input("Chassis Number", max_chars=200)
                                make = st.text_input("Make", max_chars=200)
                                model = st.text_input("Model", max_chars=200)
                                seatingcapacity = st.text_input("Seating Capacity", max_chars=200)
                                bodytype = st.text_input("Body Type", max_chars=200)
                                vehicleusage = st.text_input("Vehicle Usage", max_chars=200)
                                year = st.text_input("Year", max_chars=4)
                                submitted = st.form_submit_button("Buy Policy")

                            if submitted:
                                product = {
                                    "chassisno": chassisno,
                                    "make": make,
                                    "model": model,
                                    "seatingcapacity": seatingcapacity,
                                    "bodytype": bodytype,
                                    "vehicleusage": vehicleusage,
                                    "year": year
                                }
                                motordetails = {
                                    "name": name,
                                    "dob": dob.isoformat(),
                                    "gender": gender,
                                    "mobile": mobile,
                                    "address": address,
                                    "occupation": occupation,
                                    "licensenumber": licensenumber,
                                    "product": product
                                }
                                try:
                                    response = requests.post(API_URL_MOTOR_CREATE, json=motordetails)
                                    if response.status_code == 200:
                                        response_data = response.json()
                                        if response_data.get("status"):
                                            st.success("Policy created successfully!")
                                            st.session_state.policy_created = True
                                        else:
                                            st.error(f"Failed to create blog: {response_data.get('message')}")
                                    elif response.status_code == 400:
                                        st.error("Failed to create blog: Invalid data")
                                    else:
                                        st.error(f"Error: {response.status_code}")
                                except Exception as e:
                                    st.error(f"Failed to connect to server: {str(e)}")
                        elif st.session_state.get("selected_entry") == "Files Uploads":
                            with st.form("Customer Entry"):
                                st.subheader("Customer Information")
                                file = st.file_uploader("Upload Document", type=["jpg", "jpeg", "png", "pdf"])
                                submitted = st.form_submit_button("Buy Policy")

                            # If the file is uploaded and form is submitted
                            if submitted:
                                if file is not None:
                                    try:
                                        # Debugging: Show file information
                                        st.write(f"File uploaded: {file.name}, {file.type}")

                                        # Read the file content
                                        file_content = file.read()

                                        # Debugging: Confirm file content is read
                                        st.write(f"File content size: {len(file_content)} bytes")

                                        # Prepare the file data for multipart/form-data
                                        files = {"file": (file.name, file_content, file.type)}

                                        # Send the file as multipart/form-data to the server
                                        response = requests.post(API_URL_MOTOR_FILES, files=files)

                                        if response.status_code == 200:
                                            response_json = response.json()

                                            if response_json:
                                                # Save the response in session state
                                                st.session_state.motor_response = response_json
                                                st.session_state.file_uploaded = True  # Track that file upload was successful
                                            else:
                                                st.error("Failed to create policy: Invalid response from the API.")
                                        elif response.status_code == 400:
                                            st.error("Failed to create policy: Invalid file data")
                                        else:
                                            st.error(f"Error: {response.status_code}")
                                    except Exception as e:
                                        st.error(f"Failed to connect to server: {str(e)}")
                                else:
                                    st.error("Please upload a file.")

                            # Check if file upload was successful and display motor entry form
                            if st.session_state.get("file_uploaded", False):
                                with st.form("Motor Entry"):
                                    # Use the saved response data for motor details
                                    response_json = st.session_state.get("motor_response", {})

                                    name = st.text_input("Name", value=response_json.get("Owner name", ""), max_chars=200)
                                    dob = st.date_input("Date of Birth", value=datetime.today(), min_value=datetime(1900, 1, 1), max_value=datetime.today())
                                    gender = st.selectbox("Gender", options=["Male", "Female", "Other"], index=["Male", "Female", "Other"].index("Male"))
                                    mobile = st.text_input("Mobile", value=response_json.get("phone number", ""), max_chars=100)
                                    address = st.text_area("Address", value=response_json.get("address", ""))
                                    occupation = st.text_input("Occupation", max_chars=200)
                                    licensenumber = st.text_input("License Number", value=response_json.get("licensenumber", ""), max_chars=200)

                                    st.subheader("Motor Insurance Details")
                                    chassisno = st.text_input("Chassis Number", value=response_json.get("VIN/Chassis Number", ""), max_chars=200)
                                    make = st.text_input("Make", value=response_json.get("Make", ""), max_chars=200)
                                    model = st.text_input("Model", value=response_json.get("Model Number", ""), max_chars=200)
                                    seatingcapacity = st.text_input("Seating Capacity", value=response_json.get("Seating Capacity", ""), max_chars=200)
                                    bodytype = st.text_input("Body Type", max_chars=200)
                                    vehicleusage = st.text_input("Vehicle Usage", max_chars=200)
                                    year = st.text_input("Year", value=response_json.get("First Registration Date", ""), max_chars=4)

                                    # Submit button for the second form
                                    submitted_motor = st.form_submit_button("Buy Policy")

                                # Handle motor details submission
                                if submitted_motor:
                                    product = {
                                        "chassisno": chassisno,
                                        "make": make,
                                        "model": model,
                                        "seatingcapacity": seatingcapacity,
                                        "bodytype": bodytype,
                                        "vehicleusage": vehicleusage,
                                        "year": year
                                    }
                                    motordetails = {
                                        "name": name,
                                        "dob": dob.isoformat(),
                                        "gender": gender,
                                        "mobile": mobile,
                                        "address": address,
                                        "occupation": occupation,
                                        "licensenumber": licensenumber,
                                        "product": product
                                    }

                                    try:
                                        # Make a POST request to submit motor details
                                        response_motor = requests.post(API_URL_MOTOR_CREATE, json=motordetails)
                                        if response_motor.status_code == 200:
                                            response_data = response_motor.json()
                                            if response_data.get("status"):
                                                st.success("Policy created successfully!")
                                                st.session_state.policy_created = True
                                            else:
                                                st.error(f"Failed to create policy: {response_data.get('message')}")
                                        elif response_motor.status_code == 400:
                                            st.error("Failed to create policy: Invalid data")
                                        else:
                                            st.error(f"Error: {response_motor.status_code}")
                                    except Exception as e:
                                        st.error(f"Failed to connect to server: {str(e)}")

                        if st.session_state.get("policy_created"):
                            # Display the payment button
                            if st.button("Proceed to Payment"):
                                st.session_state.policy_created = False
                                st.success("Thank you for your payment!")
                                    


            else:    
                st.write("Please select a product:")
                st.button("Motor", on_click=select_product, args=("Motor",))
                st.button("Home", on_click=select_product, args=("Home",))
                st.button("Life", on_click=select_product, args=("Life",))


        if st.session_state["selected_service"] == "Support":
            st.write(f"You selected: {st.session_state['selected_service']}")
        if st.session_state["selected_service"] == "Renewal":
            st.write(f"You selected: {st.session_state['selected_service']}")
            

def login():
    placeholder = st.empty()

    if not st.session_state["logged_in"]:
        with placeholder.form("login"):
            st.title("Login")
            username_input = st.text_input("Username")
            password_input = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")

        if submit:
            # Placeholder for authentication (use your own logic here)
            if username_input == "admin" and password_input == "admin":
                st.session_state["logged_in"] = True
                st.success("Logged in successfully!")
                placeholder.empty()
            else:
                st.error("Invalid username or password")

def main():
    # Check login status
    login()
    
    # If logged in, show chat interface
    if st.session_state["logged_in"]:
        st.sidebar.title("Dashboard")
        option = st.sidebar.selectbox("Choose an action", ["Chat", "Logout"])

        if option == "Chat":
            show_chat()
        elif option == "Logout":
            st.session_state["logged_in"] = False
            st.success("Logged out successfully!")
            st.session_state["chat_history"].clear()  # Clear chat history on logout

if __name__ == "__main__":
    main()
