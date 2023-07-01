#!pip install GoogleNews
#!pip install newspaper3k
#!pip install openpyxl
from GoogleNews import GoogleNews
from newspaper import Article
import pandas as pd
from newspaper import Config
import nltk
import sentiment_analysis as sa
#nltk.download('punkt')

def search(name, start_date, end_date):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    config = Config()
    config.browser_user_agent = user_agent
    config.request_timeout = 50
    googlenews=GoogleNews(start=start_date,end=end_date)
    googlenews.search(name)
    result=googlenews.result()
    df=pd.DataFrame(result)

    for i in range(2,20):
        googlenews.getpage(i)
        result=googlenews.result()
        df=pd.DataFrame(result)
    list1=[]
    left_links= ''
    count = 0
    for ind in df.index:
        print(ind)
        dict={}
        article = Article(df['link'][ind],config=config)
        print(article)
        try:
            article.download()
            article.parse()
            article.nlp()
            dict['Date']=df['date'][ind]
            dict['Media']=df['media'][ind]
            
            dict['Title']=article.title
            dict['Article']=article.text
            dict['Links']=df['link'][ind]
            dict['Summary']=article.summary
            Sentiment = sa.sentiment_score(dict['Summary'])
            print(Sentiment)
            dict['Sentiment'] = Sentiment
            list1.append(dict)
            count += 1
            print('added count: ', count)
        except:
            print('count: ', count)
            print("This number of link is left: ", ind)
            left_links+= df['link'][ind] + ',/n'
            continue
        if count > 5:
            news_df=pd.DataFrame(list1)
            news_df.to_excel("C:/Users/JENILPATEL/Desktop/sentiment/data/" +name+ "_final.xlsx")
            left_links = left_links.split(',/n')
            print(left_links)
            with open(r'C:/Users/JENILPATEL/Desktop/sentiment/data/'+name+'_left_links_final.txt', 'w') as fp:
                for item in left_links:
                    fp.write("%s\n" % item)
                print('Done')
            break
    if count < 5:
        news_df=pd.DataFrame(list1)
        news_df.to_excel("C:/Users/JENILPATEL/Desktop/sentiment/data/" +name+ "_final.xlsx")
        left_links = left_links.split(',/n')
        print(left_links)

        with open(r'C:/Users/JENILPATEL/Desktop/sentiment/data/'+name+'_left_links.txt', 'w') as fp:
            for item in left_links:
                fp.write("%s\n" % item)
            print('Done')
    return news_df
