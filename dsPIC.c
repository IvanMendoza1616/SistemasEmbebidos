
// DSPIC33EV256GM102 Configuration Bit Settings

// 'C' source line config statements

// FSEC
#pragma config BWRP = OFF               // Boot Segment Write-Protect Bit (Boot Segment may be written)
#pragma config BSS = DISABLED           // Boot Segment Code-Protect Level bits (No Protection (other than BWRP))
#pragma config BSS2 = OFF               // Boot Segment Control Bit (No Boot Segment)
#pragma config GWRP = OFF               // General Segment Write-Protect Bit (General Segment may be written)
#pragma config GSS = DISABLED           // General Segment Code-Protect Level bits (No Protection (other than GWRP))
#pragma config CWRP = OFF               // Configuration Segment Write-Protect Bit (Configuration Segment may be written)
#pragma config CSS = DISABLED           // Configuration Segment Code-Protect Level bits (No Protection (other than CWRP))
#pragma config AIVTDIS = DISABLE        // Alternate Interrupt Vector Table Disable Bit  (Disable Alternate Vector Table)

// FBSLIM
#pragma config BSLIM = 0x1FFF           // Boot Segment Code Flash Page Address Limit Bits (Enter Hexadecimal value)

// FOSCSEL
#pragma config FNOSC = FRCPLL           // Initial oscillator Source Selection Bits (Fast RC Oscillator with divide-by-N with PLL module (FRCPLL))
#pragma config IESO = ON                // Two Speed Oscillator Start-Up Bit (Start up device with FRC,then automatically switch to user selected oscillator source)

// FOSC
#pragma config POSCMD = HS              // Primary Oscillator Mode Select Bits (HS Crystal Oscillator mode)
#pragma config OSCIOFNC = OFF           // OSC2 Pin I/O Function Enable Bit (OSC2 is clock output)
#pragma config IOL1WAY = ON             // Peripheral Pin Select Configuration Bit (Allow Only One reconfiguration)
#pragma config FCKSM = CSECMD           // Clock Switching Mode Bits (Clock Switching is enabled,Fail-safe Clock Monitor is disabled)
#pragma config PLLKEN = ON              // PLL Lock Enable Bit (Clock switch to PLL source will wait until the PLL lock signal is valid)

// FWDT
#pragma config WDTPOST = PS32768        // Watchdog Timer Postscaler Bits (1:32,768)
#pragma config WDTPRE = PR128           // Watchdog Timer Prescaler Bit (1:128)
#pragma config FWDTEN = ON              // Watchdog Timer Enable Bits (WDT Enabled)
#pragma config WINDIS = OFF             // Watchdog Timer Window Enable Bit (Watchdog timer in Non-Window Mode)
#pragma config WDTWIN = WIN25           // Watchdog Window Select Bits (WDT Window is 25% of WDT period)

// FPOR
#pragma config BOREN0 = ON              // Brown Out Reset Detection Bit (BOR is Enabled)

// FICD
#pragma config ICS = PGD1               // ICD Communication Channel Select Bits (Communicate on PGEC1 and PGED1)

// FDMTINTVL
#pragma config DMTIVTL = 0xFFFF         // Lower 16 Bits of 32 Bit DMT Window Interval (Enter Hexadecimal value)

// FDMTINTVH
#pragma config DMTIVTH = 0xFFFF         // Upper 16 Bits of 32 Bit DMT Window Interval (Enter Hexadecimal value)

// FDMTCNTL
#pragma config DMTCNTL = 0xFFFF         // Lower 16 Bits of 32 Bit DMT Instruction Count Time-Out Value (Enter Hexadecimal value)

// FDMTCNTH
#pragma config DMTCNTH = 0xFFFF         // Upper 16 Bits of 32 Bit DMT Instruction Count Time-Out Value (Enter Hexadecimal value)

// FDMT
#pragma config DMTEN = ENABLE           // Dead Man Timer Enable Bit (Dead Man Timer is Enabled and cannot be disabled by software)

// FDEVOPT
#pragma config PWMLOCK = ON             // PWM Lock Enable Bit (Certain PWM registers may only be written after key sequence)
#pragma config ALTI2C1 = OFF            // Alternate I2C1 Pins Selection Bit (I2C1 mapped to SDA1/SCL1 pins)

// FALTREG
#pragma config CTXT1 = NONE             // Interrupt Priority Level (IPL) Selection Bits For Alternate Working Register Set 1 (Not Assigned)
#pragma config CTXT2 = NONE             // Interrupt Priority Level (IPL) Selection Bits For Alternate Working Register Set 2 (Not Assigned)

// #pragma config statements should precede project file includes.
// Use project enums instead of #define for ON and OFF.

#include <xc.h>
#include <libpic30.h>
#define FPLL 140000000  //(7.33M*76)/4
#define FCY 67802500 // Fcy = 1/2Fpll
#define BAUD115200  ((FCY/115200)/16) - 1
#define DELAY_8_7uS asm volatile ("REPEAT, #605"); Nop();

//TX=PIN 11
//ADC=PIN 2
//frecuencia=PIN 15

void initAdc1(void);
void Delay_us(unsigned int);
int  i;
unsigned int signal=0;

void PWM_init(void)
{
    
    /* Set PWM Period on Primary Time Base */
    PTPER = 1400;
    /* Set Phase Shift */
    PHASE1 = 0;
    PHASE2 = 720;
    PHASE3 = 200;
    /* Set Duty Cycles */
    PDC1 = 700;
    PDC2 = 700;
    PDC3 = 700;
    /* Set Dead Time Values */
    DTR1 = DTR2 = DTR3 = 10;
    ALTDTR1 = ALTDTR2 = ALTDTR3 = 10;
    /* Set PWM Mode to Push-Pull */
    IOCON1 = IOCON2 = IOCON3 = 0xC800;
    /* Set Primary Time Base, Edge-Aligned Mode and Independent Duty Cycles */
    PWMCON1 = PWMCON2 = PWMCON3 = 0;
    /* Configure Faults */
    FCLCON1 = FCLCON2 = FCLCON3 = 0x0003;
    /* 1:1 Prescaler */
    PTCON2 = 0x0000;
    /* Enable PWM Module */
    PTCON = 0x8000;
}

void PLL_init(void)
{
    OSCCONbits.COSC=011;
    PLLFBD=74;              //M=76
    CLKDIVbits.PLLPOST=0;   //N2=2
    CLKDIVbits.PLLPRE=0;    //N1=2
    /*      PROBAR CODIGO
    __builtin_write_OSCCONH(0x03);
    __builtin_write_OSCCONL(0x01);
    while (OSCCONbits.COSC != 0x3);
    while (_LOCK == 0);             // Wait for PLL lock at 40 MIPS 
    */
}
void UART_init(void)
{
    U2MODEbits.UARTEN = 0; //
    // digital output
    TRISBbits.TRISB4 = 0;
    // map MONITOR_TX pin to port RB4, which is remappable RP36
    //
    RPOR1bits.RP36R = 0x03; // map UART2 TXD to pin RB4
    // set up the UART for default baud, 1 start, 1 stop, no parity
    U2MODEbits.STSEL = 0; // 1-Stop bit
    U2MODEbits.PDSEL = 0; // No Parity, 8-Data bits
    U2MODEbits.ABAUD = 0; // Auto-Baud disabled
    U2MODEbits.BRGH = 0; // Standard-Speed mode
    U2BRG = BAUD115200; // Baud Rate setting for 115200
    U2STAbits.UTXISEL0 = 0; // Interrupt after TX buffer done
    U2STAbits.UTXISEL1 = 1;
    
    IEC1bits.U2TXIE = 1; // Enable UART TX interrupt
    IFS1bits.U2TXIF = 0; // Clear TX2 Interrupt flag
    U2MODEbits.UARTEN = 1; // Enable UART (this bit must be set *BEFORE* UTXEN)
    U2STAbits.UTXEN = 1;
    DELAY_8_7uS         //    (1/115200)
}

void __attribute__((interrupt, no_auto_psv)) _U2TXInterrupt(void)
{
    IFS1bits.U2TXIF = 0; // Clear TX2 Interrupt flag
}
 
void initAdc1(void)
{
    // Set port configuration  
    //ANSELA = ANSELB = 0x0000;
   
    // Ensure AN0/RA0 is analog Initialize and enable ADC module 
    ANSELAbits.ANSA0=1;
    TRISAbits.TRISA0=1;
    AD1CON1 = 0x0000;
    
    AD1CON2 = 0x0000;
    AD1CON3bits.SAMC = 1;
    AD1CON3bits.ADCS = 0;
    AD1CON4 = 0x0000;
    AD1CHS0 = 0x0000;//selecciona AN0
    AD1CHS123 = 0x0000;
    AD1CSSH = 0x0000;
    AD1CSSL = 0x0000;
    AD1CON1bits.ADON = 1;
    Delay_us(20);
    
}

void Delay_us(unsigned int delay)
{for (i = 0; i < delay; i++)
{__asm__ volatile ("repeat #70");
__asm__ volatile ("nop");}

}

 

void main(void) {
    
    int mil=0,cent=0,dec=0,uni=0;
    char tabla[10]={48,49,50,51,52,53,54,55,56,57};
    
    PLL_init();
    PWM_init();
    UART_init();
    initAdc1();
    
    TRISBbits.TRISB6 = 0;
    
    while(1)
    {
        
        AD1CON1bits.SAMP = 1;      // Start sampling 
        Delay_us(10);               // Wait for sampling time (10us)
        AD1CON1bits.SAMP = 0;      // Start the conversion
        while (!AD1CON1bits.DONE); // Wait for the conversion to complete
        signal = ADC1BUF0;       // Read the conversion result
       
        mil=signal/1000;
        cent=signal%1000/100;
       dec=(signal%100)/10;
       uni=(signal%100)%10;
  
        while (U2STAbits.UTXBF);
        U2TXREG=tabla[mil];
        while (U2STAbits.UTXBF);
        U2TXREG=tabla[cent];
        while (U2STAbits.UTXBF);
        U2TXREG=tabla[dec];
        while (U2STAbits.UTXBF);
        U2TXREG=tabla[uni];
        while (U2STAbits.UTXBF);    //wait until TXREG is available
        U2TXREG = 10;
        
        if (PORTBbits.RB6 == 0){
            PORTBbits.RB6 = 1;}
        else{
            PORTBbits.RB6 = 0;} 
    }
}
