package com.iie.file;

import com.iie.file.filedesensitizers.OfdFileDesensitizer;
import com.iie.utils.PathUtils;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Scanner;

import static org.junit.jupiter.api.Assertions.assertTrue;


public class OfdFileDesensitizerTest {

    OfdFileDesensitizer.Builder builder = new OfdFileDesensitizer.Builder();
    String inputStr = PathUtils.getTestPath().resolve("file/ofdtest.ofd").toString();
    final boolean CLEANUP = false;

    public void testDeletePages() throws IOException {
        OfdFileDesensitizer des = builder.deletePages(1, 2).build();
        Path output = PathUtils.getTestPath().resolve("file/ofdtest_delpg_p1_p2.ofd");
        String outputStr = output.toString();

        des.desensitize(inputStr, outputStr);
        assertTrue(Files.exists(output));
        cleanUp(output);
    }

    public void testChangeKeywordOfd() throws IOException {
        OfdFileDesensitizer des = builder.changeKeyword("本科").build();
        Path output = PathUtils.getTestPath().resolve("file/ofdtest_keyword_benke_ofd.ofd");
        String outputStr = output.toString();

        des.desensitize(inputStr, outputStr);
        assertTrue(Files.exists(output));
        cleanUp(output);
    }

    public void testChangeKeywordPages() throws IOException {
        OfdFileDesensitizer des = builder.changeKeyword("本科", 1, 2).build();
        Path output = PathUtils.getTestPath().resolve("file/ofdtest_keyword_benke_p1_p2.ofd");
        String outputStr = output.toString();

        des.desensitize(inputStr, outputStr);
        assertTrue(Files.exists(output));
        cleanUp(output);
    }

    public void testChangePatternEmailOfd() throws IOException {
        OfdFileDesensitizer des = builder.changePattern(true, false, false, false, false, false).build();
        Path output = PathUtils.getTestPath().resolve("file/ofdtest_pattern_email_ofd.ofd");
        String outputStr = output.toString();

        des.desensitize(inputStr, outputStr);
        assertTrue(Files.exists(output));
        cleanUp(output);
    }

    public void testChangePatternEmailPages() throws IOException {
        OfdFileDesensitizer des = builder.changePattern(true, false, false, false, false, false, 5).build();
        Path output = PathUtils.getTestPath().resolve("file/ofdtest_pattern_email_p5.ofd");
        String outputStr = output.toString();

        des.desensitize(inputStr, outputStr);
        assertTrue(Files.exists(output));
        cleanUp(output);
    }

    public void testChangePatternComOfd() throws IOException {
        OfdFileDesensitizer des = builder.changePattern(false, true, false, false, false, false).build();
        Path output = PathUtils.getTestPath().resolve("file/ofdtest_pattern_com_ofd.ofd");
        String outputStr = output.toString();

        des.desensitize(inputStr, outputStr);
        assertTrue(Files.exists(output));
        cleanUp(output);
    }

    public void testChangePatternComPages() throws IOException {
        OfdFileDesensitizer des = builder.changePattern(false, true, false, false, false, false, 1, 2).build();
        Path output = PathUtils.getTestPath().resolve("file/ofdtest_pattern_com_p1_p2.ofd");
        String outputStr = output.toString();

        des.desensitize(inputStr, outputStr);
        assertTrue(Files.exists(output));
        cleanUp(output);
    }

    public void testChangePatternPhoneOfd() throws IOException {
        OfdFileDesensitizer des = builder.changePattern(false, false, true, false, false, false).build();
        Path output = PathUtils.getTestPath().resolve("file/ofdtest_pattern_phone_ofd.ofd");
        String outputStr = output.toString();

        des.desensitize(inputStr, outputStr);
        assertTrue(Files.exists(output));
        cleanUp(output);
    }

    public void testChangePatternPhonePages() throws IOException {
        OfdFileDesensitizer des = builder.changePattern(false, false, true, false, false, false, 1, 2).build();
        Path output = PathUtils.getTestPath().resolve("file/ofdtest_pattern_phone_p1_p2.ofd");
        String outputStr = output.toString();

        des.desensitize(inputStr, outputStr);
        assertTrue(Files.exists(output));
        cleanUp(output);
    }

    public void testChangePatternPhone2Ofd() throws IOException {
        OfdFileDesensitizer des = builder.changePattern(false, false, false, true, false, false).build();
        Path output = PathUtils.getTestPath().resolve("file/ofdtest_pattern_phone2_ofd.ofd");
        String outputStr = output.toString();

        des.desensitize(inputStr, outputStr);
        assertTrue(Files.exists(output));
        cleanUp(output);
    }

    public void testChangePatternPhone2Pages() throws IOException {
        OfdFileDesensitizer des = builder.changePattern(false, false, false, true, false, false, 1, 2).build();
        Path output = PathUtils.getTestPath().resolve("file/ofdtest_pattern_phone2_p1_p2.ofd");
        String outputStr = output.toString();

        des.desensitize(inputStr, outputStr);
        assertTrue(Files.exists(output));
        cleanUp(output);
    }

    public void testChangePatternIdcardOfd() throws IOException {
        OfdFileDesensitizer des = builder.changePattern(false, false, false, false, false, true).build();
        Path output = PathUtils.getTestPath().resolve("file/ofdtest_pattern_idcard_ofd.ofd");
        String outputStr = output.toString();

        des.desensitize(inputStr, outputStr);
        assertTrue(Files.exists(output));
        cleanUp(output);
    }

    public void testChangePatternIdcardPages() throws IOException {
        OfdFileDesensitizer des = builder.changePattern(false, false, false, false, false, true, 1, 2).build();
        Path output = PathUtils.getTestPath().resolve("file/ofdtest_pattern_idcard_p1_p2.ofd");
        String outputStr = output.toString();

        des.desensitize(inputStr, outputStr);
        assertTrue(Files.exists(output));
        cleanUp(output);
    }

    public void testChangePatternIpOfd() throws IOException {
        OfdFileDesensitizer des = builder.changePattern(false, false, false, false, true, false).build();
        Path output = PathUtils.getTestPath().resolve("file/ofdtest_pattern_ip_ofd.ofd");
        String outputStr = output.toString();

        des.desensitize(inputStr, outputStr);
        assertTrue(Files.exists(output));
        cleanUp(output);
    }

    public void testChangePatternIpPages() throws IOException {
        OfdFileDesensitizer des = builder.changePattern(false, false, false, false, true, false, 1, 2).build();
        Path output = PathUtils.getTestPath().resolve("file/ofdtest_pattern_ip_p1_p2.ofd");
        String outputStr = output.toString();

        des.desensitize(inputStr, outputStr);
        assertTrue(Files.exists(output));
        cleanUp(output);
    }

    public void testChangePic() throws IOException {
        OfdFileDesensitizer des = builder.changePic(1, 2).build();
        Path output = PathUtils.getTestPath().resolve("file/ofdtest_delpic_1_2.ofd");
        String outputStr = output.toString();

        des.desensitize(inputStr, outputStr);
        assertTrue(Files.exists(output));
        cleanUp(output);
    }

    public void testAll() throws IOException {
        OfdFileDesensitizer des = builder
                .deletePages(1, 2)
                .changeKeyword("本科")
                .changePattern(true, true, true, true, true, true)
                .changePic(6, 7)
                .build();
        Path output = PathUtils.getTestPath().resolve("file/ofdtest_all.ofd");
        String outputStr = output.toString();

        des.desensitize(inputStr, outputStr);
        assertTrue(Files.exists(output));
        cleanUp(output);
    }

    private void cleanUp(Path file) throws IOException {
        if (CLEANUP) {
            Files.delete(file);
        }
    }

    public static void main(String[] args) throws IOException {
        // new OfdFileDesensitizerTest().testDeletePages();
        // new OfdFileDesensitizerTest().testChangeKeywordOfd();
        // new OfdFileDesensitizerTest().testChangeKeywordPages();
        // new OfdFileDesensitizerTest().testChangePatternEmailOfd();
        // new OfdFileDesensitizerTest().testChangePatternEmailPages();
        // new OfdFileDesensitizerTest().testChangePatternComOfd();
        // new OfdFileDesensitizerTest().testChangePatternComPages();
        // new OfdFileDesensitizerTest().testChangePatternPhoneOfd();
        // new OfdFileDesensitizerTest().testChangePatternPhonePages();
        // new OfdFileDesensitizerTest().testChangePatternPhone2Ofd();
        // new OfdFileDesensitizerTest().testChangePatternPhone2Pages();
        // new OfdFileDesensitizerTest().testChangePatternIdcardOfd();
        // new OfdFileDesensitizerTest().testChangePatternIdcardPages();
        // new OfdFileDesensitizerTest().testChangePatternIpOfd();
        // new OfdFileDesensitizerTest().testChangePatternIpPages();
        // new OfdFileDesensitizerTest().testChangePic();
        // new OfdFileDesensitizerTest().testAll();
        OfdFileDesensitizerTest t = new OfdFileDesensitizerTest();
        Scanner cin = new Scanner(System.in);
        System.out.println("待脱敏ofd文件：");
        String inputFilePath = cin.next();
        System.out.println("选择脱敏算法：");
        System.out.println("1. 页面空白置换算法");
        System.out.println("2. 关键词假名置换算法");
        System.out.println("3. 模式匹配替换算法");
        System.out.println("4. 图片遮蔽算法");
        int choice = cin.nextInt();
        String input;
        if (choice == 1) {
            System.out.println("输入待删除的页码（逗号分隔）：");
            input = cin.next();
            String[] pgs_str = input.split(",");
            int[] pgs = new int[pgs_str.length];
            for (int i = 0; i < pgs_str.length; i++) {
                pgs[i] = Integer.parseInt(pgs_str[i].trim());
            }
            t.builder.deletePages(pgs);
        } else if (choice == 2) {
            System.out.println("输入关键词：");
            String keyword = cin.next();
            System.out.println("输入待替换的页码（逗号分隔）：");
            input = cin.next();
            if (!input.isEmpty()) {
                String[] pgs_str = input.split(",");
                int[] pgs = new int[pgs_str.length];
                for (int i = 0; i < pgs_str.length; i++) {
                    pgs[i] = Integer.parseInt(pgs_str[i].trim());
                }
                t.builder.changeKeyword(keyword, pgs);
            } else {
                t.builder.changeKeyword(keyword);
            }
        } else if (choice == 3) {
            System.out.println("输入模式匹配算法参数(email, com, phone, phone2, idcard, ip)：");
            input = cin.next();
            boolean email = false, com = false, phone = false, phone2 = false, idcard = false, ip = false;
            if (input.contains("email")) {
                email = true;
            }
            if (input.contains("com")) {
                com = true;
            }
            if (input.contains("phone")) {
                phone = true;
            }
            if (input.contains("phone2")) {
                phone2 = true;
            }
            if (input.contains("idcard")) {
                idcard = true;
            }
            if (input.contains("ip")) {
                ip = true;
            }
            System.out.println("输入待替换的页码（逗号分隔）：");
            input = cin.next();
            if (!input.isEmpty()) {
                String[] pgs_str = input.split(",");
                int[] pgs = new int[pgs_str.length];
                for (int i = 0; i < pgs_str.length; i++) {
                    pgs[i] = Integer.parseInt(pgs_str[i].trim());
                }
                t.builder.changePattern(email, com, phone, phone2, idcard, ip, pgs);
            } else {
                t.builder.changePattern(email, com, phone, phone2, idcard, ip);
            }
        } else if (choice == 4) {
            System.out.println("输入待遮蔽的图片序号（逗号分隔）：");
            input = cin.next();
            if (!input.isEmpty()) {
                String[] ids_str = input.split(",");
                int[] ids = new int[ids_str.length];
                for (int i = 0; i < ids_str.length; i++) {
                    ids[i] = Integer.parseInt(ids_str[i].trim());
                }
                t.builder.changePic(ids);
            }
        }
        String outputFilePath = t.builder.build().desensitize(inputFilePath);
        System.out.println("输出文件路径：" + outputFilePath);

    }
}
