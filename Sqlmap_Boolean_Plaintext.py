import re
import os
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', dest='read', help='select sqlmap payload log file')
    args = parser.parse_args()

    if args.read == None:
        parser.print_help()
        os._exit(0)
    
    # 用到的一些变量
    payload_list = []
    result_dict = {}
    result_list = []
    
    # 根据不同的日志填写不同的正则 请灵活修改
    re_str = "0,1\)\),\s(\s+),.+>(\s+)"

    print("\033[33m[!]\033[0m 正在使用的正则表达式:\033[33m", re_str, "\033[0m")

    try:
        print("\033[34m[*]\033[0m 正在读取分析文件:\033[34m", args.read, "\033[0m")
        f = open(args.read, "r")
        lines = ''.join(f.readlines()).split("\n")
        try:
            # 提取数字放入到列表中
            number_pattern = re.compile(r'{}'.format(re_str))
            flag = number = number_pattern.findall(lines[0])
            if flag:
                for line in lines:
                    number = number_pattern.findall(line)
                    if number:
                        payload_list.append(number[0])
                        # print(number[0]) # 观察一些这个输出就清楚正则的写法了
            else:
                print("\033[31m[-] 正则表达式无法从目标文件提取数据\033[0m")
                os._exit(0)
            
            print("\033[32m[+]\033[0m 还原的明文结果: \033[32m", end="")
            # 数据分析并转换编码
            for i in payload_list:
                result_dict[i[0]]=i[1]
            for value in result_dict.values():
                result_list.append(int(value))
            for j in result_list:
                print(chr(j), end="")
            print("\033[0m")
          
        except Exception as e:
            print("\033[31m[-] 正则表达式语法有误\033[0m")
    except Exception as e:
        print("\033[31m[-] 文件路径或文件内容有误\033[0m")

if __name__ == '__main__':
    main()