#!/usr/bin/env python3

import sys, csv

class Args(object):

    def __init__(self):
        self.par = self._read_input()

    def _read_input(self):
        self.args = sys.argv[1:]
        indexs = ['-c', '-d', '-o']
        par = []

        for i in indexs:
           if i in self.args:
               index = self.args.index(i)
               c = self.args[index+1]
               par.append(c)
           else:
               raise ValueError
        return par

class Config(object):
    def __init__(self, fname):
        self.config = self._read_config(fname)

    def _read_config(self, fname):
        config = {}
        with open(fname, 'r') as file:
            lines = file.readlines()
            for line in lines:
                strs = line.split('=')
                config[strs[0].strip()]=float(strs[1].strip())
        config['Rate'] = config['YangLao']+config['YiLiao']+config['ShiYe']+config['GongShang']+config['ShengYu']+config['GongJiJin']
        return config

class UserData(object):
    def __init__(self, fname):
        self.userdata = self._read_user_data(fname)

    def _read_user_data(self, fname):
        with open(fname, 'r') as file:
            users = {}
            lines = file.readlines()
            for line in lines:
                u = line.split(',')
                users[u[0].strip()]=float(u[1].strip())
        return users
        
class IncomeTaxCalculator(object):

    def cal_for_all_userdata(self, user_salary, config):
        user_salary = float(user_salary)
        low = config['JiShuL']
        top = config['JiShuH']
        rate = config['Rate']
        u_s = []
        low_pay_tax = user_salary*(1-rate)-3500
        top_pay_tax = user_salary-top*rate-3500
        if  user_salary >0 and low_pay_tax <= 0:
            insure = user_salary * rate
            tax = 0
            pay_tax = 0
        elif low_pay_tax > 0 and user_salary < top:
            insure = user_salary * rate
            pay_tax = low_pay_tax
        else:
            insure = top*rate
            pay_tax = top_pay_tax

        if pay_tax < 1500:
            tax = pay_tax*0.03
            after_tax = user_salary-insure-tax
        elif pay_tax < 4500:
            tax = pay_tax*0.1-105
        elif pay_tax < 9000:
            tax = pay_tax*0.2-555
        elif pay_tax < 35000:
            tax = pay_tax*0.25-1005
        elif pay_tax < 55000:
            tax = pay_tax*0.3-2755
        elif pay_tax < 80000:
            tax = pay_tax*0.35-5505
        else:
            tax = pay_tax*0.45-13505
        after_tax = user_salary-insure-tax
        u_s.append(insure)
        u_s.append(tax)
        u_s.append(after_tax)
        #return insure, tax, after_tax
        return u_s

if __name__ == '__main__':
    a = Args()
    p = a.par
    c = Config(p[0])
    u = UserData(p[1])
    i = IncomeTaxCalculator()
    ud = u.userdata
    
    for key, value in ud.items():
        s = i.cal_for_all_userdata(u.userdata[key],c.config)
        print(s)

 
