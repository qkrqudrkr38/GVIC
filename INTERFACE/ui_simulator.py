"""
[GVIC Standard Operating Procedure]
File Name: ui_simulator.py
Status: RESTORED ELITE
Function: COMMAND & CONTROL
"""

import gvic_utils
import sqlite3
import time

def show_owner_dashboard(seller_id):
    db_file = gvic_utils.DB_PATH
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # [안전장치] 테이블이 없으면 빈 상태로 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS seller_settings (
            seller_id TEXT PRIMARY KEY,
            automation_enabled INTEGER,
            primary_target TEXT
        )
    ''')
    conn.commit()

    # 1. 현재 가용 자금 조회
    cursor.execute("SELECT SUM(saved_amount) FROM ghost_cleanup_results WHERE seller_id=?", (seller_id,))
    available_cash = cursor.fetchone()[0] or 0
    
    # 2. 설정 조회
    cursor.execute("SELECT primary_target FROM seller_settings WHERE seller_id=?", (seller_id,))
    result = cursor.fetchone()
    target = result[0] if result else "#미정(설정필요)"

    # 3. 대시보드 UI 렌더링
    print("\n" + "="*60)
    print(f" 🏛️  GVIC OWNER DASHBOARD - [{seller_id}]")
    print("="*60)
    print(f" [상태] 거버넌스 모드: 수동 승인 (MANUAL)")
    print(f" [자금] 이번 달 회복된 순이익: ₩{available_cash:,}")
    print(f" [권고] 설정된 최우선 타겟: {target}")
    print("-" * 60)
    
    if available_cash == 0:
        print(" ⚠️ 현재 회복된 현금이 없습니다. 먼저 유령 소탕을 실행하세요.")
        conn.close()
        return

    choice = input(f" 🔔 [{target}] 항목으로 집행하시겠습니까? (Y/N): ").upper()

    if choice == 'Y':
        print("\n 🚀 [집행 중] 자본 이동 프로토콜 가동...")
        time.sleep(1.5)
        print(f" ✅ [완료] ₩{available_cash:,}원이 {target}에 성공적으로 투입되었습니다.")
    else:
        print("\n ✋ [보류] 오너의 다음 지시를 기다립니다.")

    conn.close()

if __name__ == "__main__":
    show_owner_dashboard("GVIC_OPERATOR_01")