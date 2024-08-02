package com.iie.file.filedesensitizers;

import com.iie.file.utils.TwoIDOneString;
import com.iie.file.utils.ZipUtils;
import com.iie.utils.CopyFileUtils;
import com.iie.utils.Logging;
import com.iie.utils.PathUtils;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;
import java.util.regex.Pattern;
import org.apache.logging.log4j.Logger;
import org.dom4j.Document;
import org.dom4j.DocumentException;
import org.dom4j.Element;
import org.dom4j.Node;
import org.dom4j.io.OutputFormat;
import org.dom4j.io.SAXReader;
import org.dom4j.io.XMLWriter;

public class OfdFileDesensitizer extends BaseFileDesensitizer<String, String> {

    private static final Logger logger = Logging.logger;
    protected static final String DesensitizedPicResPathStr = "/image_desensitized_template.jpg";
    protected static Path DesensitizedPicResPath;


    //几个需要用的固定正则
    protected static final String PatternEmail = ".*\\w+([-+.]\\w+)*@\\w+([-.]\\w+)*\\.\\w+([-.]\\w+)*.*";//邮箱
    protected static final String PatternCom = "[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(/.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+/.?";//域名
    protected static final String PatternPhone = ".*(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\\d{8}.*";//手机.*(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}.*.*(?:(?:\+|00)86)?1[3-9]\d{9}.*
    protected static final String PatternPhone2 = "^(?:(?:\\d{3}-)?\\d{8}|^(?:\\d{4}-)?\\d{7,8})(?:-\\d+)?$";//电话^(((\d{3,4}-)?[0-9]{7,8})$)
    protected static final String PatternIP = "\\d+\\.\\d+\\.\\d+\\.\\d+";//IP
    protected static final String PatternIDcard = ".*[1-9]\\d{5}[1-9]\\d{3}((0\\d)|(1[0-2]))(([0|1|2]\\d)|3[0-1])\\d{4}.*";//身份正[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{4}.*[1-9]\d{5}(?:18|19|20)\d{2}(?:0[1-9]|10|11|12)(?:0[1-9]|[1-2]\d|30|31)\d{3}[\dXx].*

    protected boolean deletepage; // 删除页
    protected List<Integer> deletepages; // 删除第ji页，从0开始

    protected boolean changekeyword; // 关键词脱敏
    protected String keyword;
    protected boolean changekeywordofd; // 关键词脱敏作用于整个文档
    protected boolean changekeywordpage; // 关键词脱敏作用于某几页
    protected List<Integer> changekeywordpages; // 更换第ji页的关键词，从0开始

    protected boolean needpattern; // 需要正则
    protected boolean changepatternofd; // 正则作用于整个文档
    protected boolean changepatternpage; // 正则作用于某几页
    protected List<Integer> changepatternpages; // 更换第ji页的正则，从0开始

    protected boolean needpatternemail;
    protected boolean needpatterncom;
    protected boolean needpatternphone;
    protected boolean needpatternphone2;
    protected boolean needpatternip;
    protected boolean needpatternidcard;

    protected boolean changepic; //图片脱敏
    protected List<Integer> changepicInds; // 更换第ji张图片，从0开始

    List<String> MyPatterns = new ArrayList<>();

    private OfdFileDesensitizer(Builder builder) {
        deletepage = builder.deletepage;
        deletepages = builder.deletepages;
        changekeyword = builder.changekeyword;
        keyword = builder.keyword;
        changekeywordofd = builder.changekeywordofd;
        changekeywordpage = builder.changekeywordpage;
        changekeywordpages = builder.changekeywordpages;
        needpattern = builder.needpattern;
        changepatternofd = builder.changepatternofd;
        changepatternpage = builder.changepatternpage;
        changepatternpages = builder.changepatternpages;
        needpatternemail = builder.needpatternemail;
        needpatterncom = builder.needpatterncom;
        needpatternphone = builder.needpatternphone;
        needpatternphone2 = builder.needpatternphone2;
        needpatternip = builder.needpatternip;
        needpatternidcard = builder.needpatternidcard;
        changepic = builder.changepic;
        changepicInds = builder.changepicInds;
    }

    public static class Builder {
        protected boolean deletepage = false; // 删除页
        protected List<Integer> deletepages; // 删除第ji页，从0开始

        protected boolean changekeyword = false; // 关键词脱敏
        protected String keyword;
        protected boolean changekeywordofd; // 关键词脱敏作用于整个文档
        protected boolean changekeywordpage; // 关键词脱敏作用于某几页
        protected List<Integer> changekeywordpages; // 更换第ji页的关键词，从0开始

        protected boolean needpattern = false; // 需要正则
        protected boolean changepatternofd; // 正则作用于整个文档
        protected boolean changepatternpage; // 正则作用于某几页
        protected List<Integer> changepatternpages; // 更换第ji页的正则，从0开始

        protected boolean needpatternemail = false;
        protected boolean needpatterncom = false;
        protected boolean needpatternphone = false;
        protected boolean needpatternphone2 = false;
        protected boolean needpatternip = false;
        protected boolean needpatternidcard = false;

        protected boolean changepic = false; //图片脱敏
        protected List<Integer> changepicInds; // 更换第ji张图片，从0开始

        /**
         * 空白置换算法
         * @param pages page number, start from 1.
         */
        public Builder deletePages(int... pages) {
            deletepage = true;
            deletepages = new ArrayList<>();
            for (int i = 0; i < pages.length; i++) {
                if (pages[i] <= 0) {
                    throw new IndexOutOfBoundsException();
                }
                deletepages.add(pages[i] - 1);
            }
            return this;
        }

        /**
         * 假名置换算法
         * if pages are not specified, apply to the entire document.
         * @param keyword separate with "；" if multiple keywords.
         */
        public Builder changeKeyword(String keyword) {
            this.keyword = keyword;
            changekeyword = true;
            changekeywordofd = true;
            changekeywordpage = false;
            return this;
        }

        /**
         * 假名置换算法
         * @param keyword separate with "；" if multiple keywords.
         * @param pages page number, start from 1. if pages are not specified, apply to the entire document.
         */
        public Builder changeKeyword(String keyword, int... pages) {
            this.keyword = keyword;
            changekeyword = true;
            changekeywordofd = false;
            changekeywordpage = true;
            changekeywordpages = new ArrayList<>();
            for (int i = 0; i < pages.length; i++) {
                if (pages[i] <= 0) {
                    throw new IndexOutOfBoundsException();
                }
                changekeywordpages.add(pages[i] - 1);
            }
            return this;
        }

        /**
         * 特殊符号置换算法
         * if pages are not specified, apply to the entire document.
         */
        public Builder changePattern(boolean email, boolean com, boolean phone, boolean phone2, boolean ip,
                boolean idcard) {
            needpattern = true;
            changepatternofd = true;
            changepatternpage = false;

            needpatternemail = email;
            needpatterncom = com;
            needpatternphone = phone;
            needpatternphone2 = phone2;
            needpatternip = ip;
            needpatternidcard = idcard;
            return this;
        }

        /**
         * 特殊符号置换算法
         * @param pages page number, start from 1. if pages are not specified, apply to the entire document.
         */
        public Builder changePattern(boolean email, boolean com, boolean phone, boolean phone2, boolean ip,
                boolean idcard, int... pages) {
            needpattern = true;
            changepatternofd = false;
            changepatternpage = true;
            changepatternpages = new ArrayList<>();

            for (int i = 0; i < pages.length; i++) {
                if (pages[i] <= 0) {
                    throw new IndexOutOfBoundsException();
                }
                changepatternpages.add(pages[i] - 1);
            }

            needpatternemail = email;
            needpatterncom = com;
            needpatternphone = phone;
            needpatternphone2 = phone2;
            needpatternip = ip;
            needpatternidcard = idcard;
            return this;
        }

        /**
         * 全黑遮蔽算法
         * @param indices index of picture, start from 1.
         */
        public Builder changePic(int... indices) {
            changepic = true;
            changepicInds = new ArrayList<>();

            for (int i = 0; i < indices.length; i++) {
                if (indices[i] <= 0) {
                    throw new IndexOutOfBoundsException();
                }
                changepicInds.add(indices[i] - 1);
            }
            return this;
        }

        public OfdFileDesensitizer build() {
            return new OfdFileDesensitizer(this);
        }
    }

    /**
     * @param args [0]: Type: String. Specify file path of output desensitized file.
     *      If not specified, add "_desensitized" to the input file's name and output to the same directory.
     * @return output file path
     */
    @Override
    public String desensitize(String ofdpath, Object... args) {
        String ofdOutPath;
        if (args.length > 0) {
            ofdOutPath = (String) args[0];
        } else {
            ofdOutPath = PathUtils.addSuffixToFilename(ofdpath, "_desensitized$0");
        }

        //读取写在txt里面的语句
        //读取写在txt里面的语句
        // logger.error("NewKeywordActivity " + ",keyword:" + keyword);

        if (needpattern) {
            if (needpatternemail) {
                // logger.error("NewKeywordActivity " + ",Pattern:" + 1);
                MyPatterns.add(PatternEmail);
            }
            if (needpatterncom) {
                // logger.error("NewKeywordActivity " + ",Pattern:" + 2);
                MyPatterns.add(PatternCom);
            }
            if (needpatternidcard) {
                // logger.error("NewKeywordActivity " + ",Pattern:" + 3);
                MyPatterns.add(PatternIDcard);
            }
            if (needpatternip) {
                // logger.error("NewKeywordActivity " + ",Pattern:" + 4);
                MyPatterns.add(PatternIP);
            }
            if (needpatternphone) {
                // logger.error("NewKeywordActivity " + ",Pattern:" + 5);
                MyPatterns.add(PatternPhone);
            }
            if (needpatternphone2) {
                // logger.error("NewKeywordActivity " + ",Pattern:" + 6);
                MyPatterns.add(PatternPhone2);
            }
        }

        //根据语句进行修改ofd
        // logger.error("temp dir at " + PathUtils.getZipUtilTempPath().toString());
        //完成解压
        String Unziproot = ZipUtils.getUnzipRoot(ofdpath, ofdOutPath);

        File needtounzip = new File(ofdpath);
        try {
            ZipUtils.upZipFile(needtounzip, Unziproot);
            // ZipUtils.unzipFile(needtounzip, Unziproot);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        //修改底层xml
        try {
            java_Change__XML(Unziproot);
        } catch (DocumentException e) {
            throw new RuntimeException(e);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        String FinOfdPath = ofdOutPath;
        File FinOfd = Paths.get(ofdOutPath).toFile();
        List<File> myfiles = new ArrayList<>();
        File myfile1 = new File(Unziproot + "/Doc_0");
        File myfile2 = new File(Unziproot + "/OFD.xml");
        myfiles.add(myfile1);
        myfiles.add(myfile2);
        // System.out.println(myfiles.size());
        try {
            ZipUtils.zipFiles(myfiles, FinOfd);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        // String newpath = Filerename(FinOFDRoot, PathUtils.getOfdTmpPath() + "/ofdloc/" + ofdpath.get "result.ofd");
        // logger.error("迁移后文件名字" + newpath);
        // logger.error("输出到" + FinOfdPath);
        return ofdOutPath;
    }

    public String java_Change__XML(String UnzipRoot) throws DocumentException, IOException {
        /*
         * 正则/关键词脱敏思路：每个文字块(node)对应一个id，遍历每个node判断是否满足脱敏规则，如果满足则替换该node的文字。
         * 存在问题：有可能一个关键词被分到了多个node里，比如跨行，需要拼在一起才能符合脱敏规则。
         * 现在的做法是把两个node拼起来再扫一次，问题是一个关键词可能需要拼不止两个node，而且不能处理跨更多行的情况。
         */
        /*
         TODO 解决思路：把所有node全部拼在一起成一个大字符串，同时记录文字块与对应的id的映射，对整个大字符串检查一遍，得到需要脱敏的子字符串位置后，反向查询对应的id，然后把这些node给脱敏掉即可。
         */
        String pos = UnzipRoot + "/";
        String OFDXML = pos + "OFD.xml";
        String DocumentXmlpos = "";
        String OFDXMLroot = "";
        String Doc = "";

        List<String> firstchange = new ArrayList<>(); //第一遍改变后全部的，改了的和没改的

        Map<String, String> second1 = new LinkedHashMap<>(); //包含ID,TEXT,用于生成TWOIdOneSTRING，此时id是全的，即不管改没改都加进了second1，string是改了的
        Map<String, String> markfin = new LinkedHashMap<>(); //用于记录所有需要改变的id以及对应的string，这个是最终的

        List<TwoIDOneString> secRound = new ArrayList<>(); //用于解决跨行的结构体list
        List<String> mykeywords = new ArrayList<>(); //keywords关键词
        if (changekeyword) {
            mykeywords = Arrays.asList(keyword.split("；"));
            // logger.error("keywords的个数" + String.valueOf(mykeywords.size()));
        }
        Map<String, String> PicIDText = new LinkedHashMap<>();
        Map<String, String> originIDtext = new LinkedHashMap<>();

        Set<String> markSetKeyword = new HashSet<>();
        Set<String> markSetPattern = new HashSet<>();
        List<String> markimageSet = new ArrayList<>();

        // logger.error("pattern size: " + String.valueOf(MyPatterns.size()));
        String ID = "";
        String text = "";
        int replength = 0;

        List<String> PagesXml = new ArrayList<>();

        //往下数70行左右，都是查询目录结构，获得各个资源的绝对路径的，例如第一页的content.xml的绝对路径，变量名非常多，非常杂
        SAXReader sr = new SAXReader();
        Document document = sr.read(new File(OFDXML));
        //1.拿到root
        List<Node> DocRoots = document.selectNodes("//ofd:DocRoot");
        for (Node docRoot : DocRoots) {
            Element docrootele = (Element) docRoot;
            OFDXMLroot = docrootele.getText();
        }

        DocumentXmlpos = pos + OFDXMLroot;
        // logger.error("pos " + pos);
        // logger.error("Ofdxmlroot " + OFDXMLroot);
        int where = OFDXMLroot.indexOf("/");
        Doc = OFDXMLroot.substring(0, where);
        String DocumentResXml = "";
        //拿到document.xml位置
        Document Documentxml = sr.read(new File(DocumentXmlpos));
        //拿到pages位置
        List<Node> documentress = Documentxml.selectNodes("//ofd:DocumentRes");
        for (Node node : documentress) {
            Element resele = (Element) node;
            DocumentResXml = resele.getText();
            // logger.error("DOCUMENTRESXML的text" + DocumentResXml);
        }
        //拿到documentres.xml相对位置
        // logger.error("DOCUMENTRESXML的text" + DocumentResXml);
        String realDocumentResRoot = "";
        List<Node> pagesnodes = Documentxml.selectNodes("//ofd:Page");
        for (Node pagesnode : pagesnodes) {
            Element pageselement = (Element) pagesnode;
            String PageLoc = pageselement.attributeValue("BaseLoc");
            // System.out.println(PageLoc);
            PagesXml.add(PageLoc);
        }
        String relativepos = OFDXMLroot.substring(0, (OFDXMLroot.indexOf("/") + 1));
        //documentres.xml的绝对位置
        realDocumentResRoot = pos + relativepos + DocumentResXml;
        // logger.error("documentres.xml位置" + realDocumentResRoot);
        Document realDocumentRESxml = sr.read(new File(realDocumentResRoot));
        //拿到pages位置,pic位置，pic id
        String relativemedialoc = "";
        List<Node> MultiMediaroot = realDocumentRESxml.selectNodes("//ofd:Res");
        for (Node node : MultiMediaroot) {
            Element Media = (Element) node;
            relativemedialoc = Media.attributeValue("BaseLoc");
            // logger.error("picMedia的baseloc" + relativemedialoc);
        }
        String PicText = "";
        List<Node> MultiMedia = realDocumentRESxml.selectNodes("//ofd:MultiMedia");
        for (Node node : MultiMedia) {
            Element Media = (Element) node;
            ID = Media.attributeValue("ID");
            // logger.error("ID" + ID);
            PicText = Media.element("MediaFile").getText();
            // logger.error("picmedia的text" + PicText);
            PicText = pos + relativepos + relativemedialoc + "/" + PicText;
            // logger.error("picmedia的text" + PicText);
            PicIDText.put(ID, PicText);
        }

        for (String relativepage : PagesXml) {
            String PageFinPos = pos + relativepos + relativepage;
            // System.out.println(PageFinPos);
            //D:/WORK/CasualWork/OFD/c/Doc_0/Pages/Page_0/Content.xml

            File PageXmlFile = new File(PageFinPos);
            Document PageXml = sr.read(PageXmlFile);

            List<Node> textobjectnodes = PageXml.selectNodes("//ofd:TextObject");
            List<Node> imageobjectnodes = PageXml.selectNodes("//ofd:ImageObject");
            if (changepic) {
                for (Node imageobjectnode : imageobjectnodes) {
                    Element imageobjectelement = (Element) imageobjectnode;
                    ID = imageobjectelement.attributeValue("ResourceID");
                    markimageSet.add(ID);
                    // System.out.println("添加ID" + ID);
                }
            }

            for (Node textobjectnode : textobjectnodes) {
                Element textobjectelement = (Element) textobjectnode;
                ID = textobjectelement.attributeValue("ID");
                Element textcode = textobjectelement.element("TextCode");
                text = textcode.getText();
                originIDtext.put(ID, text);
            }
        }

        for (Map.Entry<String, String> entry : originIDtext.entrySet()) {
            String id1 = entry.getKey();
            String text1 = entry.getValue();
            boolean markkeyword = false;
            boolean markpattern = false;
            //boolean needtopattern = true;
            if (changekeyword || needpattern) { //如果需要关键词脱敏或者需要正则
                if (changekeyword) {
                    for (String mykeyword : mykeywords) {
                        while (text1.indexOf(mykeyword) != -1) {
                            markkeyword = true;
                            replength = mykeyword.length(); //第一遍检查是否有敏感字段并全部用随机字符替换

                            text1 = fun1(replength);
                            markSetKeyword.add(id1);
                        }
                        /* begin = text1.indexOf(mykeyword);
                        replength = mykeyword.length();
                        if (begin != -1) {//第一遍检查是否有敏感字段并用********替换
                            StringBuilder sb = new StringBuilder(text1);
                            System.out.println(mykeyword+"***"+text1+"第几号"+id1);

                            for (int index = begin; index < begin + replength; index++) {
                                sb.setCharAt(index, '*');
                            }
                            text1 = sb.toString();
                            markSetKeyword.add(id1);

                            //needtopattern = false;
                        }*/

                    }
                }
                if (needpattern) {
                    //第一遍正则，用******替换，长度不一样
                    for (String pattern : MyPatterns) {
                        boolean patternchi = false;
                        patternchi = Pattern.matches(pattern, text1);
                        if (patternchi) {
                            markpattern = true;
                            // System.out.println("第一轮正则" + text1 + "正则语句" + pattern);

                            StringBuilder sb2 = new StringBuilder(text1);

                            for (int index = 0; index < text1.length(); index++) {
                                sb2.setCharAt(index, '*');
                            }
                            text1 = sb2.toString();
                            markSetPattern.add(id1);

                            break;
                            /*System.out.println("第一轮正则"+text1+"正则语句"+pattern);
                                //text1 = text1.replace(pattern, "*******");
                                text1="*****";
                                markSetPattern.add(id1);

                                break;*/
                        }
                    }
                }
            }

            firstchange.add(id1);
            //textcode.setText(text);
            //System.out.println(ID);
            //System.out.println(text);
            second1.put(id1, text1);
            if (markpattern == true) {
                markfin.put(id1, text1);
            } else if (markkeyword == true) {
                markfin.put(id1, text1);
            }
        }
        int marki = 0;
        String older = "";
        String younger = "";
        String olderId = "";
        String youngerId = "";
        //通过遍历LIST firstchange生成新的LIST，内含2 ID，1 string，用来解决关键词跨行问题

        for (String s : firstchange) {
            marki++;
            if (marki == 1) {
                String maptext = second1.get(s);
                older += maptext;
                olderId = s;
            } else {
                if (marki % 2 == 0) {
                    String maptext = second1.get(s);
                    older += maptext;
                    youngerId = s;
                    int length1 = second1.get(olderId).length();
                    int length2 = second1.get(youngerId).length();
                    TwoIDOneString twoIDOneString = new TwoIDOneString(olderId, youngerId, length1, length2, older);
                    secRound.add(twoIDOneString);

                    younger += maptext;
                    older = "";
                } else {
                    String maptext = second1.get(s);

                    younger += maptext;
                    olderId = s;
                    int length1 = second1.get(olderId).length();
                    int length2 = second1.get(youngerId).length();
                    TwoIDOneString twoIDOneString = new TwoIDOneString(
                        youngerId,
                        olderId,
                        length1,
                        length2,
                        younger
                    );
                    secRound.add(twoIDOneString);

                    older += maptext;
                    younger = "";
                }
            }
        }
        //遍历展示2个ID与string
        if (changekeyword || needpattern) { //如果需要关键词脱敏或者需要正则
            for (TwoIDOneString twoIDOneString : secRound) {
                String secRoundCheck = twoIDOneString.getTwoString();
                String secID1 = twoIDOneString.getID1();
                String secID2 = twoIDOneString.getID2();
                int seclength1 = twoIDOneString.getlength1();
                int seclength2 = twoIDOneString.getlength2();
                boolean needtopattern2 = true;
                if (changekeyword) {
                    for (String mykeyword : mykeywords) {
                        int check = secRoundCheck.indexOf(mykeyword);

                        if (check != -1) { //第2遍检查是否有敏感字段
                            StringBuilder sb = new StringBuilder(secRoundCheck);

                            int seckeywordlength = mykeyword.length();
                            for (int index = check; index < check + seckeywordlength; index++) {
                                sb.setCharAt(index, '*');
                            }
                            secRoundCheck = sb.toString();

                            markSetKeyword.add(secID1);
                            String secstring1 = (seclength1 > 1) ? secRoundCheck.substring(0, seclength1) : "";
                            markfin.put(secID1, secstring1);
                            String secstring2 = secRoundCheck.substring(seclength1);
                            markfin.put(secID2, secstring2);

                            markSetKeyword.add(secID2);
                            // System.out.println(mykeyword + "****" + secRoundCheck + "第几号" + secID1 + secID2);
                            needtopattern2 = false;
                            break;
                        }

                    }
                }

                //如果已经含关键词了就别再正则了
                //否则，第二遍正则
                if (needpattern && needtopattern2) {
                    for (String pattern : MyPatterns) {
                        boolean patternchi2 = false;
                        patternchi2 = Pattern.matches(pattern, secRoundCheck);
                        if (patternchi2) {
                            // System.out.println("第二轮正则" + secRoundCheck + "正则语句" + pattern);
                            StringBuilder sb3 = new StringBuilder();

                            for (int index = 0; index < seclength1; index++) {
                                sb3.append('*');
                            }
                            StringBuilder sb4 = new StringBuilder();

                            for (int index = 0; index < seclength2; index++) {
                                sb4.append('*');
                            }
                            String secstring1 = sb3.toString();
                            String secstring2 = sb4.toString();
                            markfin.put(secID1, secstring1);
                            markfin.put(secID2, secstring2);
                            markSetPattern.add(secID1);
                            markSetPattern.add(secID2);
                            break;
                        }
                    }
                }
            }
        }
        //遍历set，真正进行修改
        if (changepic) { //如果需要图片脱敏
            // get desensitized image template from resource or jar
            try {
                DesensitizedPicResPath = PathUtils.getResource(DesensitizedPicResPathStr);
            } catch (FileNotFoundException e) {
                e.printStackTrace();
                return null;
            }
            for (Integer whichpic : changepicInds) {
                // System.out.println("哪张图片" + whichpic);
                // System.out.println("markimageset大小" + markimageSet.size());
                if (whichpic > markimageSet.size()) {
                    // System.out.println("没那么多图片");
                } else {
                    String realPicId = "";
                    int imageobjectsize = markimageSet.size();
                    for (int imagei = 0; imagei < imageobjectsize; imagei++) {
                        if (imagei == whichpic) {
                            String realpic = markimageSet.get(imagei);
                            String whichpictochangereoot = "no pic";
                            whichpictochangereoot = PicIDText.get(realpic);
                            // logger.error("用来替换的" + DesensitizedPicResPath);
                            // logger.error("原来的" + whichpictochangereoot);
                            CopyFileUtils.copyFile(DesensitizedPicResPath.toString(), whichpictochangereoot);
                        }
                    }
                }
            }
        }
        if (changekeyword && changekeywordofd) { //如果关键词脱敏针对整个文档，代码逻辑跟下面那个针对某几页的几乎一样
            // logger.error("markkeywordset大小" + String.valueOf(markSetKeyword.size()));
            for (String relativepage : PagesXml) {
                String PageFinPos = pos + relativepos + relativepage;
                //System.out.println(PageFinPos);

                File PageXmlFile = new File(PageFinPos);
                Document PageXml = sr.read(PageXmlFile);
                for (String s : markSetKeyword) {
                    String mark = "//ofd:TextObject[@ID='12']";
                    StringBuilder stringBuilder = new StringBuilder("//ofd:TextObject[@ID='");
                    stringBuilder.append(s);
                    stringBuilder.append("']");
                    mark = stringBuilder.toString();

                    Element textobjectnode = (Element) PageXml.selectSingleNode(mark);
                    if (textobjectnode != null) {
                        //更改字体Font
                        //Attribute fontStyle = textobjectnode.attribute("Font");
                        //fontStyle.setText("it002");

                        if (textobjectnode.element("CGTransform") != null) {
                            textobjectnode.remove(textobjectnode.element("CGTransform"));
                        }

                        Element textcode = textobjectnode.element("TextCode");
                        String changetext = markfin.get(s);
                        textcode.setText(changetext);
                        //记得保存
                        saveDocument(PageXml, PageXmlFile);
                    }
                }
                if (relativepage == PagesXml.get(PagesXml.size() - 1)) {
                    // logger.error("最后一页了马上结束");
                }
            }
        }
        if (changekeyword && changekeywordpage) { //如果关键词脱敏只针对某几页
            // logger.error("markkeywordset大小" + String.valueOf(markSetKeyword.size()));
            int ii = 0;

            for (String relativepage : PagesXml) {
                for (Integer respage : changekeywordpages) {
                    if (ii == respage) {
                        String PageFinPos = pos + relativepos + relativepage;
                        //System.out.println(PageFinPos);

                        File PageXmlFile = new File(PageFinPos);
                        Document PageXml = sr.read(PageXmlFile);
                        for (String s : markSetKeyword) {
                            String mark = "//ofd:TextObject[@ID='12']";
                            StringBuilder stringBuilder = new StringBuilder("//ofd:TextObject[@ID='");
                            stringBuilder.append(s);
                            stringBuilder.append("']");
                            mark = stringBuilder.toString();

                            Element textobjectnode = (Element) PageXml.selectSingleNode(mark);
                            if (textobjectnode != null) {
                                //更改字体Font
                                /* Attribute fontStyle = textobjectnode.attribute("Font");
                                fontStyle.setText("it002");*/
                                if (textobjectnode.element("CGTransform") != null) {
                                    textobjectnode.remove(textobjectnode.element("CGTransform"));
                                }

                                Element textcode = textobjectnode.element("TextCode");
                                String changetext = markfin.get(s);
                                textcode.setText(changetext);

                                //记得保存
                                saveDocument(PageXml, PageXmlFile);
                            }
                        }
                        if (relativepage == PagesXml.get(PagesXml.size() - 1)) {
                            // logger.error("最后一页了马上结束");
                        }
                    }
                }
                ii++;
            }
        }
        if (needpattern && changepatternofd) { //如果关键词脱敏针对整个文档，代码逻辑跟下面那个针对某几页的几乎一样
            for (String relativepage : PagesXml) {
                String PageFinPos = pos + relativepos + relativepage;
                //System.out.println(PageFinPos);

                File PageXmlFile = new File(PageFinPos);
                Document PageXml = sr.read(PageXmlFile);
                for (String s : markSetPattern) {
                    String mark = "//ofd:TextObject[@ID='12']";
                    StringBuilder stringBuilder = new StringBuilder("//ofd:TextObject[@ID='");
                    stringBuilder.append(s);
                    stringBuilder.append("']");
                    mark = stringBuilder.toString();

                    Element textobjectnode = (Element) PageXml.selectSingleNode(mark);
                    if (textobjectnode != null) {
                        //更改字体Font
                        /* Attribute fontStyle = textobjectnode.attribute("Font");
                        fontStyle.setText("it002");*/
                        if (textobjectnode.element("CGTransform") != null) {
                            textobjectnode.remove(textobjectnode.element("CGTransform"));
                        }

                        Element textcode = textobjectnode.element("TextCode");
                        String changetext = markfin.get(s);
                        textcode.setText(changetext);

                        //记得保存
                        saveDocument(PageXml, PageXmlFile);
                    }
                }
                if (relativepage == PagesXml.get(PagesXml.size() - 1)) {
                    // logger.error("最后一页了马上结束");
                }
            }
        }
        if (needpattern && changepatternpage) {
            //如果patern脱敏只针对某页

            int ii = 0;
            for (String relativepage : PagesXml) {
                for (Integer respage : changepatternpages) {
                    if (ii == respage) {
                        String PageFinPos = pos + relativepos + relativepage;
                        //System.out.println(PageFinPos);

                        File PageXmlFile = new File(PageFinPos);
                        Document PageXml = sr.read(PageXmlFile);
                        for (String s : markSetPattern) {
                            String mark = "//ofd:TextObject[@ID='12']";
                            StringBuilder stringBuilder = new StringBuilder("//ofd:TextObject[@ID='");
                            stringBuilder.append(s);
                            stringBuilder.append("']");
                            mark = stringBuilder.toString();

                            Element textobjectnode = (Element) PageXml.selectSingleNode(mark);
                            if (textobjectnode != null) {
                                //更改字体Font
                                /* Attribute fontStyle = textobjectnode.attribute("Font");
                                fontStyle.setText("it002");*/
                                if (textobjectnode.element("CGTransform") != null) {
                                    textobjectnode.remove(textobjectnode.element("CGTransform"));
                                }

                                Element textcode = textobjectnode.element("TextCode");
                                String changetext = markfin.get(s);
                                textcode.setText(changetext);

                                //记得保存
                                saveDocument(PageXml, PageXmlFile);
                            }
                        }
                        if (relativepage == PagesXml.get(PagesXml.size() - 1)) {
                            logger.error("最后一页了马上结束");
                        }
                    }
                }
                ii++;
            }
        }

        if (deletepage) { //如果需要删除某一页
            int iii = 0;
            for (String relativepage : PagesXml) {
                for (Integer respage : deletepages) {
                    if (iii == respage) {
                        String PageFinPos = pos + relativepos + relativepage;
                        //System.out.println(PageFinPos);

                        File PageXmlFile = new File(PageFinPos);
                        Document document2 = sr.read(PageXmlFile);
                        Element rootelement = document2.getRootElement();
                        Element content = rootelement.element("Content");
                        Element layer = content.element("Layer");
                        content.remove(layer);
                        saveDocument(document2, PageXmlFile);
                        // logger.error("马上结束");
                    }
                }
                iii++;
            }
        }
        // 调用下面的静态方法完成xml的写出
        // saveDocument(document, new File("students.xml"));

        return Doc;
    }

    public static String fun1(int length) {
        String str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
        Random random = new Random();
        StringBuffer sb = new StringBuffer();

        for (int i = 0; i < length; i++) {
            int number = random.nextInt(62);
            sb.append(str.charAt(number));
        }
        return sb.toString();
    }

    public static void saveDocument(Document document, File xmlFile) throws IOException {
        FileOutputStream osWrite = new FileOutputStream(xmlFile); // 创建输出流
        OutputFormat format = OutputFormat.createPrettyPrint(); // 获取输出的指定格式
        format.setEncoding("UTF-8"); // 设置编码 ，确保解析的xml为UTF-8格式
        XMLWriter writer = new XMLWriter(osWrite, format); // XMLWriter
        // 指定输出文件以及格式
        writer.write(document); // 把document写入xmlFile指定的文件(可以为被解析的文件或者新创建的文件)
        writer.flush();
        writer.close();
    }

    public static String Filerename(String filePath, String newFileName) {
        File f = new File(filePath);
        if (!f.exists()) { // 判断原文件是否存在（防止文件名冲突）
            return null;
        }
        newFileName = newFileName.trim();
        if ("".equals(newFileName) || newFileName == null)
            return null; // 文件名不能为空
        String newFilePath = null;
        if (f.isDirectory()) { // 判断是否为文件夹
            //            newFilePath = filePath.substring(0, filePath.lastIndexOf("/")) + "/" + newFileName;
            newFilePath = newFileName;
        } else {
            newFilePath = newFileName;
        }
        File nf = new File(newFilePath);
        try {
            f.renameTo(nf); // 修改文件名
        } catch (Exception err) {
            err.printStackTrace();
            return null;
        }
        return newFilePath;
    }
}
