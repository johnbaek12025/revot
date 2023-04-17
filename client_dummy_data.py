from dummy_data import random_date
from datetime import datetime
import random
import requests
import websocket
import json


main_url = 'https://revot.ai/'
ses = requests.session()

class BringContents:
    def __init__(self, msg) -> None:
        self.response = []
        self.msg = msg        
        
    def on_message(self, ws, message):
        # Decode the message using json.loads()
        data = json.loads(message)
        # Close the WebSocket connection
        ws.close()
        self.response.append(data)

    def on_error(self, ws, error):
        print("WebSocket error:", error)

    def on_close(self, ws):
        print("WebSocket closed")

    def on_open(self, ws):
        print("WebSocket opened")
        # Send a message over the WebSocket connection        
        ws.send(json.dumps(self.msg))
        
    def main(self):
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp("wss://revot.ai/ws/fetch/contents/",
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        ws.on_open = self.on_open
        ws.run_forever()
        return self.response[0]
    

def login(acc_info: dict):    
    data = acc_info.update({"remember_account":True})
    ses.post(f"{main_url}", json=data)
    print(f'check login {vars(ses)}')
    
def requests_ticket_review_purchase():
    ses.post(f"{main_url}request/review/ticket/", json={"count": 100, "bank": "nh", "depositor_name": "u1"})
    ses.post(f"{main_url}request/purchase/ticket/", json={"count": 100, "bank": "nh", "depositor_name": "u1"})
    
def requests_ticket_update(data: dict):
    #{"id":"4", "cnt": 40}
    ses.put(f"{main_url}history/review/request/", json=data)
    ses.put(f"{main_url}history/purchase/request/", json=data)
    
def check_list_ticket_requests():
    data = ses.get(f"{main_url}history/review/request/")
    print(data.json())
    
def registe_products():
    ses.post(f"{main_url}user/product/", json={"url": "https://smartstore.naver.com/plusflower/products/3006726853?n_media=11068&n_query=%EA%B3%BC%EC%9D%BC&n_rank=1&n_ad_group=grp-a001-02-000000009396136&n_ad=nad-a001-02-000000051563316&n_campaign_type=2&n_mall_id=ncp_1nlx7y_01&n_mall_pid=3006726853&n_ad_group_type=2&NaPm=ct%3Dlf0lm3j4%7Cci%3D0zO0003WlezylQLgFKXg%7Ctr%3Dpla%7Chk%3D5811f684314fd565464b76670429da3e56e02dcc", "mid1":'37621009217', 'keyword':'병원 과일바구니, 선물 병문안, 문병, 선물용 과일, 과일바구니'})
    ses.post(f"{main_url}user/product/", json={"url": "https://smartstore.naver.com/garakfruit/products/123486199?n_media=11068&n_query=%EA%B3%BC%EC%9D%BC&n_rank=2&n_ad_group=grp-a001-02-000000003809751&n_ad=nad-a001-02-000000015655942&n_campaign_type=2&n_mall_id=fksdud3766&n_mall_pid=123486199&n_ad_group_type=2&NaPm=ct%3Dlf0lmye8%7Cci%3D0z40000yluzyh2ET9L2G%7Ctr%3Dpla%7Chk%3Df9100ebae29f378f42da9dc95e1a60487216d4e8", "mid1":'85494321953', 'keyword':'병원 과일바구니, 선물 병문안, 문병, 선물용 과일, 과일바구니'})
    ses.post(f"{main_url}user/product/", json={"url": "https://smartstore.naver.com/gyulmedal/products/6497325914?n_media=11068&n_query=%EA%B3%BC%EC%9D%BC&n_rank=3&n_ad_group=grp-a001-02-000000026645731&n_ad=nad-a001-02-000000179138748&n_campaign_type=2&n_mall_id=ncp_1o21iv_01&n_mall_pid=6497325914&n_ad_group_type=2&NaPm=ct%3Dlf0lndts%7Cci%3D0yK0000SluzyCX5%5FJ0Zd%7Ctr%3Dpla%7Chk%3Dc3716f94d16f8f21be10daa0139d10e0e99dcdba", "mid1":'38501838666', 'keyword':'아스미, 제주 신비향, 수라향 아스미, 제주 감귤, 과일바구니'})
    ses.post(f"{main_url}user/product/", json={"url": "https://smartstore.naver.com/homgol/products/5811396719?NaPm=ct%3Dlf0lpecw%7Cci%3D5250ce520f1f20acbc38e80088399080e93551bc%7Ctr%3Dslsl%7Csn%3D1115439%7Chk%3D6c9d64a741363569c42c264dafe60b498414f53e", "mid1":'83355896133', 'keyword':'사과, 경북 부사, 못난이 꿀사과,  사과5kg,  사과10kg'})
    ses.post(f"{main_url}user/product/", json={"url": "https://smartstore.naver.com/redfruits/products/6155530258?NaPm=ct%3Dlf0lv6ow%7Cci%3Da11b70312b4cd1357c6e6da8d2ee2e42b92eee14%7Ctr%3Dslsl%7Csn%3D346016%7Chk%3D22a19084f5023a871b5a59612ad7cc211d68d7a1", "mid1":'83700029746', 'keyword':'사과, 청송사과, 문경 껍질째먹는 사과,  사과 10kg,  사과 5kg'})
    ses.post(f"{main_url}user/product/", json={"url": "https://smartstore.naver.com/paul_frenz/products/4721606984?n_media=11068&n_query=%EC%96%B4%EB%A6%B0%EC%9D%B4%EC%96%91%EB%A7%90&n_rank=1&n_ad_group=grp-a001-02-000000012981682&n_ad=nad-a001-02-000000082056399&n_campaign_type=2&n_mall_id=ncp_1ntu1u_01&n_mall_pid=4721606984&n_ad_group_type=2&NaPm=ct%3Dlf0m0b3s%7Cci%3D0ye0002hm0zyKV5IeL2l%7Ctr%3Dpla%7Chk%3Dec39e383d5e66832d752fedf72cb99385f863469", "mid1":'82266128172', 'keyword':'폴프랜즈 유아동양말 세트, 원사이즈 유아동양말 세트, 아동양말, 키즈양말, 어린이 양말'})
    ses.post(f"{main_url}user/product/", json={"url": "https://smartstore.naver.com/ggomisocks/products/503074444?NaPm=ct%3Dlf0m2ikw%7Cci%3D0AK0003Um0zy3IZtYfj%5F%7Ctr%3Dpla%7Chk%3Ddfe057b7ff4e90693a983b610f9863b60064785b", "mid1":'10383464529', 'keyword':'국산 골지 사계절 어린이 양말, 초등생 양말, 아동양말, 키즈양말, 어린이 양말'})
    ses.post(f"{main_url}user/product/", json={"url": "https://smartstore.naver.com/nibal_nebal/products/5199848601?n_media=11068&n_query=%EC%96%B4%EB%A6%B0%EC%9D%B4%EC%96%91%EB%A7%90&n_rank=3&n_ad_group=grp-a001-02-000000018744142&n_ad=nad-a001-02-000000115564342&n_campaign_type=2&n_mall_id=ncp_1o1gt6_01&n_mall_pid=5199848601&n_ad_group_type=2&NaPm=ct%3Dlf0m34yg%7Cci%3D0z40000lmezyXnmEG1ky%7Ctr%3Dpla%7Chk%3De027744db64093966e0d6b7fd8a1c97b1b6959ff", "mid1":'82744370230', 'keyword':'유아동 데일리 베이직 골지양말 SET, 골지양말, 아동양말, 키즈양말, 어린이 양말'})
    ses.post(f"{main_url}user/product/", json={"url": "https://smartstore.naver.com/paul_frenz/products/4721606984?n_media=11068&n_query=%EC%96%B4%EB%A6%B0%EC%9D%B4%EC%96%91%EB%A7%90&n_rank=1&n_ad_group=grp-a001-02-000000012981682&n_ad=nad-a001-02-000000082056399&n_campaign_type=2&n_mall_id=ncp_1ntu1u_01&n_mall_pid=4721606984&n_ad_group_type=2&NaPm=ct%3Dlf0m0b3s%7Cci%3D0ye0002hm0zyKV5IeL2l%7Ctr%3Dpla%7Chk%3Dec39e383d5e66832d752fedf72cb99385f863469", "mid1":'84815107933', 'keyword':'밀크마일로로 에브리데이 유아양말 5종세트, 에브리데이 유아양말, 유아양말 5종세트, 일상 유아양말, 아이양말' })
    ses.post(f"{main_url}user/product/", json={"url": "https://smartstore.naver.com/paul_frenz/products/4721606984?n_media=11068&n_query=%EC%96%B4%EB%A6%B0%EC%9D%B4%EC%96%91%EB%A7%90&n_rank=1&n_ad_group=grp-a001-02-000000012981682&n_ad=nad-a001-02-000000082056399&n_campaign_type=2&n_mall_id=ncp_1ntu1u_01&n_mall_pid=4721606984&n_ad_group_type=2&NaPm=ct%3Dlf0m0b3s%7Cci%3D0ye0002hm0zyKV5IeL2l%7Ctr%3Dpla%7Chk%3Dec39e383d5e66832d752fedf72cb99385f863469", "mid1":'82522113101', 'keyword':'아동양말 유아 아기 어린이 집 선물 세트, 유치원 초등학교 성탄절 답례품, 쥬니어 여아 겨울 양말, 어린이 양말 세트, 선물 양말' })
    ses.post(f"{main_url}user/product/", json={"url": "https://smartstore.naver.com/thebasecosmetics/products/7050014992?", "mid1": "84594515314", "keyword": '수분크림, 무향 수분크림, 수분공급크림, 모이스쳐라이징, 무향 모이스쳐라이징'})
    ses.post(f"{main_url}user/product/", json={"url": "https://smartstore.naver.com/plusflower/products/3006726853?n_media=11068&n_query=%EA%B3%BC%EC%9D%BC&n_rank=1&n_ad_group=grp-a001-02-000000009396136&n_ad=nad-a001-02-000000051563316&n_campaign_type=2&n_mall_id=ncp_1nlx7y_01&n_mall_pid=3006726853&n_ad_group_type=2&NaPm=ct%3Dlf0lm3j4%7Cci%3D0zO0003WlezylQLgFKXg%7Ctr%3Dpla%7Chk%3D5811f684314fd565464b76670429da3e56e02dcc", "mid1":'37621009217', 'keyword':'병원 과일바구니, 선물 병문안, 문병, 선물용 과일, 과일바구니'})
    ses.post(f"{main_url}user/product/", json={"url": "https://smartstore.naver.com/garakfruit/products/123486199?n_media=11068&n_query=%EA%B3%BC%EC%9D%BC&n_rank=2&n_ad_group=grp-a001-02-000000003809751&n_ad=nad-a001-02-000000015655942&n_campaign_type=2&n_mall_id=fksdud3766&n_mall_pid=123486199&n_ad_group_type=2&NaPm=ct%3Dlf0lmye8%7Cci%3D0z40000yluzyh2ET9L2G%7Ctr%3Dpla%7Chk%3Df9100ebae29f378f42da9dc95e1a60487216d4e8", "mid1":'85494321953', 'keyword':'병원 과일바구니, 선물 병문안, 문병, 선물용 과일, 과일바구니'})
    ses.post(f"{main_url}user/product/", json={"url": "https://smartstore.naver.com/gyulmedal/products/6497325914?n_media=11068&n_query=%EA%B3%BC%EC%9D%BC&n_rank=3&n_ad_group=grp-a001-02-000000026645731&n_ad=nad-a001-02-000000179138748&n_campaign_type=2&n_mall_id=ncp_1o21iv_01&n_mall_pid=6497325914&n_ad_group_type=2&NaPm=ct%3Dlf0lndts%7Cci%3D0yK0000SluzyCX5%5FJ0Zd%7Ctr%3Dpla%7Chk%3Dc3716f94d16f8f21be10daa0139d10e0e99dcdba", "mid1":'38501838666', 'keyword':'아스미, 제주 신비향, 수라향 아스미, 제주 감귤, 과일바구니'})
    ses.post(f"{main_url}user/product/", json={"url": "https://smartstore.naver.com/homgol/products/5811396719?NaPm=ct%3Dlf0lpecw%7Cci%3D5250ce520f1f20acbc38e80088399080e93551bc%7Ctr%3Dslsl%7Csn%3D1115439%7Chk%3D6c9d64a741363569c42c264dafe60b498414f53e", "mid1":'83355896133', 'keyword':'사과, 경북 부사, 못난이 꿀사과,  사과5kg,  사과10kg'})
    ses.post(f"{main_url}user/product/", json={"url": "https://smartstore.naver.com/redfruits/products/6155530258?NaPm=ct%3Dlf0lv6ow%7Cci%3Da11b70312b4cd1357c6e6da8d2ee2e42b92eee14%7Ctr%3Dslsl%7Csn%3D346016%7Chk%3D22a19084f5023a871b5a59612ad7cc211d68d7a1", "mid1":'83700029746', 'keyword':'사과, 청송사과, 문경 껍질째먹는 사과,  사과 10kg,  사과 5kg'})
    ses.post(f"{main_url}user/product/", json={"url": "https://smartstore.naver.com/paul_frenz/products/4721606984?n_media=11068&n_query=%EC%96%B4%EB%A6%B0%EC%9D%B4%EC%96%91%EB%A7%90&n_rank=1&n_ad_group=grp-a001-02-000000012981682&n_ad=nad-a001-02-000000082056399&n_campaign_type=2&n_mall_id=ncp_1ntu1u_01&n_mall_pid=4721606984&n_ad_group_type=2&NaPm=ct%3Dlf0m0b3s%7Cci%3D0ye0002hm0zyKV5IeL2l%7Ctr%3Dpla%7Chk%3Dec39e383d5e66832d752fedf72cb99385f863469", "mid1":'82266128172', 'keyword':'폴프랜즈 유아동양말 세트, 원사이즈 유아동양말 세트, 아동양말, 키즈양말, 어린이 양말'})
    ses.post(f"{main_url}user/product/", json={"url": "https://smartstore.naver.com/ggomisocks/products/503074444?NaPm=ct%3Dlf0m2ikw%7Cci%3D0AK0003Um0zy3IZtYfj%5F%7Ctr%3Dpla%7Chk%3Ddfe057b7ff4e90693a983b610f9863b60064785b", "mid1":'10383464529', 'keyword':'국산 골지 사계절 어린이 양말, 초등생 양말, 아동양말, 키즈양말, 어린이 양말'})
    ses.post(f"{main_url}user/product/", json={"url": "https://smartstore.naver.com/nibal_nebal/products/5199848601?n_media=11068&n_query=%EC%96%B4%EB%A6%B0%EC%9D%B4%EC%96%91%EB%A7%90&n_rank=3&n_ad_group=grp-a001-02-000000018744142&n_ad=nad-a001-02-000000115564342&n_campaign_type=2&n_mall_id=ncp_1o1gt6_01&n_mall_pid=5199848601&n_ad_group_type=2&NaPm=ct%3Dlf0m34yg%7Cci%3D0z40000lmezyXnmEG1ky%7Ctr%3Dpla%7Chk%3De027744db64093966e0d6b7fd8a1c97b1b6959ff", "mid1":'82744370230', 'keyword':'유아동 데일리 베이직 골지양말 SET, 골지양말, 아동양말, 키즈양말, 어린이 양말'})
    ses.post(f"{main_url}user/product/", json={"url": "https://smartstore.naver.com/paul_frenz/products/4721606984?n_media=11068&n_query=%EC%96%B4%EB%A6%B0%EC%9D%B4%EC%96%91%EB%A7%90&n_rank=1&n_ad_group=grp-a001-02-000000012981682&n_ad=nad-a001-02-000000082056399&n_campaign_type=2&n_mall_id=ncp_1ntu1u_01&n_mall_pid=4721606984&n_ad_group_type=2&NaPm=ct%3Dlf0m0b3s%7Cci%3D0ye0002hm0zyKV5IeL2l%7Ctr%3Dpla%7Chk%3Dec39e383d5e66832d752fedf72cb99385f863469", "mid1":'84815107933', 'keyword':'밀크마일로로 에브리데이 유아양말 5종세트, 에브리데이 유아양말, 유아양말 5종세트, 일상 유아양말, 아이양말' })
    ses.post(f"{main_url}user/product/", json={"url": "https://smartstore.naver.com/paul_frenz/products/4721606984?n_media=11068&n_query=%EC%96%B4%EB%A6%B0%EC%9D%B4%EC%96%91%EB%A7%90&n_rank=1&n_ad_group=grp-a001-02-000000012981682&n_ad=nad-a001-02-000000082056399&n_campaign_type=2&n_mall_id=ncp_1ntu1u_01&n_mall_pid=4721606984&n_ad_group_type=2&NaPm=ct%3Dlf0m0b3s%7Cci%3D0ye0002hm0zyKV5IeL2l%7Ctr%3Dpla%7Chk%3Dec39e383d5e66832d752fedf72cb99385f863469", "mid1":'82522113101', 'keyword':'아동양말 유아 아기 어린이 집 선물 세트, 유치원 초등학교 성탄절 답례품, 쥬니어 여아 겨울 양말, 어린이 양말 세트, 선물 양말' })
    ses.post(f"{main_url}user/product/", json={"url": "https://smartstore.naver.com/thebasecosmetics/products/7050014992?", "mid1": "84594515314", "keyword": '수분크림, 무향 수분크림, 수분공급크림, 모이스쳐라이징, 무향 모이스쳐라이징'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/playg9/products/8310654375/', 'keyword': '레고10317,레고,레고,레고,레고 10317 랜드로버 디펜더 90,일타토이', 'mid1': '85855154698'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/playg9/products/8319491725/', 'keyword': '레고40504,레고,레고,레고,레고 40504 로저 선장 빌더블 피규어 한정판,일타토이', 'mid1': '85863992048'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/cherry1021/products/8232429277/', 'keyword': '재미있는블럭,성인장난감,어려보이는,어린이날,사랑의선물,아이들이좋아하는,여자선물,레고,중국,레고,어려운 레고 부품 공주 케슬 디즈니 성 블록 성인레고 조립 어린이날 선물,편한공간', 'mid1': '85776929600'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/conesland/products/7959119361/', 'keyword': '레고,레고,레고,레고 21246 마인크래프트 워든 깊고 어두운 전장의 아바레스트 네더라이트,콘스랜드', 'mid1': '85503619684'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/feel_yo/products/8366886355/', 'keyword': '창의력블럭,레고샵,레고단종품,레고역할놀이,신나는놀이,키덜트장난감,레고76164, 레고아이언맨,레고헐크버스터,레고,레고,레고,[무료배송] 레고 76164 마블 어벤져스 아이언맨 헐크버스터 VS A.I.M. 요원,더 필요샵', 'mid1': '85911386678'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/songpro/products/8217751155/', 'keyword': '레고,,,축구선수 레고 피규어 국대 손흥민 메시 호날두,해리상점', 'mid1': '85762251478'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/kkuackshop/products/8324311241/', 'keyword': '레고조립,레고블릭,레고단종품,레고소품,대관람차,놀이공원,해적선,해적선놀이,해적선모형,해적선게임,레고,레고,레고,레고 대관람차 31119 크리에이터 놀이공원 해적선 범퍼카 놀이,꽉꽉샵', 'mid1': '85868811564'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/light9/products/8286273190/', 'keyword': '테크닉레고,모듈러,매장,레고조립,레고호완블럭,레고20대선물,레고30대선물,레고일괄매입,슈퍼카,레이싱카,레고,LEGO,LEGO,레고 2023 스피드 챔피언,라이트9', 'mid1': '85830773513'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/nanjang2/products/8218701922/', 'keyword': '어린이날선물,호환레고,호환레고블럭,아들선물,닌자고피규어,레고,중국호환레고,중국호환레고,닌자고 로이드의 타이탄 로봇,난쟁이샵', 'mid1': '85763202245'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/japan_pocket/products/5782172054/', 'keyword': '레고,레고,레고,레고 (LEGO) 거신 닌자고 파이어 스톤 로봇 71720,일본 주머니', 'mid1': '83326671468'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/a-ruda/products/7659041257/', 'keyword': '초등학생,여아,남아,크리스마스선물,조카선물,초등,포켓몬피규어,포켓몬go,포켓몬스터피규어,레고,협력사 제품,협력사 제품,포켓몬 레고,어루다', 'mid1': '85203541579'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/kkuackshop/products/8000693360/', 'keyword': '레고조립,레고단종품,레고소품,레고블릭,꽃다발,꽃다발만들기,화분장식,난초,난초세트,보태니컬아트,레고,레고,레고,레고 보태니컬 난초 10311 아이콘 난초 꽃 화분 식물 컬렉션,꽉꽉샵', 'mid1': '85545193683'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/kkuackshop/products/8346426508/', 'keyword': '레고조립,레고블릭,레고단종품,레고소품,마인크래프트피규어,마인크래프트,게임캐릭터,게임캐릭터피규어,레고샵,레고대여,레고,레고,레고,레고 21246 마인크래프트 워든 깊고 어두운 전장의 아바레스트 네더라이트,꽉꽉샵', 'mid1': '85890926831'}   )
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/kkuackshop/products/8235908021/', 'keyword': '레고조립,재미있는블럭,레고블릭,레고단종품,레고소품,수퍼카,레이싱카,슈퍼카,스피드챔피언,자동차장난감,레고,레고,레고,레고 75875 스피드챔피언 포드 F-150 랩터와 핫로드,꽉꽉샵', 'mid1': '85780408344'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/harowoobin/products/8265835297/', 'keyword': '레고,하로우빈', 'mid1': '85810335620'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/sunshineglobal/products/5849212219/', 'keyword': '재미있는블럭,레고정품,블럭놀이,조립완구,어린이선물,레고,,,레고 마블 어벤져스 엔드게임 최종 결전 76192,선샤인 글로벌', 'mid1': '83393711633'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/hclmall/products/8305236949/', 'keyword': '레고,레고,레고,닌자고 오버로드 드래곤 71742,데일브릿', 'mid1': '85849737272'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/kkuackshop/products/8294158812/', 'keyword': '레고조립,레고블릭,레고단종품,레고소품,스타워즈미피,스타워즈피규어,스타워즈캐릭터,다스베이더피규어,트루퍼,스타워즈다스베이더,레고,레고,레고,레고 스타워즈 배틀팩 501 스노우트루퍼 75320 호스 스피더 바이크,꽉꽉샵', 'mid1': '85838659135'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/new-type/products/6245425630/', 'keyword': '프라모델,YOLOPARK,욜로파크,욜로파크 트랜스포머 범블비 무비 옵티머스 프라임 프라모델 YOLOPARK,NewType', 'mid1': '83789928119'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/new-type/products/8161651944/', 'keyword': '프라모델,인피니트디멘션,IN ERA,인피니트디멘션 1/100 재결 룰링 무한신성 프라모델,NewType', 'mid1': '85706152267'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/new-type/products/8321617239/', 'keyword': '조립장난감,프라모델모형,프라모델조립,조립모형,아이언맨피규어,아이언맨장난감,프라모델,이스턴모형,이스턴모형,이스턴모형 1/12 펜리르 기녀 걸프라 프라모델 ATK GIRL,NewType', 'mid1': '85866117562'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/easyjoy22/products/6412227713/', 'keyword': '슈퍼미니프라,SMP,superminipla,슈미프,반다이프라,파이널가오가이가,가오가이가파이널,반다이한정,RG가오가이가,RG가오가이거,프라모델,,반다이,,이지조이샵', 'mid1': '83956728046'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/new-type/products/5881571451/', 'keyword': '조립장난감,프라모델모형,프라모델조립,조립모형,아이언맨피규어,아이언맨장난감,프라모델,이스턴모형,이스턴모형,이스턴모형 1/9 아이언맨 MK50 마크50 호화판 디럭스 프라모델,NewType', 'mid1': '83426070865'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/new-type/products/3666392783/', 'keyword': '프라모델,폭풍모형,폭풍모형,폭풍모형 EX-S EXS 익세스 테스크 포스 알파 건담 완성품,NewType', 'mid1': '81210910480'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/new-type/products/6517636813/', 'keyword': '프라모델,반다이,반다이,반다이 RG 용자왕 가오가이가 가오가이거 프라모델,NewType', 'mid1': '84062137146'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/easyjoy22/products/8297031763/', 'keyword': '반다이프라,반다이한정,마크로스,마크로스플러스,YF19,듀랜달,사오토메기,YF29,프라모델,,반다이,,이지조이샵', 'mid1': '85841532086'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/new-type/products/7110975777/', 'keyword': '프라모델,모터뉴클리어,모터뉴클리어,모터뉴클리어 MNP-XH03 청룡 프라모델버전 인젝션,NewType', 'mid1': '84655476099'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/new-type/products/2121604101/', 'keyword': '프라모델,다반,다반,다반 MG 8802 스트라이크 프리덤 메탈빌드버전 건담 중국,NewType', 'mid1': '13341324196'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/new-type/products/2179763304/', 'keyword': '프라모델,다반,다반,다반 PG 스트라이크 건담 프라모델 뉴타입 중국,NewType', 'mid1': '12273701838'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/new-type/products/7850954057/', 'keyword': '프라모델,모터뉴클리어,모터뉴클리어,모터뉴클리어 MNP-XH02 백룡 프라모델버전 인젝션,NewType', 'mid1': '85395454379'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/new-type/products/7900481062/', 'keyword': '프라모델,다반,다반,다반 MG 6631S 사자비 버카 도색 코팅 버전 프라모델,NewType', 'mid1': '85444981385'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/the-classe/products/8241374998/', 'keyword': '변신,욜로파크,옵티머스프라임,범블비더무비,변신피규어,프라모델,욜로파크,욜로파크,옵티머스 프라임,더클라쓰', 'mid1': '85785875321'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/nikorijapan/products/7331260534/', 'keyword': '프라모델,,MGEX,MGEX 기동전사 건담 시드 데스티니 스트라이크 프리덤 건담,니코리재팬', 'mid1': '84875760856'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/new-type/products/8316757316/', 'keyword': '프라모델,다반,다반,다반 MG 8812A 레드프레임 카이 메탈빌드 버전 프라모델,NewType', 'mid1': '85861257639'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/new-type/products/5301803052/', 'keyword': '프라모델,다반,다반,다반 MG 6619s 뉴건담 버카 메탈 코팅 중국 건담,NewType', 'mid1': '82846295418'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/new-type/products/8064034608/', 'keyword': '프라모델,다반,다반,다반 MG 8802S 스트라이크 프리덤 소울블루 메탈빌드버전 프라모델,NewType', 'mid1': '85608534931'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/easyjoy22/products/8334860178/', 'keyword': '반다이프라,반다이한정,마크로스,마크로스플러스,YF19,듀랜달,사오토메기,YF29,프라모델,,반다이,,이지조이샵', 'mid1': '85879360501'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/new-type/products/2334018715/', 'keyword': '프라모델,다반,다반,다반 MG 8808 아발란체 엑시아 건담 중국 대륙,NewType', 'mid1': '12838710481'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/new-type/products/3880326789/', 'keyword': '프라모델,MC,메탈기어,메탈기어 MC 아스트레이 레드프레임 플라이트팩 건담 합금완성품,NewType', 'mid1': '81424846802'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/new-type/products/8280012460/', 'keyword': '프라모델,다반,다반,다반 PG 아스트레이 레드프레임 건담 프라모델,NewType', 'mid1': '85824512783'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/new-type/products/6612356984/', 'keyword': '프라모델,MW,MW,MW 제네식 가오가이가 합금 골격 도색 프라모델 가오가이거,NewType', 'mid1': '84156857306'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/woochu/products/8248486716/', 'keyword': '프라모델,우츄란', 'mid1': '85792987039'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/new-type/products/5868419926/', 'keyword': '프라모델,로담스,로담스,로담스 1/72 RAS-30L 덴드로비움,NewType', 'mid1': '83412919340'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/new-type/products/7408575641/', 'keyword': '프라모델,인피니트디멘션,인피니트디멘션,인피니트디멘션 1/100 제네시스 소장판 무한신성 프라모델,NewType', 'mid1': '84953075963'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/new-type/products/8262318414/', 'keyword': '프라모델,이펙트윙즈,이펙트윙즈,이펙트윙즈 RG 하이뉴 뉴건담 후쿠오카 롱레인지 메가 런처 프라모델,NewType', 'mid1': '85806818737'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/new-type/products/8024086847/', 'keyword': '프라모델,화모선,화모선,화모선 1/100 신들의 엔트로피 뇌신 프라모델,NewType', 'mid1': '85568587170'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/woochu/products/8258656668/', 'keyword': '프라모델,우츄란', 'mid1': '85803156991'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/woochu/products/7982244027/', 'keyword': '프라모델,우츄란', 'mid1': '85526744350'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/the-classe/products/8236958625/', 'keyword': '합금프라모델,프라모델,협력사,기타/기타,무한신성 재결,더클라쓰', 'mid1': '85781458948'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/new-type/products/8273769397/', 'keyword': '프라모델,누크매트릭스,누크매트릭스,누크매트릭스 판타지걸 센타우루스 섀도우 예푸나 마르키나 프라모델 걸프라,NewType', 'mid1': '85818269720'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/new-type/products/6911757402/', 'keyword': '프라모델,YOLOPARK,욜로파크,욜로파크 트랜스포머 범블비 쇼크웨이브 프라모델 YOLOPARK,NewType', 'mid1': '84456257724'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/new-type/products/7051060065/', 'keyword': '프라모델,제로G,제로G,제로G MG 저지 월야 프리덤 컬러 건담 프라모델 중국,NewType', 'mid1': '84595560387'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/mpani/products/8343510812/', 'keyword': '피규어장난감,어린이장난감,어린이선물,아이선물,피규어선물,피규어완구,소품인테리어,어린이날선물,애기선물,애니메이션피규어,로봇,상세설명참조,상세설명참조,또봇 탱크가이 변신로봇 장난감 남아토이 선물,엠파니', 'mid1': '85888011135'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/eurobeauty/products/3157139571/', 'keyword': '지아자크림,지아자산양유,지아자직구,데이크림,지아자폴란드,크림,지아자,지아자,지아자 산양유 데이크림 50ml,유럽화장품', 'mid1': '80654883900'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/parisuper/products/2938164902/', 'keyword': '피부과화장품,피부재생,피부진정,라로슈포제직구,시카플라스트,프랑스직구,크림,라로슈포제,라로슈포제,,파리한 그녀', 'mid1': '80435908878'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/doichmall/products/727433222/', 'keyword': '산양유크림,데이크림,나이트크림,데일리크림,아이크림15ml,선물용화장품,크림,지아자,지아자,,도이치몰', 'mid1': '11380266744'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/aug9market/products/4903098939/', 'keyword': '루카스포포크림,호주연고,호주포포크림,포포크림,호주국민크림,빨간크림,호주천연크림,호주화장품,매일매일촉촉하게,순한저자극보습,크림,루카스,루카스,루카스 포포크림 25g,호주직구마켓', 'mid1': '82447622514'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/elfmagic/products/6223267508/', 'keyword': '보습크림,수분크림,수분영양크림,진정크림,민감성크림,여드름크림,베이비크림,영유아크림,건성크림,촉촉한크림,크림,NEOCOSMED CO.,LTD.,피지오겔,데일리 모이스쳐 테라피 페이셜 크림 150ml,엘프의마법', 'mid1': '83767769997'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/euromoms/products/718525468/', 'keyword': '독일화장품,약국화장품,지아자산양유,지아자크림,지아자아이크림,산양유크림,지아자산양유크림,지아자수분크림,지아자나이트크림,나이트크림,크림,지아자,지아자,,유로맘스 독일직구', 'mid1': '11330144210'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/euromarkt/products/5803270665/', 'keyword': '시원촉촉,부드러운피부,촉촉한수분크림,상쾌한느낌,리치크림,간절기,사계절,크림,라로슈포제,라로슈포제,시카플라스트 밤 B5 100ml,유로마크트', 'mid1': '83347770079'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/eurocat/products/3739322818/', 'keyword': '유럽화장품,독일화장품,독일화장품직구,독일크림,지아자직구,지아자산양유,산양유크림,크림,지아자,지아자,,유로캣', 'mid1': '81283840690'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/germanpham/products/730319714/', 'keyword': '아벤느화장품,민감한피부,전신크림,피부케어,가족선물,해외화장품,미네랄성분,온천수화장품,프랑스화장품,명품화장품,크림,아벤느,아벤느,,독일팜', 'mid1': '11530871147'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/eurobeauty/products/2397033045/', 'keyword': '라로슈포제직구,라로슈포제시카,시카플라스트,라로슈포제크림,시카플라스트크림,크림,라로슈포제,라로슈포제,,유럽화장품', 'mid1': '13135196501'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/eurobeauty/products/479933815/', 'keyword': '크림,라로슈포제,라로슈포제,,유럽화장품', 'mid1': '12581544084'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/guttentag/products/6507014814/', 'keyword': '크림,Just,Just,스위스 유스트 허브크림 100ml 3종류,assome', 'mid1': '84051515147'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/eurobeauty/products/479000352/', 'keyword': '크림,바이오더마,바이오더마,,유럽화장품', 'mid1': '12985154514'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/eurobeauty/products/473493374/', 'keyword': '달팡히드라,달팡히드라스킨,달팡히드라크림,히드라크림,달팡리치크림,달팡크림,프랑스화장품구매대행,달팡추천,프랑스화장품,크림,달팡,달팡,,유럽화장품', 'mid1': '10279593739'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/eurobeauty/products/5183900418/', 'keyword': '해외직구,용카화장품,용카스킨,용카스킨케어,크림,용카,용카,,유럽화장품', 'mid1': '82728421669'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/peaubb/products/449650341/', 'keyword': '50대여성,40대여성,20대여성,30대여성,촉촉부드러움,크림,M&L,록시땅,시어 울트라 리치 컴포팅 크림 50ml,뽀베베', 'mid1': '12435141939'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/nychic/products/5891309451/', 'keyword': '피부고민,부드럽고산뜻한사용감,촉촉한수분감,피부진정,민감성피부,고보습,저자극,피부과추천,크림,듀크레이,듀크레이,[듀크레이] 덱시안 메드 수딩 크림 100ml,직구의신 ZICGOOGOD', 'mid1': '83435808865'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/eurocat/products/3708949719/', 'keyword': '크림,아더마,아더마,,유로캣', 'mid1': '81253467524'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/eurobeauty/products/478867304/', 'keyword': '크림,비쉬,비쉬,,유럽화장품', 'mid1': '13050286814'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/osakashoplist/products/4024423434/', 'keyword': '마유크림,손바유마유크림,말기름,약사당,일본마유,수분크림,보습크림,순한로션,어린이화장품,어린이로션,크림,약사당,손바유,손바유 마유크림,일본직구 플라잉박스', 'mid1': '81568943948'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/parissante/products/219639161/', 'keyword': '크림,라로슈포제,라로슈포제,시카플라스트 젤 40ml,파리쌍떼', 'mid1': '9000614760'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/parissante/products/219630909/', 'keyword': '크림,피에르파브르,아벤느,씨칼파트 리페어 크림 100ml,파리쌍떼', 'mid1': '11033909745'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/hojushopper/products/7921127552/', 'keyword': '루카스포포크림,포포크림,호주크림,진정크림,보습력우수,호주산,크림,루카스,루카스,호주 루카스 포포크림 15g 25g x 6개 튜브형,호주쇼퍼', 'mid1': '85465627875'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/peaubb/products/422144814/', 'keyword': '건강한피부,부드러운피부,탄력크림,보습크림,탄력있는얼굴,탄력있는피부,30대여성,40대여성,50대여성,크림,ELCO SAS,달팡,하이드라 스킨 리치 50ml(건성),뽀베베', 'mid1': '11779516188'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/dodosale/products/8340851904/', 'keyword': '사과,도도,도도,,도도구대', 'mid1': '85885352227'})
    ses.post(f"{main_url}user/product/", json={'url': 'https://smartstore.naver.com/dwaeppagi/products/8336466519/', 'keyword': '높은곳집개,높은곳과일따기,복숭아따기,복숭아집개,석류집개,감집개,사과집개,사과,중국,중국,,돼뺙이', 'mid1': '85880966842'})

def regist_purchase_reservation(date1, date2):
    """
    date1 = '2023-04-11 00:00'
    date2 = '2023-05-01 00:00'
    """
    c = {}
    d1 = datetime.strptime(date1, '%Y-%m-%d %H:%M')
    d2 = datetime.strptime(date2, '%Y-%m-%d %H:%M')
    products = ses.get(f"{main_url}user/product/total/?page=1&sc=100")
    for p in products.json()['data']:
        option = p.get('options')
        supplements = p.get('supplements')
        item = ses.get(f"{main_url}user/product/{p['id']}/")
        data = item.json()['data']
        if data['option_detail']:
            for sup in data['option_detail']:
                if isinstance(data['option_detail'][sup], list):
                    c[sup] = random.choice(data['option_detail'][sup])
                else:
                    c[sup] = sup
        if data['supplements']:
            for sup in data['supplements']:
                if isinstance(data['supplements'][sup], list):
                    c[sup] = random.choice(data['supplements'][sup])
                else:
                    c[sup] = sup
        rd, rc = random_date(d1, d2).strftime('%Y-%m-%d %H:%M').split(' ')
        data = {"product": p['id'], "reservation_date": rd, "options": c, "count": 20}     
        ses.post(f"{main_url}registe/purchase/", json=data)    
        c = {}
        
def registe_review_reservation(date):
    #date = '2023-05-01 23:59'
    purchases = ses.get(f"{main_url}purchase/history/total/?page=1&sc=100")
    for i, p in enumerate(purchases.json()['data']):
        d1 = datetime.strptime(f"{p['reservation_date']} 00:01", '%Y-%m-%d %H:%M')
        d2 = datetime.strptime(date, '%Y-%m-%d %H:%M')
        rd, rt = random_date(d1, d2).strftime('%Y-%m-%d %H:%M').split(' ')    
        name = p['name']
        options = ', '.join([v for k, v in p['options'].items()])
        msg = {"flag": True, "detail": {"name": name, "options": options}}
        bc = BringContents(msg)
        r = bc.main()
        data = {"purchase": p['id'], "reservation_date":rd, "contents": r['contents'], "star_count": 4}
        ses.post(f"{main_url}registe/review/", data=data)
        
        
if __name__ == '__main__':
    acc_info = {"user":"test@test.com", "pwd":"test1122"}
    login(acc_info)
    