__author__ = 'felo'

def print_welcome_info():
    '''
    打印欢迎信息。
    '''
    line = '-'*50
    print('''
%s
欢迎登陆felo的二手货市场:
1\t\t进入购物通道
2\t\t查看我的购物车
%s
''' % (line, line))

def choose_product_list(my_money, product_dict, shopping_dict):
    '''
    选择购物函数
    :param product_dict: 产品字典
    :param shopping_dict: 购物字典
    :return:shopping_dict：购物字典

    '''

    while True:
        #定义产品列表，用于临时存放用户已经选择的产品列表：
        product_list = []
        line = '-'*50
        money = 0
        for i in shopping_dict:
            #计算余款
            money = product_dict[i] * shopping_dict[i] + money
            money_left = my_money - money
            #如果钱不足，显示出来
            if money_left < 0:
                money_left = '不足'
        print('''
%s
欢迎登陆felo的二手货市场->购物通道:
%s
序号\t\t产品\t\t\t价格\t余额：%s
    ''' % (line, line, str(money_left)))

        #打印可购买产品的列表：
        for i in enumerate(product_dict):
            print('%s\t%s\t￥%s' % (str(i[0]).ljust(10, ' '), i[1].ljust(18, ' '),
                                        str(product_dict[i[1]]).ljust(9, ' ')))
            product_list.append(i[1])

        #开始选择：
        choose_product = input('请输入您的选择(B返回)：')
        #如果B就返回
        if choose_product is 'B' or choose_product is 'b':
            break
        elif choose_product in product_list:
            choose_product = product_list.index(choose_product)
        elif choose_product.isdigit():
            if int(choose_product) <= len(product_list):
                choose_product = int(choose_product)
            else:
                print('错误输入，重来')
                continue
        else:
            print('错误输入，重来')
            continue
        while True:
            try:
                choose_product_count = shopping_dict[product_list[choose_product]]
            except:
                choose_product_count = 1
            choose_count = input('输入数量（已选择%d个）：' % choose_product_count)
            if choose_count == '':
                choose_count = 1
                shopping_dict[product_list[choose_product]] = choose_count
                break
            elif choose_count.isdigit():
                choose_count = int(choose_count)
                shopping_dict[product_list[choose_product]] = choose_count
                break
            else:
                print('错误输入，重来')
                break
    return shopping_dict

def print_shopping_list(my_money, product_dict, shopping_dict):
    '''
    打印已经在购物车中产品的列表
    序号——产品——价格——数量
    分别打印出来，用于用户选择
    '''
    line = '-' * 50
    money = 0
    product_list = []

    print('''
您老人家这次选了下面这些东西：
%s
序号\t\t产品\t\t\t\t\t价格\t\t数量
''' % line)
    for i in enumerate(shopping_dict):
        print('%s\t%s\t￥%s\t%s' % (str(i[0]).ljust(10, ' '), i[1].ljust(18, ' '),
                                    str(product_dict[i[1]]).ljust(9, ' '), shopping_dict[i[1]]))
        money += product_dict[i[1]] * shopping_dict[i[1]]
        product_list.append(i[1])
    print(line)
    if my_money-money <0:
        money_left = '不足'
    else:
        money_left = my_money-money

    print('花费:￥%d,余额：￥%s' % (money, str(money_left)))
    return product_list, money

def choose_shopping_list(my_money, product_dict, shopping_dict):
    '''
    处理购物车函数
    :param my_money:我的钱
    :param product_dict: 产品字典
    :param shopping_dict: 购物字典,key:产品，value:数量
    :return:shopping_dict：购物字典
    '''
    #显示一下购物车中的产品
    product_list_money = print_shopping_list(my_money,product_dict, shopping_dict)
    while True:
        #对已经在购物车中清单进行修改删除或者完成等操作
        choose_change_list = input('是否修改购物列表(修改(c)/删除(d)/继续购物(e)/完成(q))：')
        #修改购物车中产品，通过选择产品，修改数量来实现
        if choose_change_list.lower() == 'c':
            choose_to_change_name = input('请选择修改的产品：')
            if choose_to_change_name.isdigit():
                if int(choose_to_change_name) <= len(product_list_money[0]):
                    choose_to_change_name = int(choose_to_change_name)
                    choose_to_change_count = input('请输入数量【已选数量:%d】：' %
                    shopping_dict[product_list_money[0][choose_to_change_name]])
                    if choose_to_change_count.isdigit():
                        shopping_dict[product_list_money[0][choose_to_change_name]] \
                            = int(choose_to_change_count)
                        product_list_money = print_shopping_list(my_money,product_dict, shopping_dict)
        #直接删除购物车中已购产品的字典键值对，实现删除
        elif choose_change_list.lower() == 'd':
            choose_to_change_name = input('请选择删除的产品：')
            if choose_to_change_name.isdigit():
                if int(choose_to_change_name) <= len(product_list_money[0]):
                    choose_to_change_name = int(choose_to_change_name)
                    shopping_dict.pop(product_list_money[0][choose_to_change_name])
                    product_list_money = print_shopping_list(my_money,product_dict, shopping_dict)
        #继续购物就退出循环，如果此时钱不够购物车中商品的话，不允许退出
        elif choose_change_list.lower() == 'e':
            if my_money < product_list_money[1]:
                print('你丫钱不够,请选择修改购物列表')
                continue
            else:
                break
        #退出，如果此时钱不够购物车中商品的话，不允许退出
        elif choose_change_list.lower() == 'q':
            if my_money - product_list_money[1] <0:
                print('余额不足,不能退出。')
            else:
                product_list_money = print_shopping_list(my_money, product_dict, shopping_dict)
                exit()
        else:
            print('错误输入，重来')
    return shopping_dict

def shopping():
    money = 10000
    product = {
        '破鞋子': 20,
        '旧衣服': 100,
        '旧马桶': 35,
        '苹果手机': 300,
        '读者': 5,
        '方便面': 2,
        '矿泉水': 1,
    }
    #shopping_dict = {}
    shopping_dict = {
        '破鞋子': 1,
        '旧衣服': 2,
        '旧马桶': 1,
        '苹果手机': 2,
        '读者': 100,
    }
    while True:
        #主循环
        print_welcome_info()
        choose = input('请输入您的选择(Q退出)：')
        if choose == '1':
            #开始购物
            shopping_dict = choose_product_list(money,product,shopping_dict)
        elif choose == '2':
            #查看或修改购物车中物品
            shopping_dict = choose_shopping_list(money, product, shopping_dict)
        elif choose == 'Q' or choose == 'q':
            #退出
            break
        else:
            print('错误输入，重来吧...')

if __name__ == '__main__':
    shopping()




