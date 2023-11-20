import streamlit as st
import mysql.connector

# Connect to MySQL database
mydb = mysql.connector.connect(
        host="139.5.147.31",
        port="3306",
        user="trong",
        password="c757GL28zN",
        database="trong",
        use_pure=True
)
cursor = mydb.cursor()
cursor.execute("SELECT OrderCode, Product, TotalPrice, CustomerNote FROM customer_order")
data = cursor.fetchall()

st.title('รายการคำสั่งซื้อทั้งหมด')

# Use st.form() outside the loop to manage the form submission
form = st.form(key='delete_form')

for product in data:
    OrderCode, Product, TotalPrice, CustomerNote = product
    with form:
        st.write(OrderCode)
        st.write(Product)
        st.write(f'**ราคารวม:** :red[{TotalPrice} ฿]')
        st.write(f'**โน้ตถึงร้านค้า:** {CustomerNote}')
        
        if form.form_submit_button(label=f'Delete {OrderCode}', help=f'Click to delete order {OrderCode}'):
            # Insert into history_order table
            cursor.execute("INSERT INTO history_order (ordercode) VALUES (%s)", (OrderCode,))
            # Delete from orders table
            cursor.execute("DELETE FROM customer_order WHERE OrderCode=%s", (OrderCode,))
    
# Commit changes outside the loop
mydb.commit()

# Show success message if deletion is successful
if form.form_submit_button(label='Finish', help='Finish deleting orders'):
    st.success("Selected orders deleted successfully!")

# Close the cursor and database connection
cursor.close()
mydb.close()
