python3 -m venv venv
source venv/bin/activate
pip install django
---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 使用 MariaDB 也設定 mysql
        'NAME': 'project',                   # 你的資料庫名稱
        'USER': 'root',                      # 資料庫使用者
        'PASSWORD': 'mypass',              # 密碼
        'HOST': 'localhost',                   # 主機
        'PORT': '3306',                        # 預設 MariaDB 連接埠
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

hZCZcf4yT@np8PBQzy

sudo chown -R alvin:alvin /home/alvin/Desktop/django-crm

<a class="btn btn-sm btn-warning" href="{% url 'customer_edit' c.id %}">編輯</a>
      <a class="btn btn-sm btn-danger" href="{% url 'customer_delete' c.id %}">刪除</a>