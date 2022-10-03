import pandas as pd
from ast import literal_eval


def load_data(path="ycombinator.csv"):
    df = pd.read_csv(path)

    df['about_founders'] = df['about_founders'].fillna('[]')
    df['about_founders'] = df['about_founders'].apply(literal_eval)
    df['active_founders'] = df['active_founders'].fillna('[]')
    df['active_founders'] = df['active_founders'].apply(literal_eval)
    df['company_socials'] = df['company_socials'].apply(literal_eval)
    df['tags'] = df['tags'].apply(literal_eval)

    df['no_founders'] = df['about_founders'].apply(lambda x: len(x))
    df['no_company_socials'] = df['company_socials'].apply(lambda x: len(x))
    df['no_tags'] = df['tags'].apply(lambda x: len(x))

    df.insert(0, 'company_id', range(1, 1 + len(df)))
    df['full_location'] = df['full_location'].fillna('na')

    df['team_size'] = df['team_size'].fillna('-1').astype(int)
    df['founded'] = df['founded'].fillna('-1').astype(int)
    df['country'] = df.full_location.apply(lambda x: x.split(',')[-1].strip())

    company_df = df[['company_id', 'company_name', 'link', 'short_description', 'founded', 'team_size', 'location', 'country', 'no_founders', 'no_company_socials', 'no_tags','description']]
    company_df.columns = ['id', 'company_name', 'link', 'short_description', 'founded', 'team_size', 'location', 'country', 'no_founders', 'no_company_socials', 'no_tags', 'description']

    return df, company_df


def founder_data(df):
    f_df = df[['company_id', 'company_name', 'about_founders']]
    f_df = f_df.explode("about_founders")
    
    founders = f_df['about_founders'].apply(pd.Series)
    founders = pd.concat([df['company_id'], founders], axis=1)
    founders = founders[~founders['name'].isna()]
    founders.insert(0, 'founder_id', range(1, 1 + len(founders)))

    return founders


def founder_and_social(df, socials_mapper):
    founders_info = founder_data(df)
    founder_info_only = founders_info[['founder_id', 'name', 'role', 'company_id']]
    f_social = founders_info.explode("social_media_links")
    f_social['social_media_links'] = f_social['social_media_links'].astype(str)
    f_social['social_media_links'] = f_social['social_media_links'].str.lower().str.replace(r'(//[a-zA-Z]{2}[.])', '//')
    f_social['social_name'] = f_social['social_media_links'].str.extract(r'(https://)(www.|mobile.)?([a-zA-Z0-9]*)')[2]
    f_social['social_name'] = f_social['social_name'].str.replace(r'(linkedin|linked|ca|google)', 'linkedin')
    f_social = f_social[~f_social['social_name'].isna()]

    f_social['social_media_id'] = f_social['social_name'].map(socials_mapper)
    f_social['social_media_id'] = f_social['social_media_id'].astype(int)
    f_social.insert(0, 'id', range(1, 1 + len(f_social)))

    founder_social_to_social = f_social[['id', 'social_media_id', 'founder_id']]
    founder_info_only.columns = ['id', 'name', 'role', 'company_id']
    return founder_info_only, founder_social_to_social



def get_social_data(df):
    c_social = df[['company_id', 'company_name', 'company_socials']]
    c_social = c_social.explode("company_socials")
    c_social['company_socials'] = c_social['company_socials'].str.lower().str.replace(r'(//[a-zA-Z]{1,2}[.])', '//')
    c_social['social_name'] = c_social['company_socials'].str.extract(r'(https://|http://|https:://)(www.|web.|business.)?([a-zA-Z0-9]*)')[2]

    list_socials = list(c_social['social_name'].value_counts().index)
    list_socials.append("github")

    socials_mapper = {social: i + 1 for i, social in enumerate(list_socials)}
    socials_df =pd.DataFrame(list(socials_mapper.items()),columns=['social', 'id'])
    socials_df = socials_df[['id', 'social']]

    c_social['social_media_id'] = c_social['social_name'].map(socials_mapper)
    c_social['social_media_id'] = c_social['social_media_id'].fillna(-1).astype(int)
    c_social = c_social[~c_social['social_name'].isna()]
    c_social.insert(0, 'id', range(1, 1 + len(c_social)))
    company_social_to_social = c_social[['id', 'social_media_id', 'company_id']]
    
    return socials_df, company_social_to_social, socials_mapper


def get_tags_data(df):
    t_df = df[['company_id', 'company_name', 'tags']]
    t_df = t_df.explode("tags")

    tags = list(t_df['tags'].value_counts().index)
    tags_mapper = { tag: i+1 for i, tag in enumerate(tags)}
    tag_df = pd.DataFrame(list(tags_mapper.items()),columns=['tag', 'id'])
    tag_df = tag_df[['id', 'tag']]

    tag_company = t_df.copy()
    tag_company['tag_id'] = tag_company['tags'].map(tags_mapper)
    tag_company.insert(0, 'id', range(1, 1 + len(tag_company)))
    company_to_tag = tag_company[['id', 'company_id', 'tag_id']]

    return tag_df, company_to_tag



all_df, company_df = load_data()
social_df, company_social_to_social, socials_mapper = get_social_data(all_df)
founder_df, founder_social_to_social = founder_and_social(all_df, socials_mapper)
tag_df, company_to_tag = get_tags_data(all_df)


all_df = pd.read_csv('data/ycombinator_all.csv')
company_df = pd.read_csv('data/company.csv')
founder_df = pd.read_csv('data/founder.csv')
social_df = pd.read_csv('data/socials.csv')
tags_df = pd.read_csv('data/tags.csv')
company_to_tag_df = pd.read_csv("data/company_to_tag.csv")
founder_social_to_social_df = pd.read_csv("data/founder_social_to_social.csv")
company_social_to_social = pd.read_csv("data/company_social_to_social.csv")


founder_sum = founder_df.groupby('company_id')['id'].count().sum()
if founder_sum == all_df['no_founders'].sum():
    print('\nfounder check passed')
    print('Total sum is', founder_sum)
else:
    print("Founder sum failed")


social_sum = company_social_to_social.groupby('company_id')['social_media_id'].count().sum()
if social_sum == all_df['no_company_socials'].sum():
    print('\ncompany social sum check passed')
    print('Total sum is', social_sum)
else:
    print(all_df['no_company_socials'].sum())



