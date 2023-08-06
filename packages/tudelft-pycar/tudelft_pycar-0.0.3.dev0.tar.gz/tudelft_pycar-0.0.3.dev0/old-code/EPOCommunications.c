// EPOCommunications wraps fast OS level (Win32 API) COM port handling into a
// compiled mex file usable by MATLAB
//
// Compile command:
// mex CFLAGS='$CFLAGS -std=c99 -Wall -Wextra -Wno-unused-parameter' EPOCommunications.c
// (2017) Compiled on MATLAB R2015b using TDM-GCC x64 4.9.2-3
// (2018) Compiled on MATLAB R2016b using TDM-GCC x64 4.9.2-3
//
// up to 2018-06-14 - Johan Mes
// - Recompile with same compiler, different MATLAB
// - Updated some shitty comments
// - Added read, write buffer size defines, increased buffer sizes to 8192
// up to 2017-05-23 - Johan Mes
// - When closing and no serial port was left open, return 1 as "soft pass" instead of 0 as hard failure
// - Removed EOT from return value of transmits
// up to 2017-05-09 - Johan Mes
// - Program now restores old COM state when closing serial device
// - Fixed transmit return value double/string mixup
// - Changed communication from nonoverlapped to overlapped, allowing for robust timeouts
// - Commands open and close now return 1 on success, 0 on failure
// - Commands transmit always returns empty string, filled string on success
// - Expanded help function
// - Changed communication method from Flush/Write/Read to Write/Wait/Read.
//   This allows KITT to respond to a Write by waiting for KITT response to
//   complete. Previous versions "fixed" this by implementing slow flushing
//   and waiting thereby creating a dependency on slow code.
// - Correctly zero out COM port options in SetCOMPortOptions/initSio
// - Added error checking and error text reporting for all API calls
// - Added compile command reference with extra warning/error checking
#include "mex.h"
#include <stdio.h>
#include <stdlib.h>
#include <windows.h>

HANDLE globalserialport = NULL; // global port
OVERLAPPED globaloverlapped; // overlapped IO support
COMMTIMEOUTS oldserialtimeouts; // backup of COM timeouts of device
DCB oldserialparams; // backup of COM timeouts of device
DWORD oldserialmask; // backup of COM masks

#define READBUFFERLENGTH 8192 // maximum length of received data
#define WRITEBUFFERLENGTH 8192 // maximum length of command to send
#define READTIMEOUT 1000 // ms to wait for ReadSerial command
#define WRITETIMEOUT 1000 // ms to wait for WriteSerial command
#define WAITTIMEOUT 1000 // ms to wait for WaitForSerial command
#define VERSION "20180614DRAFT2"

void PrintLongErrorText(const char* customtext); // Prints user error and appends Windows error in text and ID form
LPSTR GetLastErrorString(DWORD error); // Convert Windows error ID to string readable by user
bool SetCOMPortOptions(HANDLE serialport); // Set COM port communication options (baud, handshake ...)
HANDLE OpenSerial(const char* portname); // Try to open a COM port, if failed return NULL
bool CloseSerial(HANDLE* serialport,bool restorestate); // Try to close a COM port, modify to NULL if succeeded, otherwise don't touch
bool WriteSerial(HANDLE serialport,char* text,DWORD length); // Write string to port, return 0 on failure
bool ReadSerial(HANDLE serialport,char* buffer,DWORD bufferlength); // Read string from port, return 0 on failure
bool WaitForSerial(HANDLE serialport); // Wait for serial port to fill up
char* ltrim(char* string);
char* rtrim(char* string);
char* trim(char* string);
void ShowHelp();

void PrintLongErrorText(const char* customtext) {
    DWORD error = GetLastError();
    LPSTR errortext = GetLastErrorString(error);
    mexPrintf("%s:\n%s (%d)\n",customtext,errortext,error);
    LocalFree(errortext);
}

LPSTR GetLastErrorString(DWORD error) {
	LPSTR buffer = NULL;
	FormatMessageA(
		FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM,
		NULL,
		error, // ID to find
        MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
		(LPSTR)&buffer,
		0,
		NULL);
    return trim(buffer);
}

bool SetCOMPortOptions(HANDLE serialport) {

    // COM port state
    DCB serialparams;
    memset(&serialparams,0,sizeof(serialparams)); // GCC does not properly support = {0}?
    serialparams.DCBlength = sizeof(serialparams);

	// Get state
    if(!GetCommState(serialport,&serialparams)) {
        PrintLongErrorText("Error getting state");
		return 0; // fail
    }
    
    // Backup state
    oldserialparams = serialparams;

    // Modify state
    serialparams.BaudRate = CBR_115200;
    serialparams.ByteSize = 8;
    serialparams.StopBits = ONESTOPBIT;
    serialparams.Parity = NOPARITY;
    serialparams.fOutxCtsFlow = 1; // Enable CTS monitoring
    serialparams.fOutxDsrFlow = 0; // Disable DSR monitoring
    serialparams.fDtrControl = 0; // Disable DTR handshaking
    serialparams.fOutX = 0; // Disable XON/XOFF for transmission
    serialparams.fInX = 0; // Disable XON/XOFF for receiving
    serialparams.fRtsControl = RTS_CONTROL_HANDSHAKE; // Enable RTS handshaking
    serialparams.EvtChar = 4; // EOT
    
	// Update state
    if(!SetCommState(serialport,&serialparams)) {
        PrintLongErrorText("Error setting state");
		return 0; // fail
    }

    // COM port timeouts
    COMMTIMEOUTS serialtimeouts = {0};
    memset(&serialtimeouts,0,sizeof(COMMTIMEOUTS));
    
    // Get timeouts
    if(!GetCommTimeouts(serialport,&serialtimeouts)) {
        PrintLongErrorText("Error getting timeouts");
		return 0; // fail
    }
    
    // Backup timeouts
    oldserialtimeouts = serialtimeouts;
    
    // Modify timeouts
    serialtimeouts.ReadIntervalTimeout = MAXDWORD;
    serialtimeouts.ReadTotalTimeoutConstant = 0;
    serialtimeouts.ReadTotalTimeoutMultiplier = 0;
    serialtimeouts.WriteTotalTimeoutConstant = 0;
    serialtimeouts.WriteTotalTimeoutMultiplier = 0;
    
    // Set timeouts
    if(!SetCommTimeouts(serialport,&serialtimeouts)) {
        PrintLongErrorText("Error setting timeouts");
		return 0; // fail
    }
    
    // Get event mask
    if(!GetCommMask(serialport,&oldserialmask)) {
        PrintLongErrorText("Error getting wait mask");
		return 0; // fail
    }
    
    // Set events to listen to
    // Standard commask is 0 (no flags)
    if(!SetCommMask(serialport,EV_RXFLAG | EV_ERR)) {
        PrintLongErrorText("Error setting wait mask");
		return 0; // fail
    }
    
    return 1;
}

HANDLE OpenSerial(const char* portname) {

    // Open COM port
    HANDLE result = CreateFile(portname,
        GENERIC_READ | GENERIC_WRITE,
        0,
        0,
        OPEN_EXISTING,
        FILE_ATTRIBUTE_NORMAL | FILE_FLAG_OVERLAPPED, // use async IO
        0);
    
	// Check for errors
    if(result == INVALID_HANDLE_VALUE) {
        DWORD error = GetLastError();
    	LPSTR errortext = GetLastErrorString(error);
    	switch(error) {
    		case ERROR_FILE_NOT_FOUND: { // Wrong COM port
    			mexPrintf("Serial port %s does not exist:\n%s (%d)\n",portname,errortext,error);
				break;
			}
            case ERROR_ACCESS_DENIED: { // COM port already open
                mexPrintf("Serial port %s already open, close program that is using COM port:\n%s (%d)\n",portname,errortext,error);
                break;
            }
            case ERROR_SEM_TIMEOUT: { // device does not respond
                mexPrintf("Serial port %s exists but does not respond, check device or try again:\n%s (%d)\n",portname,errortext,error);
                break;
            }
			default: {
				mexPrintf("Some other error occured:\n%s (%d)\n",errortext,error);
				break;
			}
		}
        LocalFree(errortext);
		result = NULL;
    }
    
    // If opened, set options
    if(result) {
		if (!SetCOMPortOptions(result)) {
			// Try to close it?
			CloseSerial(&globalserialport,false); // do not restore options
		}
	}
    
    return result;
}

bool CloseSerial(HANDLE* serialport,bool restorestate) {
    // Do not restore state when setting state fails
    if(restorestate) {
        // Restore old state backed up during opening
        // State
        if(!SetCommState(*serialport,&oldserialparams)) {
            PrintLongErrorText("Error restoring state");
            return 0; // fail
        }

        // Timeouts
        if(!SetCommTimeouts(*serialport,&oldserialtimeouts)) {
            PrintLongErrorText("Error restoring timeouts");
            return 0; // fail
        }

        // Events
        if(!SetCommMask(*serialport,oldserialmask)) {
            PrintLongErrorText("Error restoring wait mask");
            return 0; // fail
        }
    }

    // Close the port
    if(CloseHandle(*serialport)) {
        *serialport = NULL;
        return 1; // success
    } else {
        PrintLongErrorText("Error closing serial port");
        return 0; // fail
    }
}

bool WriteSerial(HANDLE serialport,char* buffer,DWORD bufferlength) {
    DWORD byteswritten = 0;
    
    // Write it all directly
    BOOL writeresult = WriteFile(serialport,buffer,bufferlength,NULL,&globaloverlapped);
    if(!writeresult) {
        if(GetLastError() != ERROR_IO_PENDING) {
            PrintLongErrorText("Error preparing write to serial port");
            return 0; // fail
        }
    }
    
    // Wait for completion for X time
    DWORD timedwriteresult = WaitForSingleObject(globaloverlapped.hEvent,WRITETIMEOUT);
    switch(timedwriteresult) {
        case WAIT_OBJECT_0: { // write completed
            if(GetOverlappedResult(serialport,&globaloverlapped,&byteswritten,FALSE)) { // completed succesfully
                return 1; // pass
            } else {
                PrintLongErrorText("Error getting write result");
                return 0; // fail
            }
        }
        case WAIT_TIMEOUT: { // timeout happened
            mexPrintf("Timeout (%d ms) writing to serial port\n",WRITETIMEOUT);
            
            // Cancel read function
            if(!CancelIo(serialport)) {
               	PrintLongErrorText("Error canceling serial port write");
                return 0; // fail
            }
            return 0; // fail
        }
        default: { // error
            PrintLongErrorText("Error writing to serial port");
            return 0; // fail
        }
    }
}

bool ReadSerial(HANDLE serialport,char* buffer,DWORD bufferlength) {
	DWORD bytesread = 0; // bytes read

    // Read it all directly
    BOOL readresult = ReadFile(serialport,buffer,bufferlength,NULL,&globaloverlapped);
    if(!readresult) {
        if(GetLastError() != ERROR_IO_PENDING) {
            PrintLongErrorText("Error preparing read from serial port");
            return 0; // fail
        }
    }
    
    // Wait for completion X time
    DWORD timedreadresult = WaitForSingleObject(globaloverlapped.hEvent,READTIMEOUT);
    switch(timedreadresult) {
        case WAIT_OBJECT_0: { // read completed
            if(GetOverlappedResult(serialport,&globaloverlapped,&bytesread,FALSE)) { // completed succesfully
                if(bytesread <= bufferlength) {
                    buffer[bytesread-1] = 0; // Remove EOT
                    return 1; // pass
                } else {
                    mexPrintf("Read result does not fit in buffer\n");
                    return 0; // fail?
                }
            } else {
                PrintLongErrorText("Error getting read result");
                return 0; // fail
            }
        }
        case WAIT_TIMEOUT: { // timeout happened
            mexPrintf("Timeout (%d ms) reading from serial port\n",READTIMEOUT);
            
            // Cancel read function
            if(!CancelIo(serialport)) {
               	PrintLongErrorText("Error canceling serial port read");
                return 0; // fail
            }
            return 0; // fail
        }
        default: { // error
            PrintLongErrorText("Error reading from serial port");
            return 0; // fail
        }
    }
}

bool WaitForSerial(HANDLE serialport) {
    DWORD event = 0;
    DWORD dummy = 0;
    
    // Wait for the car to transmit something
    BOOL waitresult = WaitCommEvent(serialport,&event,&globaloverlapped);
    if(!waitresult) {
        if(GetLastError() != ERROR_IO_PENDING) {
            PrintLongErrorText("Error preparing wait from serial port");
            return 0; // fail
        }
    }
    
    // Wait for completion X time
    DWORD timedwaitresult = WaitForSingleObject(globaloverlapped.hEvent,WAITTIMEOUT);
    switch(timedwaitresult) {
        case WAIT_OBJECT_0: { // read completed
            if(GetOverlappedResult(serialport,&globaloverlapped,&dummy,FALSE)) { // completed succesfully
                if(event & EV_RXFLAG) { // The specified event occurred
                    return event; // pass
                } else { // error event
                    mexPrintf("Error received after wait\n");
                    return event; // fail
                }
            } else {
                PrintLongErrorText("Error getting wait result");
                return 0; // fail
            }
        }
        case WAIT_TIMEOUT: { // timeout happened
            mexPrintf("Timeout (%d ms) waiting for serial port\n",WAITTIMEOUT);
            
            // Cancel wait function
            if(!CancelIo(serialport)) {
               	PrintLongErrorText("Error canceling serial port wait");
                return 0; // fail
            }
            return 0; // fail
        }
        default: { // error
            PrintLongErrorText("Error waiting for serial port");
            return 0; // fail
        }
    }
}

// Trimming
char* rtrim(char* string) {
    char* original = string + strlen(string);
    while(isspace(*--original)); // walk spaces
    *(original + 1) = '\0'; // put end char
    return string;
}
char* ltrim(char* string) {
    char* original = string;
    char* p = original;
    int trimmed = 0;
    do {
        if(!isspace(*original) || trimmed) {
            trimmed = 1;
            *p++ = *original;
        }
    }
    while (*original++ != '\0');
    return string;
}
char* trim(char* string) {
    return ltrim(rtrim(string));
}

void ShowHelp() {
    mexPrintf("Usage:\n");
    mexPrintf("\n");
    mexPrintf("EPOCommunications('<command>')\n");
    mexPrintf("EPOCommunications('<command>','<arg1>')\n");
    mexPrintf("\n");
    mexPrintf("Options for <command>:\n");
    mexPrintf("  open\n");
    mexPrintf("    Open the COM port specified by <arg1>, use \\\\.\\COMx\n");
    mexPrintf("    return 1 on success, 0 on failure\n");
    mexPrintf("\n");
    mexPrintf("  close\n");
    mexPrintf("    Close the opened COM port\n");
    mexPrintf("    return 1 on success, 0 on failure\n");
    mexPrintf("\n");
    mexPrintf("  help\n");
    mexPrintf("    This help string\n");
    mexPrintf("\n");
    mexPrintf("  version\n");
    mexPrintf("    Shows EPOCommmunications version\n");
    mexPrintf("\n");
    mexPrintf("  transmit\n");
    mexPrintf("    Transmit a configuration string <arg1> to the KITT-board\n");
    mexPrintf("    Text is returned as a result of S, Sv, Sd, V commands\n");
    mexPrintf("    When no text is received after these commands an error occurred\n");
    mexPrintf("    Options for <arg1>:\n");
    mexPrintf("      A<x> Set audio on/off with <x>: 1=on and 0=off\n");
    mexPrintf("      B<x> Set bit frequency, range <x> is: 0..65535\n");
    mexPrintf("      C<x> Set 32 bit code word with <x>: 0xhhhhhhhh (h = hex digit)\n");
    mexPrintf("      D<x> Set steering direction, range <x> is: 100..200\n");
    mexPrintf("      F<x> Set carrier frequency, range <x> is: 0..65535\n");
    mexPrintf("      M<x> Set motor PWM, range <x> is: 135..165\n");
    mexPrintf("      R<x> Set repetition counter, range <x> is: 32..65535\n");
    mexPrintf("      S    Get complete status\n");
    mexPrintf("      Sv   Get battery status\n");
    mexPrintf("      Sd   Get distance sensor info\n");
    mexPrintf("      V    Get version of the board software\n");
}

//nlhs
//Number of expected output mxArrays
//
//plhs
//Array of pointers to the expected output mxArrays
//
//nrhs
//Number of input mxArrays
//
//prhs
//Array of pointers to the input mxArrays. Do not modify any prhs values in your MEX file. Changing the data in these read-only mxArrays can produce undesired side effects.
void mexFunction(int nlhs,mxArray *plhs[],int nrhs, const mxArray *prhs[]) {

    // Check if at least 1 command provided
    char* command = NULL;
    char* arg1 = NULL;
    if(nrhs >= 1) {
        command = mxArrayToString(prhs[0]);
        if(nrhs >= 2) {
            arg1 = mxArrayToString(prhs[1]);
        }
    } else {
        mexPrintf("No input provided\n\n");
        ShowHelp();
        return;
    }
    
    // Find the command
    if(!strcmp(command,"close")) {
        
        // Check second arg
        if(arg1 != NULL) {
            mexPrintf("No arg1 expected, ignoring\n");
        }
        
        // Return a double, 1 on success, 0 otherwise
        plhs[0] = mxCreateDoubleMatrix(1, 1, mxREAL);
        double* returnvaluedouble = mxGetPr(plhs[0]);        
        
        // Do not force close if no port open
        if(!globalserialport) {
            mexPrintf("No serial port to close\n");
            *returnvaluedouble = 1; // Do not consider this a hard fail
            return;
        }

        // Remove close event
        if(globaloverlapped.hEvent) {
            if(!CloseHandle(globaloverlapped.hEvent)) {
                PrintLongErrorText("Error closing wait event");
                *returnvaluedouble = 0; // fail
            } else {
                globaloverlapped.hEvent = NULL; // if closed remove
                *returnvaluedouble = 1; // pass
            }
        }
        
        // Always try to close global port
        if(!CloseSerial(&globalserialport,true)) {
            *returnvaluedouble = 0; // fail
        }
        // For pass, do not modify return value from event
        
    } else if(!strcmp(command,"version")) {
        mexPrintf("EPOCommmunications version: %s\n",VERSION);
    } else if(!strcmp(command,"help")) {
        ShowHelp();
    } else if(!strcmp(command,"open")) {
        
        // Return a double, 1 on success, 0 otherwise
        plhs[0] = mxCreateDoubleMatrix(1, 1, mxREAL);
        double* returnvaluedouble = mxGetPr(plhs[0]);
        
        // Check second arg
        if(arg1 == NULL) {
            mexPrintf("No arg1 provided for open\n");
            *returnvaluedouble = 0; // fail
            return;
        }

        // Do not force reopen
        if(globalserialport) { // reuse global port
            mexPrintf("Close previous serial port first\n");
            *returnvaluedouble = 0;
            return;
        }

        // Open it
        globalserialport = OpenSerial(arg1);
        if(!globalserialport) {
            // error message generated in OpenSerial
            *returnvaluedouble = 0;
            return;
        }
        
        // Create event that happens on successful read/write/wait
        memset(&globaloverlapped,0,sizeof(OVERLAPPED));
        globaloverlapped.hEvent = CreateEvent(NULL,0,0,NULL); // auto reset
        if(!globaloverlapped.hEvent) {
            PrintLongErrorText("Error creating wait event");
            *returnvaluedouble = 0;
        } else {
            *returnvaluedouble = 1; // PASSED ALL TESTS!
        }
    } else if(!strcmp(command,"transmit")) {
        
        // Check second arg
        if(arg1 == NULL) {
            mexPrintf("No arg1 provided for transmit\n");
            return;
        }
        if(strlen(arg1) == 0) {
        	mexPrintf("Empty arg1 provided\n");
            return;
        }
        
        // Check global port
        if(!globalserialport) { 
            mexPrintf("Open serial port before transmitting\n");
            return;
        }
        
        // Buffer to write to and read from
        bool waitandreadresponse = false;
        char readbuffer[READBUFFERLENGTH] = ""; // all zeros
        char writebuffer[WRITEBUFFERLENGTH] = ""; // all zeros -> text\n0000...
        int writelength = 0; // save strlen call

        // Split command letter and text
        char transmittype = arg1[0];
        switch(transmittype) {
            case 'B': // bit frequency
            case 'F': // carrier frequency
            case 'R': // repetition counter
            { // convert to uint16_t
                unsigned int value = 0;
                if(sscanf(arg1,"%*c%d",&value) == 1) {
                    writebuffer[0] = transmittype;
                    writebuffer[1] = (value >> 8) & 0xFF;
                    writebuffer[2] = (value >> 0) & 0xFF;
                    writebuffer[3] = '\n';
                    writelength = 4;
                } else {
                   mexPrintf("Invalid transmit format %s\n",arg1);
                   return;
                }
                break;
            }
            case 'C': // audio code (test = 0x31323334)
            { // convert hex text to uint32_t
                unsigned int value = 0;
                if(sscanf(arg1,"%*c%i",&value) == 1) { // %i converts from hex
                    writebuffer[0] = transmittype;
                    writebuffer[1] = (value >> 24) & 0xFF; // MSB first
                    writebuffer[2] = (value >> 16) & 0xFF;
                    writebuffer[3] = (value >> 8)  & 0xFF;
                    writebuffer[4] = (value >> 0)  & 0xFF;
                    writebuffer[5] = '\n';
                    writelength = 6;
                } else {
                   mexPrintf("Invalid transmit format %s\n",arg1);
                   return;
                }
                break;
            }
            case 'A': // audio beacon
            case 'D': // direction PWM
            case 'M': // motor PWM
            { // generic direct strings, no response
                sprintf(writebuffer,"%s\n",arg1);
                writelength = strlen(writebuffer);
                break;
            }
            case 'S': // status
            case 'V': // version
            { // generic direct strings with response
                sprintf(writebuffer,"%s\n",arg1);
                writelength = strlen(writebuffer);
                waitandreadresponse = true;
                break;
            }
            default: {
                mexPrintf("Unknown command character %c\n",transmittype);
                return;
            }
        }

        // Write whole command to car at once
        if(!WriteSerial(globalserialport,writebuffer,writelength)) {
            return;
        }

        // Wait for car to respond
        if(waitandreadresponse) {
            
            // Wait for it to fill up
            if(!WaitForSerial(globalserialport)) {
                plhs[0] = mxCreateString("");
                return;
            }
            
            // Read whole response from car at once
            if(!ReadSerial(globalserialport,readbuffer,sizeof(readbuffer))) {
                plhs[0] = mxCreateString("");
                return;
            }
            
            // Return good response to MATLAB
            plhs[0] = mxCreateString(readbuffer);
        }
    } else {
        mexPrintf("Unknown command %s\n\n",command);
        ShowHelp();
    }
}
