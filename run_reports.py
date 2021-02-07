from get_data import *
from report_gen import *
from dist_report import *
from content import *
from json import load


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
    
    for k in file_dict.keys():
        report = run_analysis.run_all(file_dict[k])
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
    msg = content.multi_content(cnt,img=r'./img/elon-featured.jpg',attach=list(file_dict.keys()))
    service.users().messages().send(userId=config['sendFrom'],body=msg).execute()
    input("Report sent!\nPress any key to exit...")



if __name__ == "__main__":
    run_all()
    
    
