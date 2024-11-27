# MySQL教學實驗室管理系統 - 安裝與使用指南

## 1. 系統架構

* 容器化MySQL伺服器
* Docker部署
* 多使用者權限管理

## 2. 系統需求

* Docker Desktop
* Python 3.8+

## 3. 安裝步驟

### 3.1 環境準備

1. 安裝Docker Desktop

### 3.2 Docker Compose配置

``` yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    container_name: LAB-mysql
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: LABdb
      MYSQL_USER: Member1
      MYSQL_PASSWORD: Member1
    ports:
      - "0.0.0.0:3306:3306"
    volumes:
      - mysql-data:/var/lib/mysql
      - ./init:/docker-entrypoint-initdb.d
    restart: always
    command: 
      - --bind-address=0.0.0.0  # 允許外部連線
      - --default-authentication-plugin=mysql_native_password  # 確保密碼兼容性

volumes:
  mysql-data:
```

### 3.3 使用Docker 容器自動化設定學生db

#### 在 init/ 資料夾下新增一個init.sql

``` csharp
project/
├── docker-compose.yml
├── init/
    └── init.sql
```

#### 將所有學生db建立完成並設定好權限

``` sql
CREATE DATABASE student7112056043_db;
CREATE USER 'student7112056043'@'%' IDENTIFIED BY 'student7112056043';
GRANT ALL PRIVILEGES ON student7112056043_db.* TO 'student7112056043'@'%';

CREATE DATABASE student7112056023_db;
CREATE USER 'student7112056023'@'%' IDENTIFIED BY 'student7112056023';
GRANT ALL PRIVILEGES ON student7112056023_db.* TO 'student7112056023'@'%';

FLUSH PRIVILEGES;
```

### 3.4 啟動MySQL

``` bash
docker-compose up -d
```

## 4. 使用者管理

### 4.1 進入MySQL

#### 使用 root 登入 (輸入密碼: *MYSQL_ROOT_PASSWORD* )

``` bash
docker exec -it student-mysql mysql -u root -p
```

### 4.2 使用者權限設定

#### 限制root的連接來源只能在localhost

``` sql
DELETE FROM mysql.user WHERE User='root' AND Host='%';
FLUSH PRIVILEGES;
```

#### 建立完整存取權限的使用者(admin換成老師或是助教)

``` sql
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'adminpassword';
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```

#### 查看使用者及其可登入的限制

``` sql
SELECT User, Host FROM mysql.user;
```

| user              | host          |
| -------------     |:-------------:|
| student7112056023 | %             |
| student7112056043 | %             |
| mysql.infoschema  | localhost     |
| mysql.session     | localhost     |
| mysql.sys         | localhost     |
| root              | localhost     |
| admin             | localhost     |

#### 建立完整存取權限的內網使用者

``` sql
CREATE USER 'TA_name'@'172.18.0.%' IDENTIFIED BY 'yourpassword';
GRANT ALL PRIVILEGES ON *.* TO 'TA_name'@'172.18.0.%';
FLUSH PRIVILEGES;
```

## 5. 連線測試腳本

### 5.1 資料庫連線測試

``` python
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

test_mysql_connection('serverIP', 3306, 'student7112056043', 'student7112056043', 'student7112056043_db')
```

### 5.2 資料插入測試

``` python
import pymysql

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

test_mysql_insert('140.120.14.103', 3306, 'student7112056043', '7112056043', 'student7112056043_db')
```
