# WF2HTML

### Environment Setup
1. Install Python 2.7.14
2. Install the following packages  
    * ```opencv-python (3.4.0.12)```  
    * ```numpy (1.14.1)```  
    * ```imutils (0.4.5)```  
    * ```scipy (1.0.0)```  
    * ```PySide (1.2.4)```  
    * ```dominate (2.3.1)```  


### Running the program
run the python script ```execute.py```


### Building an .exe
**Note : _Building an exe does not work correctly_. **
_Current Error_ : _The latest version of scipy (1.0.0) is not properly compatible with pyinstaller._

##### Process closest to building a working exe
1. Install ```PyInstaller (using pip)```

2. Run the command:  
    ```pyinstaller --distpath Executable --workpath build_temp --hiddenimport scipy._lib.messagestream execute.py```
