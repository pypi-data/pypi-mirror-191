# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
from typing import Any

from cbra.ext.api.credential import ApplicationClientCredential
from cbra.ext.api import Consumer


class TestConsumer(Consumer['TestConsumer']):

    def get_http_client_kwargs(self) -> dict[str, Any]:
        return {}


async def main():
    credential = ApplicationClientCredential()
    client = TestConsumer()
    await client.request(
        method='GET',
        response_model=lambda x: x,
        url='https://www.example.com',
        credential=credential
    )


if __name__ == '__main__':
    asyncio.run(main())

