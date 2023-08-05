from typing import Final, Any, Optional, Dict

from requests import Session

from .network_response import NetworkResponse
from .request_type import RequestType


class RequestFailedError(RuntimeError):

    def __init__(self) -> None:
        super().__init__(">> [Coretex] Failed to execute request after retrying")


class RequestsManager:

    MAX_RETRY_COUNT: Final = 3

    def __init__(self, baseURL: str, connectionTimeout: int, readTimeout: int):
        self.__baseURL: Final = baseURL
        self.__connectionTimeout: Final = connectionTimeout
        self.__readTimeout: Final = readTimeout
        self.__session: Final = Session()

    @property
    def isAuthSet(self) -> bool:
        return self.__session.auth is not None

    def __url(self, endpoint: str) -> str:
        return self.__baseURL + endpoint

    def genericRequest(
        self,
        requestType: RequestType,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        data: Any = None,
        files: Any = None,
        retryCount: int = 0
    ) -> NetworkResponse:
        """
            Sends generic HTTP request

            Parameters:
            requestType: RequestType -> request type
            endpoint: str -> API endpoint
            headers: Optional[dict[str, str]] -> headers (not required)
            data: Any -> (not required)
            files: Any -> (not required)
            retryCount: int -> number of function calls if request has failed

            Returns:
            NetworkResponse as response content to request
        """

        try:
            requestsResponse = self.__session.request(
                method = requestType.value,
                url = self.__url(endpoint),
                headers = headers,
                data = data,
                files = files
                # timeout = (self.__connectionTimeout, self.__readTimeout)
            )

            return NetworkResponse(requestsResponse, endpoint)
        except Exception as ex:
            if retryCount < RequestsManager.MAX_RETRY_COUNT:
                RequestsManager.__logRetry(requestType, endpoint, retryCount, ex)
                return self.genericRequest(requestType, endpoint, headers, data, files, retryCount = retryCount + 1)

            raise RequestFailedError

    def get(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        data: Any = None,
        jsonObject: Any = None,
        retryCount: int = 0
    ) -> NetworkResponse:
        """
            Sends HTTP get request

            Parameters:
            endpoint: str -> API endpoint
            headers: Optional[dict[str, str]] -> headers (not required)
            data: Any -> (not required)
            jsonObject: Any -> (not required)
            retryCount: int -> number of function calls if request has failed

            Returns:
            NetworkResponse as response content to request
        """

        try:
            requestsResponse = self.__session.get(
                url = self.__url(endpoint),
                headers = headers,
                data = data,
                json = jsonObject
                # timeout = (self.__connectionTimeout, self.__readTimeout)
            )

            return NetworkResponse(requestsResponse, endpoint)
        except Exception as ex:
            if retryCount < RequestsManager.MAX_RETRY_COUNT:
                RequestsManager.__logRetry(RequestType.get, endpoint, retryCount, ex)
                return self.get(endpoint, headers, data, jsonObject, retryCount = retryCount + 1)

            raise RequestFailedError

    def post(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        data: Any = None,
        jsonObject: Any = None,
        retryCount: int = 0
    ) -> NetworkResponse:
        """
            Sends HTTP post request

            Parameters:
            endpoint: str -> API endpoint
            headers: Optional[dict[str, str]] -> headers (not required)
            data: Any -> (not required)
            jsonObject: Any -> (not required)
            retryCount: int -> number of function calls if request has failed

            Returns:
            NetworkResponse as response content to request
        """

        try:
            requestsResponse = self.__session.post(
                url = self.__url(endpoint),
                headers = headers,
                data = data,
                json = jsonObject
                # timeout = (self.__connectionTimeout, self.__readTimeout)
            )

            return NetworkResponse(requestsResponse, endpoint)
        except Exception as ex:
            if retryCount < RequestsManager.MAX_RETRY_COUNT:
                RequestsManager.__logRetry(RequestType.post, endpoint, retryCount, ex)
                return self.post(endpoint, headers, data, jsonObject, retryCount = retryCount + 1)

            raise RequestFailedError

    def setAuth(self, username: str, password: str) -> None:
        self.__session.auth = (username, password)

    @staticmethod
    def __logRetry(requestType: RequestType, endpoint: str, retryCount: int, exception: Exception) -> None:
        """
            Logs the information about request retry
        """

        print(
            f">> [RequestsManager] Retry {retryCount + 1} for ({requestType.name} -> {endpoint}), exception: {exception.__class__.__name__}"
        )
