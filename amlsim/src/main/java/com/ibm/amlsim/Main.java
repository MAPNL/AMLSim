package com.ibm.amlsim;


public class Main {

    public static void main(String[] args){


        if(args.length < 6){
            System.err.println("Usage: java amlsim.AMLSim -file [PropertyFile] -for [Steps] -r [Repeats] [-name [SimulatorName]]");
            System.exit(1);
        }

        int nrOfTimesRepeat = Integer.parseInt(args[5]);

        System.out.println("----------------------- nrOfTimesRepeat " + nrOfTimesRepeat);



        for(int i=0; i<nrOfTimesRepeat; i++){
            AMLSim p = new AMLSim(1);
            p.setCurrentLoop(i);
            p.runSimulation(args);
        }
    }
}
