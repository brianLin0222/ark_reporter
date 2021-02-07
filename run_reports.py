from get_data import *
from report_gen import *
from dist_report import *
from content import *
from charts import *
from json import load


LINE_CHG = '\n'
IMG_PATH = [r'./img/elon-featured.jpg']

## there is zero exception handling here because I am too lazy
## also there are path references in those .py files, again I am too lazy to change them
def run_all(get_data=True):
    if get_data:
        for t in REPORTS.keys():
            data = ARKreport(t)
    else:
        print('Skipped data gathering...')
        
    
    file_dict = files_finder()
    added_df = []
    dropped_df = []
    charts = []
    
    for k in file_dict.keys():
        report = run_analysis.run_all(file_dict[k])
        
        df = report['px_diff']
        lbl = [f'{row[0]}{LINE_CHG}{"${:.2f}".format(row[1])}' for row in zip(df['Ticker'],df['Price Diff($)'],df['Current Weight %'].loc[df['Current Weight %']>=0.2])]
        img = treemap.draw(size_scale=df['Current Weight %'],label=lbl,color_scale=df['Price Change(%)'])
        fig = img.get_figure()
        fig.set_figwidth(16)
        fig.set_figheight(9)
        img_path = f'./img/{k}.png'
        fig.savefig(img_path,bbox_inches='tight')
        charts.append(img_path)
        plt.close(fig)
        
        added_df.append(report['new_members'])
        dropped_df.append(report['del_members'])
        prettify(k,report)
        
    
    with open(r'./config.json') as cfg:
        config = load(cfg)
    
    
    cnt = body_render({'new_df':f'{pd.concat(added_df).to_html(index=False)}',
                        'remove_df':f'{pd.concat(dropped_df).to_html(index=False)}'
                        })

    
    creds = find_token()
    service = service_login(creds)
    content = create_content(config['sendFrom'],f"{(',').join(config['sendTo'])}","LazyInvestor.io Report")
    file_dict = files_finder()
    IMG_PATH.extend(charts)
    msg = content.multi_content(cnt,img=IMG_PATH,attach=list(file_dict.keys()))
    service.users().messages().send(userId=config['sendFrom'],body=msg).execute()
    input("Report sent!\nPress any key to exit...")



# if __name__ == "__main__":
#     run_all()
    
    
