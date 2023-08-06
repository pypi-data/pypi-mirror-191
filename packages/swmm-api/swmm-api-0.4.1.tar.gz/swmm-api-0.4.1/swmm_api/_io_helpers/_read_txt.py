import warnings

def read_txt_file(filename, encoding):
    """
    Read text file. I.e. SWMM inp and rpt file.

    Args:
        filename (str): Path/filename to text-file.
        encoding (str): Encoding of the text-file (None -> auto-detect encoding ... takes a few seconds | '' -> use default = 'utf-8')

    Returns:
        str: Content of the text-file.
    """
    # import cchardet as chardet
    # with open(filename, "rb") as f:
    #     binary_txt = f.read()
    #     detection = chardet.detect(binary_txt)
    #     encoding1 = detection["encoding"]
    #     confidence1 = detection["confidence"]
    #     txt1 = binary_txt.decode(encoding1)
    try:
        with open(filename, 'r', encoding=encoding) as file:
            txt = file.read()
    except UnicodeDecodeError:
        warnings.warn(f'Could not find correct encoding (found "{encoding}", but is wrong) for file ("{filename}"). Please set encoding manually.')
        with open(filename, 'r') as file:
            txt = file.read()

    return txt
