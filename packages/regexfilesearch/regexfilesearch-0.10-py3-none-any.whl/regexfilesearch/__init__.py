import os
from collections import deque
import regex
import sys
import pandas as pd
from flatten_everything import flatten_everything
from flexible_partial import FlexiblePartialOwnName
from a_pandas_ex_apply_ignore_exceptions import pd_add_apply_ignore_exceptions
pd_add_apply_ignore_exceptions()

resa = sys.modules[__name__]
resa.results = []


def get_all_files_in_folders_with_subdir_limit(folders, maxsubdirs=1):
    if not isinstance(folders, list):
        folders = [folders]
    mainfi = []
    for rootdir in folders:

        allfi = []
        baselevel = len(rootdir.split(os.path.sep))
        for subdirs, dirs, files in os.walk(rootdir):
            curlevel = len(subdirs.split(os.path.sep))
            if curlevel <= baselevel + maxsubdirs:
                allfi.append([os.path.join(subdirs, k) for k in files])

        mainfi.extend([(os.path.join(rootdir, x)) for x in (flatten_everything(allfi))])
    return list(set(flatten_everything(mainfi)))


def is_file_being_used(f):
    if os.path.exists(f):
        try:
            os.rename(f, f)
            return False
        except OSError as e:
            return True
    return True


def iter_windowed_distance(filepath, chunksize):
    dada = deque([0, 0, 0], 3)

    n = 3
    accum = deque([], n)
    iti = 0
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(chunksize)
            dada.append(iti * chunksize)
            accum.append(chunk)
            iti += 1
            if len(accum) == n:
                yield b"".join(list(accum)), dada
                if not chunk:
                    break


def get_file_hash(filepath, regexpressions, *args, chunksize=8192, **kwargs):
    if not isinstance(regexpressions, list):
        regexpressions = [regexpressions]
    regexpressions = [
        x.encode() if not isinstance(x, bytes) else x for x in regexpressions
    ]
    regexpressions = [regex.compile(x, *args, **kwargs) for x in regexpressions]
    co = 0
    if is_file_being_used(filepath):
        resa.results.append((co, filepath, -1, -1, -1, -1, None))
        return
    itfile = iter_windowed_distance(filepath, chunksize)
    for chunk, chunkinfos in itfile:
        chunkstart = chunkinfos[0]
        co += 1
        chunkend = chunkinfos[-1]
        for pata in regexpressions:
            for ax in pata.finditer(chunk, concurrent=True, partial=True):
                if ax.group(0) == b"":
                    continue
                s, e = ax.span()
                bytesstart = chunkstart + s
                bytesend = chunkstart + e

                resa.results.append(
                    (co, filepath, bytesstart, bytesend, chunkstart, chunkend, ax,pata)
                )
    if not resa.results:
        resa.results.append((co, filepath, -1, 0, 0, 0, None, None))


def regex_filesearch(files, regexpressions, *args,  with_context=True,chunksize=8192, **kwargs):
    dfs = []
    if not isinstance(files, list):
        files = [files]
    for f in files:
        get_file_hash(f, regexpressions, chunksize=chunksize, *args, **kwargs)
        if not resa.results:
            continue
        df = (
            pd.DataFrame(resa.results.copy())
            .drop_duplicates(subset=[1, 2, 3], keep="first")
            .reset_index(drop=True)
        )
        df.columns = (
            "aa_chunkno",
            "aa_file",
            "aa_bytesstart",
            "aa_bytesend",
            "aa_chunkstart",
            "aa_chunkend",
            "aa_regex", "aa_regexpattern",
        )
        resa.results.clear()
        dfs.append(df.copy())
    try:
        dft = pd.concat(dfs, ignore_index=True).copy()
    except Exception:
        return pd.DataFrame()
    dft["aa_replace"] = dft.ds_apply_ignore(pd.NA,
        lambda x: pd.NA
        if x.aa_bytesstart <= 0
        else FlexiblePartialOwnName(
            sub,
            "f(newfile:str, newbytes:bytes)",
            True,
            x.aa_file,
            x.aa_bytesstart,
            x.aa_bytesend,
        ),
        axis=1,
    )
    dft["aa_get_context"] = dft.ds_apply_ignore(pd.NA,
        lambda x: pd.NA
        if x.aa_bytesstart <= 0
        else FlexiblePartialOwnName(
            get_context, "f()", True, x.aa_file, x.aa_bytesstart, x.aa_bytesend
        ),
        axis=1,
    )
    dft["aa_partial_result"] = dft.aa_regex.ds_apply_ignore(pd.NA,lambda x: x.partial if hasattr(x, "partial") else x)
    dft=dft.fillna(pd.NA)
    if with_context:
        fullf = (dft.aa_partial_result == False) & (dft.aa_bytesstart > 0)
        d1 = dft.loc[fullf].ds_apply_ignore(pd.NA,lambda x: x.aa_get_context(), axis=1).to_frame()
        d1.columns = ['aa_full_match']
        partialf = (dft.aa_partial_result == True) & (dft.aa_bytesstart > 0)
        d2 = dft.loc[partialf].ds_apply_ignore(pd.NA,lambda x: x.aa_get_context(), axis=1).to_frame()
        d2.columns = ['aa_partial_match']

        d3=dft.loc[fullf].ds_apply_ignore(pd.NA,lambda x: tuple(
            zip([(ini,)+tuple(p) for ini,p in enumerate(x.aa_regex.allcaptures())], [tuple(p) for p in x.aa_regex.allspans()])),
                            axis=1).to_frame()
        d3.columns = ['aa_groups']
        dft = pd.concat([dft, d1, d2,d3], axis=1).copy().reset_index(drop=True)
        dft = dft.explode('aa_groups').reset_index(drop=True)
        dft['aa_allcaptures']=dft.aa_groups.ds_apply_ignore(pd.NA,lambda x: x if not isinstance(x, tuple) else x[0][0]).astype('Int64')
        dft['aa_result']=dft.aa_groups.ds_apply_ignore(pd.NA,lambda x: x[0][1:] if isinstance(x, tuple) else x)
        dft=dft.explode('aa_result').reset_index(drop=True)
        dft['aa_result_utf8']=dft.aa_result.ds_apply_ignore(pd.NA,lambda x: x.decode('utf-8', 'ignore')if isinstance(x, bytes) else x)
        dft["aa_bytesstart_whole"] = dft["aa_bytesstart"].copy()
        dft["aa_bytesend_whole"] = dft["aa_bytesend"].copy()

        dft["aa_bytesstart"] = dft.ds_apply_ignore(-1, lambda x: x.aa_groups[1][0][0] + x.aa_chunkstart, axis=1)
        dft["aa_bytesend"] = dft.ds_apply_ignore(-1, lambda x: x.aa_groups[1][0][1] + x.aa_chunkstart, axis=1)
        dft["aa_replace"] = dft.ds_apply_ignore(pd.NA,
                                                lambda x: pd.NA if x.aa_bytesstart <= 0 else FlexiblePartialOwnName(sub,
                                                    "f(newfile:str, newbytes:bytes)", True, x.aa_file, x.aa_bytesstart,
                                                    x.aa_bytesend, ), axis=1, )
        dft["aa_get_context"] = dft.ds_apply_ignore(pd.NA,
                                                    lambda x: pd.NA if x.aa_bytesstart <= 0 else FlexiblePartialOwnName(
                                                        get_context, "f()", True, x.aa_file, x.aa_bytesstart,
                                                        x.aa_bytesend), axis=1, )
    dft=dft.fillna(pd.NA)

    resa.results.clear()
    return dft


def get_context(file, start, end):
    startl = 0
    chunksize = 8192
    lsta, coa = divmod(start, chunksize)
    lste, coe = divmod(end, chunksize)
    while lsta != lste:
        chunksize += 1
        lsta, coa = divmod(start, chunksize)
        lste, coe = divmod(end, chunksize)
    with open(file, mode="rb") as f:

        while True:
            chunk = f.read(chunksize)
            if not chunk:
                break
            if startl == lsta:
                try:
                    wto = chunk[:coa]
                    wto2 = chunk[coe:]
                    wto1 = chunk[coa:coe]
                    return wto, wto1, wto2
                except Exception as fe:
                    print(fe)

            startl += 1


def sub(file, start, end, newfile, newbytes):
    if not isinstance(newbytes, bytes):
        newbytes = newbytes.encode()
    if file == newfile:
        raise OSError("source and destination must be different!")

    startl = 0
    chunksize = 8192
    lsta, coa = divmod(start, chunksize)
    lste, coe = divmod(end, chunksize)
    while lsta != lste:
        chunksize += 1
        lsta, coa = divmod(start, chunksize)
        lste, coe = divmod(end, chunksize)
    with open(newfile, mode="wb") as f1:
        with open(file, mode="rb") as f:

            while True:
                chunk = f.read(chunksize)
                if not chunk:
                    break
                if startl == lsta:
                    try:
                        wto = chunk[:coa]
                        wto2 = chunk[coe:]
                        f1.write(wto)
                        f1.write(newbytes)
                        f1.write(wto2)
                    except Exception as fe:
                        print(fe)
                else:
                    f1.write(chunk)
                startl += 1


