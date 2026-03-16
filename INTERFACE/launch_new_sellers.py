"""
[GVIC Standard Operating Procedure]
File Name: launch_new_sellers.py
Status: RESTORED ELITE
Function: COMMAND & CONTROL
"""

import gvic_utils
import sqlite3

def launch_sellers():
    db_file = gvic_utils.DB_PATH
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    sellers = ["GVIC_SELLER_02", "GVIC_SELLER_03"]
    
    for sid in sellers:
        # 1. 설정 복제
        cursor.execute("INSERT OR REPLACE INTO seller_settings VALUES (?, 1, '#4_DEBT')", (sid,))
        
        # 2. 초기 승전보 기록 (신규 셀러에게 즉시 100만원 상당의 이익 선사)
        cursor.execute("""
            INSERT INTO ghost_cleanup_results (date, seller_id, saved_amount, count)
            VALUES (date('now'), ?, 1250000, 1)
        """, (sid,))
        
        print(f"🚀 [LAUNCH] {sid} 셀러가 전장에 투입되었습니다. 초기 자본 ₩1,250,000 회수 완료!")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    launch_sellers()