"""Extract SRA file into Gziped FASTQs"""
import logging
import os
from pathlib import Path
import requests
import pandas as pd
from collections import OrderedDict
# from pysradb.sraweb import SRAweb
from .command import run_command

# db = SRAweb()
logger = logging.getLogger("MassiveQC")


class DownloadException(Exception):
    """Basic exception for problems downloading from SRA"""


def _find_aspera_keypath(ascp_key=None):
    """Locate aspera key.
    Parameters
    ----------
    aspera_dir: str
                Location to aspera directory (optional)
    Returns
    -------
    aspera_keypath: str
                    Location to aspera key
    """
    if ascp_key is None:
        aspera_dir = os.path.join(os.path.expanduser("~"), ".aspera")
        aspera_keypath = os.path.join(
            aspera_dir, "connect", "etc", "asperaweb_id_dsa.openssh"
        )
    else:
        aspera_keypath = ascp_key.strip('"')
    if os.path.isfile(aspera_keypath):
        return aspera_keypath
    else:
        print(aspera_keypath)
        raise("Error in asperaweb_id_dsa.openssh file")


def verify_sra_download(log, SRR):
    if "error" in log.lower():
        logger.warning("Warning: ascp download failed, start download with wget")
        raise DownloadException("Download Failed")
    if "failed" in log.lower() or "unable" in log.lower():
        logger.error("wget download also failed")
        raise DownloadException(f"{SRR} Download Failed")
    if "command not found" in log.lower():
        raise DownloadException("Failed ascp not install")


def fetch_ena_fastq(srr):
    """Fetch FASTQ records from ENA (EXPERIMENTAL). From pysradb.
    Parameters
    ----------
    srr: string
         srr accession
    Returns
    -------
    srr_url: list
             SRR fastq urls
    """
    ena_fastq_search_url = "https://www.ebi.ac.uk/ena/portal/api/filereport"
    payload = [("result", "read_run"), ("fields", "fastq_ftp")]
    payload += [("accession", srr)]

    request = requests.get(ena_fastq_search_url, params=OrderedDict(payload))
    request_text = request.text.strip()
    urls = []
    for line in request_text.split("\n"):
        if "fastq_ftp" in line:
            continue
        line = line.strip()
        line_split = line.split("\t")
        if len(line_split) != 2:
            continue
        srr, url = line.split("\t")
        http_url = "http://{}".format(url)
        ftp_url = url.replace("ftp.sra.ebi.ac.uk/", "era-fasp@fasp.sra.ebi.ac.uk:")
        urls += [(srr, http_url, ftp_url)]

    # Paired end case
    def _handle_url_split(url_split):
        url1_1 = pd.NA
        url1_2 = pd.NA
        for url_temp in url_split:
            if "_1.fastq.gz" in url_temp:
                url1_1 = url_temp
            elif "_2.fastq.gz" in url_temp:
                url1_2 = url_temp
        return url1_1, url1_2

    if ";" in request_text:
        urls_expanded = []
        for srr, url1, url2 in urls:
            # strip _1, _2
            srr = srr.split("_")[0]
            if ";" in url1:
                url1_split = url1.split(";")
                if len(url1_split) == 2:
                    url1_1, url1_2 = url1_split
                else:
                    # warnings.warn('ignoring extra urls found for paired end accession')
                    url1_1, url1_2 = _handle_url_split(url1_split)
                url1_2 = "http://{}".format(url1_2)
                url2_split = url2.split(";")
                if len(url2_split) == 2:
                    url2_1, url2_2 = url2_split
                else:
                    # warnings.warn('ignoring extra urls found for paired end accession')
                    url2_1, url2_2 = _handle_url_split(url2_split)
            else:
                url1_1 = url1
                url2_1 = url2
                url1_2 = ""
                url2_2 = ""
            urls_expanded.append((srr, url1_1, url1_2, url2_1, url2_2))
        return pd.DataFrame(
            urls_expanded,
            columns=[
                "run_accession",
                "ena_fastq_http_1",
                "ena_fastq_http_2",
                "ena_fastq_ftp_1",
                "ena_fastq_ftp_2",
            ],
        )
    else:
        return pd.DataFrame(
            urls, columns=["run_accession", "ena_fastq_http", "ena_fastq_ftp"]
        )


def sra_ascp(SRR: str, download_path: str, ascp_key) -> Path:
    ascp = "ascp -k1 -T -l 300m -P33001 -i"
    record = fetch_ena_fastq(SRR)
    record = record.dropna(axis=1, how="any")
    for a in record.to_dict('records'):
        if SRR == a["run_accession"]:
            record = a
    ena_cols = [x for x in list(record.keys()) if "ena_fastq_ftp" in x]
    fastq_col = [x for x in list(record.keys()) if "ena_fastq_http" in x]
    if len(ena_cols) == 0:
        logger.warning(f"{SRR} can not find fastq file on EBI")
        raise DownloadException(f"{SRR} can not find fastq file on EBI")
    filenum = 0
    for ena, fastq in zip(ena_cols, fastq_col):
        try:
            download_url = record[ena]
            if download_url == "":
                continue
            if filenum == 0:
                logger.info(f"{SRR} first file start download")
            else:
                logger.info(f"{SRR} second file start download")
            cmd = "{} {} {} {}".format(
                ascp, _find_aspera_keypath(ascp_key), download_url, download_path
            )
            logger.info(f"running {cmd}")
            log = run_command(cmd)
            verify_sra_download(log, SRR)
        except:
            download_url = record[fastq]
            if download_url == "":
                continue
            if filenum == 0:
                logger.info(f"{SRR} first file start download")
            else:
                logger.info(f"{SRR} second file start download")
            cmd = "wget -N -c -q --timeout=120 -P {} {}".format(
                download_path, download_url
            )
            logger.info(f"running {cmd}")
            log = run_command(cmd)
            verify_sra_download(log, SRR)
        filenum += 1


def get_sra(SRR: str, download_path: str, ascp_key=None) -> Path:
    """Download sra fastq

    **parameter**
    SRR: str
        SRR ID.
    download_path: str
        Download directory
    ascp_key: str
        Location to aspera directory (optional)

    **return**
    Path
    """
    pe_r1 = Path(download_path) / f"{SRR}_1.fastq.gz"
    pe_r2 = Path(download_path) / f"{SRR}_2.fastq.gz"
    se_r1 = Path(download_path) / f"{SRR}.fastq.gz"
    if Path(se_r1).exists():
        logger.info("The file already exists")
        return
    if Path(pe_r1).exists() and Path(pe_r2).exists():
        logger.info("The files already exists")
        return
    try:
        sra_ascp(SRR, download_path, ascp_key)
    except:
        srrs = os.listdir(download_path)
        for srr_file in srrs:
            if SRR in srr_file:
                os.unlink(os.path.join(download_path, srr_file))
        raise DownloadException(f"{SRR} download failed")
