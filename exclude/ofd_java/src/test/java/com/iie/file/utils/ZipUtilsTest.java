package com.iie.file.utils;

import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.junit.jupiter.api.Test;

import com.iie.utils.PathUtils;

public class ZipUtilsTest {

    void deleteDir(File path) {
        if (path.isDirectory()) {
            for (File file : path.listFiles()) {
                deleteDir(file);
            }
        }
        path.delete();
    }

    void testZipUtils() throws IOException {

        String root = PathUtils.getTestPath().resolve("file").toString();
        File src = new File(root + "/ofdtest.ofd");
        String extracted = root + "/extracted";

        ZipUtils.unzipFile(src, extracted);

        assertTrue(new File(extracted).exists());

        List<File> myfiles = new ArrayList<>();
        File myfile1 = new File(extracted + "/Doc_0");
        File myfile2 = new File(extracted + "/OFD.xml");
        myfiles.add(myfile1);
        myfiles.add(myfile2);
        File target = new File(root + "/ofdtest_zipped.ofd");
        ZipUtils.zipFiles(myfiles, target);

        assertTrue(target.exists());

        deleteDir(new File(extracted));
        target.delete();
    }

    public static void main(String[] args) throws IOException {
        new ZipUtilsTest().testZipUtils();
    }
}
