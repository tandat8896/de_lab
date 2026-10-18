# 🚀 Hadoop HDFS (1 NameNode, 2 DataNodes) & Apache Spark (1 Master, 2 Workers)

Cụm phân tán Big Data chuẩn `Big Data Europe (BDE)` được tối ưu hóa cho máy cá nhân / môi trường dev (RAM ~11GB).

---

## 🏗️ Kiến trúc & Bảng cổng kết nối

| Dịch vụ | Tên Container | Cổng trong Container | Cổng trên Host | Web UI / Địa chỉ |
| :--- | :--- | :--- | :--- | :--- |
| **HDFS NameNode UI** | `hadoop-namenode` | 9870 | **`9870`** | [http://localhost:9870](http://localhost:9870) |
| **HDFS NameNode IPC** | `hadoop-namenode` | 9000 | **`9000`** | `hdfs://localhost:9000` |
| **HDFS DataNode 1 UI** | `hadoop-datanode-1` | 9864 | **`9864`** | [http://localhost:9864](http://localhost:9864) |
| **HDFS DataNode 2 UI** | `hadoop-datanode-2` | 9864 | **`9865`** | [http://localhost:9865](http://localhost:9865) |
| **Spark Master UI** | `spark-master` | 8080 | **`8082`** | [http://localhost:8082](http://localhost:8082) *(tránh đụng 8080 của Airflow)* |
| **Spark Master RPC** | `spark-master` | 7077 | **`7077`** | `spark://localhost:7077` |
| **Spark Worker 1 UI** | `spark-worker-1` | 8081 | **`8083`** | [http://localhost:8083](http://localhost:8083) |
| **Spark Worker 2 UI** | `spark-worker-2` | 8081 | **`8084`** | [http://localhost:8084](http://localhost:8084) |

---

## 🧠 Tối ưu hóa bộ nhớ (RAM Limits)

Tổng RAM máy: **~11 GB**. Cấu hình được chia tải an toàn tránh bị tràn RAM (OOM Killer - Exit Code 137):

| Container | Image | Cấu hình RAM nội bộ | Giới hạn Docker (`mem_limit`) |
| :--- | :--- | :--- | :--- |
| **NameNode** | `bde2020/hadoop-namenode:2.0.0-hadoop3.2.1-java8` | Auto Heapsize | Max: **1024 MB** (~1.0 GB) |
| **DataNode 1** | `bde2020/hadoop-datanode:2.0.0-hadoop3.2.1-java8` | Auto Heapsize | Max: **800 MB** (~0.8 GB) |
| **DataNode 2** | `bde2020/hadoop-datanode:2.0.0-hadoop3.2.1-java8` | Auto Heapsize | Max: **800 MB** (~0.8 GB) |
| **Spark Master** | `bde2020/spark-master:3.3.0-hadoop3.3` | `SPARK_DAEMON_MEMORY=512m` | Max: **800 MB** (~0.8 GB) |
| **Spark Worker 1** | `bde2020/spark-worker:3.3.0-hadoop3.3` | `SPARK_WORKER_MEMORY=1G` | Max: **1500 MB** (~1.5 GB overhead) |
| **Spark Worker 2** | `bde2020/spark-worker:3.3.0-hadoop3.3` | `SPARK_WORKER_MEMORY=1G` | Max: **1500 MB** (~1.5 GB overhead) |
| **TỔNG CỘNG** | - | - | **Max ~6.4 GB (Thực tế chạy ~3.5 - 4.5 GB)** |

*Còn dư **~5 GB RAM** cho Airflow, PostgreSQL và hệ điều hành.*

---

## 💾 Persistent Volumes (Lưu trữ bền vững)

- `hadoop_namenode_data`: Metadata HDFS (BDE tự động format NameNode lần đầu, giữ nguyên dữ liệu khi restart).
- `hadoop_datanode1_data`: Khối dữ liệu DataNode 1.
- `hadoop_datanode2_data`: Khối dữ liệu DataNode 2.
- `./apps`: Thư mục mount vào `/opt/spark-apps` bên trong container Spark để chạy script PySpark.

---

## 🚀 Hướng dẫn sử dụng

### 1. Khởi động cụm
```bash
docker compose -f hadoop-spark/docker-compose.yaml up -d
```

### 2. Kiểm tra trạng thái
```bash
docker compose -f hadoop-spark/docker-compose.yaml ps
```

### 3. Kiểm tra HDFS qua dòng lệnh CLI
```bash
# Kiểm tra danh sách live datanodes
docker exec -it hadoop-namenode hdfs dfsadmin -report

# Tạo thư mục trên HDFS
docker exec -it hadoop-namenode hdfs dfs -mkdir -p /test

# Xem nội dung thư mục HDFS
docker exec -it hadoop-namenode hdfs dfs -ls /
```

### 4. Dừng cụm
```bash
docker compose -f hadoop-spark/docker-compose.yaml down
```
*(Thêm `-v` nếu muốn xóa sạch toàn bộ volumes để reset từ đầu: `docker compose -f hadoop-spark/docker-compose.yaml down -v`)*
