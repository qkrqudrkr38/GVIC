"""
[GVIC Standard Operating Procedure]
File Name: gvic_integrated_dashboard.py
Save Directory: C:\GVIC\INTERFACE\
Version: v2.1.2 (Import-Fixed)
Created Date: 2026-03-14

Description: 
대문자 기둥 명칭(HEART, BRAIN)을 정확히 호출하고 경로 에러를 해결한 통합 지휘소입니다.
"""

import time
import os
import sys
from datetime import datetime

# GVIC 루트 디렉토리를 파이썬 경로에 등록 (ImportError 방지)
current_file_path = os.path.abspath(__file__)
interface_dir = os.path.dirname(current_file_path)
root_dir = os.path.dirname(interface_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# [핵심] 대문자 기둥 이름으로 정확히 호출
try:
    from core.gvic_vault import GVICVault
    from HEART.logic.heart_margin_patch import get_real_margin
    from BRAIN.logic.supply_chain_patch import get_safety_stock
except ImportError as e:
    print(f"🔴 [치명적 오류] 필수 신경망 누락: {e}")
    sys.exit(1)

class GVICDashboard:
    def __init__(self):
        self.refresh_rate = 2 

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def draw_header(self):
        print("="*80)
        print(f"🏰 GVIC EMPIRE INTEGRATED DASHBOARD [COMMANDER MODE]")
        status = "🔴 MANUAL_OVERRIDE" if GVICVault.MANUAL_OVERRIDE else "🟢 AUTO_PILOT"
        print(f"📡 SYSTEM STATUS: {status} | 🕒 {datetime.now().strftime('%H:%M:%S')}")
        print("="*80)

    def display_metrics(self):
        # 실시간 데이터 시뮬레이션
        price, cogs, ad_spend = 25000, 12000, 3500
        current_margin = get_real_margin(price, cogs, ad_spend)
        
        print(f"\n[❤️ HEART: 실시간 수익성 분석]")
        print(f"  - 진짜 공헌이익: ₩{current_margin:,} (단위 고정비 ₩{GVICVault.FIXED_COST_PER_UNIT:,} 포함)")
        print(f"  - 누적 광고비 절감액: ₩{GVICVault.ACCUMULATED_AD_SAVINGS:,}")
        
        print(f"\n[🛡️ IMMUNITY & LINK: 보안]")
        print(f"  - 블랙리스트 감시망: {len(GVICVault.BLACKLIST_BUYERS)}명 격리")

        print(f"\n[🧠 BRAIN & SPINE: 물류]")
        print(f"  - 권장 안전 재고: {get_safety_stock(50)}개 (리드타임 {GVICVault.CURRENT_LEAD_TIME}일 기준)")

    def run(self):
        try:
            while True:
                self.clear_screen()
                self.draw_header()
                self.display_metrics()
                print("\n" + "="*80)
                print("지휘소 가동 중... (Ctrl+C: 작전 종료)")
                time.sleep(self.refresh_rate)
        except KeyboardInterrupt:
            print("\n👋 지휘소 가동을 안전하게 종료합니다.")

if __name__ == "__main__":
    dashboard = GVICDashboard()
    dashboard.run()