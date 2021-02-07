import os
import pandas as pd



SAVE_PATH = r"./download"
REPORT_PATH = r"./report"



def files_finder():
    file_repo = os.listdir(SAVE_PATH)
    file_dir = {}
    for t in file_repo:
        file = os.listdir(os.path.join(SAVE_PATH,t))
        # print(file)
        file_dir[t] = None
        if len(file)>1:
            file.sort(reverse=True)
            file_dir[t] = [f"{t}/{file}" for file in file[0:2]]
        else:
            pass
    return file_dir


def prettify(portf_id,df_dict):
    ssht = pd.ExcelWriter(os.path.join(REPORT_PATH,f'{portf_id}.xlsx'),engine='xlsxwriter')
    for k in df_dict.keys():
        df_dict[k].to_excel(ssht, sheet_name=k,index=False)
    ssht.save()
    


def report_std(df):    
    df = df.rename(columns={'date_t0':'Current Date',
                        'date_t1':'Previous Date',
                        'fund_t0':'ETF Name',
                        'fund_t1':'ETF name',
                        'company_t0':'Company Name',
                        'company_t1':'Company name',
                        'ticker_t0':'Ticker',
                        'ticker_t1':'Ticker ',
                        'cusip':'CUSIP',
                        'shares_t0':'Current # of shares',
                        '"market value($)"_t0':'Current Market Value',
                        'weight(%)_t0':'Current Weight %',
                        'date_t1':'Previous Date',
                        'shares_t1':'Previous # of shares',
                        '"market value($)"_t1':'Previous Market Value',
                        'weight(%)_t1':'Previous Weight %'})
    return df



class run_analysis():
    
    def combine_file(filenames):
        df_t0 = pd.read_csv(os.path.join(SAVE_PATH,filenames[0]))
        df_t1 = pd.read_csv(os.path.join(SAVE_PATH,filenames[1]))
        df_c = df_t0.merge(df_t1,how='outer',on='cusip',suffixes=('_t0','_t1'),indicator=True)
        return df_c
    
    
    def new_members(df):
        df = df.loc[df['_merge']=='left_only']
        df = df[['fund_t0','date_t0','company_t0','ticker_t0','cusip','shares_t0','"market value($)"_t0','weight(%)_t0']]
        df['"market value($)"_t0'] = df['"market value($)"_t0'].map('{:,}'.format)
        df['shares_t0'] = df['shares_t0'].map('{:,}'.format)
        df = report_std(df)
        return df
    
    
    def removed_members(df):
        df = df.loc[df['_merge']=='right_only']
        df = df[['fund_t1','date_t1','company_t1','ticker_t1','cusip','shares_t1','"market value($)"_t1','weight(%)_t1']]
        df['"market value($)"_t1'] = df['"market value($)"_t1'].map('{:,}'.format)
        df['shares_t1'] = df['shares_t1'].map('{:,}'.format)
        df = report_std(df)
        return df
    
    
    def share_chg(df):
        df_chg = df.loc[(df['shares_t0']!=df['shares_t1'])&(df['_merge']=='both'),]
        # df_chg.loc[:,'diff'] = df_chg.loc[:,'shares_t0'].subtract(df_chg.loc[:,'shares_t1'])
        df_chg = df_chg.assign(diff = df_chg['shares_t0']-df_chg['shares_t1'])
        df_chg = df_chg[['date_t0','company_t0','ticker_t0','cusip','shares_t0','date_t1','shares_t1','diff']]
        df_chg = report_std(df_chg)
        return df_chg
    
    
    def value_chg(df):
        df_chg = df.loc[(df['"market value($)"_t0']!=df['"market value($)"_t1'])&(df['_merge']=='both'),]
        df_chg = df_chg.assign(diff = df_chg['"market value($)"_t0']-df_chg['"market value($)"_t1'])
        df_chg = df_chg[['date_t0','company_t0','ticker_t0','cusip','"market value($)"_t0','date_t1','"market value($)"_t1','diff']]
        df_chg = report_std(df_chg)
        return df_chg
    
    
    def weight_cht(df):
        df_chg = df.loc[(df['weight(%)_t0']!=df['weight(%)_t1'])&(df['_merge']=='both'),]
        df_chg = df_chg.assign(diff = df_chg['weight(%)_t0']-df_chg['weight(%)_t1'])
        df_chg = df_chg[['date_t0','company_t0','ticker_t0','cusip','weight(%)_t0','date_t1','weight(%)_t1','diff']]
        df_chg = report_std(df_chg)
        return df_chg

    
    def run_all(filenames):
        dfc = run_analysis.combine_file(filenames)
        new_df = run_analysis.new_members(dfc)
        del_df = run_analysis.removed_members(dfc)
        share_df = run_analysis.share_chg(dfc)
        val_df = run_analysis.value_chg(dfc)
        weight_df = run_analysis.weight_cht(dfc)
        return dict(new_members=new_df, del_members=del_df, share_change=share_df, val_change=val_df, weight_change=weight_df)
        