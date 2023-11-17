import gdown
id = {
    1:"1coRInuo8ChFsHZ6zimUDfkUMlcLrb85H",
    2:"1_GjSYKwcz22y76Dsg5itav9Mgb8y2Ryr",
    3:"1v7tYABwFuEfjVGNYTOwj21v6j5oUTy0Z",
    4:"1IV6HsHwOVl8q7RWmP3a5cJXEmr9pt8A2",
    5:"1XF8HTLi9v64n5b5XgAhv9pCt1qyW1_Wx",
    6:"1FUBMCf3nsYehboX_orG6_h_6Gtyk_r10",
    7:"1l8OupSysVqNUHs7ll-0n85SRzysrn6Tg",
}
for i in range(1,8):
    url = f'https://drive.google.com/uc?id={id[i]}'
    output = f'model_{i}.hdf5'
    gdown.download(url, output, quiet=False)