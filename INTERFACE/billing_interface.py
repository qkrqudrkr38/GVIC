"""
[GVIC Standard Operating Procedure]
File Name: billing_interface.py
Status: RESTORED ELITE
Function: COMMAND & CONTROL
"""

# C:\gvic\gvic_server\core\billing_interface.py
from finance_engine import GVICFinanceEngine

class BillingInterface:
    def __init__(self):
        self.fin_engine = GVICFinanceEngine()

    def issue_setup_invoice(self, seller_id, plan_price):
        """가입비 청구서 발행 (VAT 10% 별도)"""
        invoice = self.fin_engine.calculate_setup_billing(plan_price)
        # DB에 청구 내역 저장 (Seller_ID, Total, VAT, Status='WAITING')
        return invoice

    def confirm_activation(self, seller_id, actual_paid):
        """입금 확인 후 계정 활성화 (정합성 평가)"""
        # DB에서 예상 금액 호출 (시뮬레이션: 550,000원)
        expected = self.fin_engine.calculate_setup_billing(500000) 
        
        integrity = self.fin_engine.verify_payment_integrity(expected, actual_paid)
        
        if integrity["is_valid"]:
            # 정합성 1.0 도달 시 [SPINE] 노드에 접속 권한 개방 명령
            return {"status": "ACTIVE", "msg": "제국 입성을 환영합니다."}
        else:
            return {"status": "ERROR", "msg": f"금액 불일치: {integrity['mismatch_amount']}"}