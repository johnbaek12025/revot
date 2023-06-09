import django
import os, sys
from datetime import datetime
from random import randrange
from datetime import timedelta


# django setting 파일 설정하기 및 장고 셋업
cur_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))  # 프로젝트 폴더

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "barley.settings")
django.setup()


from main.models.client import Product, User, State, ProductFolder
from main.models.clientdata import RequestTicket
from main.models.pseudo import Purchase, Review
from django.contrib.auth.hashers import make_password
from main.models.security import LoginSession

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
    u2 = User(email_account='jllab002@gmail.com', password=make_password('jllab1122'), agency_code='1111', recommendation_code='JEHOVA', authorization=True, phone='0102222244444', name='user2', authorized_by=s2 ,review_ticket=100, purchase_ticket=100, self_code='SLOWER', higherarchy=u_s)
    u2.save()
    u3 = User(email_account='test@test.com', password=make_password('test1122'), agency_code='1111', recommendation_code='JEHOVA', authorization=True, phone='0102222244444', name='user2', authorized_by=s2 ,review_ticket=0, purchase_ticket=0, self_code='MICROS', higherarchy=u_s)
    u3.save()
    
    
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
    

def purchase_registe():    
    u1 = User.objects.get(id=5)
    s = check_state_from(1)
    p_list = Product.objects.filter(owner=u1, state=s)
    d1 = datetime.strptime('2023/3/20 1:30 PM', '%Y/%m/%d %I:%M %p')
    d2 = datetime.strptime('2024/1/1 4:50 AM', '%Y/%m/%d %I:%M %p')
    i = check_state_from(0)
    for p in p_list:        
        rd, rt = random_date(d1, d2).strftime('%Y-%m-%d %H:%M').split(' ')
        print(rd)
        # pp = Purchase(product=p, count=20, reservation_date=rd, reservation_at=rt, state=i)
        # pp.save()


def request_tickets():
    o = User.objects.get(id=1)
    d = User.objects.get(id=2)
    s1 = User.objects.get(id=3)
    s2 = User.objects.get(id=4)
    u1 = User.objects.get(id=5)
    u2 = User.objects.get(id=6)
    s = check_state_from()
    
    for i in range(1, 200):
        rt = RequestTicket(user=u1, bank='nh', depositor_name=u1.name, count=i, ticket_type='리뷰권', state=s)
        rt.save()
    for i in range(1, 200):
        rt = RequestTicket(user=u1, bank='nh', depositor_name=u1.name, count=i, ticket_type='구매권', state=s)
        rt.save()
    
    # users = [d, s1, s2, u2, o, u1]
    # for u in users:
    #     rt = RequestTicket(user=u, bank='nh', depositor_name=u.name, count=20, ticket_type='리뷰권', state=s)
    #     rt.save()

    # for u in users:
    #     rt = RequestTicket(user=u, bank='nh', depositor_name=u.name, count=20, ticket_type='구매권', state=s)
    #     rt.save()
    
def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

    
   
if __name__ =='__main__':
    """
        d_log = ses.post('http://localhost:5005/login/', json={"user": "jllab1@gmail.com", "pwd": "jllab1122", "rememeber_account": True})
        s1_log = ses.post('http://localhost:5005/login/', json={"user": "jllab01@gmail.com", "pwd": "jllab1122", "rememeber_account": True})
        s2_log = ses.post('http://localhost:5005/login/', json={"user": "jllab02@gmail.com", "pwd": "jllab1122", "rememeber_account": True})
        u1_log = ses.post('http://localhost:5005/login/', json={"user": "jllab001@gmail.com", "pwd": "jllab1122", "rememeber_account": True})
        u2_log = ses.post('http://localhost:5005/login/', json={"user": "jllab002@gmail.com", "pwd": "jllab1122", "rememeber_account": True})
        o_log = ses.post('http://localhost:5005/login/', json={"user": "jllab@gmail.com", "pwd": "jllab1122", "rememeber_account": True})
    """
    # d1 = datetime.strptime('2023/3/3 1:30 PM', '%Y/%m/%d %I:%M %p')
    # d2 = datetime.strptime('2024/1/1 4:50 AM', '%Y/%m/%d %I:%M %p')
    # for _ in range(10):
    #     print(random_date(d1, d2).strftime('%y-%m-%d %H:%M').split(' '))
    # users = make_account()
    user = User.objects.get(email_account='test@test.com')
    print(user)
    x = LoginSession.objects.filter(id=54, account=user)    
    print(x)
    
    # for u in users:
    #     make_products(u)
    # request_tickets()
    # purchase_registe()
    # date1 = input('날짜를 %Y-%m-%d 순으로 입력: ')
    # cd, ct = datetime.now().strftime('%Y-%m-%d %H:%M').split(' ')
    # # print(cd, ct)
    # if date1 == cd:
    #     d1 = datetime.strptime(f"{cd} {ct}", '%Y-%m-%d %H:%M')
    #     d2 = datetime.strptime(f"{cd} 23:59", '%Y-%m-%d %H:%M')
    #     rd, rt = random_date(d1, d2).strftime('%Y-%m-%d %H:%M').split(' ')    
    # else:
    #     d1 = datetime.strptime(f"{cd} 00:00", '%Y-%m-%d %H:%M')
    #     d2 = datetime.strptime(f"{cd} 23:59", '%Y-%m-%d %H:%M')
    #     rd, rt = random_date(d1, d2).strftime('%Y-%m-%d %H:%M').split(' ')
    # print(rd, rt)
    # datetime.strptime(f"{d1} ", )
    