import asyncio
import logging
from base64 import b64encode
from functools import wraps
from typing import List, Tuple, Dict
from random import gauss

import aiofiles
import aiofiles.os
import aiohttp.client_exceptions
from colorama import Fore
from tqdm import tqdm
from yarl import URL

from ..base_functions.base_functions import FILE_FORMATS, MAX_FILENAME_LENGTH, log, logger, sanitize, FailureException, \
    is_forum, check_free_space
from ..base_functions.sql_helper import SQLHelper
from ..base_functions.data_classes import AlbumItem, CascadeItem, FileLock
from ..client.client import Client, DownloadSession
from ..scraper.scraper_helper import ScrapeMapper


async def basic_auth(username, password):
    token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'


def retry(f):
    @wraps(f)
    async def wrapper(self, *args, **kwargs):
        while True:
            try:
                return await f(self, *args, **kwargs)
            except FailureException as e:
                if not self.disable_attempt_limit:
                    if self.current_attempt[args[0].parts[-1]] >= self.attempts - 1:
                        logger.debug('Skipping %s...', args[0])
                        raise
                logger.debug(f'Retrying ({self.current_attempt[args[0].parts[-1]]}) {args[0]}...')
                self.current_attempt[args[0].parts[-1]] += 1

                if e.rescrape:
                    link = await self.album_obj.get_referrer(URL(args[0]))
                    await log("Attempting rescrape for " + str(args[0]), quiet=True)

                    async with asyncio.Semaphore(1):
                        await self.backup_scraper.map_url(link)
                        content_object = self.backup_scraper.Cascade
                        self.backup_scraper.Cascade = CascadeItem({})

                    if not await content_object.is_empty():
                        link_pairs = []
                        for domain in content_object.domains.keys():
                            for album in content_object.domains[domain].albums.keys():
                                link_pairs = content_object.domains[domain].albums[album].link_pairs
                        url_map = await self.album_obj.replace_link_pairs(link_pairs)
                        replaced_link = url_map[args[0]]
                        args = list(args)
                        args[0] = replaced_link
                        args = tuple(args)
                    else:
                        raise

                elif 'cyberdrop' in args[0].host:
                    ext = '.' + args[0].name.split('.')[-1]
                    if ext in FILE_FORMATS['Images']:
                        args = list(args)
                        args[0] = args[0].with_host('img-01.cyberdrop.to')
                        args = tuple(args)
                await asyncio.sleep(2)
    return wrapper


class Downloader:
    def __init__(self, album_obj: AlbumItem, title: str, max_workers: int, excludes: Dict[str, bool],
                 SQL_helper: SQLHelper, client: Client, file_args: Dict, runtime_args: Dict, pixeldrain_api_key: str,
                 scraper: ScrapeMapper):
        self.album_obj = album_obj
        self.client = client
        self.folder = file_args['output_folder']
        self.title = title

        self.SQL_helper = SQL_helper
        self.File_Lock = FileLock()

        self.attempts = runtime_args['attempts']
        self.current_attempt = {}
        self.disable_attempt_limit = runtime_args['disable_attempt_limit']
        self.mark_downloaded = runtime_args['mark_downloaded']

        self.excludes = excludes

        self.max_workers = max_workers
        self._semaphore = asyncio.Semaphore(max_workers)
        self.delay = {'cyberfile.is': 1, 'anonfiles.com': 1}

        self.proxy = runtime_args['proxy']
        self.pixeldrain_api_key = pixeldrain_api_key

        self.backup_scraper = scraper

        self.runtime_args = runtime_args
        self.file_args = file_args


    @retry
    async def download_file(self, url: URL, referral: URL, filename: str, session: DownloadSession, db_path: str,
                            show_progress: bool = True) -> None:
        """Download the content of given URL"""
        if not await check_free_space(self.runtime_args['required_free_space'], self.file_args['output_folder']):
            await log("Not enough free space to download file, skipping.", quiet=True)
            return

        if url.parts[-1] not in self.current_attempt:
            self.current_attempt[url.parts[-1]] = 0

        referer = str(referral)
        current_throttle = self.client.throttle

        while await self.File_Lock.check_lock(filename):
            await asyncio.sleep(gauss(1, 1.5))
        await self.File_Lock.add_lock(filename)

        try:
            async with self._semaphore:
                # Make suffix always lower case
                original_filename = filename
                ext = '.' + filename.split('.')[-1]

                complete_file = (self.folder / self.title / filename)
                partial_file = complete_file.with_suffix(complete_file.suffix + '.part')

                if complete_file.exists() or partial_file.exists():
                    if complete_file.exists():
                        total_size = await session.get_filesize(url, referer, current_throttle)
                        if complete_file.stat().st_size == total_size:
                            await self.SQL_helper.sql_insert_file(db_path, complete_file.name, 1, referer)
                            logger.debug("\nFile already exists and matches expected size: " + str(complete_file))
                            await self.File_Lock.remove_lock(original_filename)
                            return

                    download_name = await self.SQL_helper.get_download_filename(db_path)
                    iterations = 1

                    if not download_name:
                        while True:
                            filename = f"{complete_file.stem} ({iterations}){ext}"
                            iterations += 1
                            temp_complete_file = (self.folder / self.title / filename)
                            if not temp_complete_file.exists():
                                if not await self.SQL_helper.check_filename(filename):
                                    break
                    else:
                        filename = download_name

                await self.SQL_helper.sql_insert_file(db_path, filename, 0, referer)

                if self.mark_downloaded:
                    await self.SQL_helper.sql_update_file(db_path, filename, 1, referer)
                    return

                complete_file = (self.folder / self.title / filename)
                temp_file = complete_file.with_suffix(complete_file.suffix + '.part')
                resume_point = 0

                await self.SQL_helper.sql_insert_temp(str(temp_file))

                range_num = None
                if temp_file.exists():
                    resume_point = temp_file.stat().st_size
                    range_num = f'bytes={resume_point}-'

                for key, value in self.delay.items():
                    if key in url.host:
                        current_throttle = value

                headers = {"Authorization": await basic_auth("Cyberdrop-DL", self.pixeldrain_api_key)} \
                          if (self.pixeldrain_api_key and "pixeldrain" in url.host) else {}

                await session.download_file(url, referer, current_throttle, range_num, original_filename, filename,
                                            temp_file, resume_point, show_progress, self.File_Lock, self.folder,
                                            self.title, self.proxy, headers)
                await asyncio.sleep(0.1)

            await self.rename_file(filename, url, db_path, referer)
            await self.File_Lock.remove_lock(original_filename)

        except (aiohttp.client_exceptions.ClientPayloadError, aiohttp.client_exceptions.ClientOSError,
                aiohttp.client_exceptions.ServerDisconnectedError, asyncio.TimeoutError,
                aiohttp.client_exceptions.ClientResponseError, FailureException) as e:
            if await self.File_Lock.check_lock(original_filename):
                await self.File_Lock.remove_lock(original_filename)

            if hasattr(e, "message"):
                logging.debug(f"\n{url} ({e.message})")

            if hasattr(e, "code"):
                if 400 <= e.code < 500 and e.code != 429:
                    logger.debug("We ran into a 400 level error: %s", str(e.code))
                    return
                logger.debug("Error status code: " + str(e.code))

            if e.__class__.__name__ == 'FailureException':
                if await is_forum(referral):
                    return
                raise FailureException(code=e.code, message=e.message, rescrape=e.rescrape)
            else:
                raise FailureException(code=1, message=e)

    async def rename_file(self, filename: str, url: URL, db_path: str, referer: str) -> None:
        """Rename complete file."""
        complete_file = (self.folder / self.title / filename)
        temp_file = complete_file.with_suffix(complete_file.suffix + '.part')
        if complete_file.exists():
            logger.debug(str(self.folder / self.title / filename) + " Already Exists")
            await aiofiles.os.remove(temp_file)
        else:
            temp_file.rename(complete_file)

        await self.SQL_helper.sql_update_file(db_path, filename, 1, referer)
        if url.parts[-1] in self.current_attempt.keys():
            self.current_attempt.pop(url.parts[-1])
        logger.debug("Finished " + filename)

    async def get_filename(self, url: URL, referral: URL, session: DownloadSession):
        """Does all the necessary work to try and figure out what exactly the Filename should be."""
        referer = str(referral)

        filename = url.name
        if hasattr(url, "query_string"):
            query_str = url.query_string
            ext = '.' + query_str.split('.')[-1].lower()
            if await self.check_include(ext):
                filename = query_str.split("=")[-1]
        filename = await sanitize(filename)
        if "v=" in filename:
            filename = filename.split('v=')[0]
        if len(filename) > MAX_FILENAME_LENGTH:
            fileext = filename.split('.')[-1]
            filename = filename[:MAX_FILENAME_LENGTH] + '.' + fileext

        ext = '.' + filename.split('.')[-1].lower()
        current_throttle = self.client.throttle
        if not await self.check_include(ext):
            for key, value in self.delay.items():
                if key in url.host:
                    if value > current_throttle:
                        current_throttle = value
            try:
                if "pixeldrain" in url.host:
                    filename = await session.get_json_filename(url.with_query(None) / "info", current_throttle, 'name')
                else:
                    filename = await session.get_filename(url, referer, current_throttle)
                filename = await sanitize(filename)
                ext = '.' + filename.split('.')[-1].lower()
                if not await self.check_include(ext):
                    logging.debug("No file extension on content in link: " + str(url))
                    raise FailureException(0)
            except FailureException:
                try:
                    content_type = await session.get_content_type(url, referer, current_throttle)
                    if "image" in content_type:
                        ext_temp = content_type.split('/')[-1]
                        filename = filename + '.' + ext_temp
                        filename = await sanitize(filename)
                    else:
                        logging.debug("\nUnhandled content_type for checking filename: " + content_type)
                        raise FailureException(0)
                except FailureException:
                    await log("\nCouldn't get filename for: " + str(url))
                    raise FailureException(0)

        ext = '.' + filename.split('.')[-1].lower()
        filename = filename.replace('.' + filename.split('.')[-1], ext)
        return filename

    async def check_exclude(self, filename):
        """Check the exclude arguments to see if this file should be skipped (False)."""
        ext = '.' + filename.split('.')[-1]
        if self.excludes['videos']:
            if ext in FILE_FORMATS['Videos']:
                logging.debug("Skipping " + filename)
                return False
        if self.excludes['images']:
            if ext in FILE_FORMATS['Images']:
                logging.debug("Skipping " + filename)
                return False
        if self.excludes['audio']:
            if ext in FILE_FORMATS['Audio']:
                logging.debug("Skipping " + filename)
                return False
        if self.excludes['other']:
            if ext in FILE_FORMATS['Other']:
                logging.debug("Skipping " + filename)
                return False
        return True

    async def check_include(self, ext):
        if (ext in FILE_FORMATS['Images'] or ext in FILE_FORMATS['Videos']
                or ext in FILE_FORMATS['Audio'] or ext in FILE_FORMATS['Other']):
            return True

    async def get_db_path(self, url: URL):
        db_path = url.path
        if 'anonfiles' in url.host or 'bayfiles' in url.host:
            db_path = db_path.split('/')
            db_path.pop(0)
            db_path.pop(1)
            db_path = '/' + '/'.join(db_path)
        return db_path

    async def download_and_store(self, url_tuple: Tuple, session: DownloadSession, show_progress: bool = True) -> None:
        """Download the content of given URL and store it in a file."""
        url, referral = url_tuple

        logger.debug("Working on " + str(url))

        db_path = await self.get_db_path(url)

        # return if completed already
        if await self.SQL_helper.sql_check_existing(db_path):
            if url.parts[-1] in self.current_attempt.keys():
                self.current_attempt.pop(url.parts[-1])
            logger.debug(msg=f"{db_path} found in DB: Skipping {db_path}")
            return

        try:
            filename = await self.get_filename(url, referral, session)
            if await self.check_exclude(filename):
                await self.download_file(url, referral=referral, filename=filename, session=session, db_path=db_path,
                                         show_progress=show_progress)
        except Exception as e:
            if hasattr(e, "rescrape"):
                if url.parts[-1] in self.current_attempt.keys():
                    if not (self.current_attempt[url.parts[-1]] >= self.attempts - 1) and e.rescrape:
                        return
            if url.parts[-1] in self.current_attempt.keys():
                self.current_attempt.pop(url.parts[-1])
            logging.debug(e)
            await log(f"\nError attempting {url}")
            if hasattr(e, "message"):
                logging.debug(f"\n{url} ({e.message})")
            if hasattr(e, "code"):
                logger.debug("Error status code: " + str(e.code))

    async def download_content(self, show_progress: bool = True, conn_timeout: int = 15) -> None:
        """Download the content of all links and save them as files."""
        session = DownloadSession(self.client, conn_timeout)
        if not await check_free_space(self.runtime_args['required_free_space'], self.file_args['output_folder']):
            await log("Not enough free space to run the program.", Fore.RED)
            exit(0)
        coros = [self.download_and_store(url_object, session, show_progress)
                 for url_object in self.album_obj.link_pairs]
        for func in tqdm(asyncio.as_completed(coros), total=len(coros), desc=self.title, unit='FILE'):
            await func
        await session.client_session.close()
        self.SQL_helper.conn.commit()


async def get_downloaders(Cascade: CascadeItem, excludes: Dict[str, bool], SQL_helper: SQLHelper, client: Client,
                          max_workers: int, file_args: Dict, runtime_args: Dict, pixeldrain_api_key: str,
                          scraper: ScrapeMapper) -> List[Downloader]:
    """Get a list of downloader objects to run."""
    downloaders = []

    for domain, domain_obj in Cascade.domains.items():
        max_workers_temp = max_workers
        if 'bunkr' in domain or 'pixeldrain' in domain or 'anonfiles' in domain:
            max_workers_temp = 2 if (max_workers > 2) else max_workers
        for title, album_obj in domain_obj.albums.items():
            downloader = Downloader(album_obj, title=title, max_workers=max_workers_temp, excludes=excludes,
                                    SQL_helper=SQL_helper, client=client, file_args=file_args,
                                    runtime_args=runtime_args, pixeldrain_api_key=pixeldrain_api_key,
                                    scraper=scraper)
            downloaders.append(downloader)
    return downloaders
