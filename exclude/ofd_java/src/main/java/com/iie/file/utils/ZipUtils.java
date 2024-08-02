package com.iie.file.utils;

import static com.iie.utils.CopyFileUtils.copyFile;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.Charset;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.Enumeration;
import java.util.List;

import com.iie.utils.PathUtils;

import net.lingala.zip4j.ZipFile;

public class ZipUtils {
    
    
    /**
     * 把ofd文件复制到getZipUtilTempPath()/files/ofdzip/系统时间.zip
     */
    public static String ofdToZip(String ofdInPath, String ofdOutPath) {
        String CommonZipRoot = PathUtils.getZipUtilTempPath().resolve("files").toString();
        // SimpleDateFormat df = new SimpleDateFormat("yyyyMMddHHmmss");
        // String ZipFileName = df.format(System.currentTimeMillis());
        String ofdOutName = new File(ofdOutPath).getName();
        String ZipFileName = ofdOutName.substring(0, ofdOutName.lastIndexOf("."));
        String OriOFDFile = ofdInPath;
        String FinZipFile = CommonZipRoot + "/ofdzip/";
        File folder = new File(FinZipFile);
        if (!folder.exists()) {
            folder.mkdirs();
        }
        FinZipFile = FinZipFile + ZipFileName + ".zip";
        createFileIfNotExist(FinZipFile);
        try {
            copyFile(OriOFDFile, FinZipFile);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        return FinZipFile;
    }

    /**
     * 生成目录 getZipUtilTempPath()/files/unzip/<ofdNameWithoutExtension>/
     */
    public static String getUnzipRoot(String ofdInPath, String ofdOutPath) {
        String FinZipPath = ofdToZip(ofdInPath, ofdOutPath);
        String FinZipName = Paths.get(FinZipPath).getFileName().toString();
        String FinZipStem = FinZipName.substring(0, FinZipName.lastIndexOf(".")); // name without extension
        Path UnZipRoot = PathUtils.getZipUtilTempPath().resolve("files/unzip").resolve(FinZipStem);

        PathUtils.createFolderIfNotExist(UnZipRoot);
        return UnZipRoot.toString();
    }

    /**
     * 解压缩一个文件
     *
     * @param zipFile 压缩文件
     * @param folderPath 解压缩的目标目录
     */
    public static void unzipFile(File zipFilePath, String extractToDirectory) throws IOException {
        ZipFile zipFile = new ZipFile(zipFilePath);
        zipFile.setCharset(Charset.forName("UTF-8"));

        // Set the extraction destination directory
        zipFile.extractAll(extractToDirectory);

        zipFile.close();
    }
    /**
     * 解压缩一个文件
     *
     * @param zipFile 压缩文件
     * @param folderPath 解压缩的目标目录
     * @throws IOException 当解压缩过程出错时抛出
     */
    public static void upZipFile(File zipFile, String folderPath) throws IOException {
        final int BUFF_SIZE = 1924 * 1024;
        File desDir = new File(folderPath);
        if (!desDir.exists()) {
            desDir.mkdirs();
        }
        java.util.zip.ZipFile zf = new java.util.zip.ZipFile(zipFile);
        for (Enumeration<?> entries = zf.entries(); entries.hasMoreElements();) {
            java.util.zip.ZipEntry entry = ((java.util.zip.ZipEntry) entries.nextElement());
            InputStream in = zf.getInputStream(entry);
            String str = folderPath + File.separator + entry.getName();
            str = new String(str.getBytes("8859_1"), "GB2312");
            File desFile = new File(str);
            if (!desFile.exists()) {
                File fileParentDir = desFile.getParentFile();
                if (!fileParentDir.exists()) {
                    fileParentDir.mkdirs();
                }
                desFile.createNewFile();
            }
            OutputStream out = new FileOutputStream(desFile);
            byte buffer[] = new byte[BUFF_SIZE];
            int realLength;
            while ((realLength = in.read(buffer)) > 0) {
                out.write(buffer, 0, realLength);
            }
            in.close();
            out.close();
        }
    }
    
    /**
     * 批量压缩文件（夹）
     *
     * @param resFileList 要压缩的文件（夹）列表
     * @param zipFile 生成的压缩文件
     */
    public static void zipFiles(List<File> srcPathList, File zipFilePath) throws IOException {
        ZipFile zipFile = new ZipFile(zipFilePath);
        zipFile.setCharset(Charset.forName("UTF-8"));

        for (File srcPath : srcPathList) {
            if (srcPath.isDirectory()) {
                zipFile.addFolder(srcPath);
            } else {
                zipFile.addFile(srcPath);
            }
        }
        zipFile.close();
    }
    
    public static void createFileIfNotExist(String name) {
        File writefile;
        String path = name;
        writefile = new File(path);
        if (writefile.exists() == false) { // 判断文件是否存在，不存在则生成
            try {
                writefile.createNewFile();
                writefile = new File(path);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
    }

    public static void main(String[] args) throws IOException {
        File src = new File("E:/Coding2/im_modules/im-modules/src/test/java/com/iie/file/ofdtest.ofd");
        String target = "E:/Coding2/im_modules/im-modules/src/test/java/com/iie/file/ofdtest_extracted";
        File zipped = new File("E:/Coding2/im_modules/im-modules/src/test/java/com/iie/file/ofdtest_zip.ofd");
        unzipFile(src, target);
        zipFiles(Arrays.asList(new File(target, "Doc_0"), new File(target, "OFD.xml")), zipped);
        // upZipFile(src, target);
    }
}
