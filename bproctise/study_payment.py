# -*- coding: utf-8 -*-
# user = www
import requests
class Payment:
    def requestOutofSystem(self, card_num, amount):
        url = "http://third.payment.com/"
        data = {"card_num": card_num, "amount": amount}
        response = requests.post(url, data=data)
        return response.status_code

    def dopay(self, user_id, card_num, amount):
        try:
            res = self.requestOutofSystem(card_num, amount)
        except TimeoutError:
            res = self.requestOutofSystem(card_num, amount)
        if res == 200:
            print("{0}支付{1}成功！扣款并记录支付记录".format(user_id, amount))
            return 'success'
        if res == 500:
            print("{0}支付{1}失败！不扣款".format(user_id, amount))
            return 'fail'
