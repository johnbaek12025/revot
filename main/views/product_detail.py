import json
import random
import time
import requests
from bs4 import BeautifulSoup as bs
import re

class ClientDataException(Exception):
    pass
class DataValueEmpty(ClientDataException):
    pass

class FetchData:
    def __init__(self, pid, mall_name) -> None:
        self.url = f"https://smartstore.naver.com/{mall_name}/products/{pid}/"
        self.pid = pid
        self.mall_name = mall_name
        self.session = None
        
    def main(self):
        self.session = requests.session()
        res = self.status_validation(self.url)
        if not res:
            raise DataValueEmpty
        options = self.extract_options_data_from(res)
        print(options)
        product_dict = self.extract_product_data_from(res)        
        product_dict['options'] = options
        return product_dict
        
    def extract_product_data_from(self, info):
        info = bs(info, 'html.parser')
        options_info = info.find_all('script')[0]
        data_dict = json.loads(options_info.text)
        name = data_dict['name'].split(' : ')[0]
        img_url = data_dict['image']
        price = data_dict['offers']['price']
        return {"name": name, "img_url": img_url, "price": price}
        # self.save_file(json.dumps(data_dict, ensure_ascii=False), f'checking_data/{self.pid}_{self.mall_name}_product.json')
    
    def extract_options_data_from(self, info):
        info = bs(info, 'html.parser')
        options_info = info.find_all('script')[1]
        options_info = re.sub(r'window.__PRELOADED_STATE__=', '', options_info.text)
        data_dict = json.loads(options_info)['selectedOptions']['A']
        text_options = data_dict.get('textOptions')
        simple_options = data_dict.get('simpleOptions')
        comb_options = data_dict.get("combinationOptions")
        color_options = data_dict.get("colorOptions")
        size_options = data_dict.get("sizeOptions")
        supplements = data_dict.get('supplementProducts', None)
             
        option_dict = {}
        cnt = 0        
        if text_options:                      
            cnt += len(text_options)
            print(f"text_options {len(text_options)}")
            option_dict.update(self.extract_text_options_from(text_options))
        if simple_options:
            cnt += len(simple_options)
            print(f"simple_options {len(simple_options)}")
            option_dict.update(self.extract_simple_options_from(simple_options))
        if comb_options:
            opt_cnt, extracted_option = self.extract_comb_options_from(comb_options)
            cnt += opt_cnt
            option_dict.update(extracted_option)
        if color_options:
            print(f"color_options {len(color_options)}")
            cnt += len(color_options)
            option_dict.update(self.extract_color_options_from(color_options))
        if size_options:
            print(f"size_options {len(size_options)}")
            cnt += len(size_options)
            option_dict.update(self.extract_size_options_from(size_options))
        options_info = {"option_count": cnt, "options": option_dict}
        if supplements:
            print(supplements, len(supplements))
            print(f"supplements {len(supplements)}")
            cnt += len(supplements)
            options_info.update({"supplements": self.extract_supplements_from(supplements)})
        # self.save_file(json.dumps(data_dict, ensure_ascii=False), f'checking_data/{self.pid}_{self.mall_name}_options.json')        
        return options_info
        
        
        # options_dict = data_dict['selectedOptions']
        
    def extract_text_options_from(self, text_options):
        option_dict = {}
        for option in text_options:
            option_dict[option['groupName']] = ""
        # self.save_file(json.dumps(option_dict, ensure_ascii=False), f'checking_data/{self.pid}_{self.mall_name}_text_options.json')
        return option_dict        
    
    def extract_simple_options_from(self, simple_options):
        option_dict = {}
        for option in simple_options:
            option_dict[option['groupName']] = [o['name'] for o in option['options']]
        # self.save_file(json.dumps(option_dict, ensure_ascii=False), f'checking_data/{self.pid}_{self.mall_name}_simple_options.json')
        return option_dict
    
    def extract_comb_options_from(self, comb_options):
        option_dict = {}
        key_list = []
        detail_list = []
        for cnt, option in enumerate(comb_options, start=1):
            print(cnt)
            key_list.append(option['groupName'])
        options = comb_options[0]['options']
        for option in options:
            detail_list.append(', '.join([option[o] for o in option if re.match(r'optionName\d', o)]))
                    
        option_dict['-'.join(key_list)] = detail_list
        return cnt, option_dict
            
        
    # def extract_comb_options_from(self, comb_options):
    #     option_dict = {}
        
    #     for option in comb_options:
    #         option_dict[option['groupName']] = []            
            
    #     option_list = []
    #     options = comb_options[0]['options']
    #     for option in options:
    #         option_list.append([option[o] for o in option if re.match(r'optionName\d', o)])
            
    #     for option in option_list:
    #         for i, o in enumerate(option):
    #             option_dict[list(option_dict.keys())[i]].append(o)
    #     # self.save_file(json.dumps(option_dict, ensure_ascii=False), f'checking_data/{self.pid}_{self.mall_name}_comb_options.json')
    #     return option_dict
        
    def extract_size_options_from(self, size_options):
        option = size_options[self.pid]
        option_dict = {option['groupName']: [o['optionName'] for o in option['options']]}
        # self.save_file(json.dumps(option_dict, ensure_ascii=False), f'checking_data/{self.pid}_{self.mall_name}_size_options.json')
        return option_dict
        

    def extract_color_options_from(self, color_options):
        option = color_options[self.pid]
        option_dict = {option['groupName']: [o['optionName'] for o in option['options']]}
        # self.save_file(json.dumps(option_dict, ensure_ascii=False), f'checking_data/{self.pid}_{self.mall_name}_color_options.json')
        return option_dict
        
        
        
    def extract_supplements_from(self, supplements):
        option_dict = {}
        for sup in supplements:
            option_dict[sup['groupName']] = [o['name'] for o in sup['options']]
        # self.save_file(json.dumps(option_dict, ensure_ascii=False), f'checking_data/{self.pid}_{self.mall_name}_supplements.json')
        return option_dict
        
    
    def save_file(self, data, file_name):
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(str(data))
    
    def status_validation(self, url):       
        time.sleep(random.choice([1, 3]))
        try:
            res = self.session.get(url)
        except:
            time.sleep(10)
            res = self.session.get(url)
        status = res.status_code
        if status == 200:            
            try:                
                return res.json()
            except json.JSONDecodeError:                
                return res.text
        else:
            return None

if __name__ == '__main__':
    fd = FetchData(mall_name='garakfruit', pid='123486199')
    fd.main()