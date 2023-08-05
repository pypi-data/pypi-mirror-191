# pylint: disable=too-many-lines
# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
import datetime
import sys
from typing import Any, AsyncIterable, Callable, Dict, Optional, TypeVar, Union
import urllib.parse

from azure.core.async_paging import AsyncItemPaged, AsyncList
from azure.core.exceptions import (
    ClientAuthenticationError,
    HttpResponseError,
    ResourceExistsError,
    ResourceNotFoundError,
    ResourceNotModifiedError,
    map_error,
)
from azure.core.pipeline import PipelineResponse
from azure.core.pipeline.transport import AsyncHttpResponse
from azure.core.rest import HttpRequest
from azure.core.tracing.decorator import distributed_trace
from azure.core.utils import case_insensitive_dict
from azure.mgmt.core.exceptions import ARMErrorFormat

from ... import models as _models
from ..._vendor import _convert_request
from ...operations._usage_aggregates_operations import build_list_request

if sys.version_info >= (3, 8):
    from typing import Literal  # pylint: disable=no-name-in-module, ungrouped-imports
else:
    from typing_extensions import Literal  # type: ignore  # pylint: disable=ungrouped-imports
T = TypeVar("T")
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, AsyncHttpResponse], T, Dict[str, Any]], Any]]


class UsageAggregatesOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~azure.mgmt.commerce.aio.UsageManagementClient`'s
        :attr:`usage_aggregates` attribute.
    """

    models = _models

    def __init__(self, *args, **kwargs) -> None:
        input_args = list(args)
        self._client = input_args.pop(0) if input_args else kwargs.pop("client")
        self._config = input_args.pop(0) if input_args else kwargs.pop("config")
        self._serialize = input_args.pop(0) if input_args else kwargs.pop("serializer")
        self._deserialize = input_args.pop(0) if input_args else kwargs.pop("deserializer")

    @distributed_trace
    def list(
        self,
        reported_start_time: datetime.datetime,
        reported_end_time: datetime.datetime,
        show_details: Optional[bool] = None,
        aggregation_granularity: Union[str, _models.AggregationGranularity] = "Daily",
        continuation_token_parameter: Optional[str] = None,
        **kwargs: Any
    ) -> AsyncIterable["_models.UsageAggregation"]:
        """Query aggregated Azure subscription consumption data for a date range.

        .. seealso::
           - https://docs.microsoft.com/rest/api/commerce/usageaggregates

        :param reported_start_time: The start of the time range to retrieve data for. Required.
        :type reported_start_time: ~datetime.datetime
        :param reported_end_time: The end of the time range to retrieve data for. Required.
        :type reported_end_time: ~datetime.datetime
        :param show_details: ``True`` returns usage data in instance-level detail, ``false`` causes
         server-side aggregation with fewer details. For example, if you have 3 website instances, by
         default you will get 3 line items for website consumption. If you specify showDetails = false,
         the data will be aggregated as a single line item for website consumption within the time
         period (for the given subscriptionId, meterId, usageStartTime and usageEndTime). Default value
         is None.
        :type show_details: bool
        :param aggregation_granularity: ``Daily`` (default) returns the data in daily granularity,
         ``Hourly`` returns the data in hourly granularity. Known values are: "Daily" and "Hourly".
         Default value is "Daily".
        :type aggregation_granularity: str or ~azure.mgmt.commerce.models.AggregationGranularity
        :param continuation_token_parameter: Used when a continuation token string is provided in the
         response body of the previous call, enabling paging through a large result set. If not present,
         the data is retrieved from the beginning of the day/hour (based on the granularity) passed in.
         Default value is None.
        :type continuation_token_parameter: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: An iterator like instance of either UsageAggregation or the result of cls(response)
        :rtype: ~azure.core.async_paging.AsyncItemPaged[~azure.mgmt.commerce.models.UsageAggregation]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: Literal["2015-06-01-preview"] = kwargs.pop(
            "api_version", _params.pop("api-version", self._config.api_version)
        )
        cls: ClsType[_models.UsageAggregationListResult] = kwargs.pop("cls", None)

        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        def prepare_request(next_link=None):
            if not next_link:

                request = build_list_request(
                    subscription_id=self._config.subscription_id,
                    reported_start_time=reported_start_time,
                    reported_end_time=reported_end_time,
                    show_details=show_details,
                    aggregation_granularity=aggregation_granularity,
                    continuation_token_parameter=continuation_token_parameter,
                    api_version=api_version,
                    template_url=self.list.metadata["url"],
                    headers=_headers,
                    params=_params,
                )
                request = _convert_request(request)
                request.url = self._client.format_url(request.url)

            else:
                # make call to next link with the client's api-version
                _parsed_next_link = urllib.parse.urlparse(next_link)
                _next_request_params = case_insensitive_dict(
                    {
                        key: [urllib.parse.quote(v) for v in value]
                        for key, value in urllib.parse.parse_qs(_parsed_next_link.query).items()
                    }
                )
                _next_request_params["api-version"] = self._config.api_version
                request = HttpRequest(
                    "GET", urllib.parse.urljoin(next_link, _parsed_next_link.path), params=_next_request_params
                )
                request = _convert_request(request)
                request.url = self._client.format_url(request.url)
                request.method = "GET"
            return request

        async def extract_data(pipeline_response):
            deserialized = self._deserialize("UsageAggregationListResult", pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)  # type: ignore
            return deserialized.next_link or None, AsyncList(list_of_elem)

        async def get_next(next_link=None):
            request = prepare_request(next_link)

            pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
                request, stream=False, **kwargs
            )
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, pipeline_response)
                raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

            return pipeline_response

        return AsyncItemPaged(get_next, extract_data)

    list.metadata = {"url": "/subscriptions/{subscriptionId}/providers/Microsoft.Commerce/UsageAggregates"}
