'''

@brief: 同步2个目录中的内容, 把src_dir同步成dst_dir, 但是同名文件中的内容不做比较
@date: 2024年9月30日
@author: rogerg6

'''

import os
import shutil
# import time

def sync(dp, sdir, ddir):
    if os.path.basename(sdir) != os.path.basename(ddir):
        print("basename: [%s] != [%s]" % (sdir, ddir))
        return

    if dp == 1:
        print("%s%s is sync..." % (dp*'\t', os.path.basename(ddir)), end='\r')

    # get s_set, d_set
    s_set = set(os.listdir(sdir))
    d_set = set(os.listdir(ddir))

    # s-d, d-s, s&d
    pub = s_set & d_set
    union = s_set | d_set
    s_priv = union - d_set
    d_priv = union - s_set

    # sync
    # file only in src_dir
    for i in s_priv:
        fn = os.path.join(sdir, i)
        # print("%s%s" % (dp*"\t", fn), end=' ')
        try:
            if os.path.isfile(fn):
                os.remove(fn)
            elif os.path.isdir(fn):
                shutil.rmtree(fn)
        except Exception as e:
            print(f"An error occurred: {e}")

    # file only in dst_dir
    for i in d_priv:
        sfn = os.path.join(sdir, i)
        dfn = os.path.join(ddir, i)
        # print("%s%s" % (dp*"\t", fn), end=' ')
        try:
            if os.path.isfile(dfn):
                shutil.copy2(dfn, sfn)
            elif os.path.isdir(dfn):
                shutil.copytree(dfn, sfn)
        except Exception as e:
            print(f"An error occurred: {e}")

    # file which exist in this 2 directories
    for i in sorted(pub):
        sfile = os.path.join(sdir, i)
        dfile = os.path.join(ddir, i)
        # print("%s[%s, %s]" % (dp*"\t", sfile, dfile), end=' ')

        try:
            if os.path.isdir(sfile) and os.path.isdir(dfile):
                sync(dp+1, sfile, dfile)
            elif os.path.isfile(sfile) and os.path.isdir(dfile):
                os.remove(sfile)
                shutil.copytree(dfile, sfile)
            elif os.path.isdir(sfile) and os.path.isfile(dfile):
                shutil.rmtree(sfile)
                shutil.copy2(dfile, sfile)
        except Exception as e:
            print(f"An error occurred: {e}")
    
    if dp == 1:
        print("\r%s%s sync is done!" % (dp*'\t', os.path.basename(ddir)))


TEST=False

if TEST:
    src_dir = '.\\a\\b'
    dst_dir = '.\\b'
else:
    src_dir = 'E:\\csbooklist'
    dst_dir = 'J:\\csbooklist'
sync(0, src_dir, dst_dir)