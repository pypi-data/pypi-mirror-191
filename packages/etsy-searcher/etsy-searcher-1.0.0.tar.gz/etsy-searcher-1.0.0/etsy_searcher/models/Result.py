from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class AsyncSearchResult(BaseModel):
    html: Optional[str] = Field(None, alias="async_search_results")

class Result(BaseModel):
    output: AsyncSearchResult
    organic_listing_ids: List[int]
    ad_listing_ids: List[int]
    
    @property
    def all_listing_ids(self):
        return self.ad_listing_ids + self.organic_listing_ids
    
    def __init__(__pydantic_self__, **data: dict):
        data["organic_listing_ids"] = data.get("jsData").get("lazy_loaded_listing_ids")
        data["ad_listing_ids"] = data.get("jsData").get("lazy_loaded_ad_ids")
        super().__init__(**data)