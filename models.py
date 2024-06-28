import enums
from typing import Annotated, Optional

import httpx
import pandas as pd
from pydantic import BaseModel, ConfigDict, conint, Field, PlainSerializer

# Create a special type for cs_degree that is a boolean
# which translates to "yes" or "no" instead of regular
# boolean values
DegreeType = Annotated[
    bool, PlainSerializer(lambda x: "yes" if x else "no")
]

# Create a special type for include_relocated and include_remote_abroad
# that is a boolean which translates to "true" or "false"
IncludeType = Annotated[
    bool, PlainSerializer(lambda x: "true" if x else "false")
]

# Create an optional constricted integer with type annotations type that only accepts
# integers between 0 and 20 and another that only accepts those between 1 and 26
min_yoe = Optional[Annotated[int, conint(strict=True, ge=0, le=20)]]
max_yoe = Optional[Annotated[int, conint(strict=True, ge=1, le=26)]]


class ParticipantsQueryParams(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Optional[Annotated[str, TitleEnum]] = None
    level: Optional[Annotated[str, LevelEnum]] = None
    min_yoe: Optional[Annotated[int, conint(strict=True, ge=0, le=20)]] = Field(
        default=None, alias="yoe_from_included"
    )
    max_yoe: Optional[Annotated[int, conint(strict=True, ge=1, le=26)]] = Field(
        default=None, alias="yoe_to_excluded"
    )
    gender: Optional[Annotated[str, GenderEnum]] = None
    cs_degree: Optional[Annotated[str, DegreeType]] = None
    business_market: Optional[Annotated[str, BusinessMarketEnum]] = None
    business_size: Optional[Annotated[str, BusinessSizeEnum]] = None
    business_focus: Optional[Annotated[str, BusinessFocusEnum]] = None
    business_line: Optional[Annotated[str, BusinessLineEnum]] = None
    include_relocated: Optional[Annotated[bool, IncludeType]] = None
    include_remote_abroad: Optional[Annotated[bool, IncludeType]] = None


class StatsQueryParams(ParticipantsQueryParams):
    model_config = ConfigDict(extra="forbid")

    programming_language: Optional[Annotated[str, ProgrammingLanguageEnum]] = None


class Participants(ParticipantsQueryParams):
    model_config = ConfigDict(
        arbitrary_types_allowed=True, use_enum_values=True, extra="forbid"
    )
    _participants: Optional[pd.DataFrame] = None

    def model_post_init(self, __context: Any):
        self.make_api_call()

    def make_api_call(self):
        url = "https://api.egytech.fyi/participants"
        headers = {"accept": "application/json"}

        response = httpx.get(
            url,
            headers=headers,
            params=self.model_dump(mode="json", exclude_none=True),
        )
        participants_list = response.json()["results"]
        self._participants = pd.DataFrame.from_records(participants_list)

    def get_dataframe(self):
        return self._participants

    def save_csv(self):
        self._participants.to_csv(index=False)

    def save_excel(self):
        self._participants.to_excel(index=False)


class Stats(StatsQueryParams):
    model_config = ConfigDict(
        arbitrary_types_allowed=True, use_enum_values=True, extra="forbid"
    )
    _buckets: Optional[pd.DataFrame] = None
    _stats: Optional[Dict[str, str]] = None

    def model_post_init(self, __context: Any):
        self.make_api_call()

    def make_api_call(self):
        url = "https://api.egytech.fyi/stats"
        headers = {"accept": "application/json"}

        response = httpx.get(
            url,
            headers=headers,
            params=self.model_dump(mode="json", exclude_none=True),
        )
        bucket_list = response.json()["buckets"]
        self._buckets = pd.DataFrame.from_records(bucket_list)

    def get_dataframe(self):
        return self._buckets

    def get_stats(self):
        return self._stats

    def save_csv(self):
        self._buckets.to_csv(index=False)

    def save_excel(self)
        self._buckets.to_excel(index=False)
