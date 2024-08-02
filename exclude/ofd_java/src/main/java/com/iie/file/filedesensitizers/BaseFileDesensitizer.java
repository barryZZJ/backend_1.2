package com.iie.file.filedesensitizers;

import com.iie.BaseDesensitizer;

/**
 * @param FileIn input file type
 * @param FileOut output file type
 */
public abstract class BaseFileDesensitizer<FileIn, FileOut> extends BaseDesensitizer<FileIn, FileOut> {

    public abstract FileOut desensitize(FileIn image, Object... args);
}
