# 📦 S3 CLI Tool (Python)

A custom command-line tool to manage Amazon S3 buckets and objects using Python.

Built with **boto3** and **argparse**, this tool provides AWS S3-like functionality directly from the terminal.

---

## 🚀 Features

* Create S3 buckets
* Upload & download files
* Configure bucket settings
* Manage bucket policies
* Enable / disable versioning
* List objects with prefix filtering
* List object versions (including delete markers)
* Delete objects
* Fully empty and delete buckets

---

## 🧰 Requirements

* Python 3.8+
* AWS credentials configured
* boto3 installed

Install dependencies:

```bash
pip install boto3
```

Configure AWS credentials:

```bash
aws configure
```

---

## 📁 Project Structure

```
project/
│
├── main.py   # S3Manager class (all AWS logic)
├── app.py    # CLI entry point
└── README.md
|__policy.json #change the policy based on your bucket name
|__public_access_configuration.json 
|__data
|__downloads
|__images

```
## 📄 Configuration Files

This project uses two JSON configuration files to manage bucket settings for Amazon S3 via boto3.

---

### 🔐 1. `policy.json`

Used to define the **S3 bucket policy** (permissions such as public access or restricted access).

Example:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicRead",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME/*"
    }
  ]
}
```

📌 Used in:

```bash
python app.py putpolicy <bucket_name>
```

---

### ⚙️ 2. `access_configuration.json`

Used to control **S3 Public Access Block settings**, such as:

* blocking public ACLs
* allowing or restricting public bucket access

Example:

```json
{
  "BlockPublicAcls": false,
  "IgnorePublicAcls": false,
  "BlockPublicPolicy": false,
  "RestrictPublicBuckets": false
}
```

📌 Used in:

```bash
python app.py putconfiguration <bucket_name>
```

---

## 🧠 Important Notes

* These files are loaded by `main.py` when running configuration commands
* Modify them carefully—wrong settings can expose your bucket publicly
* JSON syntax must be valid (no trailing commas, lowercase booleans)

---

## ⚠️ Safety Warning

Misconfiguring these files may:

* expose data publicly
* allow unintended access to your bucket
* violate security best practices of Amazon Web Services


---

## ⚙️ Commands

### 🧱 Create bucket

```bash
python app.py create my-bucket
```

---

### 📤 Upload file

```bash
python app.py upload my-bucket data/images/brain2.png images/brain2.png
```

---

### 📥 Download file

```bash
python app.py download my-bucket images/brain2.png downloads/brain2.png
```

---

### ⚙️ Bucket configuration

```bash
python app.py putconfiguration my-bucket
python app.py getconfiguration my-bucket
```

---

### 🔐 Bucket policy

```bash
python app.py putpolicy my-bucket
python app.py getpolicy my-bucket
```

---

### 🔁 Versioning

```bash
python app.py versioning my-bucket true
python app.py versioning my-bucket false
```

---

### 📂 List objects

```bash
python app.py list my-bucket
python app.py list my-bucket --prefix images/
```

---

### 🧾 List object versions

```bash
python app.py listversions my-bucket
python app.py listversions my-bucket --prefix images/
```

---

### 🗑 Delete object

```bash
python app.py deleteobject my-bucket images/brain2.png
```

---

### 🧨 Delete bucket (full wipe)

```bash
python app.py deletebucket my-bucket
```

---

## 🧠 Key Concepts

* **Bucket** → container for S3 objects
* **Key** → file path inside bucket
* **Prefix** → folder-like filter
* **Versioning** → keeps multiple object versions
* **Delete marker** → soft delete in versioned buckets

---

## ⚠️ Safety Notes

* Bucket names must be globally unique
* Deletions are irreversible
* Versioned buckets may retain hidden data
* Always double-check before deleting buckets

---

## 📌 Example Workflow

```bash
python app.py create demo-bucket
python app.py upload demo-bucket data/images/brain2.png images/brain2.png
python app.py list demo-bucket --prefix images/
python app.py versioning demo-bucket true
python app.py listversions demo-bucket
python app.py deletebucket demo-bucket
```

---

## 🚀 Future Improvements

* Progress bar for uploads
* Recursive folder upload
* JSON/CSV export
* Dry-run mode for safety
* Multi-account AWS support

---

## 👨‍💻 Author

Built as a learning project to understand AWS S3 + Python CLI design.


