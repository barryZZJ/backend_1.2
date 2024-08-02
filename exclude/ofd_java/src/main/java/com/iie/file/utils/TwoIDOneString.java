package com.iie.file.utils;

public class TwoIDOneString {
    public String ID1;
    public String ID2;
    public String twoString;
    public int length1;
    public  int length2;

    public TwoIDOneString(){

    }
    public TwoIDOneString(String Id1,String Id2, int len1,int len2,String twostring){
        ID1=Id1;
        ID2=Id2;
        length1=len1;
        length2=len2;
        twoString=twostring;
    }

    public String getID1() {
        return ID1;
    }
    public int getlength1() {
        return length1;
    }
    public int getlength2() {
        return length2;
    }

    public String getTwoString() {
        return twoString;
    }

    public String getID2() {
        return ID2;
    }

    @Override
    public String toString() {
        return super.toString();
    }
}
