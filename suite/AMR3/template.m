# parameters for the script 'm'
setenv Problem {{enzo_parameter}}

setenv DataDir "./Data"     #I don't know if this does anything right now.
setenv RestartDump data0030 #filename for restart
setenv ExtractDump data0011 #filename for extration

setenv Compile yes
setenv nprocRun {{ncores}}           #processor count
setenv dbg -d               #debug flag
setenv RestartClean yes      #rm data* on restart
setenv KillDataOnStartup no #rm data* on plain starts
setenv KillExec  no         #remove enzo executable from src or not. 
                            #(catches link errors, slower)
setenv RestartDebugging no  #failsafe, to prevent plain start if 
			    #debugging something in restart
#List of name* files that won't be deleted.  Good for restarts
#setenv SaveList data0030
setenv ExtractionLevel 2    #extraction level.
setenv poe poe              #for datastar, which nodes to run on.
#end

setenv src ../enzo-g57/src/enzo
