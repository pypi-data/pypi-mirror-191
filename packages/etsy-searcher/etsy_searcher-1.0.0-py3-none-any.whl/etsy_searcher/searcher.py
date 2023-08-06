from typing import List
from bs4 import BeautifulSoup
import requests

from etsy_searcher.models.Result import Result

class EtsySearcher:
    
    def __init__(self) -> None:
        self.session = requests.Session()
        self.request_url = "https://www.etsy.com/api/v3/ajax/bespoke/member/neu/specs/async_search_results"
        
    def get_csrf_token(self) -> str:
        req = self.session.get("https://etsy.com/")
        bs = BeautifulSoup(req.content, "html.parser")
        csrf_nonce = bs.find("meta", attrs={"name": "csrf_nonce"})
        return csrf_nonce.get("content")
    
    def prepare_request_body(self, keyword: str, page: int, order: str, only_star_seller: bool):
        
        ref = "search_bar"
        if page != 1:
            ref = "pagination"
        
        data = {
            "log_performance_metrics": True,
            "specs[async_search_results][]": "Search2_ApiSpecs_WebSearch",
            "specs[async_search_results][1][search_request_params][detected_locale][language]": "en-US",
            "specs[async_search_results][1][search_request_params][detected_locale][currency_code]": "USD",
            "specs[async_search_results][1][search_request_params][detected_locale][region]": "US",
            "specs[async_search_results][1][search_request_params][locale][language]": "en-US",
            "specs[async_search_results][1][search_request_params][locale][currency_code]": "USD",
            "specs[async_search_results][1][search_request_params][locale][region]": "US",
            "specs[async_search_results][1][search_request_params][name_map][query]": "q",
            "specs[async_search_results][1][search_request_params][name_map][query_type]": "qt",
            "specs[async_search_results][1][search_request_params][name_map][results_per_page]": "result_count",
            "specs[async_search_results][1][search_request_params][name_map][min_price]": "min",
            "specs[async_search_results][1][search_request_params][name_map][max_price]": "max",
            "specs[async_search_results][1][search_request_params][parameters][q]": keyword,
            "specs[async_search_results][1][search_request_params][parameters][order]": order,
            "specs[async_search_results][1][search_request_params][parameters][page]": page,
            "specs[async_search_results][1][search_request_params][parameters][ref]": ref,
            "specs[async_search_results][1][search_request_params][parameters][referrer]": "https://www.etsy.com/",
            "specs[async_search_results][1][search_request_params][parameters][is_prefetch]": False,
            "specs[async_search_results][1][search_request_params][parameters][placement]": "wsg",
            "specs[async_search_results][1][search_request_params][user_id]":None,
            "specs[async_search_results][1][request_type]": "pagination_preact",
            "view_data_event_name": "search_async_pagination_specview_rendered",
        }
        
        if only_star_seller:
            data.update({
                "specs[async_search_results][1][search_request_params][parameters][is_star_seller]": True
            })
        
        return data
            
    
    def get_headers(self) -> dict:
        return {
            "x-csrf-token":self.get_csrf_token(),
            "x-detected-locale": "USD|en-US|US",
            "x-recs-primary-referrer": "https://www.etsy.com/",
            "x-requested-with": "XMLHttpRequest",
            "x-recs-primary-location": "https://www.etsy.com/",
            "x-page-guid": "f3f20ba1f29.6138e068b862963a63ae.00",
            "sec-fetch-mode": "cors",
            "origin": "https://www.etsy.com",
            "sec-fetch-dest": "empty",
            "dnt": "1",
            "pragma": "no-cache",
            "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-site": "same-origin",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "cache-control": "no-cache",
            "accept-encoding": "gzip, deflate, br",
            "accept": "*/*",
            "accept-language": "en-US,en,q=0.9",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "referer": "https://www.etsy.com/"
        }
    
    def search(self, keyword: str, max_page: int = 10, order: str = "most_relevant", only_star_seller: bool = False) -> List[Result]:
        headers = self.get_headers()
        results = []
        
        for page in range(1, max_page + 1):
            if page != 1:
                keyword_with_plus = "+".join(keyword.split(" "))
                headers.update({
                    "referer": f"https://www.etsy.com/search?q={keyword_with_plus}&ref=pagination&page={page}",
                    "x-recs-primary-location": f"https://www.etsy.com/search?q={keyword_with_plus}&ref=pagination&page={page}"
                })
                
            data = self.prepare_request_body(
                keyword, page, order, only_star_seller
            )
            req = self.session.post(self.request_url, data=data, headers=headers)
            results.append(Result(**req.json()))
        
        return results
    