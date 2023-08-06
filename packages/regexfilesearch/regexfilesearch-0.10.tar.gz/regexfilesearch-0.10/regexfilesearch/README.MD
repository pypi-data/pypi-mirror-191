# Regex search in all kind of files  (in chunks) + binary sub

### pip install regexfilesearch
```python
import regex

from regexfilesearch import regex_filesearch, get_all_files_in_folders_with_subdir_limit

alf = get_all_files_in_folders_with_subdir_limit(
    folders=r"C:\Users\Gamer\anaconda3\envs\stopjogo", maxsubdirs=0
)
df = regex_filesearch(
    files=alf,
    regexpressions=[r"\bchar\b", r"import.*?pandas "],
    with_context=True,
    chunksize=8192,
    flags=regex.IGNORECASE,
)




print(df.loc[df.aa_bytesstart > 1][:20].to_string(max_colwidth=10))
    aa_chunkno    aa_file  aa_bytesstart  aa_bytesend  aa_chunkstart  aa_chunkend   aa_regex aa_regexpattern aa_replace aa_get_context aa_partial_result aa_full_match aa_partial_match  aa_groups  aa_allcaptures aa_result aa_result_utf8  aa_bytesstart_whole  aa_bytesend_whole
12          1   C:\Use...         52             56            0          16384    <regex...  regex....       f(newf...        f()          False         (b'#in...          <NA>        ((0, b...          0        b'char'       char             52                   56        
13          1   C:\Use...        182            186            0          16384    <regex...  regex....       f(newf...        f()          False         (b'#in...          <NA>        ((0, b...          0        b'char'       char            182                  186        
14          1   C:\Use...        217            221            0          16384    <regex...  regex....       f(newf...        f()          False         (b'#in...          <NA>        ((0, b...          0        b'char'       char            217                  221        
15          1   C:\Use...        254            258            0          16384    <regex...  regex....       f(newf...        f()          False         (b'#in...          <NA>        ((0, b...          0        b'char'       char            254                  258        
16          1   C:\Use...        440            444            0          16384    <regex...  regex....       f(newf...        f()          False         (b'#in...          <NA>        ((0, b...          0        b'char'       char            440                  444        
17          1   C:\Use...        582            586            0          16384    <regex...  regex....       f(newf...        f()          False         (b'#in...          <NA>        ((0, b...          0        b'char'       char            582                  586        
18          1   C:\Use...        622            626            0          16384    <regex...  regex....       f(newf...        f()          False         (b'#in...          <NA>        ((0, b...          0        b'char'       char            622                  626        
19          1   C:\Use...        661            665            0          16384    <regex...  regex....       f(newf...        f()          False         (b'#in...          <NA>        ((0, b...          0        b'char'       char            661                  665        
20          1   C:\Use...         52             56            0          16384    <regex...  regex....       f(newf...        f()          False         (b'#in...          <NA>        ((0, b...          0        b'char'       char             52                   56        
21          1   C:\Use...        182            186            0          16384    <regex...  regex....       f(newf...        f()          False         (b'#in...          <NA>        ((0, b...          0        b'char'       char            182                  186        
22          1   C:\Use...        217            221            0          16384    <regex...  regex....       f(newf...        f()          False         (b'#in...          <NA>        ((0, b...          0        b'char'       char            217                  221        
23          1   C:\Use...        254            258            0          16384    <regex...  regex....       f(newf...        f()          False         (b'#in...          <NA>        ((0, b...          0        b'char'       char            254                  258        
24          1   C:\Use...        440            444            0          16384    <regex...  regex....       f(newf...        f()          False         (b'#in...          <NA>        ((0, b...          0        b'char'       char            440                  444        
25          1   C:\Use...        582            586            0          16384    <regex...  regex....       f(newf...        f()          False         (b'#in...          <NA>        ((0, b...          0        b'char'       char            582                  586        
26          1   C:\Use...        622            626            0          16384    <regex...  regex....       f(newf...        f()          False         (b'#in...          <NA>        ((0, b...          0        b'char'       char            622                  626        
27          1   C:\Use...        661            665            0          16384    <regex...  regex....       f(newf...        f()          False         (b'#in...          <NA>        ((0, b...          0        b'char'       char            661                  665        
29          1   C:\Use...      20080          20084            0          16384    <regex...  regex....       f(newf...        f()          False         (b'<\x...          <NA>        ((0, b...          0        b'char'       char          20080                20084        
30          1   C:\Use...      20236          20240            0          16384    <regex...  regex....       f(newf...        f()          False         (b'<\x...          <NA>        ((0, b...          0        b'char'       char          20236                20240        
31          1   C:\Use...      20260          20264            0          16384    <regex...  regex....       f(newf...        f()          False         (b'<\x...          <NA>        ((0, b...          0        b'char'       char          20260                20264        
32          1   C:\Use...      21457          21461            0          16384    <regex...  regex....       f(newf...        f()          False         (b'<\x...          <NA>        ((0, b...          0        b'char'       char          21457                21461        




print(df.loc[df.aa_bytesstart > 1][:20].iloc[0].to_string())
aa_chunkno                                                             1
aa_file                C:\Users\Gamer\anaconda3\envs\stopjogo\mademod...
aa_bytesstart                                                         52
aa_bytesend                                                           56
aa_chunkstart                                                          0
aa_chunkend                                                        16384
aa_regex               <regex.Match object; span=(52, 56), match=b'ch...
aa_regexpattern        regex.Regex(b'\\bchar\\b', flags=regex.A | reg...
aa_replace                                f(newfile:str, newbytes:bytes)
aa_get_context                                                       f()
aa_partial_result                                                  False
aa_full_match          (b'#include <stdio.h>\r\n\r\n\r\n\r\n\r\n// np...
aa_partial_match                                                    <NA>
aa_groups                                    ((0, b'char'), ((52, 56),))
aa_allcaptures                                                         0
aa_result                                                        b'char'
aa_result_utf8                                                      char
aa_bytesstart_whole                                                   52
aa_bytesend_whole                                                     56



# df.loc[df.aa_bytesstart > 1][:20].aa_replace.iloc[0]('c:\\testestest.py', 'CHARRRRRRR')
# substitutes one match, never changes the original file
// np=np.byte, c=signed CHARRRRRRR, ctypes=ctypes.c_byte, code=b
// numpy.int8: 8-bit signed integer (-128 to 127).
// Signed integer type, compatible with C char
void cfun_byte(const  signed char  *indatav, size_t size,  signed char  *outdatav ) 
```
