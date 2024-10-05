package com.dimas;

import java.io.Serializable;

public class Gadget implements Serializable {

    private Command command;

    public Gadget(Command command) {
        this.command = command;
    }

    public String toString(){
        return command.run();
    }


}
