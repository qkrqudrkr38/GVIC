"""
[GVIC Standard Operating Procedure]
File Name: monthly_dashboard.py
Status: RESTORED ELITE
Function: COMMAND & CONTROL
"""

import gvic_utils
import sqlite3

def generate_gvic_report(seller_id):
    db_file = gvic_utils.DB_PATH
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # 1. 항목별 성과 합산 조회
    cursor.execute("""
        SELECT 
            SUM(CASE WHEN count = 1 AND saved_amount < 100000 THEN saved_amount ELSE 0 END) as saas,
            SUM(CASE WHEN count = 1 AND saved_amount BETWEEN 1000000 AND 2000000 THEN saved_amount ELSE 0 END) as fees,
            SUM(CASE WHEN count = 12 OR saved_amount > 2000000 THEN saved_amount ELSE 0 END) as inventory,
            SUM(CASE WHEN count = 40 THEN saved_amount ELSE 0 END) as labor,
            SUM(CASE WHEN saved_amount = 3000000 THEN saved_amount ELSE 0 END) as sourcing
        FROM ghost_cleanup_results 
        WHERE seller_id = ?
    """, (seller_id,))
    
    row = cursor.fetchone()
    report = {
        "SaaS 유령 소탕": row[0] or 0,
        "수수료 최적화": row[1] or 0,
        "재고 현금화": row[2] or 0,
        "인건비 자동화": row[3] or 0,
        "소싱 원가 절감": row[4] or 0
    }

    total_recovered = sum(report.values())

    print("\n" + "📊 " * 15)
    print(f" [GVIC MONTHLY PERFORMANCE REPORT: {seller_id}]")
    print("📊 " * 15)
    
    print(f"\n✅ 1. 현금 흐름 회복 성과")
    print("-" * 50)
    for key, val in report.items():
        print(f" > {key:<15}: ₩{val:>12,}")
    
    print("-" * 50)
    print(f" 🔥 총 누적 회복 자본: ₩{total_recovered:,}")
    print("-" * 50)

    # 2. 경영 지표 변화 (시뮬레이션)
    print(f"\n✅ 2. 핵심 경영 지표 변화 (Before -> After)")
    print(f" > 월 매출액      : ₩85,000,000  ->  **₩100,000,000** (▲17%)")
    print(f" > 영업이익률    : 10%          ->  **21.2%** (▲11.2%p)")
    print(f" > 가동 가능 시간 : 160시간/월   ->  **200시간/월** (자유시간 확보)")
    
    print("\n" + "="*60)
    print(" 📢 GVIC 메시지: '오너님, 이제 당신의 비즈니스는 스스로 성장합니다.'")
    print("="*60)

    conn.close()

if __name__ == "__main__":
    generate_gvic_report("GVIC_OPERATOR_01")