import streamlit as st
import mysql.connector
import ast

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="139.5.147.31",
    port=3306,
    user="trong",
    password="c757GL28zN",
    database="trong",
    ssl_disabled=True
)
cursor = mydb.cursor()
cursor.execute("SELECT OrderCode, Product, TotalPrice, CustomerNote FROM customer_order")
data = cursor.fetchall()

st.title('รายการคำสั่งซื้อทั้งหมด')

for product in data:
    OrderCode, Product, TotalPrice, CustomerNote = product
    product_dict = ast.literal_eval(Product)
    with st.form(key=f'form_{OrderCode}'):
        st.write(OrderCode)
        st.write("**สินค้า:**")
        for item_name, item_quantity in product_dict.items():
            st.write(f"- {item_name} จำนวน {item_quantity}")
        st.write(f'**ราคารวม:** :red[{TotalPrice} ฿]')
        st.write(f'**โน้ตถึงร้านค้า:** {CustomerNote}')
        
        # ใส่ st.form_submit_button() ภายในบล็อกของ with st.form()
        if st.form_submit_button(label='Finish', use_container_width=True):
            # Insert into history_order table
            cursor.execute("INSERT INTO history_order (ordercode) VALUES (%s)", (OrderCode,))
            mydb.commit()
            
            # Delete from orders table
            cursor.execute("DELETE FROM customer_order WHERE OrderCode=%s", (OrderCode,))
            mydb.commit()
            
            st.toast(f'Order {OrderCode} deleted successfully! The order is ready for pickup.', icon='❎')

# Close the cursor and database connection outside the loop
cursor.close()
mydb.close()
