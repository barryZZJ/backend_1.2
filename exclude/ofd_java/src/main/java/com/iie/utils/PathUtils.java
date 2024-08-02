package com.iie.utils;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URISyntaxException;
import java.net.URLDecoder;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;


public class PathUtils {

    private static Path tempDir = null;

    /**
     * 获取文件后缀名
     * @param filePath 文件路径
     * @param defaultExtension 不含后缀名时使用的默认值
     * @return 后缀名
     */
    public static String getFileExtension(String filePath, String defaultExtension) {
        Path path = Paths.get(filePath);

        String fileName = path.getFileName().toString();
        int dotIndex = fileName.lastIndexOf('.');

        if (dotIndex > 0 && dotIndex < fileName.length() - 1) {
            return fileName.substring(dotIndex + 1).toLowerCase();
        } else {
            return defaultExtension; // Unable to determine the file extension
        }
    }

    /**
     * 给定文件路径，对其中文件名部分（后缀名之前）添加指定字符串后缀
     * @return 新的文件路径
     */
    public static String addSuffixToFilename(String filePath, String suffix) {
        return filePath.replaceFirst("[.][^.]+$", suffix + "$0");
    }

    /**
     * get resource from src/main/resources, if running in jar environment, will extract resource first.
     * @param resPathStr path of resource, usually start with '/'
     * @return absolute path to the requested resource.
     * @throws FileNotFoundException
     */
    public static Path getResource(String resPathStr) throws FileNotFoundException {
        Path resPath;
        try {
            if (PathUtils.isJarEnvironment()) {
                resPath = JarExtractor.extractResource(resPathStr);
            } else {
                resPath = Paths.get(PathUtils.class.getResource(resPathStr).toURI());
            }
        } catch (URISyntaxException | IOException e) {
            throw new FileNotFoundException("Resource " + resPathStr + " cannot be found!");
        }
        return resPath.toAbsolutePath();
    }

    /**
     *
     * @return project root if running directly, jar's directory if running from jar.
     */
    public static String getRootPath() {
        String runningJarPath = getJarPath();

        if (runningJarPath != null) {
            return new File(runningJarPath).getParent();
        } else {
            return getProjectPath();
        }
    }

    public static Path getLocalTempDirectory() {
        if (tempDir == null) {
            tempDir = Paths.get(getRootPath(), "temp");
            try {
                Files.createDirectories(tempDir);
            } catch (IOException e) {
                throw new RuntimeException("Fail to create temp directory!");
            }
        }
        return tempDir;
    }
    public static Path getSystemTempDirectory() {
        return Paths.get(System.getProperty("java.io.tmpdir"));
    }

    public static Path getSystemTempFile(String fileName) {
        return getSystemTempDirectory().resolve(fileName);
    }

    public static Path getZipUtilTempPath() {
        return getSystemTempDirectory().resolve("zip");
    }

    public static Path getTestPath() {
        String resourcePath = PathUtils.class.getResource("/").getPath();
        return new File(resourcePath).toPath().getParent().resolve("test-classes/com/iie");
    }

    public static boolean isJarEnvironment() {
        return getJarPath() != null;
    }

    private static String getProjectPath() {
        String resourcePath = PathUtils.class.getResource("/").getPath();
        return new File(resourcePath).getParentFile().getParentFile().getAbsolutePath();
    }

    private static String getJarPath() {
        try {
            String jarPath = PathUtils.class.getProtectionDomain().getCodeSource().getLocation().getPath();
            jarPath = URLDecoder.decode(jarPath, "UTF-8");

            // Check if the application is running from a JAR file
            if (jarPath.endsWith(".jar")) {
                return jarPath;
            }
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }
        return null;
    }

    public static void createFolderIfNotExist(Path folder) {
        if (!Files.exists(folder)) { // 判断文件是否存在，不存在则生成
            try {
                Files.createDirectories(folder);
            } catch (IOException e) {
                throw new RuntimeException("fail to create folder " + folder.toFile());
            }
        }
    }

    public static void main(String[] args) {
        String projectRootPath = getRootPath();
        System.out.println("Project Root Path: " + projectRootPath);
        System.out.println("System temp path: " + getSystemTempDirectory());
    }
}
