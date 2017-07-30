# -*- coding: utf-8 -*-

import tushare as ts
import json
import pickle

def main():
    # df = ts.get_h_data('600816', start='2017-01-01', end='2017-03-16')
    # df.to_pickle('test.pickle')
    with open('test.pickle','rb') as fd:
        df = pickle.load(fd)
        print df
    return
    # for v in df['open']:
    #     print v
    # print df['open']
    # return
    # 注意数据是按时间的递减序排的
    names = ['open', 'high', 'close', 'low', 'volume', 'amount']
    startYear = 2011
    endYear = 2018
    for code in ['600816']:
        jsonMap = {'colNames': names, 'rows': []}
        try:
            df = ts.get_h_data(code, start=str(startYear)+'-01-01', end=str(endYear)+'-01-01')
            if df is None:
                continue
        except Exception, ex:
            print ex
            continue
        m = len(df[names[0]])
        for i in range(m):
            map_ = {}
            for name in names:
                if type(df[name][i]) == str:
                    map_[name] = df[name][i]
                elif type(df[name][i]) == unicode:
                    map_[name] = df[name][i].encode('utf-8')
                else:
                    try:
                        map_[name] = float(df[name][i])
                    except Exception, ex:
                        print ex
                        map_[name] = 'error'
            jsonMap['rows'].append(map_)
        with open('priceData/' + ('.'.join(['price', code, str(startYear), str(endYear), 'json'])), 'w') as fd:
            json.dump(jsonMap, fd, encoding='utf-8', indent=4, separators=[',', ':'], ensure_ascii=False)
            # return


if __name__ == '__main__':
    main()
