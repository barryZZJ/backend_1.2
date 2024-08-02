package com.iie.utils;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;

public class JarExtractor {

    /**
     *
     * @param resPath the path to the resource, should start with "/"
     * @return
     * @throws IOException
     */
    public static Path extractResource(String resPath) throws IOException {
        // Get the input stream for the Resource within the JAR
        InputStream inputStream = JarExtractor.class.getResourceAsStream(resPath);
        if (inputStream == null) {
            throw new IOException("Resource not found in JAR");
        }

        // Define the target path for the extracted Resource
        Path targetPath = PathUtils.getSystemTempFile(resPath.replaceFirst("^/", ""));

        // Copy the Resource from the JAR to the temporary directory
        Files.copy(inputStream, targetPath, StandardCopyOption.REPLACE_EXISTING);
        return targetPath;
    }
}
