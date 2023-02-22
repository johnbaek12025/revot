import django
import os, sys

# django setting 파일 설정하기 및 장고 셋업
cur_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
print(cur_dir)
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))  # 프로젝트 폴더

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "barley.settings")
django.setup()


from main.models.client import Product, User, State, ProductFolder
from main.models.clientdata import RequestTicket
from main.models.pseudo import Purchase, Review
from django.contrib.auth.hashers import make_password

def check_state_from(state_n=0):
    try:
        s = State.objects.get(state=state_n)
    except State.DoesNotExist:
        s = State(state=state_n)
        s.save()
    return s

def make_account():
    o_s = check_state_from(2)
    d_s = check_state_from(2)
    s_s = check_state_from(1)
    u_s = check_state_from()
    o = User(email_account='jllab@gmail.com', password=make_password('jllab1122'), agency_code='1111', self_code='NAZARE', authorization=True, phone='01012341234', name='oper', review_ticket=100, purchase_ticket=100, is_operator=True, higherarchy=o_s)  
    o.save()    
    d = User(email_account='jllab1@gmail.com', password=make_password('jllab1122'), agency_code='1111', self_code='JEHOVA', authorization=True, phone='01022223333', name='dev', review_ticket=100, purchase_ticket=100, higherarchy=d_s)  
    d.save()    
    s1 = User(email_account='jllab01@gmail.com', password=make_password('jllab1122'), agency_code='1111', recommendation_code='JEHOVA', authorization=True, phone='01022224444', name='sell', authorized_by=d ,review_ticket=100, purchase_ticket=100, self_code="SEELER", higherarchy=s_s)
    s1.save()
    d = User.objects.get(id=1)
    s2 = User(email_account='jllab02@gmail.com', password=make_password('jllab1122'), agency_code='1111', recommendation_code='JEHOVA', authorization=True, phone='01022223333', name='sell2', authorized_by=d ,review_ticket=100, purchase_ticket=100, self_code="SELLER", higherarchy=s_s)
    s2.save()    
    u = User(email_account='jllab001@gmail.com', password=make_password('jllab1122'), agency_code='1111', recommendation_code='JEHOVA', authorization=True, phone='010111122222', name='user', authorized_by=s1 ,review_ticket=100, purchase_ticket=100, self_code='SOLOMO', higherarchy=u_s)
    u.save()
    u2 = User(email_account='jllab002@gmail.com', password=make_password('jllab2233'), agency_code='1111', recommendation_code='JEHOVA', authorization=True, phone='0102222244444', name='user2', authorized_by=s2 ,review_ticket=100, purchase_ticket=100, self_code='SLOWER', higherarchy=u_s)
    u2.save()
    return [u, u2]
    
def make_products(user: User):
    s = check_state_from()
    p1 = Product(pid="7779190842", mid1='85323691164', keyword='찰보리빵, 경주빵, 경주 찰보리빵, 경주 보리빵, 찰보리빵 경주, 찰 보리 경주빵과', state=s, owner=user)
    p1.save()
    p2 = Product(pid="6155621368", mid1='83700120856', keyword='고당도 써니트 한라봉, 한라봉, 제주 한라봉, 산지직송 한라봉, 고당도 한라봉, 과일 한라봉', state=s, owner=user)
    p2.save()
    p3 = Product(pid="5268175998", mid1='82812698711', keyword='고당도 사과, 사과, 청송사과, 산지직송 사과, 못난이 사과, 과일 사과', state=s, owner=user)
    p3.save()
    p4 = Product(pid="8056367839", mid1='83869789582', keyword='성주 참외, 고당도 꿀참외, 고씨네 참외, 고당도 참외, 참외 고당도, 맛있는 참외', state=s, owner=user)
    p4.save()
    p5 = Product(pid="2190688497", mid1='35026624758', keyword='저농약 감귤, 제주 감귤, 프리미엄 감귤, 고당도 감귤, 찰보리빵 경주, 감귤', state=s, owner=user)
    p5.save()
    
    


def request_tickets():
    o = User.objects.get(id=1)
    d = User.objects.get(id=2)
    s1 = User.objects.get(id=3)
    s2 = User.objects.get(id=4)
    u1 = User.objects.get(id=5)
    u2 = User.objects.get(id=6)
    s = check_state_from()
    users = [d, s1, s2, u2, o, u1]
    for u in users:
        rt = RequestTicket(user=u, bank='nh', depositor_name=u.name, count=20, ticket_type='리뷰권', state=s)
        rt.save()

    for u in users:
        rt = RequestTicket(user=u, bank='nh', depositor_name=u.name, count=20, ticket_type='구매권', state=s)
        rt.save()
    
   
if __name__ =='__main__':
    """
        d_log = ses.post('http://localhost:5005/login/', json={"user": "jllab1@gmail.com", "pwd": "jllab1122", "rememeber_account": True})
        s1_log = ses.post('http://localhost:5005/login/', json={"user": "jllab01@gmail.com", "pwd": "jllab1122", "rememeber_account": True})
        s2_log = ses.post('http://localhost:5005/login/', json={"user": "jllab02@gmail.com", "pwd": "jllab1122", "rememeber_account": True})
        u1_log = ses.post('http://localhost:5005/login/', json={"user": "jllab001@gmail.com", "pwd": "jllab1122", "rememeber_account": True})
        u2_log = ses.post('http://localhost:5005/login/', json={"user": "jllab002@gmail.com", "pwd": "jllab1122", "rememeber_account": True})
        o_log = ses.post('http://localhost:5005/login/', json={"user": "jllab@gmail.com", "pwd": "jllab1122", "rememeber_account": True})
    """
    users = make_account()
    # user = User.objects.get(id=3)
    # for u in users:
    #     make_products(u)
    request_tickets()