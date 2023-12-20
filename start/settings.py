"""
项目配置
"""
from pathlib import Path


# 基础路径
BASE_DIR = Path(__file__).resolve().parent.parent
# 开启调试模式
DEBUG = True
# 定义密钥  https://password.buyaocha.com/ 密钥生成
SECRET_KEY = 't7xbeV>RX^naH56AAYy!e-wdk}/(?dZ4r[C%hc.33TQw&n<{$q'
# 数据库连接信息
SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/security?charset=utf8mb4'



