import re
from unidecode import unidecode
import urllib.parse

regex_home = r'^https?://www\.data\.gouv\.fr/(?:fr|en|es)/$'
regex_datasets_page = r'^https?://www\.data\.gouv\.fr/(?:fr|en|es)/datasets/$'
regex_datasets = r'^https?://www\.data\.gouv\.fr/(?:fr|en|es)/datasets/([a-z\-0-9]+)/$'
regex_datasets_search = r'^https?://www\.data\.gouv\.fr/(?:fr|en|es)/datasets/\?'
regex_organizations = r'^https?://www\.data\.gouv\.fr/(?:fr|en|es)/organizations/'
regex_reuses = r'^https?://www\.data\.gouv\.fr/(?:fr|en|es)/reuses/'
regex_territory = r'^https?://www\.data\.gouv\.fr/(?:fr|en|es)/territory/'
regex_topics = r'^https?://www\.data\.gouv\.fr/(?:fr|en|es)/topics/'
regex_town = r'^https?://www\.data\.gouv\.fr/(?:fr|en|es)/town/'
regex_users = r'^https?://www\.data\.gouv\.fr/(?:fr|en|es)/users/'
regex_search = r'^https?://www\.data\.gouv\.fr/(?:fr|en|es)/search/'
regex_posts = r'^https?://www\.data\.gouv\.fr/(?:fr|en|es)/posts/'
regex_faq = r'^https?://www\.data\.gouv\.fr/(?:fr|en|es)/faq/'
regex_dashboard = r'^https?://www\.data\.gouv\.fr/(?:fr|en|es)/dashboard/'
regex_apidoc = r'^https?://www\.data\.gouv\.fr/(?:fr|en|es)/apidoc/'
regex_groups = r'^https?://www\.data\.gouv\.fr/groups/'
regex_reference = r'^https?://www\.data\.gouv\.fr/(?:fr|en|es)/reference$'
regex_id = r'^https?://id\.data\.gouv\.fr/'
regex_api_spatial = r'^https?://www\.data\.gouv\.fr/api/1/spatial/'
regex_api_discussions = r'^https?://www\.data\.gouv\.fr/api/1/discussions/\?'
regex_api_issues = r'^https?://www\.data\.gouv\.fr/api/1/issues/\?'
regex_api_swagger = r'^https?://www\.data\.gouv\.fr/api/1/swagger\.json'
regex_api_datasets_frequencies = r'^https?://www\.data\.gouv\.fr/api/1/datasets/frequencies/'
regex_api_reuses = r'^https?://www\.data\.gouv\.fr/api/1/reuses/'
regex_api_metrics = r'^https?://www\.data\.gouv\.fr/api/1/metrics/'
regex_api_activity = r'^https?://www\.data\.gouv\.fr/api/1/activity'
regex_api_organizations = r'^https?://www\.data\.gouv\.fr/api/1/organizations/'
regex_api_datasets = r'^https?://www\.data\.gouv\.fr/api/1/datasets/([a-z\-0-9]+)/'
regex_api_datasets_search = r'^https?://www\.data\.gouv\.fr/api/1/datasets/\?'
regex_api_community = r'^https?://www\.data\.gouv\.fr/api/1/datasets/community_resources/\?'
regex_api_oembeds = r'^https?://www\.data\.gouv\.fr/api/1/oembeds/'
regex_api_me = r'^https?://www\.data\.gouv\.fr/api/1/me/'
regex_api_site = r'^https?://www\.data\.gouv\.fr/api/1/site/'
regex_api_users = r'^https?://www\.data\.gouv\.fr/api/1/users/'
regex_api_transfer = r'^https?://www\.data\.gouv\.fr/api/1/transfer/'
regex_api_harvest = r'^https?://www\.data\.gouv\.fr/api/1/harvest/'


def parse_visits(visits):
    unhandled_actions = []
    visits_parsed = []
    for visit in visits:
        visit_parsed = []
        for action in visit['actions']:
            match_home = re.match(regex_home, action['url'])
            match_datasets_page = re.match(regex_datasets_page, action['url'])
            match_datasets = re.match(regex_datasets, action['url'])
            match_datasets_search = re.match(
                regex_datasets_search, action['url'])
            match_organizations = re.match(regex_organizations, action['url'])
            match_reuses = re.match(regex_reuses, action['url'])
            match_territory = re.match(regex_territory, action['url'])
            match_topics = re.match(regex_topics, action['url'])
            match_town = re.match(regex_town, action['url'])
            match_users = re.match(regex_users, action['url'])
            match_search = re.match(regex_search, action['url'])
            match_posts = re.match(regex_posts, action['url'])
            match_faq = re.match(regex_faq, action['url'])
            match_dashboard = re.match(regex_dashboard, action['url'])
            match_apidoc = re.match(regex_apidoc, action['url'])
            match_groups = re.match(regex_groups, action['url'])
            match_reference = re.match(regex_reference, action['url'])
            match_id = re.match(regex_id, action['url'])
            match_api_spatial = re.match(regex_api_spatial, action['url'])
            match_api_discussions = re.match(
                regex_api_discussions, action['url'])
            match_api_issues = re.match(regex_api_issues, action['url'])
            match_api_swagger = re.match(regex_api_swagger, action['url'])
            match_api_datasets_frequencies = re.match(
                regex_api_datasets_frequencies, action['url'])
            match_api_reuses = re.match(regex_api_reuses, action['url'])
            match_api_metrics = re.match(regex_api_metrics, action['url'])
            match_api_activity = re.match(regex_api_activity, action['url'])
            match_api_organizations = re.match(
                regex_api_organizations, action['url'])
            match_api_datasets = re.match(regex_api_datasets, action['url'])
            match_api_datasets_search = re.match(
                regex_api_datasets_search, action['url'])
            match_api_community = re.match(regex_api_community, action['url'])
            match_api_oembeds = re.match(regex_api_oembeds, action['url'])
            match_api_me = re.match(regex_api_me, action['url'])
            match_api_site = re.match(regex_api_site, action['url'])
            match_api_users = re.match(regex_api_users, action['url'])
            match_api_transfer = re.match(regex_api_transfer, action['url'])
            match_api_harvest = re.match(regex_api_harvest, action['url'])

            if action['type'] == 'search':
                visit_parsed.append(('keyword', action['keyword']))

            elif action['type'] == 'action':
                if match_home:
                    pass
                elif match_datasets_page:
                    pass
                elif match_datasets:
                    dataset_slug = match_datasets.groups()[0]
                    visit_parsed.append(('slug_or_id', dataset_slug))
                elif match_datasets_search:
                    pass
                elif match_organizations:
                    pass
                elif match_reuses:
                    pass
                elif match_territory:
                    pass
                elif match_topics:
                    pass
                elif match_town:
                    pass
                elif match_users:
                    pass
                elif match_search:
                    pass
                elif match_posts:
                    pass
                elif match_faq:
                    pass
                elif match_dashboard:
                    pass
                elif match_apidoc:
                    pass
                elif match_groups:
                    pass
                elif match_reference:
                    pass
                elif match_id:
                    pass
                elif match_api_spatial:
                    pass
                elif match_api_discussions:
                    parsed = urllib.parse.urlparse(action['url'])
                    params = urllib.parse.parse_qs(parsed.query)
                    if 'for' in params:
                        dataset_id = params['for'][0]
                        visit_parsed.append(('id', dataset_id))
                elif match_api_issues:
                    parsed = urllib.parse.urlparse(action['url'])
                    params = urllib.parse.parse_qs(parsed.query)
                    if 'for' in params:
                        dataset_id = params['for'][0]
                        visit_parsed.append(('id', dataset_id))
                elif match_api_swagger:
                    pass
                elif match_api_datasets_frequencies:
                    pass
                elif match_api_reuses:
                    pass
                elif match_api_metrics:
                    pass
                elif match_api_activity:
                    pass
                elif match_api_organizations:
                    pass
                elif match_api_datasets:
                    dataset_id = match_api_datasets.groups()[0]
                    visit_parsed.append(('slug_or_id', dataset_id))
                elif match_api_datasets_search:
                    pass
                elif match_api_community:
                    parsed = urllib.parse.urlparse(action['url'])
                    params = urllib.parse.parse_qs(parsed.query)
                    if 'for' in params:
                        dataset_id = params['for'][0]
                        visit_parsed.append(('id', dataset_id))
                elif match_api_oembeds:
                    pass
                elif match_api_me:
                    pass
                elif match_api_site:
                    pass
                elif match_api_users:
                    pass
                elif match_api_transfer:
                    pass
                elif match_api_harvest:
                    pass
                else:
                    unhandled_actions.append(action)

            elif action['type'] == 'goal':
                if match_reuses:
                    pass
                elif match_datasets:
                    dataset_slug = match_datasets.groups()[0]
                    visit_parsed.append(('slug_or_id', dataset_slug))
                elif match_api_reuses:
                    pass
                elif match_id:
                    pass
                elif match_api_organizations:
                    pass
                elif match_api_transfer:
                    pass
                else:
                    unhandled_actions.append(action)

            elif action['type'] == 'outlink':
                pass

            elif action['type'] == 'download':
                pass

            else:
                unhandled_actions.append(action)
        visits_parsed.append(visit_parsed)

    return visits_parsed, unhandled_actions
