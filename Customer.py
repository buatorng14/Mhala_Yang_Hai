import streamlit as st
import sqlite3
import json
from streamlit_lottie import st_lottie
import mysql.connector



#ติดต่อฐานข้อมูล MySQL
mydb = mysql.connector.connect(
  host="sql12.freesqldatabase.com",
  port="3306",
  user="sql12662953",
  password="xxhfidUS7g",
  database="sql12662953"
)

# ติดต่อฐานข้อมูล SQL
conn = sqlite3.connect('dbproject.db')
cursor = conn.cursor()  # สร้าง cursor
mycursor = mydb.cursor()

# ปฏิบัติการ SQL 
cursor.execute("SELECT IDproduct, NameProduct, PricePerUnit, Image FROM ProduceInfo")
data = cursor.fetchall()


# Function for creating GIF
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


# Create a dictionary to store product information in the shopping cart
cart = {}
shopping_cart = {}

class CartItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.quantity = 1

    def increase_quantity(self):
        self.quantity += 1

    def decrease_quantity(self):
        if self.quantity > 0:
            self.quantity -= 1
            if self.quantity == 0:
                return self.name  # Return the item name when quantity becomes zero
        return None  # Return None if quantity is not zero

def set_to_begin():
    return None  

# Function to handle the delete button click
def handle_delete_button(item_name):
    if item_name is not None and item_name in shopping_cart:
        del shopping_cart[item_name]

# Create a shopping cart
shopping_cart = st.session_state.get("cart", {})

#กำหนดค่า session_state
if 'stage' not in st.session_state:
    st.session_state.stage = 0

def set_state(i):
    st.session_state.stage = i

if st.session_state.stage == 0 :
# Optin
    st.set_page_config(page_title="Ping Yang MHALA" , page_icon=":tada:",layout="wide")

    def load_lottiefile(filepath: str):
        with open(filepath, 'r') as f:
            return json.load(f)

    # Local CSS
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}<style>", unsafe_allow_html=True)

    # Load assets
    local_css("style.css")
    lottie_duck = load_lottiefile(("Duck.json"))


    # Header
    with st.container():
        left_column, right_column = st.columns(2)
        with left_column:
            st.subheader("Hi :wave:, Welcome to ours website!!")
            st.title("Ping Yang MHALA")
            st.write("We are passionate about giving you with the happiness")
        # Apply CSS to center the duck animation
        with right_column:
            st.markdown(
                """
                <style>
                    .centered-duck {
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        height: 100%;
                        margin-right: 20px; /* Adjust the margin as needed */
                    }
                </style>
                """,
                unsafe_allow_html=True
            )

            # Add the centered duck animation
            st.markdown(
                """
                <div class="centered-duck">
                    <div>
                        {}
                    </div>
                </div>
                """.format(st_lottie(lottie_duck, speed=1, height=150, key="duck")),
                unsafe_allow_html=True
            )
    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        with left_column:
            st.header('About Us')
            st.write('This website has been created by a group of students who identified challenges related to queuing at a local restaurant. The decision to build this website was driven by the desire to address both customer waiting times and improve the organization of order processing for the business.')
            st.write()
            st.write("Upon entering the website, users can expect a convenient and efficient experience without long waiting times. Additionally, the website aims to assist in organizing the restaurant's order processing, streamlining operations for a smoother and more effective workflow.")
        with right_column:
            st.header('')
            st.image("Pic1.jpg", caption="Ping Yang MHALA", use_column_width=True)

    with st.container():
        st.write('---')
        st.button('Go to Shop', key="back3", on_click=lambda: (set_state(1)), use_container_width=True)


    with st.container():
        st.write("---")
        st.header("Comment Us")

        comment_form = """
        <form action="https://formsubmit.co/mhalapingyang@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your Email" required>
        <textarea name="comment" placeholder="Your comment here" required></textarea>
        <button type="submit">Send</button>
        </form>
        """

        st.markdown(comment_form, unsafe_allow_html=True)

    

#Main page    
if st.session_state.stage == 1 :
    st.markdown("<h1 style='text-align: center;'>รายการสินค้า</h1>", unsafe_allow_html=True)
    #ไปหน้าตะกร้าสินค้า   
    st.button(':shopping_trolley: ตะกร้าสินค้า', on_click=set_state, args=[2] ,use_container_width=True)
    #ปุ่มตรวจสอบสินค้า
    st.button('ตรวจสอบสถานะ',key=1,on_click=set_state, args=[6], use_container_width=True)
    # Search input
    search_manu = st.text_input("Search manu:", "")

    for product in data:
        IDproduct, NameProduct, PricePerUnit, Image = product
        existing_item = st.session_state.get(NameProduct, None)
        if existing_item:
            existing_item["จำนวน"] += 1

        # Check if the product matches the search input
        if search_manu.lower() in NameProduct.lower():
            col1, col2, col3 = st.columns(3)
            with col1:
                st.image(Image, caption=NameProduct, use_column_width=True)

            with col2:
                st.markdown(f"**ชื่อสินค้า:** {NameProduct}")
                st.write(f'**ราคา:** :red[{PricePerUnit} ฿]', unsafe_allow_html=True)

            with col3:
                if st.button("เพิ่มสินค้าในตะกร้า", key=f"button_{IDproduct}"):
                    if NameProduct in shopping_cart:
                        shopping_cart[NameProduct].increase_quantity()
                    else:
                        shopping_cart[NameProduct] = CartItem(NameProduct, PricePerUnit)
                    st.success('เพิ่มสินค้าสำเร็จ', icon="✅")
            st.divider()


# Update the cart in the session state    
st.session_state.cart = shopping_cart
    
total_price=0

#Basket page
if st.session_state.stage == 2:
    st.title("สินค้าของคุณอยู่ที่นี่")

    # Function to display and update the shopping cart in the sidebar
    def display_shopping_cart():
        for item_name, item in shopping_cart.items():
            # Display product name, price, quantity, and buttons to increase or decrease quantity
            if item.quantity > 0:
                col1, col2, col3, col4 ,col5 = st.columns([2, 2, 1, 0.7, 1])
                col1.write(item.name)
                col2.write(f"ราคา: {item.price} ฿  :gray[({item.quantity} ชิ้น)]")
                col3.button(":heavy_minus_sign:", key=f"decrease_{item_name}", on_click=decrease_quantity, args=(item_name,))
                col4.write( f'{item.quantity}')
                col5.button(":heavy_plus_sign:", key=f"increase_{item_name}", on_click=increase_quantity, args=(item_name,))

        # Calculate and display the total price in the sidebar
        total_price = sum(item.price * item.quantity for item in shopping_cart.values())
        st.markdown(f"**ยอดรวมสินค้า: {total_price} ฿**  :gray[({sum(item.quantity for item in shopping_cart.values())} ชิ้น)]")
        return total_price

    # Function to increase the quantity of a product
    def increase_quantity(item_name):
        shopping_cart[item_name].increase_quantity()

    # Function to decrease the quantity of a product
    def decrease_quantity(item_name):
        shopping_cart[item_name].decrease_quantity()

    display_shopping_cart()

    # # Update the cart in the session state
    # st.session_state.cart = shopping_cart
    col1, col2 = st.columns(2)
    item_quantity = 0
    for item_name, item in shopping_cart.items():
        item_quantity +=item.quantity

    with col1:
            st.button('ย้อนกลับ',key = 1, on_click=set_state, args=[1],use_container_width=True)
    with col2:        
        if item_quantity>0:
            st.button('ถัดไป',key='ถัดไป1', on_click=set_state, args=[3],use_container_width=True)
        elif item_quantity<=0:
            if st.button('ถัดไป',key='ถัดไป2', on_click=set_state,args=[2],use_container_width=True):
                st.error('คุณไม่สินค้าที่เลือก กรุณาเพิ่มสินค้าเข้ามาในตะกร้า',icon='❌')
                
def set_state(new_state):
    st.session_state.stage = new_state
#Summary page
if st.session_state.stage == 3:
    st.title("Summary page")
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
    # Create a container (column) to display the summary section
    for item_name, item in shopping_cart.items():
        if item.quantity > 0:
            with col1:
                st.write(item.name)
            with col2:
                st.write(f"จำนวน: {item.quantity}")
            with col3:
                st.write(f"ราคา: :red[{item.price} ฿]")
            with col4:
                item_total_price = item.price * item.quantity
                st.write(f"ราคารวม: :red[{item_total_price} ฿]")
        # Calculate and display the total price for all items
    total_price = sum(item.price * item.quantity for item in shopping_cart.values())
    st.markdown(f"**ยอดรวมสินค้า: :red[{total_price} ฿]**  :gray[({sum(item.quantity for item in shopping_cart.values())} ชิ้น)]")
    store_note = st.text_area("โน้ตถึงร้านค้า (ทั้งหมด):", key="store_note")
    name_customer = st.text_area("ชื่อของผู้ซื้อ:", key="name_customer")
    col1, col2 = st.columns(2)
    with col1:
        st.button('ย้อนกลับ', key=2, on_click=set_state, args=[2], use_container_width=True)
    with col2:
        if not name_customer:
            if st.button('SUBMIT',key='submit1', on_click=set_state, args=[3], use_container_width=True):
                st.warning('โปรดใส่ชื่อผู้สั่งซื้อด้วย')
        else:
            mycursor.execute("SELECT * FROM customer_order WHERE OrderCode=%s", (name_customer,))
            result = mycursor.fetchone()
            if result:
                if st.button('SUBMIT',key='submit3', on_click=set_state, args=[3], use_container_width=True):
                    st.warning('ชื่อนี้มีอยู่แล้ว กรุณาเปลี่ยนชื่อ')
            else:
                st.button('SUBMIT',key='submit2', on_click=set_state, args=[4], use_container_width=True)
            
# สรุปใบคำสั่งซื้อ
if st.session_state.stage == 4:
    st.title("ใบรายการคำสั่งซื้อ")
    total_price = sum(item.price * item.quantity for item in shopping_cart.values())
    order_data = {
        "items": shopping_cart,
        "total_price": total_price,
        "customer_note": st.session_state.store_note,
        "customer_name": st.session_state.name_customer,}
    if order_data:
        st.markdown("**สรุปรายการสั่งซื้อ**", unsafe_allow_html=True)
        "---"
        st.write(f"ออเดอร์ของคุณ: {order_data['customer_name']}")
        st.divider()

        # Create a dictionary to store product quantities
        product_quantities = {}

        for item_name, item_info in order_data["items"].items():
            item = item_info
            item_quantity = item.quantity
            item_price = item.price
            item_total_price = item_quantity * item_price
            if item_quantity > 0:
                product_quantities[item_name] = item_quantity
                st.markdown(f"{item_name}")
                col1, col2, col3 = st.columns([1, 1, 1])
                col1.markdown(f":gray[{item_price} ฿]")
                col2.markdown(f":gray[x {item_quantity}]")
                col3.markdown(f":gray[{item_total_price} ฿]")

        st.divider()
        st.write(f"**ยอดรวมทั้งหมด: {order_data['total_price']} ฿**")
        st.divider()
        st.write(f"โน้ตถึงร้านค้า (ทั้งหมด): {order_data['customer_note']}")
        
        # Convert dictionary to JSON string before inserting
        # Insert data into the orders table
        mycursor.execute("INSERT INTO customer_order (OrderCode, Product,TotalPrice,CustomerNote) VALUES (%s, %s, %s, %s)",(order_data['customer_name'], str(product_quantities),int(order_data['total_price']), str(order_data["customer_note"])))
        mydb.commit()
        

        col1, col2 = st.columns(2)
        col1.button('กลับหน้าหลัก', key="back1",on_click=lambda: (set_state(0), st.session_state.update(cart={})), use_container_width=True)
        col2.button('สถานะสินค้า', on_click=set_state, args=[5], use_container_width=True)
        st.session_state.order_data = order_data
        st.write(product_quantities)
        

# แสดงสถานะสินค้า
if st.session_state.stage == 5:
    col1, col2 = st.columns(2)
    ordercode = st.session_state. order_data['customer_name']
    col1.button('กลับหน้าหลัก', key="back2",on_click=lambda: (set_state(0), st.session_state.update(cart={})), use_container_width=True)
    if col2.button('ตรวจสอบสถานะอีกครั้ง',on_click=set_state, args=[5], use_container_width=True):
        st.markdown("<h2 style='text-align: center;'>สถานะสินค้า</h2>", unsafe_allow_html=True)
        st.markdown("""<div style='text-align: center;'>ออร์เดอร์ของคุณ</div>""", unsafe_allow_html=True)
        if ordercode:
            # Check if the product code exists in the database.
            query = "SELECT * FROM customer_order WHERE OrderCode=%s"
            mycursor.execute(query, (ordercode,))
            result = mycursor.fetchone() 
            query2 = "SELECT * FROM history_order WHERE OrderCode=%s"
            mycursor.execute(query2, (ordercode,))
            result1 = mycursor.fetchone()
            st.markdown(f"""<div style='text-align: center;'>รหัสสินค้า: {ordercode}</div>""", unsafe_allow_html=True)
            if result:
                st.markdown(f"""<div style='text-align: center; color: red;'>อาหารของคุณกำลังทำอยู่</div>""", unsafe_allow_html=True)
                col1,col2,col3=st.columns([1,2,1])
                #insert incorrect GIF
                with col2:
                    incorrect_gif = load_lottiefile("incorrect.json")
                    st_lottie(
                        incorrect_gif,
                        speed=2,
                        reverse=False,
                        loop=False,
                        quality="low",
                        height=560,
                        width=560,
                        key='incorrect',
                        )
            elif result1:
                st.markdown(f"""<div style='text-align: center; color: green;'>อาหารเสร็จแล้วมารับได้เลย</div>""", unsafe_allow_html=True)
                col1,col2,col3=st.columns([1,2,1])
                #insert correct GIF
                with col2:
                    correct_gif = load_lottiefile("correct.json")
                    st_lottie(
                        correct_gif,
                        speed=2,
                        reverse=False,
                        loop=False,
                        quality="low",
                        height=560,
                        width=560,
                        key='correct',
                        )
            else:st.markdown(f"""<div style='text-align: center; color: red;'>ไม่มีรายการอาหารขอคุณกรุณาสั่งอาหาร</div>""", unsafe_allow_html=True)
                
if st.session_state.stage == 6:
    name_chek = st.text_area("ชื่อของผู้ซื้อ:")
    col1, col2 = st.columns(2)
    col1.button('กลับหน้าหลัก', key="back3",on_click=lambda: (set_state(0), st.session_state.update(cart={})), use_container_width=True)
    if not name_chek :
            if col2.button('ตรวจสอบสถานะอีกครั้ง',key="chek1",on_click=set_state, args=[6], use_container_width=True):
                st.warning('โปรดใส่ชื่อผู้สั่งซื้อด้วย')
    else :
        if col2.button('ตรวจสอบสถานะอีกครั้ง',on_click=set_state, args=[6], use_container_width=True):
            st.markdown("<h2 style='text-align: center;'>สถานะสินค้า</h2>", unsafe_allow_html=True)
            st.markdown("""<div style='text-align: center;'>ออร์เดอร์ของคุณ</div>""", unsafe_allow_html=True)
            if name_chek:
                
                # Check if the product code exists in the database.
                query = "SELECT * FROM customer_order WHERE OrderCode=%s"
                mycursor.execute(query, (name_chek,))
                result = mycursor.fetchone() 
                
                query2 = "SELECT * FROM history_order WHERE OrderCode=%s"
                mycursor.execute(query2, (name_chek,))
                result1 = mycursor.fetchone()
                
                st.markdown(f"""<div style='text-align: center;'>รหัสสินค้า: {name_chek}</div>""", unsafe_allow_html=True)
                if result:
                    st.markdown(f"""<div style='text-align: center; color: red;'>อาหารของคุณกำลังทำอยู่</div>""", unsafe_allow_html=True)
                    col1,col2,col3=st.columns([1,2,1])
                #insert incorrect GIF
                    with col2:
                        #insert incorrect GIF
                        incorrect_gif = load_lottiefile("incorrect.json")
                        st_lottie(
                            incorrect_gif,
                            speed=2,
                            reverse=False,
                            loop=False,
                            quality="low",
                            height=560,
                            width=560,
                            key='incorrect',
                            ) 
                elif result1:
                    st.markdown(f"""<div style='text-align: center; color: green;'>อาหารเสร็จแล้วมารับได้เลย</div>""", unsafe_allow_html=True)
                    col1,col2,col3=st.columns([1,2,1])
                #insert incorrect GIF
                    with col2:
                        correct_gif = load_lottiefile("correct.json")
                        st_lottie(
                            correct_gif,
                            speed=2,
                            reverse=False,
                            loop=False,
                            quality="low",
                            height=560,
                            width=560,
                            key='correct',
                            )
                else:st.markdown(f"""<div style='text-align: center; color: red;'>ไม่มีรายการอาหารขอคุณกรุณาสั่งอาหาร</div>""", unsafe_allow_html=True)

    # ปิดการเชื่อมต่อ
    conn.close()
    mycursor.close()
    mydb.close()
    
