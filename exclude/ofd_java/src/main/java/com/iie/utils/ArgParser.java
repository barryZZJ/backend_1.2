package com.iie.utils;
import org.apache.commons.cli.*;
// TODO use picocli to implement subcommands
public class ArgParser {
    public CommandLine parse(String[] args) {
        Options options = new Options();
        
        options.addOption(Option.builder("p")
                .longOpt("param")
                .hasArgs()
                .required()
                .build());
        
        
        options.addOption(Option.builder("o")
                .longOpt("output")
                .hasArgs()
                .required()
                .build());
        
        CommandLineParser parser = new DefaultParser();
        try {
            CommandLine cmd = parser.parse(options, args);
            
            return cmd;
        } catch (ParseException e) {
            System.err.println("Error parsing command-line arguments: " + e.getMessage());
            return null;
        }
    }
}
