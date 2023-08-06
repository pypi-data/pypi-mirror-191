import pickle, datetime, time
import numpy as np
import pandas as pd
import os
import json
from functools import lru_cache

def save_pkl(data, dest):
    with open(dest, 'wb') as f:
        pickle.dump(data, f)

@lru_cache(500)
def load_pkl(dest):
    try:
        with open(dest, 'rb') as f:
            return pickle.load(f)
    except:
        return None

def load_json(dest):
    try:
        with open(dest, 'rb') as f:
            return json.load(f)
    except:
        return None

def calc_nav(df, ignore_first=False):
    df = df.copy()
    if ignore_first:
        df.iloc[0] = 0
        df += 1
        return df.cumprod()
    else:
        df += 1
        return df.cumprod()

def ticker_join(data, tickers): # FS에만 주로 효과가 있는듯..?
    if type(data) == pd.DataFrame:
        a = data.columns
    elif type(data) == pd.Series:
        a = data.index
    tickers = list(set(a) & set(tickers))
    return data[tickers]


class QuickDB:
    def __init__(self, yqtb=None, path=None):
        if path is None:
            self.path = "S:/all member/퀀트운용팀/93 QuickDB/"
        else:
            self.path = path
        if yqtb is None:
            self.refresh()
        else:
            self.yqtb = yqtb
    
    def getFSaccounts(self):
        return list(load_pkl(os.path.join(self.path, 'fs/200012')).keys())

    def getIDX(self):
        idx = load_pkl(os.path.join(self.path, 'ts/IDX.data'))
        idx.index = idx.index.map(lambda x : x.strftime("%Y%m%d"))
        return idx
    
    def getBdays(self, stringify=True, inverted=False):
        if stringify:
            _ = self.getIDX().index.map(lambda x : x.strftime("%Y%m%d"))
        else:
            _ = self.getIDX().index
        if inverted:
            return {v:i for i, v in enumerate(_)}
        else:
            return _

        
    def refresh(self): # daily update하면 refresh 해줘야함.
        self.yqtb = load_pkl(os.path.join(self.path, 'yq.table'))
        #self.fsdata = load_pkl(os.path.join(self.path, 'fsdata.data'))
        
    def getYQ(self, when):
        return self.yqtb.loc[:str(when)].iloc[-1]

    def getFS(self, account, date, tickers=None):
        data = {}
        for yq in self.getYQ(date).dropna().unique():
            data[yq] = load_pkl(os.path.join(self.path, f'fs/{yq}.data'))

        result = {}
        for ticker, yq in self.getYQ(date).dropna().iteritems():
            #result[ticker] = self.fsdata[yq][account].get(ticker)
            result[ticker] = data[yq][account].get(ticker)
        if tickers is not None:
            return pd.Series(result)[tickers]
        else:
            return pd.Series(result)

    def getTradables(self, start, end=None, index=""):
        """
        date에 거래정지, 정리매매 상태가 아닌 종목을 list로 반환.
        Args:
            date (str; int): 날짜. int 혹은 str 타입으로 8자리. ex)20221231

        Returns:
            list : 해당 일이 휴일이라면 빈 리스트를 반환. 그렇지 않다면 거래가능한 종목코드를 반환.
        """
        if end is None:
            end = start
        trdstp = self.getTS(88, start, end).replace({1:0, 0:1})
        liqsell = self.getTS(92, start, end).replace({1:0, 0:1})
        liqsell.loc[:'20090320'] = 1 
        # 090320 이전까지는 데이터 없음.
        # 따라서 1로 처리해서 trdstp가 1인 경우 1x1 = 1이 되도록, trdstp가 0인 경우 1x0=0이 되도록 처리
        tradable = trdstp * liqsell
        if index.upper() == "FIRST":
            return tradable.iloc[0:1].where(lambda x : x == 1).dropna(axis=1).columns.to_list()
        elif index.upper() == "LAST":
            return tradable.iloc[-1:].where(lambda x : x == 1).dropna(axis=1).columns.to_list()
        elif index.upper() == "TIPS":
            idx = [tradable.index[0], tradable.index[-1]] 
            return tradable.loc[idx].where(lambda x : x == 1).dropna(axis=1).columns.to_list()
        else:
            if len(tradable) == 0:
                return []
            return tradable
        # tradable = (trdstp * liqsell).where(lambda x : x == 1).dropna(axis=1)
        # if tradable.shape[0]:
        #     return tradable.columns.to_list()
        # else:
        #     return []

    def _getTrailingYQ(self, yq, n=4):
        y,q = yq[:4], (yq[4:])
        roll = ['03' , '06', '09', '12']

        while roll[0] != q:
            roll = np.roll(roll, 1)

        YQ = [y+q]

        for i in range(n-1):
            roll = np.roll(roll, 1)
            if roll[0] == '12':
                y = str(int(y) - 1)
            q = roll[0]
            YQ.append(y+q)
        return YQ

    def getTrailingFS(self, account, date, n=4, method=None):
        YQ = self.getYQ(date).dropna().map(lambda x : self._getTrailingYQ(x, n))
        data = {}
        for yq in np.unique(np.array(YQ.to_list()).reshape(-1)):
            data[yq] = load_pkl(os.path.join(self.path, f'fs/{yq}.data'))
        
        res = {}
        for ticker, yq in YQ.iteritems():
            try:
                res[ticker] = pd.Series(
                    #self.fsdata[_yq][account].get(ticker) for _yq in yq
                    data[_yq][account].get(ticker) for _yq in yq
                )
            except:
                pass
        df = pd.DataFrame(res).dropna(axis=1)

        if method == 'sum':
            return df.sum()
        if method == 'std':
            return df.std()
        if method == 'mean':
            return df.mean()
        else:
            return df


    def getTS(self, n, start:str, end:str=None):
        start = str(start)
        if end is None:
            end = start
        end = str(end)
        y1 = int(str(start)[:4])
        res = []
        try:
            y2 = int(str(end)[:4])
            for y in range(y1, y2+1):
                _ = load_pkl(os.path.join(self.path, f"ts/{y}_{n}.data"))
                if _ is not None:
                    res.append(_)
            return pd.concat(res).sort_index().loc[start : end]
            #.sort_index().drop_duplicates().loc[start:].iloc[0]
        except Exception as e:
            raise e