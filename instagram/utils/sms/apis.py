from rest_framework.views import APIView

"""
class SMSSerializer:
    receiver에 휴대전화 형식의 데이터가 왔는지 validate
    message에 90자 이하의 문자열이 왔는지 validate
    
    is_valid()검사 후 
        serializer.data에 있는 내용을 이용해서 send처리
"""


class SendSMS(APIView):
    def post(self, request):
        # receiver, message키로 데이터 전송
        # receiver의 번호로 message내용을 문자보내기
        # Response에는 메시지 없이 status 200리턴

        # /api/utils/sms/send/ 로 연결
        # postman작성
        pass
