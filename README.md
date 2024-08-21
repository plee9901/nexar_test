# nexar_test

Dự án xây dựng một đường ống dữ liệu sử dụng Apache Airflow, Google Cloud Storage (GCS), và Bigquery. Nhiệm vụ là tải dữ liệu dạng ndjson, chuyển nó sang dạng CSV và nén thành file Gzip, sau đó tải lên GCS và cuối cùng chuyển từ GCS sang Bigquery. Đường ống dữ liệu được đặt giờ chạy hàng ngày vào 7:00 sáng (Theo giờ Việt Nam).

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/plee9901/nexar_test.git
cd nexar_test
```

### 2. Setup Docker images

Chạy lệnh sau để xây dựng docker images:

```bash
docker compose build
```
## Run project

### 1. Chạy chương trình
Sau khi xây dựng docker images thành công, chạy lệnh sau:

```bash
docker compose up
```
Sử dụng Web UI của airflow để chạy DAGs và theo dõi trạng thái của các task.

### 2. Dừng chương trình
Khi muốn dừng chương trình, chạy lệnh sau:

```bash
docker compose down
```

## Lưu ý: 
- Cần có credentials Google Cloud API key để chạy.
- Nếu muốn tải dữ liệu từ Kaggle, cần bỏ comment trong requirements.txt và download kaggle dataset trong dags/dag_python.py. 
    - Yêu cầu cần có kaggle.json và gắn kaggle.json vào Docker container.




