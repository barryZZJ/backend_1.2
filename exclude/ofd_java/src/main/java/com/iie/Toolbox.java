package com.iie;

import java.io.IOException;
import java.net.URISyntaxException;

import org.apache.commons.cli.CommandLine;

import com.iie.file.filedesensitizers.OfdFileDesensitizer;
import com.iie.utils.ArgParser;

public final class Toolbox {

    public static void doFileDesensitize(String[] params, String output) {
        if (params.length < 2) {
            System.err.println("not enough parameters!");
            return;
        }
        String fileInPathStr = params[0];
        String fileOutPathStr = output;
        String alg = params[1];
        int[] pages = new int[params.length - 2];
        
        for (int i = 2; i < params.length; i++) {
            pages[i - 2] = Integer.parseInt(params[i]);
        }
        if (alg.equals("ofd")) {
            System.out.println("Input:\n" + fileInPathStr);
            OfdFileDesensitizer des = new OfdFileDesensitizer.Builder().deletePages(pages).build();
            des.desensitize(fileInPathStr, fileOutPathStr);
            System.out.println("\nOutput:\n" + fileOutPathStr);
        } else {
            System.err.println("Unknown alg: " + alg);
        }
    }

    public static void main(String[] args) throws URISyntaxException, IOException {
        ArgParser parser = new ArgParser();
        CommandLine cmd = parser.parse(args);

        String action = cmd.getArgs()[0];
        String[] params = cmd.getOptionValues("param");
        String output = cmd.getOptionValue("output");
        if (params == null) {
            System.err.println("empty parameter!");
            return;
        }
        // Check which subcommand was provided
        if (action.equals("file")) {
            doFileDesensitize(params, output);
        } else {
            // Handle the case when no subcommand is provided
            System.err.println("Error: action must be 'file'.");
        }
    }
}
