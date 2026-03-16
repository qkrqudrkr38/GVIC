"""
[GVIC Standard Operating Procedure]
File Name: gvic_empire_rebuilder.py
Status: RESTORED ELITE
Function: COMMAND & CONTROL
"""

# C:\gvic\gvic_empire_rebuilder.py
import os
import shutil
import sqlite3
import json

# [설정] 제국 표준 경로
ROOT_DIR = r"C:\gvic"
TARGET_DIR = r"C:\gvic\gvic_server\scripts"
CONFIG_PATH = r"C:\gvic\config\api_config.json"

# [집결 명단] 실전 운영 핵심 파일
CORE_SCRIPTS = [
    "gvic_utils.py",
    "ad_sniper.py",
    "inventory_sync.py",
    "gvic_panel_v5.py",
    "gvic_final_judgment.py"
]

def rebuild_and_validate():
    print("\n" + "🏗️  " * 15)
    print(" [GVIC EMPIRE: 물리적 집결 및 논리적 정합성 강제 집행] ")
    print("🏗️  " * 15)

    # --- 1단계: 물리적 이전 (Physical Move) ---
    print("\n[STEP 1] 물리적 위치 재정렬 중...")
    if not os.path.exists(TARGET_DIR): os.makedirs(TARGET_DIR)

    for file_name in CORE_SCRIPTS:
        # 루트나 다른 곳에 있는 파일을 scripts 폴더로 강제 이동
        current_loc = os.path.join(ROOT_DIR, file_name)
        target_loc = os.path.join(TARGET_DIR, file_name)

        if os.path.exists(current_loc) and current_loc != target_loc:
            try:
                # 기존 파일이 있으면 덮어쓰기 위해 shutil.copy2 후 os.remove 사용
                shutil.copy2(current_loc, target_loc)
                os.remove(current_loc)
                print(f"  📦 [이동완료] {file_name} -> {TARGET_DIR}")
            except Exception as e:
                print(f"  ❌ [이동실패] {file_name}: {e}")
        elif os.path.exists(target_loc):
            print(f"  ✨ [위치정상] {file_name}는 이미 올바른 위치에 있습니다.")

    # --- 2단계: 논리적 정합성 검증 (Logical Alignment) ---
    print("\n[STEP 2] 논리적 정합성 및 연결성 검사...")
    os.chdir(TARGET_DIR) # 작업 디렉토리를 성소로 변경하여 로컬 import 활성화
    
    import sys
    sys.path.append(TARGET_DIR)

    try:
        # 1. 모듈 간 연결 확인
        import gvic_utils
        import ad_sniper
        print("  ✅ [연결] gvic_utils 및 엔진 모듈 간 상호 인식 성공")

        # 2. 데이터베이스 실제 경로 및 테이블 확인
        conn = sqlite3.connect(gvic_utils.DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cursor.fetchall()]
        print(f"  ✅ [DB] 연결 성공 (물리 경로: {gvic_utils.DB_PATH})")
        print(f"  ✅ [스키마] 현재 활성화된 테이블: {', '.join(tables)}")
        conn.close()

        # 3. 설정 데이터 가독성 확인
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            json.load(f)
        print("  ✅ [설정] api_config.json 논리 구조 정상")

        print("\n" + "★" * 60)
        print(" 🎊 [최종판정] 물리적 위치와 논리적 정합성이 완벽히 일치합니다!")
        print(" ★ GVIC 제국 사령부 시연 준비 완료 ★")
        print("★" * 60)

    except Exception as e:
        print(f"\n 🚨 [정합성 붕괴] 논리적 결함 발견: {e}")

if __name__ == "__main__":
    rebuild_and_validate()