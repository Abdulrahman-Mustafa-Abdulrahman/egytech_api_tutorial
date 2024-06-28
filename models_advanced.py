import asyncio
import itertools
from typing import Optional

import httpx
import pandas as pd
from pydantic import BaseModel, ConfigDict, Field


class PoolingClient(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, extra="forbid")
    query_list: list[ParticipantsQueryParams] = Field(exclude=True)
    _dataframe: Optional[pd.DataFrame] = None

    # define a model_post_init() and a make_calls()
    def model_post_init(self, __context: Any):
        self.make_calls()

    def make_calls(self):
        url = "https://api.egytech.fyi"
        headers = {"accept": "application/json"}
        # create a client instance to make a series of API calls
        with httpx.Client(base_url=url, headers=headers) as client:
            # create a responses list to hold the deserialized response values
            responses = []
            for query in self.query_list:
                response = client.get(
                    "/participants",
                    params=query.model_dump(
                        mode="json", exclude_none=True
                    ),
                )
                # Cancel initialization if unsuccessful API call
                if response.status_code != 200:
                    raise Exception("Unsuccessful API Call")
                # Deserialize the received response
                deser_response = response.json()
                # Retrieve the last value from the deser_response dict
                # and extend the responses list from it
                responses.extend(list(deser_response.values())[-1])
        # Construct a DataFrame from the compiled responses
        self._dataframe = pd.DataFrame.from_records(responses)

    # define a method get_dataframe() to retrieve the constructed df
    def get_df(self):
        return self._dataframe


class AsyncPoolingClient(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, extra="forbid")
    query_list: list[ParticipantsQueryParams] = Field(exclude=True)
    _dataframe: Optional[pd.DataFrame] = None

    def model_post_init(self, __context: Any):
        asyncio.run(self.make_calls())

    async def make_calls(self):
        async def make_single_call(
                query: ParticipantsQueryParams, c: httpx.AsyncClient
        ):
            response = await c.get(
                "/participants",
                params=query.model_dump(mode="json", exclude_none=True),
            )
            if response.status_code != 200:
                raise Exception("Unsuccessful API Call")
            return response.json()["results"]

        headers = {"accept": "application/json"}
        client = httpx.AsyncClient(
            base_url="https://api.egytech.fyi", headers=headers
        )
        responses = await asyncio.gather(
            *map(make_single_call, self.query_list, itertools.repeat(client))
        )
        results = itertools.chain(*responses)
        await client.aclose()

        self._dataframe = pd.DataFrame.from_records(results)

    def get_df(self):
        return self._dataframe
