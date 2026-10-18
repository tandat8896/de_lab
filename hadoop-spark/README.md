# 🚀 Hadoop HDFS (1 NameNode, 2 DataNodes) & Apache Spark (1 Master, 2 Workers)

Cụm phân tán Big Data thu nhỏ được tối ưu hóa cho máy cá nhân / môi trường dev (RAM ~11GB).

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

Tổng RAM khả dụng trên máy: **~11 GB**. Cấu hình được chia tải vừa phải để máy không bị tràn RAM/OOM:

| Container | Heapsize (JVM) | Giới hạn Docker (`mem_limit`) |
| :--- | :--- | :--- |
| **NameNode** | 256MB - 768MB | Max: 1200MB (~1.2GB) |
| **DataNode 1** | 128MB - 512MB | Max: 800MB (~0.8GB) |
| **DataNode 2** | 128MB - 512MB | Max: 800MB (~0.8GB) |
| **Spark Master** | 512MB | Max: 800MB (~0.8GB) |
| **Spark Worker 1** | 1GB Worker Memory | Max: 1200MB (~1.2GB) |
| **Spark Worker 2** | 1GB Worker Memory | Max: 1200MB (~1.2GB) |
| **TỔNG CỘNG** | - | **Max ~6.0 GB (Thực tế chạy ~3.5 - 4.5 GB)** |

*Còn thừa khoảng **5-6 GB RAM** cho Airflow, Postgres và hệ điều hành hoạt động mượt mà.*

---

## 💾 Persistent Volumes (Lưu trữ bền vững)

Dữ liệu được lưu trữ trong các named volume Docker, không bị mất khi restart container:
- `hadoop_namenode_data`: Metadata của HDFS NameNode.
- `hadoop_datanode1_data`: Khối dữ liệu (blocks) trên DataNode 1.
- `hadoop_datanode2_data`: Khối dữ liệu (blocks) trên DataNode 2.
- `spark_master_data` & `spark_worker*_data`: Trạng thái và work directories của Spark.
- `./apps`: Thư mục mount trực tiếp từ host vào container (`/opt/spark-apps`) để chứa mã nguồn PySpark.

---

## 🚀 Hướng dẫn sử dụng

### 1. Khởi động cụm
Từ thư mục gốc dự án:
```bash
docker compose -f hadoop-spark/docker-compose.yaml up -d
```
*(Hoặc `cd hadoop-spark && docker compose up -d`)*

> [!NOTE]
> NameNode sẽ **tự động kiểm tra và format lần đầu tiên** nếu thư mục volume trống. Những lần restart sau sẽ giữ nguyên dữ liệu mà không format lại.

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

### 4. Chạy thử script PySpark đọc/ghi HDFS
Một file script mẫu đã được chuẩn bị sẵn trong `apps/test_spark_hdfs.py`:
```bash
docker exec -it spark-master spark-submit /opt/spark-apps/test_spark_hdfs.py
```

### 5. Dừng cụm
```bash
docker compose -f hadoop-spark/docker-compose.yaml down
```
*(Nếu muốn xóa sạch toàn bộ dữ liệu volume để bắt đầu lại: thêm cờ `-v`: `docker compose -f hadoop-spark/docker-compose.yaml down -v`)*
