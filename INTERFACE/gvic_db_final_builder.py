"""
[GVIC Standard Operating Procedure]
File Name: gvic_db_final_builder.py
Status: RESTORED ELITE
Function: COMMAND & CONTROL
"""

# C:\gvic\gvic_server\scripts\gvic_db_final_builder.py
import sqlite3
import os
import gvic_utils
import gvic_logger

def force_rebuild_db():
    gvic_logger.write_log("BUILDER", "DB 재건축 프로세스 시작", "START")
    db_path = gvic_utils.DB_PATH
    
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            gvic_logger.write_log("BUILDER", f"기존 DB 파일 삭제 완료: {db_path}", "INFO")
        except Exception as e:
            gvic_logger.write_log("BUILDER", f"DB 삭제 실패: {e}", "ERROR")
            return False

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 테이블 생성
        cursor.execute('''CREATE TABLE inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            master_sku TEXT UNIQUE NOT NULL,
            product_name TEXT NOT NULL,
            current_stock INTEGER DEFAULT 0,
            price INTEGER DEFAULT 0
        )''')
        cursor.execute('''CREATE TABLE product_mapping (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            market_name TEXT, market_code TEXT, master_sku TEXT, internal_product_name TEXT
        )''')
        
        conn.commit()
        conn.close()
        gvic_logger.write_log("BUILDER", "최신 스키마(market_code 포함) 구축 성공", "SUCCESS")
        return True
    except Exception as e:
        gvic_logger.write_log("BUILDER", f"DB 생성 중 치명적 오류: {e}", "ERROR")
        return False

if __name__ == "__main__":
    force_rebuild_db()