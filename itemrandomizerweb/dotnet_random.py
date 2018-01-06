#!/usr/bin/python

# python conversion of the C# random algorithm
# http://referencesource.microsoft.com/#mscorlib/system/random.cs

import time

class Random:
    # Private Constants 
    int32_maxValue = 2147483647
    int32_minValue = -2147483648
    MBIG =  int32_maxValue
    MSEED = 161803398

    # Member Variables
    inext = 0
    inextp = 0
    SeedArray = [0]*56

    def __init__(self, Seed=None):
        if Seed is None:
            Seed = int(time.time())
    
        ii = 0
        mj = 0
        mk = 0
    
        # Initialize our Seed array.
        # This algorithm comes from Numerical Recipes in C (2nd Ed.)
        subtraction = self.int32_maxValue if Seed == self.int32_minValue else abs(Seed)
        mj = self.MSEED - subtraction
        self.SeedArray[55] = mj
        mk = 1
        for i in range(1, 55):
            ii = (21*i)%55
            self.SeedArray[ii] = mk
            mk = mj - mk
            if mk < 0:
                mk += self.MBIG
            mj = self.SeedArray[ii]

        for k in range(1, 5):
            for i in range(1, 56):
                self.SeedArray[i] -= self.SeedArray[1+(i+30)%55]
                if self.SeedArray[i] < 0:
                    self.SeedArray[i] += self.MBIG

        self.inext = 0
        self.inextp = 21
        Seed = 1

    
    #/*====================================Sample====================================
    #**Action: Return a new random number [0..1) and reSeed the Seed array.
    #**Returns: A double [0..1)
    #**Arguments: None
    #**Exceptions: None
    #==============================================================================*/
    def Sample(self):
        # Including this division at the end gives us significantly improved
        # random number distribution.
        return (self.InternalSample()*(1.0/self.MBIG));

    def InternalSample(self):
        locINext = self.inext
        locINextp = self.inextp
 
        locINext += 1
        if locINext >= 56:
            locINext=1
        locINextp += 1
        if locINextp >= 56:
            locINextp = 1

        retVal = self.SeedArray[locINext]-self.SeedArray[locINextp]
 
        if retVal == self.MBIG:
            retVal -= 1
        if retVal < 0:
            retVal += self.MBIG
          
        self.SeedArray[locINext] = retVal
 
        self.inext = locINext
        self.inextp = locINextp
                    
        return retVal
    
    def GetSampleForLargeRange(self):
        # The distribution of double value returned by Sample 
        # is not distributed well enough for a large range.
        # If we use Sample for a range [self.int32_minValue..self.int32_maxValue)
        # We will end up getting even numbers only.

        result = self.InternalSample()

        # Note we can't use addition here. The distribution will be bad if we do that.
        negative = True if (self.InternalSample()%2 == 0) else False  # decide the sign based on second sample
        if negative is True:
            result = -result

        d = result
        d += (self.int32_maxValue - 1) # get a number in range [0 .. 2 * Int32MaxValue - 1)
        d /= float(2 * self.int32_maxValue - 1)

        return d

    # /*=====================================Next=====================================
    # **Returns: An int [minvalue..maxvalue)
    # **Arguments: minValue -- the least legal value for the Random number.
    # **           maxValue -- One greater than the greatest legal return value.
    # **Exceptions: None.
    # ==============================================================================*/
    def Next(self, minValue=0, maxValue=int32_maxValue):
        if minValue > maxValue:
            raise Exception("minValue > maxValue")

        range = maxValue - minValue
        if range <= self.int32_maxValue:
            retValue = ((int)(self.Sample() * range) + minValue)
        else:
            retValue = (int)((long)(self.GetSampleForLargeRange() * range) + minValue)
    
        # print("Next({}, {}) -> {}".format(minValue, maxValue, retValue))
        return retValue
    
    #/*=====================================Next=====================================
    # **Returns: A double [0..1)
    # **Arguments: None
    # **Exceptions: None
    # ==============================================================================*/
    def NextDouble(self):
        return self.Sample()
    
    #/*==================================NextBytes===================================
    # **Action:  Fills the byte array with random bytes [0..0x7f].  The entire array is filled.
    # **Returns:Void
    # **Arugments:  buffer -- the array to be filled.
    # **Exceptions: None
    # ==============================================================================*/
    def NextBytes(self, buffer):
        for i in range(0, len(buffer)):
            buffer[i] = (self.InternalSample()%(255+1))

if __name__ == "__main__":
    r = Random(42)
    print(r.Sample())
    print(r.InternalSample())
    print(r.GetSampleForLargeRange())
    print(r.Next(1000000, 9999999))
    print(r.Next())
    print(r.NextDouble())
    buffer = [0]*10
    r.NextBytes(buffer)
    print(buffer)
