# Copyright (c) 2019 Paulo Kauscher Pinto

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# MIT License

# Copyright (c) 2018 Matt Lisivick

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import asyncio
import logging

import aiohttp
import async_timeout

from asyncnewsapi.auth import env_variable_api_key, KeyAuth


class Session:

    TOP_HEADLINES_URL = 'https://newsapi.org/v2/top-headlines'
    EVERYTHING_URL = 'https://newsapi.org/v2/everything'
    SOURCES_URL = 'https://newsapi.org/v2/sources'

    CATEGORY_OPTIONS = {'business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology'}
    LANGUAGE_OPTIONS = {'ar', 'de', 'en', 'es', 'fr', 'he', 'it', 'nl', 'no', 'pt', 'ru', 'se', 'ud', 'zh'}
    COUNTRY_OPTIONS = {'ae', 'ar', 'at', 'au', 'be', 'bg', 'br', 'ca', 'ch', 'cn', 'co', 'cu', 'cz', 'de',
                       'eg', 'fr', 'gb', 'gr', 'hk', 'hu', 'id', 'ie', 'il', 'in', 'it', 'jp', 'kr', 'lt',
                       'lv', 'ma', 'mx', 'my', 'ng', 'nl', 'no', 'nz', 'ph', 'pl', 'pt', 'ro', 'rs', 'ru',
                       'sa', 'se', 'sg', 'si', 'sk', 'th', 'tr', 'tw', 'ua', 'us', 've', 'za'}
    SORTBY_OPTIONS = {'relevancy', 'popularity', 'publishedAt'}

    def __init__(self, api_key=None, loop=None, timeout=None):
        self.auth = KeyAuth(api_key=api_key if api_key else env_variable_api_key())
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self.session = aiohttp.ClientSession(auth=self.auth, loop=self.loop)
        self.timeout = timeout

    async def close(self):
        await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def top_headlines(self, country=None, category=None, language=None, sources=None, q=None, page_size=20, timeout=None):
        '''
        Provides live top and breaking headlines for a country, specific category in a country, single source,
        or multiple sources. You can also search with keywords. Articles are sorted by the earliest date published first.

        Optional parameters:
            (str) country - The 2-letter ISO 3166-1 code of the country you want to get headlines for.
                            Possible options:
                            'ae', 'ar', 'at', 'au', 'be', 'bg', 'br', 'ca', 'ch', 'cn', 'co', 'cu', 'cz', 'de',
                            'eg', 'fr', 'gb', 'gr', 'hk', 'hu', 'id', 'ie', 'il', 'in', 'it', 'jp', 'kr', 'lt',
                            'lv', 'ma', 'mx', 'my', 'ng', 'nl', 'no', 'nz', 'ph', 'pl', 'pt', 'ro', 'rs', 'ru',
                            'sa', 'se', 'sg', 'si', 'sk', 'th', 'tr', 'tw', 'ua', 'us', 've', 'za'.
                            Note: you can't mix this param with the sources param.

            (str) category - The category you want to get headlines for.
                             Possible options:
                             'business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology'.
                             Note: you can't mix this param with the sources param.

            (str) language - The 2-letter ISO-639-1 code of the language you want to get headlines for.
                             Possible options:
                             'ar', 'de', 'en', 'es', 'fr', 'he', 'it', 'nl', 'no', 'pt', 'ru', 'se', 'ud', 'zh'.
                             Default: all languages returned.
                             Note: this feature is undocumented in https://newsapi.org/docs/endpoints/top-headlines

            (str) sources - A comma-seperated string of identifiers for the news sources or blogs you want headlines from.
                            Use the .sources function to locate these programmatically or look at the sources index.
                            Note: you can't mix this param with the country or category params.

            (str) q - Keywords or a phrase to search for.

            (int) page_size - The number of results to return per page (request). 20 is the default, 100 is the maximum.

            (int) page - Use this to page through the results if the total results found is greater than the page size.
        '''
        logger = logging.getLogger(__name__)
        # get first result page to check number of results
        r = await self._top_headlines_req(country=country, category=category, language=language, sources=sources, q=q, page_size=page_size, page=1, timeout=timeout)
        for article in r['articles']:
            yield article
        # paginate
        if r['totalResults'] > page_size:
            p = 2
            while len(r['articles']) > 0:
                try:
                    r = await self._top_headlines_req(country=country, category=category, language=language, sources=sources, q=q, page_size=page_size, page=p, timeout=timeout)
                except aiohttp.client_exceptions.ClientResponseError as e:
                    if e.status == 426:
                        logger.error('Upgrade required: free account can only download 100 articles per request')
                        # raising StopIteration during handling of exception goes uncaugth, empty the list of articles instead
                        r['articles'] = []
                    else:
                        raise e
                finally:
                    for article in r['articles']:
                        yield article
                    p += 1

    async def _top_headlines_req(self, country=None, category=None, language=None, sources=None, q=None, page_size=None, page=None, timeout=None):
        logger = logging.getLogger(__name__)

        if (q is None) and (sources is None) and (language is None) and (country is None) and (category is None):
            raise ValueError('one of q, sources, language, coutry or category parameters must be provided')

        if (sources is not None) and ((country is not None) or (category is not None)):
            raise ValueError('cannot mix country/category parameter with sources parameter')

        # Define Payload
        payload = {}

        # Country
        if country is not None:
            country = str(country)
            if country in self.COUNTRY_OPTIONS:
                payload['country'] = country
            else:
                raise ValueError('invalid country')

        # Category
        if category is not None:
            category = str(category)
            if category in self.CATEGORY_OPTIONS:
                payload['category'] = category
            else:
                raise ValueError('invalid category')

        # Language
        if language is not None:
            language = str(language)
            if language in self.LANGUAGE_OPTIONS:
                payload['language'] = language
            else:
                raise ValueError('invalid language')

        # Sources
        if sources is not None:
            payload['sources'] = str(sources)

        # Keyword/Phrase
        if q is not None:
            payload['q'] = str(q)

        # Page Size
        if page_size is not None:
            page_size = int(page_size)
            if 0 <= page_size <= 100:
                payload['pageSize'] = page_size
            else:
                raise ValueError('page_size should be an int between 1 and 100')

        # Page
        if page is not None:
            page = int(page)
            if page > 0:
                payload['page'] = page
            else:
                raise ValueError('page should be an int greater than 0')

        # Send Request
        logger.debug('top_headlines request payload: {}'.format(payload))
        async with async_timeout.timeout(timeout if timeout else self.timeout):
            async with self.session.get(self.TOP_HEADLINES_URL, params=payload, raise_for_status=True) as r:
                return await r.json()

    async def everything(self, q=None, sources=None, domains=None, exclude_domains=None, from_=None, to=None, language=None, sort_by=None, page_size=20, timeout=None):
        '''
        Search through millions of articles from over 30,000 large and small news sources and blogs.
        This includes breaking news as well as lesser articles.

        Optional parameters:
            (str) q - Keywords or phrases to search for.

                      Advanced search is supported here:

                      Surround phrases with quotes (") for exact match.
                      Prepend words or phrases that must appear with a + symbol. Eg: +bitcoin
                      Prepend words that must not appear with a - symbol. Eg: -bitcoin
                      Alternatively you can use the AND / OR / NOT keywords, and optionally group these with parenthesis.
                      Eg: crypto AND (ethereum OR litecoin) NOT bitcoin.

            (str) sources - A comma-seperated string of identifiers for the news sources or blogs you want headlines from.
                            Use the .sources function to locate these programmatically or look at the sources index.

            (str) domains - A comma-seperated string of domains (eg bbc.co.uk, techcrunch.com, engadget.com) to restrict
                            the search to.

            (str) exclude_domains - A comma-seperated string of domains (eg bbc.co.uk, techcrunch.com, engadget.com) to
                                    remove from the results.

            (str) from_ - A date and optional time for the oldest article allowed.
                          This should be in ISO 8601 format (e.g. '2019-03-12' or '2019-03-12T22:00:07')
                          Default: the oldest according to your plan.

            (str) to - A date and optional time for the newest article allowed.
                       This should be in ISO 8601 format (e.g. '2019-03-12' or '2019-03-12T22:00:07')
                       Default: the newest according to your plan.

            (str) language - The 2-letter ISO-639-1 code of the language you want to get headlines for.
                             Possible options:
                             'ar', 'de', 'en', 'es', 'fr', 'he', 'it', 'nl', 'no', 'pt', 'ru', 'se', 'ud', 'zh'.
                             Default: all languages returned.

            (str) sort_by - The order to sort the articles in.
                            Possible options: 'relevancy', 'popularity', 'publishedAt'.
                            'relevancy' = articles more closely related to q come first.
                            'popularity' = articles from popular sources and publishers come first.
                            'publishedAt' = newest articles come first.
                            Default: 'publishedAt'

            (int) page_size - The number of results to return per page (request). 20 is the default, 100 is the maximum.

            (int) page - Use this to page through the results if the total results found is greater than the page size.
        '''
        logger = logging.getLogger(__name__)
        # get first result page to check number of results
        r = await self._everything_req(q=q, sources=sources, domains=domains, exclude_domains=exclude_domains, from_=from_, to=to,
                                       language=language, sort_by=sort_by, page=1, page_size=page_size, timeout=timeout)
        for article in r['articles']:
            yield article
        # paginate
        if r['totalResults'] > page_size:
            p = 2
            while len(r['articles']) > 0:
                try:
                    r = await self._everything_req(q=q, sources=sources, domains=domains, exclude_domains=exclude_domains, from_=from_, to=to,
                                                   language=language, sort_by=sort_by, page=p, page_size=page_size, timeout=timeout)
                except aiohttp.client_exceptions.ClientResponseError as e:
                    if e.status == 426:
                        logger.error('Upgrade required: free account can only download 100 articles per request')
                        # raising StopIteration during handling of exception goes uncaugth, empty the list of articles instead
                        r['articles'] = []
                    else:
                        raise e
                finally:
                    for article in r['articles']:
                        yield article
                    p += 1

    async def _everything_req(self, q=None, sources=None, domains=None, exclude_domains=None, from_=None, to=None, language=None, sort_by=None, page=None, page_size=None, timeout=None):
        logger = logging.getLogger(__name__)

        if (q is None) and (sources is None) and (domains is None):
            raise ValueError('one of q, sources or domains parameters must be provided')

        # Define Payload
        payload = {}

        # Keyword/Phrase
        if q is not None:
            payload['q'] = str(q)

        # Sources
        if sources is not None:
            payload['sources'] = str(sources)

        # Domains to search
        if domains is not None:
            payload['domains'] = str(domains)

        # Domains to exclude
        if exclude_domains is not None:
            payload['excludeDomains'] = str(exclude_domains)

        # Search From This Date ...
        if from_ is not None:
            from_ = str(from_)
            if (len(from_)) >= 10:
                for i in range(len(from_)):
                    if (i == 4 and from_[i] != '-') or (i == 7 and from_[i] != '-'):
                        raise ValueError('from_ should be in the format of YYYY-MM-DD')
                    else:
                        payload['from'] = from_
            else:
                raise ValueError('from_ should be in the format of YYYY-MM-DD')

        # ... To This Date
        if to is not None:
            to = str(to)
            if (len(to)) >= 10:
                for i in range(len(to)):
                    if (i == 4 and to[i] != '-') or (i == 7 and to[i] != '-'):
                        raise ValueError('to should be in the format of YYYY-MM-DD')
                    else:
                        payload['to'] = to
            else:
                raise ValueError('to param should be in the format of YYYY-MM-DD')

        # Language
        if language is not None:
            language = str(language)
            if language in self.LANGUAGE_OPTIONS:
                payload['language'] = language
            else:
                raise ValueError('invalid language')

        # Sort Method
        if sort_by is not None:
            sort_by = str(sort_by)
            if sort_by in self.SORTBY_OPTIONS:
                payload['sortBy'] = sort_by
            else:
                raise ValueError('invalid sort')

        # Page Size
        if page_size is not None:
            page_size = int(page_size)
            if 0 <= page_size <= 100:
                payload['pageSize'] = page_size
            else:
                raise ValueError('page_size should be an int between 1 and 100')

        # Page
        if page is not None:
            page = int(page)
            if page > 0:
                payload['page'] = page
            else:
                raise ValueError('page should be an int greater than 0')

        # Send Request
        logger.debug('everything request payload: {}'.format(payload))
        async with async_timeout.timeout(timeout if timeout else self.timeout):
            async with self.session.get(self.EVERYTHING_URL, params=payload, raise_for_status=True) as r:
                return await r.json()

    async def sources(self, category=None, language=None, country=None, timeout=None):
        '''
        Returns the subset of news publishers that top headlines are available from.
        It's mainly a convenience endpoint that you can use to keep track of the publishers available on the API,
        and you can pipe it straight through to your users.

        Optional parameters:
            (str) category - Find sources that display news of this category.
                             Possible options:
                             'business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology'.
                             Default: all categories.

            (str) language - Find sources that display news in a specific language.
                             Possible options:
                             'ar', 'de', 'en', 'es', 'fr', 'he', 'it', 'nl', 'no', 'pt', 'ru', 'se', 'ud', 'zh'.
                             Default: all languages.

            (str) country - Find sources that display news in a specific country.
                            Possible options:
                            'ae', 'ar', 'at', 'au', 'be', 'bg', 'br', 'ca', 'ch', 'cn', 'co', 'cu', 'cz', 'de',
                            'eg', 'fr', 'gb', 'gr', 'hk', 'hu', 'id', 'ie', 'il', 'in', 'it', 'jp', 'kr', 'lt',
                            'lv', 'ma', 'mx', 'my', 'ng', 'nl', 'no', 'nz', 'ph', 'pl', 'pt', 'ro', 'rs', 'ru',
                            'sa', 'se', 'sg', 'si', 'sk', 'th', 'tr', 'tw', 'ua', 'us', 've', 'za'.
                            Default: all countries.
        '''
        r = await self._sources_req(category=category, language=language, country=country, timeout=timeout)
        for source in r['sources']:
            yield source

    async def _sources_req(self, category=None, language=None, country=None, timeout=None):
        logger = logging.getLogger(__name__)

        # Define Payload
        payload = {}

        # Category
        if category is not None:
            category = str(category)
            if category in self.CATEGORY_OPTIONS:
                payload['category'] = category
            else:
                raise ValueError('invalid category')

        # Language
        if language is not None:
            language = str(language)
            if language in self.LANGUAGE_OPTIONS:
                payload['language'] = language
            else:
                raise ValueError('invalid language')

        # Country
        if country is not None:
            country = str(country)
            if country in self.COUNTRY_OPTIONS:
                payload['country'] = country
            else:
                raise ValueError('invalid country')

        # Send Request
        logger.debug('sources request payload: {}'.format(payload))
        async with async_timeout.timeout(timeout if timeout else self.timeout):
            async with self.session.get(self.SOURCES_URL, params=payload, raise_for_status=True) as r:
                return await r.json()
