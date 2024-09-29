import asyncio
import logging
from typing import Iterator, List
from langchain_core.documents import Document
from langchain_community.document_loaders.base import BaseLoader
from langchain_community.document_loaders.chromium import AsyncChromiumLoader

#https://github.com/langchain-ai/langchain/issues/10475
#https://github.com/langchain-ai/langchain/blob/master/libs/community/langchain_community/document_loaders/chromium.py
# This wrapper was created because FastAPI and AsyncChromiumLoader has conflicts over async mechanism

class AsyncChromiumLoaderWrapper(AsyncChromiumLoader):
    def __init__(
            self,
            urls: List[str],
    ):
        super().__init__(urls)

    async def lazy_load_async(self) -> Iterator[Document]:
        """
        Lazily load text content from the provided URLs.

        This method yields Documents one at a time as they're scraped,
        instead of waiting to scrape all URLs before returning.

        Yields:
            Document: The scraped content encapsulated within a Document object.
        """
        for url in self.urls:
            html_content = await self.ascrape_playwright(url)
            metadata = {"source": url}
            yield Document(page_content=html_content, metadata=metadata)

    async def load_async(self) -> List[Document]:
        """
        Load and return all Documents from the provided URLs.

        Returns:
            List[Document]: A list of Document objects
            containing the scraped content from each URL.

        """
        return [doc async for doc in self.lazy_load_async()]