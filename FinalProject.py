import streamlit as st
import json
from pathlib import Path
import datetime
import uuid
import time

st.set_page_config(page_title="The Sunshine Bakery and Shop Website",
    page_icon = "",
    layout = "centered")
backgroundcolor = "#FFFF93"
st.markdown(
    f"""<style>.stApp {{background-color: {backgroundcolor};
    }}</style>""",unsafe_allow_html=True
)

with st.sidebar:
    st.title("Navigate")
    if st.button("Home"):
        st.session_state["page"] = "home"
    if st.button("Register"):
        st.session_state["page"] = "register"
    

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "user" not in st.session_state:
    st.session_state["user"] = None
    
if "page" not in st.session_state:
    st.session_state["page"] = "home"

if "owner_logged_in" not in st.session_state:
    st.session_state["owner_logged_in"] = False

if "employee_logged_in" not in st.session_state:
    st.session_state["employee_logged_in"] = False

if "messages" not in st.session_state:
    st.session_state["messages"] =[{
        "role": "assistant",
        "content": "Hi! How can I help you?"
    }]

users = [
{
"id":1,
"email": "owner@bakery.com",
"full_name": "System Owner",
"password": "123",
"role": "Owner"
},
{
"id":2,
"email": "employee@bakery.com",
"full_name": "System Employee",
"password": "1234",
"role": "Employee"
}
]

next_inventory_id_number = 9
inventory = [
    {"id": 1, "name": "Muffin", "price": 2.00, "stock": 20},
    {"id": 2, "name": "Crossiant", "price": 3.00, "stock": 15},
    {"id": 3, "name": "Cookie", "price": 2.50, "stock": 25},
    {"id": 4, "name": "Cake", "price": 4.50, "stock": 10},
    {"id": 5, "name": "Bread", "price": 5.00, "stock": 10},
    {"id": 6, "name": "Coffee", "price": 3.20, "stock": 20},
    {"id": 7, "name": "Orange Juice", "price": 2.75, "stock": 15},
    {"id": 8, "name": "Apple Juice", "price": 2.75, "stock": 25}
]

#Users Json
json_path = Path("users.json")
if json_path.exists():
    with open(json_path, "r") as f:
        users = json.load(f)
def save_users(users, path):
    with open(path, "w") as f:
        json.dump(users, f)

#Inventory Json
inventory_json_file = Path("inventory.json")
if inventory_json_file.exists():
    with open(inventory_json_file, "r") as f:
        inventory = json.load(f)
else:
    with open(inventory_json_file, "w") as f:
        json.dump(inventory, f, indent=4)

#Orders json
orders_json_file = Path("orders.json")
if orders_json_file.exists():
    with open(orders_json_file, "r") as f:
        orders = json.load(f)
else:
    # Default data if file doesn't exist
    orders = [] 

with open(orders_json_file, "w") as f:
    json.dump(orders, f, indent=4)

#Discontinued items json
discontinued_json_file = Path("discontinued_items.json")
if discontinued_json_file.exists():
    with open(discontinued_json_file, "r") as f:
        discontinued_items = json.load(f)
else:
    discontinued_items = []

with open(discontinued_json_file, "w") as f:
    json.dump(discontinued_items, f, indent=4)

ai_response_list = [
            {
                "user":"What items are low on stock?",
                "ai":""
            },
            {
                "user":"What is the total sales revenue?",
                "ai":""
            },
            {
                "user":"How many orders were placed today?",
                "ai":""
            },
            {
                "user":"What is the most popular item?",
                "ai":""
            },
            {
                "user":"What items are discontinued?",
                "ai":""
            }
        ]

if st.session_state["page"]== "home":
    st.title("The Sunshine Bakery and Shop")
    st.divider()
    st.subheader("About Us")
    with st.container(border =True):
        st.markdown("The Sunshine Bakery Shop is a family owned and operated business. Our goal is to make sure every customer has a great start to their morning! Our prices are extremely affordable and very high quality, we specialize in signature coffee and pasteries.")
    st.divider()
    st.subheader("Administrative Log In Options")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Owner Log In"):
            st.session_state["page"] = "owner_login"
            st.rerun()
    with col2:
        if st.button("Employee Log In"):
            st.session_state["page"] = "employee_login"
            st.rerun()

elif st.session_state["page"] == "owner_login":
    st.title ("Owner Login Page")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    

    if st.button("Log In"):
        owner = next((user for user in users if user["email"] == email and user["password"]== password and user["role"]== "Owner"), None)
        if owner:
            st.session_state["owner_logged_in"]= True
            st.session_state["user"] = owner
            st.session_state["page"] = "owner_dashboard"
    
        
            st.rerun()


        else:
            st.error("Invalid Credentials!")

elif st.session_state["page"] == "owner_dashboard":
    st.title("Owner Dashboard")
    st.success("Welcome to the Owner Dashboard")

    if st.button("Logout"):
        st.session_state["owner_logged_in"] = False
        st.session_state["user"] = None
        st.session_state["page"] = "home"
        st.rerun()

    # Inventory metrics
    total_products = 0
    total_stock = 0
    low_stock_count = 0
    total_inventory_value = 0

    for item in inventory:
        total_products = total_products + 1
        total_stock = total_stock + item["stock"]
        total_inventory_value = total_inventory_value + (item["price"] * item["stock"])

        if item["stock"] <= 5:
            low_stock_count = low_stock_count + 1

    st.markdown("## Inventory Overview")
    owner_tab1, owner_tab2 = st.tabs(["Dashboard", "Inventory Management"])

    with owner_tab1:
        st.markdown("## Inventory Overview")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Products", total_products)

        with col2:
            st.metric("Total Items In Stock", total_stock)

        with col3:
            st.metric("Low Stock Items", low_stock_count)

        with col4:
            st.metric("Inventory Value", f"${total_inventory_value:.2f}")

        # Sales metrics
        total_sales = 0
        total_units_sold = 0
        total_sales_revenue = 0

        for order in orders:
            total_sales = total_sales + 1
            total_units_sold = total_units_sold + order["quantity"]
            total_sales_revenue = total_sales_revenue + order["total"]

        st.markdown("## Sales Overview")
        col5, col6, col7 = st.columns(3)

        with col5:
            st.metric("Number of Sales", total_sales)

        with col6:
            st.metric("Units Sold", total_units_sold)

        with col7:
            st.metric("Sales Revenue", f"${total_sales_revenue:.2f}")

        col_left, col_right = st.columns([2, 1])

        with col_left:
            st.markdown("## Current Inventory Dashboard")

            if inventory:
                for item in inventory:
                    with st.container(border=True):
                        st.markdown(f"Item ID: {item['id']}")
                        st.markdown(f"Name: {item['name']}")
                        st.markdown(f"Price: ${item['price']:.2f}")
                        st.markdown(f"Stock: {item['stock']}")

                        if item["stock"] <= 5:
                            st.warning("Low Stock!")
            else:
                st.warning("No inventory available. Please add products first.")
            
            with col_right:
                st.markdown("## Recent Sales")

                if orders:
                    for order in orders:
                        with st.container(border=True):
                            st.markdown(f"Order ID: {order['order_id']}")
                            st.markdown(f"Item: {order['item']}")
                            st.markdown(f"Quantity: {order['quantity']}")
                            st.markdown(f"Total: ${order['total']:.2f}")
                            st.markdown(f"Status: {order['status']}")
                else:
                    st.info("No sales recorded yet.")
                
                st.markdown("## ChatBot Assistant")

                st.markdown("Try asking:")
                for item in ai_response_list:
                    st.markdown("- " + item["user"])

                with st.container(border=True):
                    for message in st.session_state["messages"]:
                        with st.chat_message(message["role"]):
                            st.write(message["content"])

                user_input = st.chat_input("Ask a question...")
                if user_input:
                    with st.spinner("Thinking..."):
                        st.session_state["messages"].append({
                            "role": "user",
                            "content": user_input
                        })

                        ai_response = "I can answer questions about stock, orders, revenue, and discontinued items."

                        for item in ai_response_list:
                            if user_input.lower() == item["user"].lower():

                                if item["user"] == "What items are low on stock?":
                                    low_stock_items = []

                                    for inv in inventory:
                                        if inv["stock"] <= 5:
                                            low_stock_items.append(inv["name"])

                                    if len(low_stock_items) > 0:
                                        answer = "Low stock items: "

                                        for low_item in low_stock_items:
                                            answer = answer + low_item + ", "

                                        answer = answer[:-2]
                                        ai_response = answer
                                    else:
                                        ai_response = "There are no low stock items."

                                elif item["user"] == "What is the total sales revenue?":
                                    total_sales_revenue = 0

                                    for order in orders:
                                        total_sales_revenue = total_sales_revenue + order["total"]

                                    ai_response = f"The total sales revenue is ${total_sales_revenue:.2f}"

                                elif item["user"] == "How many orders were placed today?":
                                    total_orders = 0

                                    for order in orders:
                                        total_orders = total_orders + 1

                                    ai_response = f"There are {total_orders} orders."

                                elif item["user"] == "What is the most popular item?":
                                    item_count = {}

                                    for order in orders:
                                        name = order["item"]

                                        if name in item_count:
                                            item_count[name] = item_count[name] + order["quantity"]
                                        else:
                                            item_count[name] = order["quantity"]

                                    most_popular = None
                                    highest = 0

                                    for name in item_count:
                                        if item_count[name] > highest:
                                            highest = item_count[name]
                                            most_popular = name

                                    if most_popular is not None:
                                        ai_response = f"The most popular item is {most_popular}."
                                    else:
                                        ai_response = "No sales data yet."

                                elif item["user"] == "What items are discontinued?":
                                    if len(discontinued_items) > 0:
                                        answer = "Discontinued items: "

                                        for discontinued_item in discontinued_items:
                                            answer = answer + discontinued_item + ", "

                                        answer = answer[:-2]
                                        ai_response = answer
                                    else:
                                        ai_response = "There are no discontinued items."

                                break

                        st.session_state["messages"].append({
                            "role": "assistant",
                            "content": ai_response
                        })

                    time.sleep(2)
                    st.rerun()

        with owner_tab2:
            tab1, tab2, tab3, tab4 = st.tabs(["Add Product", "Update Prices", "Restock Inventory", "Delete Product"])

            with tab1:
                st.subheader("Add Product")
                st.markdown("Enter a new product to add to the inventory.")

                with st.container(border=True):
                    product_name = st.text_input("Enter Product Name")
                    product_price = st.number_input("Enter Product Price", min_value=0.0, step=0.25, format="%.2f")
                    product_stock = st.number_input("Enter product stock", min_value=0, step=1)

                    btn_add_product = st.button("Add New Product", key="new_product_btn", use_container_width=True)

                if btn_add_product:
                    with st.spinner("Adding Product..."):
                        time.sleep(2)

                    found_item = None
                    for item in inventory:
                        if item["name"].lower() == product_name.lower():
                            found_item = item

                    if not product_name:
                        st.warning("Please enter a product name.")
                    elif found_item is not None:
                        st.warning("This product already exists.")
                    else:
                        new_inventory_id = next_inventory_id_number
                        if inventory:
                            new_inventory_id = inventory[-1]["id"] + 1

                        new_product = {
                            "id": new_inventory_id,
                            "name": product_name,
                            "price": product_price,
                            "stock": product_stock
                        }

                        inventory.append(new_product)

                        with open(inventory_json_file, "w") as f:
                            json.dump(inventory, f, indent=4)

                        st.success("Success! New product added successfully!")
                        st.markdown(f"Added: {new_product['name']}")
                        st.markdown(f"Price: ${new_product['price']:.2f}")
                        st.markdown(f"Stock: {new_product['stock']}")

            with tab2:
                st.subheader("Update Prices")
                st.markdown("Select an item to update its price.")

                item_names = []
                for item in inventory:
                    item_names.append(item["name"])

                if item_names:
                    with st.container(border=True):
                        selected_item = st.selectbox("Select an item to update", item_names, key="updated_price")
                        new_price = st.number_input("Enter the updated price of the selected item.", min_value=0.0, step=0.25, format="%.2f")
                        btn_update_price = st.button("Update Price", key="update_price_btn", use_container_width=True)

                    if btn_update_price:
                        with st.spinner("Updating Price..."):
                            time.sleep(2)

                        found_item = None
                        for item in inventory:
                            if item["name"] == selected_item:
                                found_item = item

                        if found_item is not None:
                            old_price = found_item["price"]
                            found_item["price"] = new_price

                            with open(inventory_json_file, "w") as f:
                                json.dump(inventory, f, indent=4)

                            st.success("Price updated successfully!")
                            st.markdown(f"Item: {found_item['name']}")
                            st.markdown(f"Old Price: ${old_price:.2f}")
                            st.markdown(f"New Price: ${found_item['price']:.2f}")
                else:
                    st.warning("No items available. Please add inventory first.")

            with tab3:
                st.subheader("Restock Inventory")
                st.markdown("Select an item and enter how much stock to add.")

                item_names = []
                for item in inventory:
                    item_names.append(item["name"])

                if item_names:
                    with st.container(border=True):
                        selected_item = st.selectbox("Select an item to restock", item_names, key="restock_inventory")
                        restock_quantity = st.number_input("Restock amount", min_value=1, step=1)
                        btn_restock = st.button("Restock", key="restock_btn", use_container_width=True)

                    if btn_restock:
                        with st.spinner("Restocking..."):
                            time.sleep(2)

                        found_item = None
                        for item in inventory:
                            if item["name"] == selected_item:
                                found_item = item

                        if found_item is not None:
                            old_stock = found_item["stock"]
                            found_item["stock"] = found_item["stock"] + restock_quantity
                            new_stock = found_item["stock"]

                            with open(inventory_json_file, "w") as f:
                                json.dump(inventory, f, indent=4)

                            st.success("Restocked successfully!")
                            st.markdown(f"Item: {found_item['name']}")
                            st.markdown(f"Previous Stock: {old_stock}")
                            st.markdown(f"Quantity Added: {restock_quantity}")
                            st.markdown(f"New Stock: {new_stock}")
                else:
                    st.warning("No items available. Please add inventory first.")

            with tab4:
                st.subheader("Delete/Discontinue Product")
                st.markdown("Select an item to delete/discontinue.")

                item_names = []
                for item in inventory:
                    item_names.append(item["name"])

                if item_names:
                    selected_item = st.selectbox("Select an item to discontinue", item_names, key="delete_product")
                    btn_delete = st.button("Delete Product", type="primary", key="delete_btn", use_container_width=True)

                    if btn_delete:
                        with st.spinner("Deleting Item..."):
                            time.sleep(2)

                        updated_inventory = []

                        for item in inventory:
                            if item["name"] == selected_item:
                                discontinued_items.append(item["name"])
                            else:
                                updated_inventory.append(item)

                        inventory = updated_inventory

                        with open(inventory_json_file, "w") as f:
                            json.dump(inventory, f, indent=4)

                        with open(discontinued_json_file, "w") as f:
                            json.dump(discontinued_items, f, indent=4)

                        st.success("Product deleted successfully!")
                        st.markdown(f"Deleted Item: {selected_item}")
                else:
                    st.warning("No items available. Please add inventory first.")


#Employee Login
elif st.session_state["page"] == "employee_login":
    st.title ("Employee Login Page")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Log In employee"):
        employee = next((user for user in users if user["email"] == email and user["password"]== password and user["role"]== "Employee"), None)
        if employee:
            st.session_state["employee_logged_in"]= True
            st.session_state["user"] = employee
            st.session_state["page"] = "employee_dashboard"
            st.rerun()


        else:
            st.error("Invalid Credentials!")

#Employee Dashboard
elif st.session_state["page"] == "employee_dashboard":
    st.success("Welcome to the Employee Dashboard")
    st.title("Employee Dashboard")
    if st.button("Logout"):
        st.session_state["employee_logged_in"] = False
        st.session_state["user"] = None
        st.session_state["page"] = "home"
        st.rerun()
    col1, col2 =st.columns([2,1])
    with col1:
        tab1, tab2, tab3= st.tabs(["Current Catalog", "Daily Sales", "Low Stock" ])
        with tab1:
            st.subheader("Current Catalog")
            st.markdown("View all current products in inventory or select a product to view its details.")

            total_stock = 0
            for item in inventory:
                total_stock = total_stock + item["stock"]

            st.metric("Total Items In Stock", total_stock)

            item_names = []
            for item in inventory:
                item_names.append(item["name"])

            if item_names:
                selected_item = st.selectbox("Select a product", item_names)

                found_item = None
                for item in inventory:
                    if item["name"] == selected_item:
                        found_item = item

                st.markdown("### Selected Product")
                if found_item is not None:
                    with st.container(border=True):
                        st.markdown(f"Item ID: {found_item['id']}")
                        st.markdown(f"Name: {found_item['name']}")
                        st.markdown(f"Price: ${found_item['price']}")
                        st.markdown(f"Stock: {found_item['stock']}")

                        if found_item["stock"] < 5:
                            st.warning("Low Stock!")

                st.markdown("### Full Inventory Dashboard")
                for item in inventory:
                    with st.container(border=True):
                        st.markdown(f"Item ID: {item['id']}")
                        st.markdown(f"Name: {item['name']}")
                        st.markdown(f"Price: ${item['price']}")
                        st.markdown(f"Stock: {item['stock']}")

                        if item["stock"] < 5:
                            st.warning("Low Stock!")
            else:
                st.warning("No products available. Please add inventory first.")
            
        with tab2:
            st.subheader("Daily Sales")
            st.markdown("Log sales to update inventory.")

            with st.container(border=True):
                item_names=[]
                for item in inventory:
                    item_names.append(item['name'])

                selected_item = st.selectbox("Select item sold", item_names, key="daily_sales")
                quantity_sold = st.number_input("Quantity Sold")
                btn_log_sale = st.button("Log Sale", key="log_sale_btn", use_container_width=True, type='primary')

                if btn_log_sale:
                    with st.spinner("Logging Sale..."):
                        time.sleep(2)

                    found_item = None
                    for item in inventory:
                        if item["name"] == selected_item:
                            found_item = item

                    if found_item is not None:
                        if found_item["stock"] >= quantity_sold:
                            found_item["stock"] = found_item["stock"] - quantity_sold

                            new_order = {
                                "order_id": "Order_" + str(len(orders) + 1),
                                "customer": "Walk-In Customer",
                                "item": found_item["name"],
                                "quantity": quantity_sold,
                                "total": found_item["price"] * quantity_sold,
                                "status": "Placed"
                            }

                            orders.append(new_order)

                            with open(inventory_json_file, "w") as f:
                                json.dump(inventory, f, indent=4)

                            with open(orders_json_file, "w") as f:
                                json.dump(orders, f, indent=4)

                            st.success("Sale logged successfully!")
                            st.markdown(f"Item: {found_item['name']}")
                            st.markdown(f"Quantity Sold: {quantity_sold}")
                            st.markdown(f"Remaining Stock: {found_item['stock']}")
                        else:
                            st.warning("Not enough stock available.")
        with tab3:
            st.subheader("Low Stock")
            st.markdown("View items with low stock (stock less than 5).")

            low_stock_items = []

            for item in inventory:
                if item['stock'] <= 5:
                    low_stock_items.append(item)
            
            if low_stock_items:
                for item in low_stock_items:
                    with st.container(border=True):
                        st.markdown(f"**Name:** {item['name']}")
                        st.markdown(f"**Stock:** {item['stock']}")
                        st.warning("Dangerously Low Stock")
            else:
                st.success("No low stock items right now.")
    
    with col2:
        st.markdown("## ChatBot Assistant")

        st.markdown("Try asking:")
        for item in ai_response_list:
            st.markdown("- " + item["user"])

        with st.container(border=True):
            for message in st.session_state["messages"]:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

        user_input = st.chat_input("Ask a question...")
        if user_input:
            with st.spinner("Thinking..."):
                st.session_state["messages"].append({
                    "role": "user",
                    "content": user_input
                })

                ai_response = "I can answer questions about stock, orders, revenue, and discontinued items."

                for item in ai_response_list:
                    if user_input.lower() == item["user"].lower():

                        if item["user"] == "What items are low on stock?":
                            low_stock_items = []

                            for inv in inventory:
                                if inv["stock"] <= 5:
                                    low_stock_items.append(inv["name"])

                            if len(low_stock_items) > 0:
                                answer = "Low stock items: "

                                for low_item in low_stock_items:
                                    answer = answer + low_item + ", "

                                answer = answer[:-2]
                                ai_response = answer
                            else:
                                ai_response = "There are no low stock items."

                        elif item["user"] == "What is the total sales revenue?":
                            total_sales_revenue = 0

                            for order in orders:
                                total_sales_revenue = total_sales_revenue + order["total"]

                            ai_response = f"The total sales revenue is ${total_sales_revenue:.2f}"

                        elif item["user"] == "How many orders were placed today?":
                            total_orders = 0

                            for order in orders:
                                total_orders = total_orders + 1

                            ai_response = f"There are {total_orders} orders."

                        elif item["user"] == "What is the most popular item?":
                            item_count = {}

                            for order in orders:
                                name = order["item"]

                                if name in item_count:
                                    item_count[name] = item_count[name] + order["quantity"]
                                else:
                                    item_count[name] = order["quantity"]

                            most_popular = None
                            highest = 0

                            for name in item_count:
                                if item_count[name] > highest:
                                    highest = item_count[name]
                                    most_popular = name

                            if most_popular is not None:
                                ai_response = f"The most popular item is {most_popular}."
                            else:
                                ai_response = "No sales data yet."

                        elif item["user"] == "What items are discontinued?":
                            if len(discontinued_items) > 0:
                                answer = "Discontinued items: "

                                for discontinued_item in discontinued_items:
                                    answer = answer + discontinued_item + ", "

                                answer = answer[:-2]
                                ai_response = answer
                            else:
                                ai_response = "There are no discontinued items."

                        break

                st.session_state["messages"].append({
                    "role": "assistant",
                    "content": ai_response
                })

            time.sleep(2)
            st.rerun()
    
elif st.session_state["page"] == "register":
    st.title("Register")
    Full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["Employee", "Owner"])
    if st.button("Create Account"):
        email_available = any(user["email"]== email for user in users)
        if not Full_name or not email or not password:
            st.warning("One or more fields missing!")
        elif email_available:
            st.error("Email already taken! ")
        else:
            new_user = {
                "id": len(users) + 1,
                "email": email,
                "full_name": Full_name,
                "password": password,
                "role": role

            }
            users.append(new_user)
            save_users(users, json_path)
            st.success(" Account Created!")
            st.session_state["page"] = "home"
            st.rerun()