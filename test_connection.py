import pymysql

def test_mysql_connection(host, port, user, password, database):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user, 
            password=password,
            database=database
        )
        print("連線成功!")
        connection.close()
    except Exception as e:
        print(f"連線失敗: {e}")
def test_mysql_insert(host, port, user, password, database):
    try:
        connection = pymysql.connect(
            host=host,      
            port=port,
            user=user, 
            password=password,
            database=database
        )
        
        cursor = connection.cursor()
        
        # 創建測試表格
        create_table_query = """
        CREATE TABLE IF NOT EXISTS test_table (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100)
        )
        """
        cursor.execute(create_table_query)
        
        # 插入測試數據
        insert_query = "INSERT INTO test_table (name, email) VALUES (%s, %s)"
        test_data = ('Test User', 'test@example.com')
        
        cursor.execute(insert_query, test_data)
        connection.commit()
        
        print("插入成功!")
        
    except pymysql.Error as e:
        print(f"發生錯誤: {e}")
        
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
# 使用範例
test_mysql_connection('140.120.14.103', 3306, 'student7112056043', '7112056043', 'student7112056043_db')
test_mysql_insert('140.120.14.103', 3306, 'student7112056043', '7112056043', 'student7112056043_db')